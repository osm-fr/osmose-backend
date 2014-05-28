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


class Analyser_Merge_Sport_FR_Gironde_Equestrian(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8170", "class": 1, "level": 3, "tag": ["merge", "sport"], "desc": T_(u"Gironde equestrian spot not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.datalocale.fr/drupal7/dataset/liste-centres-equestre-cdt33"
        self.officialName = u"Liste des centres équestres de Gironde"
        self.csv_file = "merge_data/sport_FR_gironde_equestrian.csv"
        self.osmTags = {
            "sport": "equestrian"
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "gironde_equestrian"
        self.sourceX = "LONGITUDE"
        self.sourceY = "LATITUDE"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Observatoire du comité départemental du Tourisme de la Gironde - 09/2013",
            "sport": "equestrian"
        }
        self.defaultTagMapping = {
            "name": "RAISON_SOCIALE",
            "website": "SITE_WEB",
        }
        self.conflationDistance = 1000
        self.text = lambda tags, fields: {
            "en": u"%s, %s %s %s" % (fields["RAISON_SOCIALE"], fields["ADRESSE"], fields["ADRESSE_SUITE"], fields["COMMUNE"]),
        }
