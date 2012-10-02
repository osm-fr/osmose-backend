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


class Analyser_Merge_Merimee(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.classs[1] = {"item":"8010", "level": 3, "tag": ["merge", "building"], "desc":{"fr":"Monument historique non intégrée"} }
        self.classs[2] = {"item":"7080", "level": 3, "tag": ["merge", "post"], "desc":{"fr":"Monument historique sans ref:mhs ou invalide"} }
        self.classs[3] = {"item":"8011", "level": 3, "tag": ["merge", "post"], "desc":{"fr":"Monument historique, proposition d'intégration"} }
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Liste-des-Immeubles-prot%C3%A9g%C3%A9s-au-titre-des-Monuments-Historiques-30382152"
        self.officialName = "Liste des Immeubles protégés au titre des Monuments Historiques"
        self.osmTags = {
            "heritage": ["1", "2", "3"],
            "heritage:operator": None,
        }
        self.osmRef = "ref:mhs"
        self.osmTypes = ["nodes", "ways", "relations"]
        self.sourceTable = "merimee"
        self.sourceRef = "ref"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "heritage:operator": "mhs",
            "source": "data.gouv.fr:Ministère de la Culture - 08/2011"
        }
        self.defaultTagMapping = {
            "ref:mhs": "ref",
            "name": "tico",
            "mhs:inscription_date": lambda res: u"%s" % res["ppro"][-4:],
            "heritage": lambda res: 2 if "classement par arrêté" in res["ppro"] else 3 if "inscription par arrêté" in res["ppro"] else None,
            "wikipedia": self.wikipedia,
        }
        self.conflationDistance = 1000
        self.text = lambda tags, fields: {"fr":"Monument historique : %s" % ", ".join(filter(lambda x: x!= None and x != "", [fields["ppro"], fields["adrs"], fields["loca"]]))}
        self.WikipediaSearch = re.compile("\[\[.*\]\]")
        self.WikipediaSub = re.compile("[^[]*\[\[([^|]*).*\]\][^]]*")

    def wikipedia(self, res):
        name = res["monument"]
        if re.search(self.WikipediaSearch, name):
            nameWikipedia = re.sub(self.WikipediaSub, "\\1", name)
            return "fr:%s" % nameWikipedia
