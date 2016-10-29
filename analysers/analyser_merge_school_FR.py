#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

# https://gitorious.org/osm-hacks/osm-hacks/trees/master/etablissements-scolaires

class _Analyser_Merge_School_FR(Analyser_Merge):
    def __init__(self, config, classs, officialName, srid, logger = None):
        self.missing_official = {"item":"8030", "class": classs+1, "level": 3, "tag": ["merge"], "desc": T_(u"School not integrated") }
        self.missing_osm      = {"item":"7070", "class": classs+2, "level": 3, "tag": ["merge"], "desc": T_(u"School without ref:UAI or invalid") }
        self.possible_merge   = {"item":"8031", "class": classs+3, "level": 3, "tag": ["merge"], "desc": T_(u"School, integration suggestion") }
        self.update_official  = {"item":"8032", "class": classs+4, "level": 3, "tag": ["merge"], "desc": T_(u"School update") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/adresse-et-geolocalisation-des-etablissements-denseignement-du-premier-et-second-degres/",
            u"Adresse et géolocalisation des établissements d'enseignement du premier et second degrés - " + officialName,
            CSV(Source(attribution = u"data.gouv.fr:Éducation Nationale", millesime = "05/2016",
                    file = "school_FR.csv.bz2", encoding = "ISO-8859-15",
                filter = lambda t: t.replace("Ecole", u"École").replace("Saint ", "Saint-").replace("Sainte ", "Sainte-").replace(u"élementaire", u"élémentaire"))),
            Load("X", "Y", srid = srid,
                select = {"etat_etablissement": ["1", "3"]},
                where = lambda res: res["nature_uai"][0] != "8" and res["code_postal_uai"] and self.is_in(res["code_postal_uai"])),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"amenity": ["school", "kindergarten"]}),
                osmRef = "ref:UAI",
                conflationDistance = 50,
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {
                        "amenity": lambda res: "kindergarten" if res["nature_uai"] in ("101", "102", "103", "111") else "school",
                        "ref:UAI": "numero_uai",
                        "school:FR": lambda res: self.School_FR_nature_uai[res["nature_uai"]],
                        "operator:type": lambda res: "private" if res["secteur_public_prive"] == "PR" else None},
                    mapping2 = {"name": "appellation_officielle_uai"},
                    text = self.text)))

    def text(self, tags, fields):
      lib = ', '.join(filter(lambda x: x and x != 'None', [fields["appellation_officielle_uai"], fields["adresse_uai"], fields["lieu_dit_uai"], fields["boite_postale_uai"], fields["code_postal_uai"], fields["localite_acheminement_uai"], fields[""]]))
      return {
          "en": lib + " (positioned: %s, matching: %s)" % (self.School_FR_loc[fields["loc"]]["en"], self.School_FR_app[fields["app"]]["en"]),
          "fr": lib + " (position : %s, appariement : %s)" % (self.School_FR_loc[fields["loc"]]["fr"], self.School_FR_app[fields["app"]]["fr"]),
      }

    School_FR_loc = {
        "None": {"en": u"none", "fr": u"aucun"},
        "AUCUN": {"en": u"none", "fr": u"aucun"},
        "BATIMENT": {"en": u"building", "fr": u"bâtiment"},
        "CENTRE_PARCELLE_PROJETE": {"en": u"parcel", "fr": u"parcelle"},
        "COMMUNE": {"en": u"city", "fr": u"commune"},
        "DEFAUT_DE_NUMERO": {"en": u"missing number", "fr": u"défaut de numéro"},
        "DEFAUT_DE_TRONCON": {"en": u"missing street", "fr": u"défaut de troncon"},
        "DIFF_NOM": {"en": u"different name", "fr": u"nom dfférent"},
        "DIFF_TYPE": {"en": u"different type", "fr": u"type différent"},
        "INTERPOLATION": {"en": u"interpolated", "fr": u"interpolation"},
        "MANUEL": {"en": u"manual", "fr": u"manuel"},
        "PLAQUE_ADRESSE": {"en": u"house number", "fr": u"plaque adresse"},
        "SIMILAIRE": {"en": u"similar", "fr": u"similaire"},
        "ZONE_ADRESSAGE": {"en": u"addresse area", "fr": u"zone d'adressage"},
    }

    School_FR_app = {
        "None": {"en": u"none", "fr": u"aucun"},
        "AUCUN": {"en": u"none", "fr": u"aucun"},
        "DIFF_NOM": {"en": u"different name", "fr": u"nom dfférent"},
        "DIFF_TYPE": {"en": u"different type", "fr": u"type différent"},
        "MANUEL": {"en": u"manual", "fr": u"manuel"},
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
        "349": None,
        "350": u"collège",
        "352": u"collège",
        "370": None,
        "380": None,
        "390": None,
    }

class Analyser_Merge_School_FR_Metropole(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 0, u"Métropole", 2154, logger)

    def is_in(self, code_postal):
        return code_postal[0:2] != "97"


class Analyser_Merge_School_FR_Guadeloupe(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 10, u"Guadeloupe", 2970, logger)

    def is_in(self, code_postal):
        return code_postal[0:3] == "971"


class Analyser_Merge_School_FR_Guyane(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 20, u"Guyane", 2972, logger)

    def is_in(self, code_postal):
        return code_postal[0:3] == "973"


class Analyser_Merge_School_FR_Reunion(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 30, u"Réunion", 2975, logger)

    def is_in(self, code_postal):
        return code_postal[0:3] == "974"


class Analyser_Merge_School_FR_Martinique(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 40, u"Martinique", 2973, logger)

    def is_in(self, code_postal):
        return code_postal[0:3] == "972"
