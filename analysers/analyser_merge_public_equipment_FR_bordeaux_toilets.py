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


class Analyser_Merge_Public_Equipment_FR_Bordeaux_Toilets(Analyser_Merge):

    create_table = """
        cle VARCHAR(254),
        adresse VARCHAR(254),
        nom VARCHAR(254),
        options VARCHAR(254),
        quartier VARCHAR(254),
        typologie VARCHAR(254),
        x_long VARCHAR(254),
        y_lat VARCHAR(254),
        geometrie VARCHAR(254),
        num_quartier VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8160", "class": 1, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Bordeaux bicycle parking not integrated") }
        self.possible_merge   = {"item":"8161", "class": 3, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Bordeaux bicycle parking integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.bordeaux.fr/content/toilettes-publiques"
        self.officialName = "Toilettes publiques"
        self.csv_file = "merge_data/public_equipment_FR_bordeaux_toilets.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS '' CSV HEADER"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "amenity": "toilets",
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "bordeaux_toilets"
        self.sourceX = "x_long"
        self.sourceY = "y_lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Ville de Bordeaux - 01/2014",
            "amenity": "toilets",
            "fee": "no",
            "access": "public",
        }
        self.defaultTagMapping = {
            "toilets:wheelchair": lambda res: "yes" if res["options"] == u"Handicapé" else None,
            "toilets:position": lambda res: "urinal" if res["typologie"] == u"Urinoir" else None,
        }
        self.conflationDistance = 100
