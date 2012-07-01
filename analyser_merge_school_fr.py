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

# http://www.data.gouv.fr/donnees/view/G%C3%A9olocalisation-des-%C3%A9tablissements-d%27enseignement-du-premier-degr%C3%A9-et-du-second-degr%C3%A9-du-minist%C3%A8re-d-30378093
# https://gitorious.org/osm-hacks/osm-hacks/trees/master/etablissements-scolaires

class Analyser_Merge_School_Fr(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.classs[1] = {"item":"8030", "level": 3, "tag": ["merge"], "desc":{"fr":"École"} }
        self.osmTags = {
            "amenity": "school",
            "school:FR": None,
            "ref:UAI": None,
        }
        self.osmRef = "ref:UAI"
        self.osmTypes = ["nodes", "ways", "relations"]
        self.sourceTable = "school_fr"
        self.sourceRef = "numero_uai"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "amenity": "school",
            "source": "data.gouv.fr:Ministère de l'Éducation nationale, de la Jeunesse et de la Vie associative - 05/2012"
        }
        self.defaultTagMapping = {
            "ref:UAI": "numero_uai",
            "school:FR": self.school_FR,
            "name": "appellation_officielle_uai",
            "operator:type": lambda res: "private" if "PRIVE" in res["denomination_principale_uai"] else None,
        }
        self.text = lambda res: {"fr":"%s" % res["appellation_officielle_uai"] }

    School_FR_token = {
        "ECOLE ELEMENTAIRE": "élémentaire",
        "ECOLE DE NIVEAU ELEMENTAIRE": "élémentaire",
        "ECOLE MATERNELLE": "maternelle",
        "ECOLE PRIMAIRE": "primaire",
        "COLLEGE": "collège",
        "LYCEE": "lycée",
        "LP": "lycée",
        "LYC": "lycée",
        "ECOLE SECONDAIRE": "secondaire",
    }

    def school_FR(self, res):
        for k, v in self.School_FR_token.items():
            if res["lib_nature"].startswith(k):
                return v
        return res["lib_nature"]
