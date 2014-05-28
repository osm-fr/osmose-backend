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

from Analyser_Merge import Analyser_Merge


class Analyser_Merge_Parking_FR_cub(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 31, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking not integrated") }
        self.possible_merge   = {"item":"8131", "class": 33, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=10" # joins on http://data.lacub.fr/data.php?themes=1
        self.officialName = u"Parking public données techniques" # joins on "Équipement public"
        self.csv_file = "merge_data/parking_FR_cub.csv"
        self.csv_select = {
            u"PARKINGS_DONNEES_Propriétaire": ["CUB", "CHU"]
        }
        self.osmTags = {
            "amenity": "parking",
        }
        self.osmRef = "ref:FR:CUB"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "cub_parking"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "parking",
        }
        self.defaultTagMapping = {
            "ref:FR:CUB": "IDENT",
            "start_date": "PARKINGS_DONNEES_Année de mise en service",
            "parking": lambda res: "surface" if "surface" in res["PARKINGS_DONNEES_Type de construction"].lower() else "underground" if u"enterré" in res["PARKINGS_DONNEES_Type de construction"].lower() else None,
            "levels": "PARKINGS_DONNEES_Nombre de niveaux",
            "capacity": "PARKINGS_DONNEES_Total places VL",
            "capacity:disabled": "PARKINGS_DONNEES_Dont places PMR",
            "name": "PARKINGS_DONNEES_Nom du parking",
            "operator": "PARKINGS_DONNEES_Exploitant",
        }
        self.conflationDistance = 300
        self.text = lambda tags, fields: {"en": u"Parking %s" % fields[u"PARKINGS_DONNEES_Nom du parking"]}


class Analyser_Merge_Parking_FR_cub_disabled(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 21, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking disabled not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=8"
        self.officialName = u"Place de stationnement PMR"
        self.csv_file = "merge_data/parking_FR_cub_disabled.csv"
        self.csv_encoding = "ISO-8859-15"
        self.osmTags = {
            "amenity": "parking",
            "capacity:disabled": None,
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "cub_parking_disabled"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "parking",
            "capacity:disabled": "yes",
        }
        self.conflationDistance = 100
