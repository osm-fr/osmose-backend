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

    create_table = """
        x VARCHAR(254),
        y VARCHAR(254),
        gid VARCHAR(254),
        numstat VARCHAR(254),
        ident VARCHAR(254),
        adresse VARCHAR(254),
        commune VARCHAR(254),
        dateserv VARCHAR(254),
        ligncorr VARCHAR(254),
        nbsuppor VARCHAR(254),
        nom VARCHAR(254),
        tarif VARCHAR(254),
        termbanc VARCHAR(254),
        typea VARCHAR(254),
        geom_o VARCHAR(254),
        cdate VARCHAR(254),
        mdate VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8160", "class": 1, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"CUB bicycle rental not integrated") }
        self.possible_merge   = {"item":"8161", "class": 3, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"CUB bicycle rental integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=10"
        self.officialName = "Station VCUB"
        self.csv_file = "merge_data/bicycle_rental_FR_cub.csv"
        self.csv_encoding = "ISO-8859-15"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.osmTags = {
            "amenity": "bicycle_rental",
        }
        self.osmRef = "ref"
        self.osmTypes = ["nodes"]
        self.sourceTable = "cub_bicycle_rental"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": "Communauté Urbaine de Bordeaux -03/2014",
            "amenity": "bicycle_rental",
            "network": "VCUB",
        }
        self.defaultTagMapping = {
            "name": "nom",
            "ref": "numstat",
            "capacity": "nbsuppor",
            "vending_machine": lambda res: "yes" if res["termbanc"] == "OUI" else None,
            "description": lambda res: "VCUB+" if res["tarif"] == "VLS PLUS" else None,
        }
        self.conflationDistance = 100
