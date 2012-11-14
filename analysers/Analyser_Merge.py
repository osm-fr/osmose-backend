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

import re, io, bz2
import inspect
import psycopg2.extras
from collections import defaultdict
from Analyser_Osmosis import Analyser_Osmosis

sql00 = """
CREATE TABLE official (
    ref varchar(254),
    tags hstore,
    fields hstore,
    geom geography
);
"""

sql01_ref = """
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
    %(y)s::varchar != '' AND
    %(where)s
"""

sql01_geo = """
SELECT
    NULL::varchar AS _ref,
    %(x)s AS _x,
    %(y)s AS _y,
    *
FROM
    osmose.%(table)s
WHERE
    %(x)s IS NOT NULL AND
    %(y)s IS NOT NULL AND
    %(x)s::varchar != '' AND
    %(y)s::varchar != '' AND
    %(where)s
"""

sql02 = """
INSERT INTO
    official
VALUES (
    %(ref)s,
    %(tags)s,
    %(fields)s,
    ST_Transform(ST_SetSRID(ST_MakePoint(%(x)s, %(y)s), %(SRID)s), 4326)::geography
);
"""

sql03 = """
CREATE INDEX official_index_ref ON official(ref);
CREATE INDEX official_index_geom ON official USING GIST(geom);
"""

sql10_ref = """
CREATE TABLE missing_official AS
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
"""

sql10_geo = """
CREATE TABLE missing_official AS
SELECT
    official.ref,
    ST_AsText(official.geom),
    official.tags,
    official.fields,
    official.geom::geography
FROM
    official
    LEFT JOIN osm_item ON
        ST_DWithin(official.geom, osm_item.geom, %(conflationDistance)s)
WHERE
    osm_item.id IS NULL
"""

sql11 = """
CREATE INDEX missing_official_index_ref ON missing_official(ref);
CREATE INDEX missing_official_index_geom ON missing_official USING GIST(geom);
"""

sql12 = """
SELECT * FROM missing_official;
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
    osm_item.ref IS NULL AND
    official.ref IS NULL
"""

sql21 = """
CREATE INDEX missing_osm_index_geom ON missing_osm USING GIST(geom)
"""

sql22 = """
SELECT * FROM missing_osm
"""

sql23 = """
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
    osm_item.ref IS NOT NULL AND
    official.ref IS NULL
"""

sql30 = """
SELECT
    DISTINCT ON (id)
    missing_osm.id,
    missing_osm.type,
    ST_AsText(missing_osm.geom),
    missing_official.tags AS official_tags,
    missing_official.fields AS official_fields,
    missing_osm.tags AS osm_tags
FROM
    missing_official,
    missing_osm
WHERE
    ST_DWithin(missing_official.geom, missing_osm.geom, %(conflationDistance)s)
ORDER BY
    missing_osm.id,
    ST_Distance(missing_official.geom, missing_osm.geom) ASC
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
        id::bigint AS osm_id,
        type::varchar AS osm_type,
        tags::hstore,
        ST_X(geom::geometry)::float AS lon,
        ST_Y(geom::geometry)::float AS lat
    FROM
        match
) UNION (
    SELECT
        NULL::bigint AS osm_id,
        NULL::varchar AS osm_type,
        tags::hstore,
        ST_X(geom::geometry)::float AS lon,
        ST_Y(geom::geometry)::float AS lat
    FROM
        missing_official
) UNION (
    SELECT
        id::bigint AS osm_id,
        type::varchar AS osm_type,
        tags::hstore,
        ST_X(geom::geometry)::float AS lon,
        ST_Y(geom::geometry)::float AS lat
    FROM
        missing_osm
);
"""

sql50 = """
SELECT
    osm_item.id,
    ST_AsText(osm_item.geom),
    ST_AsText(official.geom)
FROM
    official
    JOIN osm_item ON
        official.ref = osm_item.ref AND
        NOT official.geom && osm_item.geom
"""

class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        # Default
        self.csv_format = ""
        self.csv_encoding = "utf-8"
        self.csv_filter = lambda i: i
        self.csv_select = {}
        if hasattr(self, 'missing_official'):
            self.classs[self.missing_official["class"]] = self.missing_official
        else:
            self.missing_official = None
        if hasattr(self, 'missing_osm'):
            self.classs[self.missing_osm["class"]] = self.missing_osm
        else:
            self.missing_osm = None
        if hasattr(self, 'possible_merge'):
            self.classs[self.possible_merge["class"]] = self.possible_merge
        else:
            self.possible_merge = None
        if hasattr(self, 'moved_official'):
            self.classs[self.moved_official["class"]] = self.moved_official
        else:
            self.moved_official = None
        self.osmRef = "NULL"
        self.sourceRef = "NULL"
        self.sourceWhere = lambda res: True
        self.sourceXfunction = lambda i: i
        self.sourceYfunction = lambda i: i
        self.defaultTag = {}
        self.defaultTagMapping = {}
        self.text = lambda tags, fields: {}

    def analyser_osmosis(self):
        data = False
        def setDataTrue():
            data=True
        self.run0("SELECT * FROM pg_stat_user_tables WHERE schemaname='osmose' AND relname='%s'" % self.sourceTable, lambda res: setDataTrue())
        if not data:
            self.logger.log(u"Load CSV into database")
            self.run("DROP TABLE IF EXISTS osmose.%s" % self.sourceTable)
            self.run("CREATE TABLE osmose.%s (%s)" % (self.sourceTable, self.create_table))
            f = io.StringIO(self.csv_filter(bz2.BZ2File(self.csv_file+".bz2").read().decode(self.csv_encoding)))
            f.seek(0)
            self.giscurs.copy_expert("COPY osmose.%s FROM STDIN %s" % (self.sourceTable, self.csv_format), f)

        # Convert
        self.run(sql00)
        self.logger.log(u"Convert official to OSM")
        giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.run0((sql01_ref if self.sourceRef != "NULL" else sql01_geo) % {"table":self.sourceTable, "ref":self.sourceRef, "x":self.sourceX, "y":self.sourceY, "where":self.formatCSVSelect(self.csv_select)}, lambda res:
            giscurs.execute(sql02, {
                "ref": res[0],
                "tags": self.tagFactory(res),
                "fields": dict(zip(dict(res).keys(), map(lambda x: str(x), dict(res).values()))),
                "x": self.sourceXfunction(res[1]), "y": self.sourceYfunction(res[2]), "SRID": self.sourceSRID
            } ) if self.sourceWhere(res) else False
        )
        giscurs.execute("SELECT ST_AsText(ST_Envelope(ST_Extent(geom::geometry))::geography) FROM official")
        bbox = giscurs.fetchone()[0]
        self.run(sql03)

        typeGeom = {'n': 'geom', 'w': 'way_locate(linestring)', 'r': 'relation_locate(id)'}
        self.logger.log(u"Retrive OSM item")
        self.run("CREATE TABLE osm_item AS" +
            ("UNION".join(
                map(lambda type:
                    """(
                    SELECT
                        '%(type)s' AS type,
                        id,
                        CASE
                            WHEN (tags->'%(ref)s') IS NULL THEN NULL
                            ELSE trim(both from regexp_split_to_table(tags->'%(ref)s', ';'))
                        END AS ref,
                        %(geom)s::geography AS geom,
                        tags
                    FROM
                        %(from)s
                    WHERE
                        %(geom)s IS NOT NULL AND
                        ST_SetSRID(ST_GeomFromText('%(bbox)s'), 4326) && %(geom)s AND
                        %(where)s)""" % {"type":type[0], "ref":self.osmRef, "geom":typeGeom[type[0]], "from":type, "bbox":bbox, "where":self.where(self.osmTags)},
                    self.osmTypes
                )
            ))
        )
        self.run("CREATE INDEX osm_item_index_ref ON osm_item(ref)")
        self.run("CREATE INDEX osm_item_index_geom ON osm_item USING GIST(geom)")

        # Missing official
        if self.sourceRef != "NULL":
            self.run(sql10_ref)
        else:
            self.run(sql10_geo % {"conflationDistance":self.conflationDistance})
        self.run(sql11)
        self.run(sql12, lambda res: {
            "class": self.missing_official["class"],
            "subclass": str(abs(int(hash("%s%s"%(res[0],res[1]))))),
            "self": lambda r: [0]+r[1:],
            "data": [self.node_new, self.positionAsText],
            "text": self.text(defaultdict(lambda:None,res[2]), defaultdict(lambda:None,res[3])),
            "fix": {"+": res[2]} if res[2] != {} else None,
        } )

        if self.sourceRef == "NULL":
            return # Job done, can't do more in geo mode

        self.run(sql20)
        self.run(sql21)
        typeMapping = {'n': self.node_full, 'w': self.way_full, 'r': self.relation_full}
        if self.missing_osm:
            # Missing OSM
            self.run(sql22, lambda res: {
                "class": self.missing_osm["class"],
                "data": [typeMapping[res[1]], None, self.positionAsText]
            } )
            # Invalid OSM
            self.run(sql23, lambda res: {
                "class": self.missing_osm["class"],
                "data": [typeMapping[res[1]], None, self.positionAsText]
            } )

        # Possible merge
        if self.possible_merge:
            self.run(sql30 % {"conflationDistance":self.conflationDistance}, lambda res: {
                "class": self.possible_merge["class"],
                "data": [typeMapping[res[1]], None, self.positionAsText],
                "text": self.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[4])),
                "fix": self.mergeTags(res[5], res[3]),
            } )

        # Moved official
        if self.moved_official:
            self.run(sql50, lambda res: {
                "class": self.moved_official["class"],
                "data": [self.node_full, self.positionAsText],
            } )

        self.dumpCSV("SELECT ST_X(geom::geometry) AS lon, ST_Y(geom::geometry) AS lat, tags FROM official", "", ["lon","lat"], lambda r, cc:
            list((r['lon'], r['lat'])) + cc
        )

        self.run(sql40)
        self.dumpCSV(sql41, ".byOSM", ["osm_id","osm_type","lon","lat"], lambda r, cc:
            list((r['osm_id'], r['osm_type'], r['lon'], r['lat'])) + cc
        )

        file = open("%s/%s.metainfo.csv" % (self.config.dst_dir, self.officialName), "w")
        file.write("file,origin,osm_date,official_non_merged,osm_non_merged,merged\n")
        self.giscurs.execute("SELECT COUNT(*) FROM missing_official;")
        official_non_merged = self.giscurs.fetchone()[0]
        self.giscurs.execute("SELECT COUNT(*) FROM missing_osm;")
        osm_non_merged = self.giscurs.fetchone()[0]
        self.giscurs.execute("SELECT COUNT(*) FROM match;")
        merged = self.giscurs.fetchone()[0]
        file.write("\"%s\",\"%s\",FIXME,%s,%s,%s\n" % (self.officialName, self.officialURL, official_non_merged, osm_non_merged, merged))
        file.close()

    def mergeTags(self, osm, official):
        fix = {"+": {}, "~":{}}
        for o in official:
            if o in osm:
                if osm[o] == official[o]:
                    pass
                else:
                    if o == "source":
                        fix["~"][o] = osm[o]+";"+official[o]
                    else:
                        fix["~"][o] = official[o]
            else:
                fix["+"][o] = official[o]
        if "name" in osm and "name" in official and osm["name"] != official["name"]:
            fix0 = {"+": fix["+"], "~": dict(fix["~"])}
            del(fix0["~"]["name"])
            fix = [fix0, fix]
        return fix

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

    def formatCSVSelect(self, csv_select):
        where = []
        for k, v in csv_select.items():
            where.append("%s = '%s'" % (k, v))
        if where == []:
            return "1=1"
        else:
            return " AND ".join(where)
