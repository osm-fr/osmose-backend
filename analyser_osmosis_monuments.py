#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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
from Analyser_Osmosis import Analyser_Osmosis

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

class Analyser_Osmosis_Monuments(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"7011", "desc":{"fr":"Monument historique"} }
        self.osmTags = ["heritage", "heritage:operator", "ref:mhs"]
        self.osmRef = "ref:mhs"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "monuments_fr"
        self.sourceRef = "notice"
        self.sourceGeom = "ST_SetSRID(ST_MakePoint(lat2, long2),4326)"
        self.defaultTag = {"heritage:operator": "mhs"}
        self.defaultTagMapping = {"mhs:inscription_date": "date", "ref:mhs": "notice"}
        self.text = lambda res: {"fr":"Manque monument historique name=%s (%s, %s)" % (res["monument"], res["adresse"], res["commune"])}

    def analyser_osmosis(self):
        self.run("DROP VIEW IF EXISTS osm_merged CASCADE;")
        self.run("CREATE TEMP VIEW osm_merged AS" +
            ("UNION".join(
                map(lambda type:
                    "(SELECT '%s' AS type, id, tags->'%s' AS ref FROM %s WHERE %s)" % (
                        type[0],
                        self.osmRef,
                        type,
                        " AND ".join(map(lambda tag: "tags?'%s'" % tag, self.osmTags))
                    ),
                    self.osmTypes
                )
            ))
        )
        self.run(sql10 % {"table":self.sourceTable, "ref":self.sourceRef, "geom":self.sourceGeom}, lambda res: {
            "class":1, "subclass":str(abs(int(hash(res[0])))),
            "self": lambda r: [0]+r[1:],
            "data": [self.node_new, self.positionAsText],
            "text": self.text(res),
            "fix": {"+": self.tagFactory(res, self.extraTagFactory)} } )

    def tagFactory(self, res, extraTagFactory):
        tags = dict(self.defaultTag)
        tags.update(dict((tag, str(res[colomn])) for tag, colomn in self.defaultTagMapping.items()))
        extraTagFactory(res, tags)
        return tags

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
