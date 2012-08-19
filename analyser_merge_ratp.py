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


class Analyser_Merge_Ratp(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.classs[1] = {"item":"8040", "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Station RATP non intégrée"} }
        self.classs[3] = {"item":"8041", "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Station RATP, proposition d'intégration"} }
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Positions-g%C3%A9ographiques-des-stations-du-r%C3%A9seau-ferr%C3%A9-RATP-564122"
        self.officialName = "Positions géographiques des stations du réseau ferré RATP"
        self.osmTags = {
            "railway": "station",
        }
        self.osmRef = "ref:FR:RATP"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "ratp"
        self.sourceRef = "id"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "railway": "station",
            "source": "data.gouv.fr:RATP - 07/2012"
        }
        self.defaultTagMapping = {
            "ref:FR:RATP": "id",
            "name": "nom_station",
        }
        self.text = lambda tags, fields: {"fr":"Station RATP de %s" % tags["name"]}
