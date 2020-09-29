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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

# https://gitorious.org/osm-hacks/osm-hacks/trees/master/etablissements-scolaires

class Analyser_Merge_School_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)

        if config.db_schema == 'france_guadeloupe':
            classs = 10
            officialName = u"Guadeloupe"
            self.is_in = lambda code_postal: code_postal[0:3] == "971"
        elif config.db_schema == 'france_guyane':
            classs = 20
            officialName = u"Guyane"
            self.is_in = lambda code_postal: code_postal[0:3] == "973"
        elif config.db_schema == 'france_reunion':
            classs = 30
            officialName = u"Réunion"
            self.is_in = lambda code_postal: code_postal[0:3] == "974"
        elif config.db_schema == 'france_martinique':
            classs = 40
            officialName = u"Martinique"
            self.is_in = lambda code_postal: code_postal[0:3] == "972"
        else:
            classs = 0
            officialName = u"Métropole"
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
            u"https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre",
            u"Adresse et géolocalisation des établissements d'enseignement du premier et second degrés - " + officialName,
            CSV(Source(attribution = u"Ministère de l'Éducation nationale et de la Jeunesse", millesime = "09/2020",
                    fileUrl = u"https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=true",
                    filter = lambda t: t.replace("Ecole", u"École").replace("Saint ", "Saint-").replace("Sainte ", "Sainte-").replace(u"élementaire", u"élémentaire")),
                 separator = u";"),
            Load("Position", "Position",
                xFunction = lambda x: x is not None and x.split(',')[1] or None,
                yFunction = lambda y: y is not None and y.split(',')[0] or None,
                select = {"Code état établissement": ["1", "3"]},
                where = lambda res: res["Code postal"] and self.is_in(res["Code postal"])),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"amenity": "school"}),
                osmRef = "ref:UAI",
                conflationDistance = 50,
                generate = Generate(
                    static2 = {
                        "source": self.source,
                        "amenity": "school"},
                    mapping1 = {
                        "ref:UAI": "Code établissement",
                        "school:FR": lambda res: self.School_FR_nature_uai[res["Code nature"]],
                        "operator:type": lambda res: "private" if res[u"Secteur Public/Privé"] == u"Privé" else "public" if res[u"Secteur Public/Privé"] == u"Public" else None},
                    mapping2 = {"name": lambda res: res["Appellation officielle"].replace(u"Ecole", u"École").replace(u"ECOLE", u"École").replace(u"College", u"Collège").replace(u"elementaire", u"élémentaire").replace(u"ELEMENTAIRE", u"élémentaire") if res["Appellation officielle"] not in ["A COMPLETER", u"Ecole primaire", u"Ecole Primaire", u"ECOLE PRIMAIRE", u"Ecole PRIMAIRE", u"ECOLE Primaire", u"école primaire", u"École Primaire", u"Ecole primaire publique", u"ECOLE PRIMAIRE PUBLIQUE", u"Ecole Primaire Publique", u"Ecole PRIMAIRE publique", u"Ecole primaire privée", u"ECOLE PRIMAIRE PRIVÉE", u"Ecole primaire intercommunale", u"Ecole primaire Intercommunale", u"Ecole Primaire Intercommunale", u"Ecole élémentaire", u"Ecole Elémentaire", u"Ecole elémentaire", u"Ecole élementaire", u"ECOLE ELEMENTAIRE", u"Ecole ELEMENTAIRE", u"Ecole elementaire", u"Ecole Elementaire", u"École Élémentaire", u"école élémentaire", u"Ecole élémentaire publique", u"Ecole élémentaire Publique", u"ECOLE ELEMENTAIRE PUBLIQUE", u"Ecole élémentaire privée", u"Ecole élémentaire intercommunale", u"Ecole élémentaire école publique", u"Ecole maternelle", u"ECOLE MATERNELLE", u"Ecole Maternelle", u"Ecole MATERNELLE", u"École Maternelle", u"école maternelle", u"Ecole maternelle publique", u"ECOLE MATERNELLE PUBLIQUE", u"Ecole Maternelle Publique", u"Ecole maternelle Publique", u"ecole maternelle publique", u"Ecole maternelle intercommunale", u"Ecole maternelle Intercommunale", u"Collège"] else None},
                    text = self.text)))

    def text(self, tags, fields):
        lib = ', '.join(filter(lambda x: x and x != "None", [fields["Appellation officielle"], fields["Adresse"], fields["Lieu dit"], fields["Boite postale"], fields["Code postal"], fields["Localite d'acheminement"], fields["Commune"]]))
        return {
            "en": lib + " (positioned: %s, matching: %s)" % (self.School_FR_loc[fields["Localisation"]]["en"], self.School_FR_app[fields[u"Qualité d'appariement"]]["en"]),
            "fr": lib + " (position : %s, appariement : %s)" % (self.School_FR_loc[fields["Localisation"]]["fr"], self.School_FR_app[fields[u"Qualité d'appariement"]]["fr"]),
        }

    School_FR_loc = {
        "None": {"en": u"none", "fr": u"aucun"},
        "NE SAIT PAS": {"en": u"none", "fr": u"aucun"},
        "BATIMENT": {"en": u"building", "fr": u"bâtiment"},
        "CENTRE_PARCELLE": {"en": u"parcel centre", "fr": u"centre de la parcelle"},
        "CENTRE_PARCELLE_PROJETE": {"en": u"parcel", "fr": u"parcelle"},
        "COMMUNE": {"en": u"municipality", "fr": u"commune"},
        "DEFAUT_DE_NUMERO": {"en": u"missing number", "fr": u"défaut de numéro"},
        "DEFAUT_DE_TRONCON": {"en": u"missing street", "fr": u"défaut de troncon"},
        "ENTREE PRINCIPALE": {"en": u"main entrance", "fr": u"entrée principale"},
        "INTERPOLATION": {"en": u"interpolated", "fr": u"interpolation"},
        "Lieu-dit": {"en": u"locality", "fr": u"lieu-dit"},
        "NUMERO (ADRESSE)": {"en": u"addresse number", "fr": u"numéro d'adresse"},
        u"Numéro de rue": {"en": u"street number", "fr": u"numéro de rue"},
        "PLAQUE_ADRESSE": {"en": u"house number", "fr": u"plaque adresse"},
        "Rue": {"en": u"street", "fr": u"rue"},
        "Ville": {"en": u"city", "fr": u"ville"},
        "ZONE_ADRESSAGE": {"en": u"addresse area", "fr": u"zone d'adressage"},
        "CENTROIDE (D'EMPRISE)": {"en": u"Centroid", "fr": u"centroïde d'emprise"},
    }

    School_FR_app = {
        "None": {"en": u"none", "fr": u"aucun"},
        "Erreur": {"en": u"none", "fr": u"aucun"},
        "NE SAIT PAS": {"en": u"none", "fr": u"aucun"},
        "COMMUNE": {"en": u"municipality", "fr": u"commune"},
        "Correcte": {"en": u"good", "fr": u"correcte"},
        "Mauvaise": {"en": u"bad", "fr": u"imparfaite"},
        "DIFF_NOM": {"en": u"different name", "fr": u"nom dfférent"},
        "DIFF_TYPE": {"en": u"different type", "fr": u"type différent"},
        "Imparfaite": {"en": u"imperfect", "fr": u"imparfaite"},
        "MANUEL": {"en": u"manual", "fr": u"manuel"},
        "METRE": {"en": u"meter", "fr": u"metre"},
        "Moyenne": {"en": u"medium", "fr": u"moyenne"},
        "Parfaite": {"en": u"parfect", "fr": u"parfaite"},
        "SIMILAIRE": {"en": u"similar", "fr": u"similaire"},
    }

    School_FR_nature_uai = {
        "101": u"maternelle",
        "102": u"maternelle",
        "103": u"maternelle",
        "111": u"maternelle",
        "151": u"primaire",
        "152": u"primaire",
        "153": u"primaire",
        "154": u"primaire",
        "160": None,
        "161": None,
        "162": u"élémentaire",
        "169": u"primaire",
        "170": None,
        "300": u"lycée",
        "301": u"lycée",
        "302": u"lycée",
        "306": u"lycée",
        "307": u"lycée",
        "310": u"lycée",
        "312": u"secondaire",
        "315": None,
        "320": u"lycée",
        "332": None,
        "334": None,
        "335": None,
        "336": None,
        "340": u"collège",
        "342": None,
        "344": None,
        "349": None,
        "350": u"collège",
        "352": u"collège",
        "370": None,
        "380": None,
        "390": None,
    }
