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


class Analyser_Merge_Monuments(Analyser_Merge):

    protection = {
        "Classement": 2, "Classé": 2, "classement": 2, "classé": 2,
        "Inscription": 3, "Inscrit": 3, "inscription": 3, "inscrit": 3,
    }

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.classs[1] = {"item":"8010", "level": 3, "tag": ["merge", "building"], "desc":{"fr":"Monument historique non intégrée"} }
        self.classs[2] = {"item":"7080", "level": 3, "tag": ["merge", "post"], "desc":{"fr":u"Monument historique sans ref:mhs ou invalide"} }
        self.classs[3] = {"item":"8011", "level": 3, "tag": ["merge", "post"], "desc":{"fr":u"Monument historique, proposition d'intégration"} }
        self.officialURL = "http://fr.wikipedia.org"
        self.officialName = "Monuments Historiques - base mérimée via wikipédia"
        self.osmTags = {
            "heritage": ["1", "2", "3"],
            "heritage:operator": None,
        }
        self.osmRef = "ref:mhs"
        self.osmTypes = ["nodes", "ways", "relations"]
        self.sourceTable = "monuments_fr"
        self.sourceRef = "notice"
        self.sourceX = "long2"
        self.sourceY = "lat2"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "heritage:operator": "mhs"
        }
        self.defaultTagMapping = {
            "mhs:inscription_date": "date",
            "ref:mhs": "notice",
            "heritage": lambda res: self.protection[res["protection"]] if self.protection.has_key(res["protection"]) else res["protection"],
            "wikipedia": self.wikipedia,
        }
        self.text = lambda tags, fields: {"fr":"Monument historique : %s" % ", ".join(filter( lambda x: x!= None and x != "", [fields["monument"], fields["adresse"], fields["commune"]]))}
        self.WikipediaSearch = re.compile("\[\[.*\]\]")
        self.WikipediaSub = re.compile("[^[]*\[\[([^|]*).*\]\][^]]*")

    def wikipedia(self, res):
        name = res["monument"]
        if re.search(self.WikipediaSearch, name):
            nameWikipedia = re.sub(self.WikipediaSub, "\\1", name)
            return "fr:%s" % nameWikipedia
