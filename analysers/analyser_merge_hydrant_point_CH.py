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

from Analyser_Merge import Analyser_Merge


class Analyser_Merge_Hydrant_Point_CH(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8090", "class": 1, "level": 3, "tag": ["merge", "hydrant"], "desc": T_(u"Hydrant not integrated") }
        self.possible_merge   = {"item":"8091", "class": 3, "level": 3, "tag": ["merge", "hydrant"], "desc": T_(u"Hydrant, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www1.lausanne.ch/ville-officielle/administration/travaux/eauservice.html"
        self.officialName = u"Bornes hydrantes"
        self.csv_file = "Hydrants_Lausanne.csv.bz2"
        self.csv_separator = ";"
        self.csv_encoding = "utf-8"
        self.osmTags = [{
            "emergency": "fire_hydrant",
        },{
            "amenity": "fire_hydrant",
        }]
        self.osmTypes = ["nodes"]
        self.sourceTable = "hydrant_point_ch"
        self.sourceX = "@lat"
        self.sourceY = "@lon"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Ville de Lausanne - 2013 - Eauservice"
        }
        self.defaultTagMapping = {
            "emergency": "emergency",
            "fire_hydrant:type": "type",
            "fire_hydrant:pressure": "pressure",
            "ref:eauservice": "ref",
        }
        self.conflationDistance = 150
