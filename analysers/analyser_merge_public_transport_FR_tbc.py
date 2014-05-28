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


class Analyser_Merge_Public_Transport_FR_TBC(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8040", "class": 51, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TBC stop not integrated") }
        self.possible_merge   = {"item":"8041", "class": 53, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TBC stop, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=10"
        self.officialName = u"Arrêt physique sur le réseau"
        self.csv_file = "merge_data/public_transport_FR_tbc.csv"
        self.csv_encoding = "ISO-8859-15"
        self.csv_select = {
            "RESEAU": [None, "BUS"]
        }
        self.osmTags = {"highway": "bus_stop"}
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "tbc"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Communauté Urbaine de Bordeaux - 03/2014",
            "highway": "bus_stop",
            "public_transport": "stop_position",
            "bus": "yes",
            "network": "TBC",
        }
        self.defaultTagMapping = {
            "name": lambda res: res['NOMARRET'],
            "shelter": lambda res: "yes" if res["MOBILIE1"] and "abribus" in res["MOBILIE1"].lower() else "no" if res["MOBILIE1"] and "poteau" in res["MOBILIE1"].lower() else None,
        }
        self.conflationDistance = 100
        self.text = lambda tags, fields: {"en": u"TBC stop %s" % fields["NOMARRET"], "fr": u"Arrêt TBC %s" % fields["NOMARRET"]}
