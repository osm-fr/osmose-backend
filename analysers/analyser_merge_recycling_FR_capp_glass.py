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


class Analyser_Merge_Recycling_FR_capp(Analyser_Merge):

    create_table = """
        typ_dechet VARCHAR(254),
        volume VARCHAR(254),
        usage_ VARCHAR(254),
        type_c_e VARCHAR(254),
        x VARCHAR(254),
        y VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8120", "class": 11, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"CAPP glass recycling not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=8"
        self.officialName = "Point d'apport volontaire du verre : Bornes à verres sur la CAPP"
        self.csv_file = "merge_data/recycling_FR_capp_glass.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.csv_select = {
            "usage_": "En service"
        }
        self.osmTags = {
            "amenity": "recycling",
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "capp_recycling_glass"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Communauté d'Agglomération Pau-Pyrénées - 01/2013",
            "amenity": "recycling",
            "recycling:glass": "yes",
            "recycling:glass_bottles": "yes",
            "recycling_type": "container",
        }
        self.conflationDistance = 100
