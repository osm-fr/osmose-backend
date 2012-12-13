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

import re
from Analyser_Merge import Analyser_Merge


class Analyser_Merge_Street_Number_Toulouse(Analyser_Merge):

    create_table = """
        no VARCHAR(255),
        numero VARCHAR(255),
        lib_off VARCHAR(255),
        mot_directeur VARCHAR(255),
        sti VARCHAR(255),
        nrivoli VARCHAR(255),
        rivoli VARCHAR(255),
        X_CC43 NUMERIC(11, 3),
        Y_CC43 NUMERIC(11, 3),
        X_WGS84 NUMERIC(11, 8),
        Y_WGS84 NUMERIC(11, 8)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8080", "class": 1, "level": 3, "tag": ["addr"], "desc":{"fr":"Adresse manquante"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.grandtoulouse.fr/les-donnees/-/opendata/card/12673-n-de-rue"
        self.officialName = "GrandToulouse-N° de rue"
        self.csv_file = "merge_data/Numeros.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS '' CSV HEADER"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "addr:housenumber": None,
        }
        self.extraJoin = "addr:housenumber"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "street_number_toulousee"
        self.sourceX = "X_WGS84"
        self.sourceY = "Y_WGS84"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "ToulouseMetropole",
            "source:date": "2012-10-04",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "no",
        }
        self.conflationDistance = 15
        self.text = lambda tags, fields: {"fr":"%s %s" % (fields["no"], fields["lib_off"])}
