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


class Analyser_Merge_Hydrant_Point_CH(Analyser_Merge):

    create_table = """
        id VARCHAR(254),
        lat NUMERIC(10,7),
        lon NUMERIC(10,7),
        emergency VARCHAR(254),
        type VARCHAR(254),
        pressure VARCHAR(254),
        ref VARCHAR(254),
        source VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8090", "class": 1, "level": 3, "tag": ["merge", "hydrant"], "desc":{"fr":u"Borne hydrante non intégrée", "es": u"Boca de terminal no integrada"} }
        self.possible_merge   = {"item":"8091", "class": 3, "level": 3, "tag": ["merge", "hydrant"], "desc":{"fr":u"Borne hydrante, proposition d'intégration", "es": u"Boca de terminal, propuesta de integración"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www1.lausanne.ch/ville-officielle/administration/travaux/eauservice.html"
        self.officialName = "Bornes hydrantes"
        self.csv_file = "merge_data/Hydrants_Lausanne.csv"
        # CSV header :
        # @id;@lon;@lat;emergency;fire_hydrant:type;fire_hydrant:pressure;ref:eauservice;source
        self.csv_format = "WITH DELIMITER AS ';' NULL AS '' CSV HEADER"
        self.csv_encoding = "utf-8"
        self.osmTags = [{
            "emergency": "fire_hydrant",
        },{
            "amenity": "fire_hydrant",
        }]
        self.osmTypes = ["nodes"]
        self.sourceTable = "hydrant_point_ch"
        self.sourceX = "lat"
        self.sourceY = "lon"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Ville de Lausanne - 2013 - Eauservice"
        }
        self.defaultTagMapping = {
            "emergency": "emergency",
            "fire_hydrant:type": "type",
            "fire_hydrant:pressure": "pressure",
            "ref:eauservice": "ref",
        }
        self.conflationDistance = 150
