#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.data.gouv.fr/donnees/view/G%C3%A9olocalisation-des-%C3%A9tablissements-d%27enseignement-du-premier-degr%C3%A9-et-du-second-degr%C3%A9-du-minist%C3%A8re-d-30378093",
                name = u"établissements d'enseignement du premier degré et du second degré - " + officialName,
                file = "school_FR.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";", null = "null")),
            Load("X", "Y", srid = srid, table = "School_FR",
                filter = lambda t: t.replace("; ", ";null").replace(";.", ";null").replace("Ecole", u"École").replace("Saint ", "Saint-").replace("Sainte ", "Sainte-").replace(u"élementaire", u"élémentaire"),
                where = self.where),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"amenity": ["school", "kindergarten"]}),
                osmRef = "ref:UAI",
                conflationDistance = 50,
                generate = Generate(
                    static = {
                        "amenity": "school",
                        "source": u"data.gouv.fr:Ministère de l'Éducation nationale, de la Jeunesse et de la Vie associative - 05/2012"},
                    mapping = {
                        "ref:UAI": "numero_uai",
                        "school:FR": self.School_FR,
                        "name": "appellation_officielle_uai",
                        "operator:type": lambda res: "private" if res["denomination_principale_uai"] and "PRIVE" in res["denomination_principale_uai"] else None},
                    text = lambda tags, fields: {"en":fields["appellation_officielle_uai"] if fields["appellation_officielle_uai"] else ""} )))

    School_FR_token = {
        "ECOLE ELEMENTAIRE": u"élémentaire",
        "ECOLE DE NIVEAU ELEMENTAIRE": u"élémentaire",
        "ECOLE MATERNELLE": u"maternelle",
        "ECOLE PRIMAIRE": u"primaire",
        "COLLEGE": u"collège",
        "LYCEE": u"lycée",
        "LP": u"lycée",
        "LYC": u"lycée",
        "ECOLE SECONDAIRE": u"secondaire",
    }

    def School_FR(self, res):
        for k, v in self.School_FR_token.items():
            if res["lib_nature"].startswith(k):
                return v
        return res["lib_nature"]

    # No overlaping bbox
    def where(self, res):
        self.sourceWhere = lambda res: res["_x"] and res["_y"] and self.is_in(float(res["_x"]), float(res["_y"]))


class Analyser_Merge_School_FR_Metropole(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 0, u"Métropole", 2154, logger)

    def is_in(self, x, y):
        return x > -357823.2365 and x < 1313632.3628 and y > 6037008.6939 and y < 7230727.3772


class Analyser_Merge_School_FR_Guadeloupe(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 10, u"Guadeloupe", 2970, logger)

    def is_in(self, x, y):
        return x > 627264 and x < 693664 and y > 1755023 and y < 1826414


class Analyser_Merge_School_FR_Guyane(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 20, u"Guyane", 2972, logger)

    def is_in(self, x, y):
        return x > 166254.8015 and x < 653463.1459 and y > 238817.6898 and y < 1002848.2203


class Analyser_Merge_School_FR_Reunion(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 30, u"Réunion", 2975, logger)

    def is_in(self, x, y):
        return x > 312514 and x < 379436 and y > 7634041 and y < 7693301


class Analyser_Merge_School_FR_Martinique(_Analyser_Merge_School_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_School_FR.__init__(self, config, 40, u"Martinique", 2973, logger)

    def is_in(self, x, y):
        return x > 689211 and x < 735159 and y > 1591528 and y < 1646407
