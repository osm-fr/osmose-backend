#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2020                                 ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping

# https://gitorious.org/osm-hacks/osm-hacks/trees/master/etablissements-scolaires

class Analyser_Merge_School_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)

        if config.db_schema == 'france_guadeloupe':
            classs = 10
            officialName = "Guadeloupe"
            self.is_in = lambda code_postal: code_postal[0:3] == "971"
        elif config.db_schema == 'france_guyane':
            classs = 20
            officialName = "Guyane"
            self.is_in = lambda code_postal: code_postal[0:3] == "973"
        elif config.db_schema == 'france_reunion':
            classs = 30
            officialName = "Réunion"
            self.is_in = lambda code_postal: code_postal[0:3] == "974"
        elif config.db_schema == 'france_martinique':
            classs = 40
            officialName = "Martinique"
            self.is_in = lambda code_postal: code_postal[0:3] == "972"
        else:
            classs = 0
            officialName = "Métropole"
            self.is_in = lambda code_postal: code_postal[0:2] != "97"

        trap = T_(
'''Check the location. Warning data from the Ministry may have several
administrative schools for a single physical school.''')
        self.def_class_missing_official(item = 8030, id = classs+1, level = 3, tags = ['merge'],
            title = T_('School not integrated'),
            trap = trap)
        self.def_class_missing_osm(item = 7070, id = classs+2, level = 3, tags = ['merge'],
            title = T_('School without tag \"ref:UAI\" or invalid'),
            trap = trap)
        self.def_class_possible_merge(item = 8031, id = classs+3, level = 3, tags = ['merge'],
            title = T_('School, integration suggestion'),
            trap = trap)
        self.def_class_update_official(item = 8032, id = classs+4, level = 3, tags = ['merge'],
            title = T_('School update'),
            trap = trap)

        self.init(
            "https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre",
            "Adresse et géolocalisation des établissements d'enseignement du premier et second degrés - " + officialName,
            CSV(SourceOpenDataSoft(
                attribution="Ministère de l'Éducation nationale et de la Jeunesse",
                base_url="https://data.education.gouv.fr",
                dataset="fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre",
                filter=lambda t: t.replace("Ecole", "École").replace("ecole", "école").replace("Saint ", "Saint-").replace("Sainte ", "Sainte-").replace("élementaire", "élémentaire").replace("elementaire", "élémentaire").replace("Elémentaire", "Élémentaire").replace("elémentaire", "élémentaire").replace("College", "Collège"))),
            Load("Longitude", "Latitude",
                select = {"Code état établissement": ["1", "3"]},
                where = lambda res: res["Code postal"] and self.is_in(res["Code postal"])),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"amenity": "school"}),
                osmRef = "ref:UAI",
                conflationDistance = 50,
                mapping = Mapping(
                    static2 = {
                        "source": self.source,
                        "amenity": "school"},
                    mapping1 = {
                        "ref:UAI": "Code établissement",
                        "school:FR": lambda res: self.School_FR_nature_uai[res["Code nature"]],
                        "operator:type": lambda res: "private" if res["Secteur Public/Privé"] == "Privé" else "public" if res["Secteur Public/Privé"] == "Public" else None},
                    mapping2 = {"name": lambda res: res["Appellation officielle"].replace("ECOLE", "École").replace("ELEMENTAIRE", "élémentaire") if res["Appellation officielle"] not in [None, "A COMPLETER", "École primaire", "École Primaire", "ECOLE PRIMAIRE", "École PRIMAIRE", "ECOLE Primaire", "école primaire", "École primaire publique", "ECOLE PRIMAIRE PUBLIQUE", "École Primaire Publique", "École PRIMAIRE publique", "École primaire privée", "ECOLE PRIMAIRE PRIVÉE", "École primaire intercommunale", "École primaire Intercommunale", "École Primaire Intercommunale", "École élémentaire", "École Élémentaire", "ECOLE ELEMENTAIRE", "École ELEMENTAIRE", "École Elementaire", "école élémentaire", "École élémentaire publique", "École élémentaire Publique", "ECOLE ELEMENTAIRE PUBLIQUE", "École élémentaire privée", "École élémentaire intercommunale", "École élémentaire école publique", "École maternelle", "ECOLE MATERNELLE", "École Maternelle", "École MATERNELLE", "École Maternelle", "école maternelle", "École maternelle publique", "ECOLE MATERNELLE PUBLIQUE", "École Maternelle Publique", "École maternelle Publique", "école maternelle publique", "École maternelle intercommunale", "École maternelle Intercommunale", "Collège"] else None},
                    text = self.text)))

    def text(self, tags, fields):
        lib = ', '.join(filter(lambda x: x and x != "None", [fields["Appellation officielle"], fields["Adresse"], fields["Lieu dit"], fields["Boite postale"], fields["Code postal"], fields["Localite d'acheminement"], fields["Commune"]]))
        return {
            "en": lib + " (positioned: {0}, matching: {1})".format(self.School_FR_loc[fields["Localisation"]]["en"], self.School_FR_app[fields["Qualité d'appariement"]]["en"]),
            "fr": lib + " (position : {0}, appariement : {1})".format(self.School_FR_loc[fields["Localisation"]]["fr"], self.School_FR_app[fields["Qualité d'appariement"]]["fr"]),
        }

    School_FR_loc = {
        "None": {"en": "none", "fr": "aucun"},
        "NE SAIT PAS": {"en": "none", "fr": "aucun"},
        "BATIMENT": {"en": "building", "fr": "bâtiment"},
        "CENTRE_PARCELLE": {"en": "parcel centre", "fr": "centre de la parcelle"},
        "CENTRE_PARCELLE_PROJETE": {"en": "parcel", "fr": "parcelle"},
        "COMMUNE": {"en": "municipality", "fr": "commune"},
        "DEFAUT_DE_NUMERO": {"en": "missing number", "fr": "défaut de numéro"},
        "DEFAUT_DE_TRONCON": {"en": "missing street", "fr": "défaut de troncon"},
        "ENTREE PRINCIPALE": {"en": "main entrance", "fr": "entrée principale"},
        "INTERPOLATION": {"en": "interpolated", "fr": "interpolation"},
        "Lieu-dit": {"en": "locality", "fr": "lieu-dit"},
        "NUMERO (ADRESSE)": {"en": "addresse number", "fr": "numéro d'adresse"},
        "Numéro de rue": {"en": "street number", "fr": "numéro de rue"},
        "PLAQUE_ADRESSE": {"en": "house number", "fr": "plaque adresse"},
        "Rue": {"en": "street", "fr": "rue"},
        "Ville": {"en": "city", "fr": "ville"},
        "ZONE_ADRESSAGE": {"en": "addresse area", "fr": "zone d'adressage"},
        "CENTROIDE (D'EMPRISE)": {"en": "Centroid", "fr": "centroïde d'emprise"},
    }

    School_FR_app = {
        "None": {"en": "none", "fr": "aucun"},
        "Erreur": {"en": "none", "fr": "aucun"},
        "NE SAIT PAS": {"en": "none", "fr": "aucun"},
        "COMMUNE": {"en": "municipality", "fr": "commune"},
        "Correcte": {"en": "good", "fr": "correcte"},
        "Mauvaise": {"en": "bad", "fr": "imparfaite"},
        "DIFF_NOM": {"en": "different name", "fr": "nom dfférent"},
        "DIFF_TYPE": {"en": "different type", "fr": "type différent"},
        "Imparfaite": {"en": "imperfect", "fr": "imparfaite"},
        "MANUEL": {"en": "manual", "fr": "manuel"},
        "METRE": {"en": "meter", "fr": "metre"},
        "Moyenne": {"en": "medium", "fr": "moyenne"},
        "Parfaite": {"en": "parfect", "fr": "parfaite"},
        "SIMILAIRE": {"en": "similar", "fr": "similaire"},
    }

    School_FR_nature_uai = {
        "101": "maternelle",
        "102": "maternelle",
        "103": "maternelle",
        "111": "maternelle",
        "151": "primaire",
        "152": "primaire",
        "153": "primaire",
        "154": "primaire",
        "160": None,
        "161": None,
        "162": "élémentaire",
        "169": "primaire",
        "170": None,
        "300": "lycée",
        "301": "lycée",
        "302": "lycée",
        "306": "lycée",
        "307": "lycée",
        "310": "lycée",
        "312": "secondaire",
        "315": None,
        "320": "lycée",
        "332": None,
        "334": None,
        "335": None,
        "336": None,
        "340": "collège",
        "342": None,
        "344": None,
        "349": None,
        "350": "collège",
        "352": "collège",
        "370": None,
        "380": None,
        "390": None,
    }
