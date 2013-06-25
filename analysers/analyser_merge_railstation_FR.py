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


class Analyser_Merge_RailStation_FR(Analyser_Merge):

    create_table = """
        stop_id VARCHAR(254) PRIMARY KEY,
        stop_name VARCHAR(254),
        stop_desc VARCHAR(254),
        stop_lat VARCHAR(254),
        stop_lon VARCHAR(254),
        zone_id VARCHAR(254),
        stop_url VARCHAR(254),
        location_type VARCHAR(254),
        parent_station VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8050", "class": 1, "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Gare non intégrée", "es": u"Estación no integrada"} }
        self.missing_osm      = {"item":"7100", "class": 2, "level": 3, "tag": ["merge", "railway"], "desc":{"fr": u"Gare sans uic_ref ou invalide", "es": u"Estación sin uic_ref o inválida"} }
        self.possible_merge   = {"item":"8051", "class": 3, "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Gare, proposition d'intégration", "es": u"Estación, propuesta de integración"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://test.data-sncf.com/index.php/ter.html"
        self.officialName = "Horaires prévus des trains TER"
        self.csv_file = "merge_data/Horaires prévus des trains TER-stops.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_select = {
            "stop_id": "StopArea:%"
        }
        self.osmTags = {
            "railway": ["station", "halt"],
        }
        self.osmRef = "uic_ref"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "railstation_fr"
        self.sourceX = "stop_lon"
        self.sourceY = "stop_lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "railway": "station",
            "operator": "SNCF",
            "source": "SNCF - 06/2013"
        }
        self.defaultTagMapping = {
            "uic_ref": lambda res: res["stop_id"].split(":")[1][3:].split("-")[-1][:-1],
            "name": lambda res: res["stop_name"].replace("gare de ", ""),
        }
        self.conflationDistance = 500
        self.text = lambda tags, fields: {"fr": fields["stop_name"][0].upper() + fields["stop_name"][1:]}
