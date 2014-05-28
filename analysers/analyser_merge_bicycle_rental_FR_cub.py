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


class Analyser_Merge_Bicycle_Rental_FR_CUB(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8160", "class": 1, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"CUB bicycle rental not integrated") }
        self.possible_merge   = {"item":"8161", "class": 3, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"CUB bicycle rental integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=10"
        self.officialName = u"Station VCUB"
        self.csv_file = "bicycle_rental_FR_cub.csv.bz2"
        self.csv_encoding = "ISO-8859-15"
        self.osmTags = {
            "amenity": "bicycle_rental",
        }
        self.osmRef = "ref"
        self.osmTypes = ["nodes"]
        self.sourceTable = "cub_bicycle_rental"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "bicycle_rental",
            "network": "VCUB",
        }
        self.defaultTagMapping = {
            "name": "NOM",
            "ref": "NUMSTAT",
            "capacity": "NBSUPPOR",
            "vending_machine": lambda res: "yes" if res["TERMBANC"] == "OUI" else None,
            "description": lambda res: "VCUB+" if res["TARIF"] == "VLS PLUS" else None,
        }
        self.conflationDistance = 100
