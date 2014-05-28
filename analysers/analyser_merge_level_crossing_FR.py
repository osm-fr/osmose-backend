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


class Analyser_Merge_Level_Crossing_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8060", "class": 1, "level": 3, "tag": ["merge", "railway"], "desc": T_(u"Crossing level not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Passages-%C3%A0-niveau-30383135"
        self.officialName = u"Passages à niveau"
        self.csv_file = "merge_data/747a4bf66c3ea4a876739de8857bdd09.csv"
        self.csv_separator = ";"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "railway": ["level_crossing", "crossing"],
        }
        self.osmTypes = ["nodes"]
        self.sourceTable = "level_crossing_fr"
        self.sourceWhere = lambda res: res["TYPE"] != 'PN de classe 00'
        self.sourceX = "LONGITUDE (WGS84)"
        self.sourceY = "LATITUDE (WGS84)"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"data.gouv.fr:RFF - 11/2011"
        }
        self.defaultTagMapping = {
            "railway": lambda res: self.type[res["TYPE"]],
        }
        self.conflationDistance = 150

    type = {
        u"PN de classe 00": None,
        u"PN privé isolé pour piétons avec portillons": "crossing",
        u"PN privé isolé pour piétons sans portillons": "crossing",
        u"PN privé pour voitures avec barrières avec passage piétons accolé privé": "level_crossing",
        u"PN privé pour voitures avec barrières avec passage piétons accolé public": "level_crossing",
        u"PN privé pour voitures avec barrières sans passage piétons accolé": "level_crossing",
        u"PN privé pour voitures sans barrières": "level_crossing",
        u"PN public isolé pour piétons avec portillons": "crossing",
        u"PN public isolé pour piétons sans portillons": "crossing",
        u"PN public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à distance": "level_crossing",
        u"PN public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à pied d'oeuvre": "level_crossing",
        u"PN public pour voitures avec barrières gardé sans passage piétons accolé à pied d'oeuvre et distance": "level_crossing",
        u"PN public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à distance": "level_crossing",
        u"PN public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à pied d'oeuvre": "level_crossing",
        u"PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 et SAL 2B": "level_crossing",
        u"PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 + ilôt séparateur": "level_crossing",
        u"PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 4": "level_crossing",
        u"PN public pour voitures sans barrières avec SAL 0": "level_crossing",
        u"PN public pour voitures sans barrières protection assurée par un agent": "level_crossing",
        u"PN public pour voitures sans barrières sans SAL": "level_crossing",
    }
