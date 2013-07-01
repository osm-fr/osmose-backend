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


class _Analyser_Merge_Ratp(Analyser_Merge):

    create_table = """
        id VARCHAR(254),
        lon VARCHAR(254),
        lat VARCHAR(254),
        nom_station VARCHAR(254),
        ville_cp VARCHAR(254),
        reseau VARCHAR(254)
    """

    def __init__(self, config, logger, clas, select, osmTags, defaultTag):
        self.missing_official = {"item":"8040", "class": 1+10*clas, "level": 3, "tag": ["merge", "railway"], "desc":{"en": u"RATP station not integrated", "fr":u"Station RATP non intégrée", "es": u"Estación RATP no integrada"} }
        self.possible_merge   = {"item":"8041", "class": 3+10*clas, "level": 3, "tag": ["merge", "railway"], "desc":{"en": u"RATP station, integration suggestion", "fr":u"Station RATP, proposition d'intégration", "es": u"Estación RATP, proposición de integración"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.ratp.fr/fr/les-donnees/fiche-de-jeu-de-donnees/dataset/positions-geographiques-des-stations-du-reseau-ratp.html"
        self.officialName = "Positions géographiques des stations du réseau RATP"
        self.csv_file = "merge_data/ratp_arret_graphique.csv"
        self.csv_format = "WITH DELIMITER AS '#' NULL AS '' CSV"
        self.csv_select = {
            "reseau": select
        }
        self.osmTags = osmTags
        self.osmRef = "ref:FR:RATP"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "ratp"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "RATP - 07/2012",
        }
        self.defaultTag.update(defaultTag)
        self.defaultTagMapping = {
            "ref:FR:RATP": "id",
            "name": "nom_station",
        }
        self.conflationDistance = 100
        self.text = lambda tags, fields: {"en": u"RATP station of %s" % tags["name"], "fr": u"Station RATP de %s" % tags["name"]}


#class Analyser_Merge_Ratp_Bus(_Analyser_Merge_Ratp):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_Ratp.__init__(self, config, logger, 3, "bus", {"highway": "bus_stop"}, {"highway": "bus_stop", "public_transport": "stop_position", "bus": "yes"})

class Analyser_Merge_Ratp_Metro(_Analyser_Merge_Ratp):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Ratp.__init__(self, config, logger, 0, "metro", {"railway": "station"}, {"railway": "station"})

class Analyser_Merge_Ratp_RER(_Analyser_Merge_Ratp):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Ratp.__init__(self, config, logger, 1, "rer", {"railway": "station"}, {"railway": "station"})

class Analyser_Merge_Ratp_Tram(_Analyser_Merge_Ratp):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Ratp.__init__(self, config, logger, 2, "tram", {"railway": "tram_stop"}, {"railway": "tram_stop", "public_transport": "stop_position", "tram": "yes"})
