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


class Analyser_Merge_RailStation_Fr(Analyser_Merge):

    create_table = """
        uic VARCHAR(254) PRIMARY KEY,
        nom VARCHAR(254),
        adresse VARCHAR(254),
        type VARCHAR(254),
        region VARCHAR(254),
        lat NUMERIC(10,7),
        lon NUMERIC(10,7)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8050", "class": 1, "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Gare RFN non intégrée"} }
        self.missing_osm      = {"item":"7100", "class": 2, "level": 3, "tag": ["merge", "railway"], "desc":{"fr":"Gare sans uic_ref ou invalide"} }
        self.possible_merge   = {"item":"8051", "class": 3, "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Gare RFN, proposition d'intégration"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Liste-des-gares-de-voyageurs-du-RFN-avec-coordonn%C3%A9es-30383099"
        self.officialName = "Liste des gares de voyageurs du RFN"
        self.csv_file = "merge_data/liste_gares_ferroviaires_DRR2012_23-11-2011.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS 'null' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "railway": ["station", "halt"],
        }
        self.osmRef = "uic_ref"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "railstation_fr"
        self.sourceRef = "uic"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "railway": "station",
            "source": "data.gouv.fr:RFF - 12/2011"
        }
        self.defaultTagMapping = {
            "uic_ref": "uic",
            "name": "nom",
        }
        self.conflationDistance = 500
        self.text = lambda tags, fields: {"fr":"Gare de %s %s" % (fields["nom"], fields["adresse"])}
