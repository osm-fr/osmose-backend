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


class Analyser_Merge_Wikipedia_Insee_FR(Analyser_Merge):

    create_table = """
        insee VARCHAR(254) PRIMARY KEY,
        title VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.update_official = {"item":"8101", "class": 100, "level": 3, "tag": ["merge", "wikipedia"], "desc": {"fr":"Mise à jour tag wikipedia"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://wikipedia.fr"
        self.officialName = "wikipedia insee"
        self.csv_file = "merge_data/wikipedia_insee_FR.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV"
        self.csv_encoding = "UTF-8"
        self.osmTags = {
            "type": "boundary",
            "boundary": "administrative",
            "admin_level": "8",
        }
        self.osmRef = "ref:INSEE"
        self.osmTypes = ["relations"]
        self.sourceTable = "wikipedia_insee_FR"
        self.defaultTag = {}
        self.defaultTagMapping = {
            "ref:INSEE": "insee",
            "wikipedia": lambda res: "fr:"+res["title"],
        }
