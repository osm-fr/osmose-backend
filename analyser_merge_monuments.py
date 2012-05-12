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

sql10 = """
SELECT
    %(table)s.%(ref)s AS ref,
    ST_AsText(%(geom)s) AS geom,
    %(table)s.*
FROM
    osmose.%(table)s
    LEFT JOIN osm_merged ON
        %(table)s.%(ref)s = osm_merged.ref
WHERE
    osm_merged.ref IS NULL AND
    lat2 IS NOT NULL AND
    long2 IS NOT NULL
;
"""

class Analyser_Merge_Monuments(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.classs[1] = {"item":"8010", "desc":{"fr":"Monument historique"} }
        self.osmTags = ["heritage", "heritage:operator", "ref:mhs"]
        self.osmRef = "ref:mhs"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "monuments_fr"
        self.sourceRef = "notice"
        self.sourceGeom = "ST_SetSRID(ST_MakePoint(lat2, long2),4326)"
        self.defaultTag = {"heritage:operator": "mhs"}
        self.defaultTagMapping = {"mhs:inscription_date": "date", "ref:mhs": "notice"}
        self.text = lambda res: {"fr":"Manque monument historique name=%s (%s, %s)" % (res["monument"], res["adresse"], res["commune"])}

    heritage = {
        "Classement": 2, "Classé": 2, "classement": 2, "classé": 2,
        "Inscription": 3, "Inscrit": 3, "inscription": 3, "inscrit": 3,
    }

    def extraTagFactory(self, res, tags):
        tags["heritage"] = str(self.heritage[res["protection"]]) if self.heritage.has_key(res["protection"]) else "* (%s)" % res["protection"]

        name = res["monument"]
        if re.search("\[\[.*\]\]", name):
            nameWikipedia = re.sub("[^[]*\[\[([^|]*).*\]\][^]]*", "\\1", name)
            tags["wikipedia"] = "fr:%s" % nameWikipedia
            name = re.sub("\[\[[^|]*\|(.*)\]\]", "\\1", name)
            name = re.sub("\[\[(.*)\]\]", "\\1", name)
