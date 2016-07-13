#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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

from Analyser_Merge import Analyser_Merge, Source, CSV, SHP, Load, Mapping, Select, Generate


class Analyser_Merge_Parking_FR_cub(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 31, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking not integrated") }
        self.possible_merge   = {"item":"8131", "class": 33, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            "http://data.lacub.fr/data.php?themes=10", # joins on http://data.lacub.fr/data.php?themes=1
            u"Parking public données techniques", # joins on "Équipement public"
            CSV(Source(file = "parking_FR_cub.csv.bz2")),
            Load("X", "Y", srid = 2154,
                select = {u"PARKINGS_DONNEES_Propriétaire": ["CUB", "CHU"]}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "parking"}),
                osmRef = "ref:FR:CUB",
                conflationDistance = 300,
                generate = Generate(
                    static = {
                        "source": u"Communauté Urbaine de Bordeaux - 03/2014",
                        "amenity": "parking"},
                    mapping = {
                        "ref:FR:CUB": "IDENT",
                        "start_date": "PARKINGS_DONNEES_Année de mise en service",
                        "parking": lambda res: "surface" if "surface" in res["PARKINGS_DONNEES_Type de construction"].lower() else "underground" if u"enterré" in res["PARKINGS_DONNEES_Type de construction"].lower() else None,
                        "levels": "PARKINGS_DONNEES_Nombre de niveaux",
                        "capacity": "PARKINGS_DONNEES_Total places VL",
                        "capacity:disabled": "PARKINGS_DONNEES_Dont places PMR",
                        "name": "PARKINGS_DONNEES_Nom du parking",
                        "operator": "PARKINGS_DONNEES_Exploitant"},
                    text = lambda tags, fields: {"en": u"Parking %s" % fields[u"PARKINGS_DONNEES_Nom du parking"]} )))


class Analyser_Merge_Parking_FR_cub_disabled(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 21, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking disabled not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "http://data.lacub.fr/data.php?themes=8",
            u"Place de stationnement PMR",
            SHP(Source(fileUrl = "http://data.bordeaux-metropole.fr/files.php?gid=73&format=2", zip = "GRS_GIGC_P.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {
                        "amenity": "parking",
                        "capacity:disabled": None}),
                conflationDistance = 100,
                generate = Generate(
                    static = {
                        "source": u"Communauté Urbaine de Bordeaux - 03/2014",
                        "amenity": "parking",
                        "capacity:disabled": "yes"} )))