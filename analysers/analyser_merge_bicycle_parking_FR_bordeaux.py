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
import re


class Analyser_Merge_Bicycle_Parking_FR_Bordeaux(Analyser_Merge):

    create_table = """
        cle VARCHAR(254),
        commune VARCHAR(254),
        domanialite VARCHAR(254),
        nature VARCHAR(254),
        nombre VARCHAR(254),
        observations VARCHAR(254),
        proprietaire VARCHAR(254),
        quartier VARCHAR(254),
        realisation VARCHAR(254),
        x_long VARCHAR(254),
        y_lat VARCHAR(254),
        geometrie VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8150", "class": 1, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"Bordeaux bicycle parking not integrated") }
        self.possible_merge   = {"item":"8151", "class": 3, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"Bordeaux bicycle parking integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.bordeaux.fr/content/mobiliers-urbains-stationnement-velo"
        self.officialName = "Mobiliers urbains : Stationnement vélo"
        self.csv_file = "merge_data/bicycle_parking_FR_bordeaux.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS '' CSV HEADER"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.csv_select = {
            "realisation": "Réalisé",
            "nature": ["Arceau vélo", "Rack", "Potelet"],
        }
        self.osmTags = {
            "amenity": "bicycle_parking",
        }
        self.osmTypes = ["nodes"]
        self.sourceTable = "bordeaux_bicycle_parking"
        self.sourceX = "x_long"
        self.sourceY = "y_lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Ville de Bordeaux - 01/2014",
            "amenity": "bicycle_parking",
        }
        self.defaultTagMapping = {
            "capacity": lambda res: res["nombre"] if res["nature"] == "Rack" else str(int(res["nombre"])*2),
        }
        self.conflationDistance = 50
