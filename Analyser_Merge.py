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
import inspect
from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    %(table)s.%(ref)s AS ref,
    'POINT(' || %(lat)s || ' ' || %(long)s || ')' AS geom,
    %(table)s.*
FROM
    osmose.%(table)s
    LEFT JOIN osm_merged ON
        %(table)s.%(ref)s = osm_merged.ref
WHERE
    osm_merged.ref IS NULL AND
    %(lat)s IS NOT NULL AND
    %(long)s IS NOT NULL
;
"""

class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

    def analyser_osmosis(self):
        self.run("DROP VIEW IF EXISTS osm_merged CASCADE;")
        self.run("CREATE TEMP VIEW osm_merged AS" +
            ("UNION".join(
                map(lambda type:
                    "(SELECT '%s' AS type, id, tags->'%s' AS ref FROM %s WHERE %s)" % (type[0], self.osmRef, type, self.where(self.osmTags)),
                    self.osmTypes
                )
            ))
        )
        self.run(sql10 % {"table":self.sourceTable, "ref":self.sourceRef, "lat":self.sourceLat, "long": self.sourceLong}, lambda res: {
            "class":1, "subclass":str(abs(int(hash(res[0])))),
            "self": lambda r: [0]+r[1:],
            "data": [self.node_new, self.positionAsText],
            "text": self.text(res),
            "fix": {"+": self.tagFactory(res)} } )

    def where(self, tags):
        clauses = []
        for k, v in tags.items():
            clauses.append("tags?'%s'" % k)
            if v:
                clauses.append("tags->'%s' = '%s'" % (k, v))
        return " AND ".join(clauses)

    def tagFactory(self, res):
        tags = dict(self.defaultTag)
        for tag, colomn in self.defaultTagMapping.items():
            if inspect.isfunction(colomn) or inspect.ismethod(colomn):
                try:
                    r = colomn(res)
                    if r:
                        tags[tag] = str(r)
                except:
                    pass
            elif colomn and res.has_key(colomn) and res[colomn]:
                tags[tag] = str(res[colomn])
        return tags
