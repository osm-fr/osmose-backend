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


class Analyser_Merge_Recycling_FR_cub(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8120", "class": 1, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"CUB glass recycling not integrated") }
        self.possible_merge   = {"item":"8121", "class": 1, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"CUB glass recycling, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=5"
        self.officialName = u"Emplacements d'apport volontaire"
        self.csv_file = "recycling_FR_cub.csv.bz2"
        self.csv_encoding = "ISO-8859-15"
        self.csv_select = {
            "IDENT": "%"
        }
        self.osmTags = {
            "amenity": "recycling",
        }
        self.osmRef = "ref:FR:CUB"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "cub_recycling_glass"
        self.sourceX = "IDENT_X"
        self.sourceY = "IDENT_Y"
        self.sourceSRID = "3945"
        self.defaultTag = {
            "source": u"Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "recycling",
            "recycling:glass": "yes",
            "recycling:glass_bottles": "yes",
            "recycling_type": "container",
        }
        self.defaultTagMapping = {
            "ref:FR:CUB": "IDENT",
        }
        self.conflationDistance = 100
