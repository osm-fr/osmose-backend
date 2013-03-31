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
import os.path
from collections import defaultdict
from Analyser_Osmosis import Analyser_Osmosis

sql00 = """
DROP TABLE IF EXISTS %(official)s CASCADE;
CREATE TABLE %(official)s (
    ref varchar(254),
    tags hstore,
    fields hstore,
    geom geography
)
"""

sql01_ref = """
SELECT
    %(x)s AS _x,
    %(y)s AS _y,
    *
FROM
    %(table)s
WHERE
    %(where)s
"""

sql01_geo = """
SELECT
    %(x)s AS _x,
    %(y)s AS _y,
    *
FROM
    %(table)s
WHERE
    %(x)s IS NOT NULL AND
    %(y)s IS NOT NULL AND
    %(x)s::varchar != '' AND
    %(y)s::varchar != '' AND
    %(where)s
"""

sql02 = """
INSERT INTO
    %(official)s
VALUES (
    %(ref)s,
    %(tags)s,
    %(fields)s,
    ST_Transform(ST_SetSRID(ST_MakePoint(%(x)s, %(y)s), %(SRID)s), 4326)::geography
)
"""

sql03 = """
CREATE INDEX index_ref_%(official)s ON %(official)s(ref);
CREATE INDEX index_geom_%(official)s ON %(official)s USING GIST(geom);
"""

sql10 = """
CREATE TABLE missing_official AS
SELECT
    official.ref,
    ST_AsText(official.geom),
    official.tags,
    official.fields,
    official.geom
FROM
    %(official)s AS official
    LEFT JOIN osm_item ON
        %(joinClause)s
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
    osm_item.geom,
    osm_item.shape
FROM
    osm_item
    LEFT JOIN %(official)s AS official ON
        %(joinClause)s
WHERE
    osm_item.ref IS NULL AND
    official.ref IS NULL
"""

sql21 = """
CREATE INDEX missing_osm_index_shape ON missing_osm USING GIST(shape)
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
    osm_item.geom
FROM
    osm_item
    LEFT JOIN %(official)s AS official ON
        %(joinClause)s
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
    ST_DWithin(missing_official.geom, missing_osm.shape, %(conflationDistance)s)
ORDER BY
    missing_osm.id,
    ST_Distance(missing_official.geom, missing_osm.shape) ASC
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
    JOIN %(official)s AS official ON
        %(joinClause)s
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
)
"""

sql50 = """
SELECT
    osm_item.id,
    ST_AsText(osm_item.geom),
    ST_AsText(official.geom)
FROM
    %(official)s AS official
    JOIN osm_item ON
        %(joinClause)s AND
        NOT official.geom && osm_item.geom
"""

sql60 = """
SELECT
    osm_item.id,
    osm_item.type,
    ST_AsText(osm_item.geom),
    official.tags,
    osm_item.tags
FROM
    %(official)s AS official
    JOIN osm_item ON
        %(joinClause)s
WHERE
    official.tags - osm_item.tags != ''::hstore
"""

class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        # Default
        self.csv_format = "NULL AS ''"
        self.csv_encoding = "utf-8"
        self.csv_filter = None
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
        if hasattr(self, 'update_official'):
            self.classs[self.update_official["class"]] = self.update_official
        else:
            self.update_official = None
        self.osmRef = "NULL"
        self.sourceX = "NULL"
        self.sourceY = "NULL"
        self.sourceSRID = None
        self.extraJoin = None
        self.sourceWhere = lambda res: True
        self.sourceXfunction = lambda i: i
        self.sourceYfunction = lambda i: i
        self.defaultTag = {}
        self.defaultTagMapping = {}
        self.text = lambda tags, fields: {}

    def lastUpdate(self):
        csv_file_time = int(os.path.getmtime(self.csv_file+".bz2")+.5)
        time = [csv_file_time]
        h = inspect.getmro(self.__class__)
        h = h[:-3]
        for c in h:
            time.append(int(os.path.getmtime(inspect.getfile(c))+.5))
        return max(time)

    def analyser_osmosis(self):
        if not isinstance(self.osmTags, list):
            self.osmTags = [self.osmTags]

        time = self.lastUpdate()
        self.data = False
        def setDataTrue():
            self.data=True
        self.run0("SELECT * FROM meta WHERE name='%s' AND update>=%s" % (self.sourceTable, time), lambda res: setDataTrue())
        if not self.data:
            self.logger.log(u"Load CSV into database")
            self.run("DROP TABLE IF EXISTS %s" % self.sourceTable)
            self.run("CREATE TABLE %s (%s)" % (self.sourceTable, self.create_table))
            f = bz2.BZ2File(self.csv_file+".bz2")
            if self.csv_encoding not in ("UTF8", "UTF-8"):
                f = io.StringIO(f.read().decode(self.csv_encoding))
            if self.csv_filter:
                f = io.StringIO(self.csv_filter(f.read()))
            f.seek(0)
            self.giscurs.copy_expert("COPY %s FROM STDIN %s" % (self.sourceTable, self.csv_format), f)

            self.run("DELETE FROM meta WHERE name LIKE '%s%%'" % self.sourceTable)
            self.run("INSERT INTO meta VALUES ('%s', %s, NULL)" % (self.sourceTable, time))
            self.run0("COMMIT")
            self.run0("BEGIN")

        # Convert
        tableOfficial = self.sourceTable+"_"+self.__class__.__name__
        self.data = False
        def setDataTrue(res):
            self.data=res
        self.run0("SELECT bbox FROM meta WHERE name='%s'" % tableOfficial, lambda res: setDataTrue(res))
        if not self.data:
            self.run(sql00 % {"official": tableOfficial})
            giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            def insertOfficial(res):
                tags = self.tagFactory(res)
                giscurs.execute(sql02.replace("%(official)s", tableOfficial), {
                    "ref": tags[self.osmRef] if self.osmRef != "NULL" else None,
                    "tags": tags,
                    "fields": dict(zip(dict(res).keys(), map(lambda x: unicode(x), dict(res).values()))),
                    "x": self.sourceXfunction(res[0]), "y": self.sourceYfunction(res[1]), "SRID": self.sourceSRID
                } ) if self.sourceWhere(res) else False
            self.run0((sql01_ref if self.osmRef != "NULL" else sql01_geo) % {"table":self.sourceTable, "x":self.sourceX, "y":self.sourceY, "where":self.formatCSVSelect(self.csv_select)}, insertOfficial)
            if self.sourceSRID:
                giscurs.execute("SELECT ST_AsText(ST_Envelope(ST_Extent(geom::geometry))::geography) FROM %s" % tableOfficial)
                bbox = giscurs.fetchone()[0]
            else:
                bbox = None
            self.run(sql03 % {"official": tableOfficial})

            self.run("DELETE FROM meta WHERE name='%s'" % tableOfficial)
            self.run("INSERT INTO meta VALUES ('%s', NULL, '%s')" % (tableOfficial, bbox))
            self.run0("COMMIT")
            self.run0("BEGIN")
        else:
            bbox = self.data[0]

        if self.sourceSRID and not bbox:
            self.logger.log(u"Empty bbox, abort")
            return # Stop, no data

        typeGeom = {'n': 'geom', 'w': 'way_locate(linestring)', 'r': 'relation_locate(id)'}
        typeShape = {'n': 'geom', 'w': 'ST_Envelope(linestring)', 'r': 'relation_shape(id)'}
        self.logger.log(u"Retrive OSM item")
        where = "(" + (") OR (".join(map(lambda x: self.where(x), self.osmTags))) + ")"
        self.run("CREATE TABLE osm_item AS" +
            ("UNION".join(
                map(lambda type:
                    ("""(
                    SELECT
                        '%(type)s' AS type,
                        id,
                        CASE
                            WHEN (tags->'%(ref)s') IS NULL THEN NULL
                            ELSE trim(both from regexp_split_to_table(tags->'%(ref)s', ';'))
                        END AS ref,
                        %(geom)s::geography AS geom,
                        %(shape)s::geography AS shape,
                        tags
                    FROM
                        %(from)s
                    WHERE
                        %(geom)s IS NOT NULL AND""" + ("""
                        ST_SetSRID(ST_GeomFromText('%(bbox)s'), 4326) && %(geom)s AND""" if bbox else "") + """
                        %(where)s)""") % {"type":type[0], "ref":self.osmRef, "geom":typeGeom[type[0]], "shape":typeShape[type[0]], "from":type, "bbox":bbox, "where":where},
                    self.osmTypes
                )
            ))
        )
        if self.osmRef != "NULL":
            self.run("CREATE INDEX osm_item_index_ref ON osm_item(ref)")
        self.run("CREATE INDEX osm_item_index_shape ON osm_item USING GIST(shape)")

        joinClause = []
        if self.osmRef != "NULL":
            joinClause.append("official.ref = osm_item.ref")
        elif self.sourceSRID:
            joinClause.append("ST_DWithin(official.geom, osm_item.shape, %s)" % self.conflationDistance)
        if self.extraJoin:
            joinClause.append("osm_item.tags->'%(tag)s' = official.tags->'%(tag)s'" % {"tag": self.extraJoin})
        joinClause = " AND\n".join(joinClause) + "\n"

        # Missing official
        self.run(sql10 % {"official": tableOfficial, "joinClause": joinClause})
        self.run(sql11)
        if self.missing_official:
            self.run(sql12, lambda res: {
                "class": self.missing_official["class"],
                "subclass": str(abs(int(hash("%s%s"%(res[0],res[1]))))),
                "self": lambda r: [0]+r[1:],
                "data": [self.node_new, self.positionAsText],
                "text": self.text(defaultdict(lambda:None,res[2]), defaultdict(lambda:None,res[3])),
                "fix": {"+": res[2]} if res[2] != {} else None,
            } )

        if self.osmRef == "NULL":
            return # Job done, can't do more in geo mode

        self.run(sql20 % {"official": tableOfficial, "joinClause": joinClause})
        self.run(sql21)
        typeMapping = {'n': self.node_full, 'w': self.way_full, 'r': self.relation_full}
        if self.missing_osm:
            # Missing OSM
            self.run(sql22, lambda res: {
                "class": self.missing_osm["class"],
                "data": [typeMapping[res[1]], None, self.positionAsText]
            } )
            # Invalid OSM
            self.run(sql23 % {"official": tableOfficial, "joinClause": joinClause}, lambda res: {
                "class": self.missing_osm["class"],
                "data": [typeMapping[res[1]], None, self.positionAsText]
            } )

        # Possible merge
        if self.possible_merge:
            self.run(sql30 % {"conflationDistance":self.conflationDistance}, lambda res: {
                "class": self.possible_merge["class"],
                "subclass": str(abs(int(hash("%s%s"%(res[0],str(res[3])))))),
                "data": [typeMapping[res[1]], None, self.positionAsText],
                "text": self.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[4])),
                "fix": self.mergeTags(res[5], res[3]),
            } )

        # Moved official
        if self.moved_official:
            self.run(sql50 % {"official": tableOfficial, "joinClause": joinClause}, lambda res: {
                "class": self.moved_official["class"],
                "data": [self.node_full, self.positionAsText],
            } )

        # Update official
        if self.update_official:
            self.run(sql60 % {"official": tableOfficial, "joinClause": joinClause}, lambda res: {
                "class": self.update_official["class"],
                "subclass": str(abs(int(hash("%s%s"%(res[0],str(res[4])))))),
                "data": [typeMapping[res[1]], None, self.positionAsText],
                "text": self.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[4])),
                "fix": self.mergeTags(res[4], res[3]),
            } )

        self.dumpCSV("SELECT ST_X(geom::geometry) AS lon, ST_Y(geom::geometry) AS lat, tags FROM %s" % tableOfficial, "", ["lon","lat"], lambda r, cc:
            list((r['lon'], r['lat'])) + cc
        )

        self.run(sql40 % {"official": tableOfficial, "joinClause": joinClause})
        self.dumpCSV(sql41, ".byOSM", ["osm_id","osm_type","lon","lat"], lambda r, cc:
            list((r['osm_id'], r['osm_type'], r['lon'], r['lat'])) + cc
        )

        file = open("%s/%s.metainfo.csv" % (self.config.dst_dir, self.officialName), "w")
        file.write("file,origin,osm_date,official_non_merged,osm_non_merged,merged\n")
        if self.missing_official:
            self.giscurs.execute("SELECT COUNT(*) FROM missing_official;")
            official_non_merged = self.giscurs.fetchone()[0]
        else:
            official_non_merged = 0
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
        column = filter(lambda a: a!=self.osmRef and not a in self.osmTags[0], column)
        column = [self.osmRef] + self.osmTags[0].keys() + column
        file = bz2.BZ2File("%s/%s%s.csv.bz2" % (self.config.dst_dir, self.officialName, ext), "w")
        file.write((u"%s\n" % ','.join(head + column)).encode("utf-8"))
        for r in row:
            cc = []
            for c in column:
                tags = r['tags']
                if tags.has_key(c):
                    cc.append(tags[c])
                else:
                    cc.append(None)
            cc = map(lambda x: (x if not ',' in x or not '"' else "\"%s\"" % x.replace('"','\\\"')).replace('\r','').replace('\n',''), map(lambda x: '' if not x else unicode(x), callback(r, cc)))
            file.write((u"%s\n" % ','.join(cc).rstrip(',')).encode("utf-8"))
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
                        tags[tag] = unicode(r)
                except:
                    pass
            elif colomn and res.has_key(colomn) and res[colomn]:
                tags[tag] = unicode(res[colomn])
        return tags

    def formatCSVSelect(self, csv_select):
        where = []
        for k, v in csv_select.items():
            where.append("%s = '%s'" % (k, v))
        if where == []:
            return "1=1"
        else:
            return " AND ".join(where)
