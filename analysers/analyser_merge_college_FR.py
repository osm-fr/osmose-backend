#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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


class Analyser_Merge_College_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8030", "class": 100, "level": 3, "tag": ["merge", "railway"], "desc": T_(u"College not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/DataSet/30382046"
        self.officialName = u"Etablissements d'enseignement supérieur"
        self.csv_file = "college_FR.csv.bz2"
        self.osmTags = {
            "amenity": ["college", "university"],
        }
        self.osmTypes = ["nodes", "ways", "relations"]
        self.sourceTable = "college_fr"
        self.sourceX = "GPS_Y"
        self.sourceXfunction = self.float_comma
        self.sourceY = "GPS_X"
        self.sourceYfunction = self.float_comma
        self.sourceSRID = "4326"
        self.defaultTag = {
            "amenity": "college",
            "source": u"data.gouv.fr:Office national d'information sur les enseignements et les professions - 11/2011"
        }
        self.defaultTagMapping = {
            "name": "NOM_ETABLISSEMENT",
            "short_name": "SIGLE_ETABLISSEMENT",
            "operator:type": lambda res: "private" if res["STATUT_ETABLISSEMENT"] in [u"CFA privé", u"Privé hors contrat", u"Privé reconnu", u"Privé sous contrat"] else None,
        }
        self.conflationDistance = 50
        self.text = lambda tags, fields: {"en": " - ".join(filter(lambda i: i != "None", [fields["SIGLE_ETABLISSEMENT"], fields["NOM_ETABLISSEMENT"]]))}
