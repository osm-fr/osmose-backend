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
import psycopg2.extras
from Analyser_Osmosis import Analyser_Osmosis

sql00 = """
CREATE TABLE official (
    ref varchar(254) PRIMARY KEY,
    tags hstore,
    fields hstore,
    geom geometry
);
"""

sql01 = """
SELECT
    %(table)s.%(ref)s AS _ref,
    %(x)s AS _x,
    %(y)s AS _y,
    *
FROM
    osmose.%(table)s
WHERE
    %(x)s IS NOT NULL AND
    %(y)s IS NOT NULL
;
"""

sql02 = """
INSERT INTO
    official
VALUES (
    %(ref)s,
    %(tags)s,
    %(fields)s,
    ST_Transform(ST_SetSRID(ST_MakePoint(%(x)s, %(y)s), %(SRID)s), 4326)
);
"""

sql10 = """
CREATE TABLE missing_offcial AS
SELECT
    official.ref,
    ST_AsText(official.geom),
    official.tags,
    official.fields,
    official.geom
FROM
    official
    LEFT JOIN osm_item ON
        official.ref = osm_item.ref
WHERE
    osm_item.id IS NULL
;
"""

sql11 = """
SELECT * FROM missing_offcial;
"""

sql20 = """
CREATE TABLE missing_osm AS
SELECT
    osm_item.id,
    osm_item.type,
    ST_AsText(osm_item.geom),
    osm_item.tags,
    osm_item.geom
FROM
    osm_item
    LEFT JOIN official ON
        official.ref = osm_item.ref
WHERE
    osm_item.ref IS NULL OR
    official.ref IS NULL
;
"""

sql21 = """
SELECT * FROM missing_osm;
"""

sql30 = """
SELECT
    id,
    type,
    ST_AsText(geom),
    delete(official_tags, 'amenity'),
    osm_tags
FROM (
    SELECT
        DISTINCT ON (ref, id)
        missing_offcial.ref,
        missing_offcial.tags AS official_tags,
        missing_osm.type,
        missing_osm.id,
        missing_osm.tags AS osm_tags,
        missing_osm.geom
    FROM
        missing_offcial,
        missing_osm
    WHERE
        ST_DWithin(missing_offcial.geom::geography, missing_osm.geom::geography, 1000)
    ORDER BY
        ref,
        id,
        ST_Distance(missing_offcial.geom, missing_osm.geom) ASC
) AS t
WHERE
    array_upper(ARRAY(SELECT UNNEST(akeys(delete(delete(osm_tags, 'amenity'), 'source'))) INTERSECT SELECT UNNEST(akeys(official_tags))), 1 ) IS NULL
"""

class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

    def analyser_osmosis(self):
        typeGeom = {'n': 'geom', 'w': 'way_locate(linestring)', 'r': 'relation_locate(id)'}
        self.run("CREATE TABLE osm_item AS" +
            ("UNION".join(
                map(lambda type:
                    "(SELECT '%s' AS type, id, tags->'%s' AS ref, %s AS geom, tags FROM %s WHERE %s)" % (type[0], self.osmRef, typeGeom[type[0]], type, self.where(self.osmTags)),
                    self.osmTypes
                )
            ))
        )
        self.run(sql00)
        giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.run(sql01 % {"table":self.sourceTable, "ref":self.sourceRef, "x":self.sourceX, "y":self.sourceY}, lambda res:
            giscurs.execute(sql02, {
                "ref": res[0],
                "tags": self.tagFactory(res),
                "fields": dict(zip(res.keys(), map(lambda x: str(x), res.values()))),
                "x": res[1], "y": res[2], "SRID": self.sourceSRID
            } )
        )
        self.run(sql10)
        self.run(sql11, lambda res: {
            "class":1, "subclass":str(abs(int(hash(res[0])))),
            "self": lambda r: [0]+r[1:],
            "data": [self.node_new, self.positionAsText],
            "text": self.text(res[2], res[3]),
            "fix": {"+": res[2]},
        } )
        typeMapping = {'n': self.node_full, 'w': self.way_full, 'r': self.relation_full}
        self.run(sql20)
        self.run(sql21, lambda res: {
            "class":2,
            "data": [typeMapping[res[1]], None, self.positionAsText]
        } )
        self.run(sql30, lambda res: {
            "class":3,
            "data": [typeMapping[res[1]], None, self.positionAsText],
            "fix": {"+": res[3], "~": {"source": res[3]['source']}} if res[4].has_key('source') else {"+": res[3]},
        } )

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
