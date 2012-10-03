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

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.classs[1] = {"item":"8050", "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Gare RFN non intégrée"} }
        self.classs[2] = {"item":"7100", "level": 3, "tag": ["merge", "railway"], "desc":{"fr":"Gare sans uic_ref ou invalide"} }
        self.classs[3] = {"item":"8051", "level": 3, "tag": ["merge", "railway"], "desc":{"fr":u"Gare RFN, proposition d'intégration"} }
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Liste-des-gares-de-voyageurs-du-RFN-avec-coordonn%C3%A9es-30383099"
        self.officialName = "Liste des gares de voyageurs du RFN"
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
            "source": "data.gouv.fr:RFN - 12/2011"
        }
        self.defaultTagMapping = {
            "uic_ref": "uic",
            "name": "nom",
        }
        self.conflationDistance = 500
        self.text = lambda tags, fields: {"fr":"Gare de %s %s" % (fields["nom"], fields["adresse"])}
