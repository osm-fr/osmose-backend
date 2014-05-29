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


class Analyser_Merge_Bicycle_Parking_FR_Bordeaux(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8150", "class": 1, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"Bordeaux bicycle parking not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.bordeaux.fr/content/mobiliers-urbains-stationnement-velo"
        self.officialName = u"Mobiliers urbains : Stationnement vélo"
        self.csv_file = "bicycle_parking_FR_bordeaux.csv.bz2"
        self.csv_separator = ";"
        self.csv_select = {
            "REALISATION": u"Réalisé",
            "NATURE": [u"Arceau vélo", u"Rack", u"Potelet"],
        }
        self.osmTags = {
            "amenity": "bicycle_parking",
        }
        self.osmTypes = ["nodes"]
        self.sourceTable = "bordeaux_bicycle_parking"
        self.sourceX = "X_LONG"
        self.sourceXfunction = self.float_comma
        self.sourceY = "Y_LAT"
        self.sourceYfunction = self.float_comma
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Ville de Bordeaux - 01/2014",
            "amenity": "bicycle_parking",
        }
        self.defaultTagMapping = {
            "capacity": lambda res: res["NOMBRE"] if res["NATURE"] == "Rack" else str(int(res["NOMBRE"])*2),
        }
        self.conflationDistance = 50
