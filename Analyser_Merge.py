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
    %(y)s IS NOT NULL AND
    %(x)s::varchar != '' AND
    %(y)s::varchar != ''
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
    official.geom::geography
FROM
    official
    LEFT JOIN osm_item ON
        official.ref = osm_item.ref
WHERE
    osm_item.id IS NULL
;
CREATE INDEX missing_offcial_index_ref ON missing_offcial(ref);
CREATE INDEX missing_offcial_index_geom ON missing_offcial USING GIST(geom);
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
    osm_item.geom::geography
FROM
    osm_item
    LEFT JOIN official ON
        official.ref = osm_item.ref
WHERE
    osm_item.ref IS NULL OR
    official.ref IS NULL
;
CREATE INDEX missing_osm_index_geom ON missing_osm USING GIST(geom);
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
        ST_DWithin(missing_offcial.geom, missing_osm.geom, 1000)
    ORDER BY
        ref,
        id,
        ST_Distance(missing_offcial.geom, missing_osm.geom) ASC
) AS t
WHERE
    NOT akeys(delete(delete(osm_tags, 'amenity'), 'source')) && akeys(official_tags)
;
"""

sql40 = """
CREATE TABLE match AS
SELECT
    osm_item.id,
    osm_item.type,
    osm_item.tags,
    osm_item.geom
FROM
    osm_item
    JOIN official ON
        official.ref = osm_item.ref
;
"""

sql41 = """
(
    SELECT
        id AS osm_id,
        type AS osm_type,
        tags,
        ST_X(geom::geometry) AS lon,
        ST_Y(geom::geometry) AS lat
    FROM
        match
) UNION (
    SELECT
        NULL AS osm_id,
        NULL AS osm_type,
        tags,
        ST_X(geom::geometry) AS lon,
        ST_Y(geom::geometry) AS lat
    FROM
        missing_offcial
) UNION (
    SELECT
        id AS osm_id,
        type AS osm_type,
        tags,
        ST_X(geom::geometry) AS lon,
        ST_Y(geom::geometry) AS lat
    FROM
        missing_osm
);
"""

class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

    def analyser_osmosis(self):
        # Convert
        typeGeom = {'n': 'geom', 'w': 'way_locate(linestring)', 'r': 'relation_locate(id)'}
        self.run("CREATE TABLE osm_item AS" +
            ("UNION".join(
                map(lambda type:
                    "(SELECT '%(type)s' AS type, id, tags->'%(ref)s' AS ref, %(geom)s AS geom, tags FROM %(from)s WHERE %(geom)s IS NOT NULL AND %(where)s)" %
                        {"type":type[0], "ref":self.osmRef, "geom":typeGeom[type[0]], "from":type, "where":self.where(self.osmTags)},
                    self.osmTypes
                )
            ))
        )
        self.run("CREATE INDEX osm_item_index_ref ON osm_item(ref)")
        self.run(sql00)
        giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.run(sql01 % {"table":self.sourceTable, "ref":self.sourceRef, "x":self.sourceX, "y":self.sourceY}, lambda res:
            giscurs.execute(sql02, {
                "ref": res[0],
                "tags": self.tagFactory(res),
                "fields": dict(zip(dict(res).keys(), map(lambda x: str(x), dict(res).values()))),
                "x": res[1], "y": res[2], "SRID": self.sourceSRID
            } )
        )

        # Missing official
        self.run(sql10)
        self.run(sql11, lambda res: {
            "class":1, "subclass":str(abs(int(hash(res[0])))),
            "self": lambda r: [0]+r[1:],
            "data": [self.node_new, self.positionAsText],
            "text": self.text(res[2], res[3]),
            "fix": {"+": res[2]},
        } )

        # Missing OSM
        self.run(sql20)
        if self.classs.has_key(2):
            typeMapping = {'n': self.node_full, 'w': self.way_full, 'r': self.relation_full}
            self.run(sql21, lambda res: {
                "class":2,
                "data": [typeMapping[res[1]], None, self.positionAsText]
            } )

        # Possible merge
        if self.classs.has_key(3):
            self.run(sql30, lambda res: {
                "class":3,
                "data": [typeMapping[res[1]], None, self.positionAsText],
                "text": self.text(res[2], res[3]),
                "fix": {"+": res[3], "~": {"source": res[3]['source']}} if res[4].has_key('source') else {"+": res[3]},
            } )

        self.dumpCSV("SELECT ST_X(geom) AS lon, ST_Y(geom) AS lat, tags FROM official", "", ["lon","lat"], lambda r, cc:
            list((r['lon'], r['lat'])) + cc
        )

        self.run(sql40)
        self.dumpCSV(sql41, ".byOSM", ["osm_id","osm_type","lon","lat"], lambda r, cc:
            list((r['osm_id'], r['osm_type'], r['lon'], r['lat'])) + cc
        )

        file = open("%s/%s.metainfo.csv" % (self.config.dst_dir, self.officialName), "w")
        file.write("file,origin,osm_date,official_non_merged,osm_non_merged,merged\n")
        self.giscurs.execute("SELECT COUNT(*) FROM missing_offcial;")
        official_non_merged = self.giscurs.fetchone()[0]
        self.giscurs.execute("SELECT COUNT(*) FROM missing_osm;")
        osm_non_merged = self.giscurs.fetchone()[0]
        self.giscurs.execute("SELECT COUNT(*) FROM match;")
        merged = self.giscurs.fetchone()[0]
        file.write("\"%s\",\"%s\",FIXME,%s,%s,%s\n" % (self.officialName, self.officialURL, official_non_merged, osm_non_merged, merged))
        file.close()

    def dumpCSV(self, sql, ext, head, callback):
        self.giscurs.execute(sql)
        row = []
        column = {}
        while True:
            many = self.giscurs.fetchmany(1000)
            if not many:
                break
            for res in many:
                row.append(res)
                for k in res['tags'].keys():
                    if not column.has_key(k):
                        column[k] = 1
                    else:
                        column[k] += 1
        column = sorted(column, key=column.get, reverse=True)
        column = filter(lambda a: a!=self.osmRef and not a in self.osmTags, column)
        column = [self.osmRef] + self.osmTags.keys() + column
        file = open("%s/%s%s.csv" % (self.config.dst_dir, self.officialName, ext), "w")
        file.write("%s\n" % ','.join(head + column))
        for r in row:
            cc = []
            for c in column:
                tags = r['tags']
                if tags.has_key(c):
                    cc.append(tags[c])
                else:
                    cc.append(None)
            cc = map(lambda x: (x if not ',' in x or not '"' else "\"%s\"" % x.replace('"','\\\"')).replace('\r','').replace('\n',''), map(lambda x: '' if not x else str(x), callback(r, cc)))
            file.write("%s\n" % ','.join(cc).rstrip(','))
        file.close()

    def where(self, tags):
        clauses = []
        for k, v in tags.items():
            clauses.append("tags?'%s'" % k)
            if isinstance(v, list):
                clauses.append("tags->'%s' IN ('%s')" % (k, "','".join(v)))
            elif v:
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
