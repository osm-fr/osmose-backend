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


class Analyser_Merge_Parking_FR_cub_disabled(Analyser_Merge):

    create_table = """
        x VARCHAR(254),
        y VARCHAR(254),
        gid VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 21, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking disabled not integrated") }
        self.possible_merge   = {"item":"8131", "class": 23, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking disabled integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=8"
        self.officialName = "Place de stationnement PMR"
        self.csv_file = "merge_data/parking_FR_cub_disabled.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        self.osmTags = {
            "amenity": "parking",
            "capacity:disabled": None,
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "cub_parking_disabled"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": "Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "parking",
            "capacity:disabled": "yes",
        }
        self.conflationDistance = 100
