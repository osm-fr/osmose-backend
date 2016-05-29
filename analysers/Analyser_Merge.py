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

import io
import bz2
import csv
import hashlib
import inspect
import psycopg2.extras
import os.path
from collections import defaultdict
from Analyser_Osmosis import Analyser_Osmosis
from modules import downloader

sql_schema = """
DO language 'plpgsql' $$
BEGIN
  IF NOT EXISTS (SELECT * FROM information_schema.schemata WHERE schema_name = '%(schema)s' ) THEN
    CREATE SCHEMA %(schema)s;
  END IF;
END $$
"""

sql00 = """
DROP TABLE IF EXISTS %(official)s CASCADE;
CREATE TABLE %(schema)s.%(official)s (
    ref varchar(65534),
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
    CASE
        WHEN osm_item.geom IS NOT NULL THEN ST_AsText(osm_item.geom)
        ELSE ST_AsText(any_locate(osm_item.type, osm_item.id))
    END,
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
    CASE
        WHEN osm_item.geom IS NOT NULL THEN ST_AsText(osm_item.geom)
        ELSE ST_AsText(any_locate(osm_item.type, osm_item.id))
    END,
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
    CASE
        WHEN missing_osm.geom IS NOT NULL THEN ST_AsText(missing_osm.geom)
        ELSE ST_AsText(any_locate(missing_osm.type, missing_osm.id))
    END,
    missing_official.tags AS official_tags,
    missing_official.fields AS official_fields,
    missing_osm.tags AS osm_tags
FROM
    missing_official
    JOIN missing_osm ON
        %(joinClause)s
ORDER BY
    missing_osm.id
    %(orderBy)s
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
    osm_item.tags,
    official.fields AS official_fields
FROM
    %(official)s AS official
    JOIN osm_item ON
        %(joinClause)s
WHERE
    official.tags - osm_item.tags != ''::hstore
"""

class CSV:
    def __init__(self, separator = ',', null = '', header = True, quote = '"', csv = True):
        """
        Describe the CSV file format, mainly for postgres COPY command in order to load data, but also for other thing, like load header.
        Setting param as None disable parameter into the COPY command.
        @param separator: one char separator
        @param null: string loaded à NULL
        @param header: CSV have header row
        @param quote: one char string delimiter
        @param csv: load file as CSV on COPY command
        """
        self.separator = separator
        self.null = null
        self.header = header
        self.quote = quote
        self.csv = csv

class Source:
    def __init__(self, url = None, name = None, encoding = "utf-8", file = None, fileUrl = None, fileUrlCache = 30, csv = CSV()):
        """
        Describe the source file.
        @param url: remote URL of data source, webpage
        @param name: official name of the data set
        @param encoding: file charset encoding
        @param file: file name in storage
        @param urlFile: remote URL of source file
        @param csv: the CSV format description
        """
        self.url = url
        self.name = name
        self.encoding = encoding
        self.file = file
        self.fileUrl = fileUrl
        self.fileUrlCache = fileUrlCache
        self.csv = csv

class Load:
    def __init__(self, x = ("NULL",), y = ("NULL",), srid = 4326, table = None, create = None,
            filter = None, select = {}, where = lambda res: True, xFunction = lambda i: i, yFunction = lambda i: i):
        """
        Describ the conversion of data set loaded with COPY into the database into an other table more usable for processing.
        @param x: the name of x column, as or converted to longitude, can be a SQL expression formatted as ("SQL CODE",)
        @param y: the name of y column, as or converted to latitude, can be a SQL expression formatted as ("SQL CODE",)
        @param srid: the projection of x and y coordinate
        @param table: the data base table name for load data into, generated automatically by default
        @param create: the data base table description, generated by default from CSV header
        @param filter: lambda expression applied on text file before loading
        @param select: dict reformatted as SQL to filter row CSV import before conversion, prefer this as the where param
        @param where: lambda expression taking row as dict and returning boolean to determine whether or not inserting the row into the table
        @param xFunction: lambda expression for convert x content column before reprojection, identity by default
        @param yFunction: lambda expression for convert y content column before reprojection, identity by default
        """
        self.x = x
        self.y = y
        self.srid = srid
        self.table = table
        self.create = create
        self.filter = filter
        self.select = select
        self.where = where
        self.xFunction = xFunction
        self.yFunction = yFunction

class Select:
    def __init__(self, types = [], tags = {}):
        """
        On witch OSM we try to join data set.
        @param types: object types, array of "relations", "ways" and "nodes"
        @param tags: dict of tags or array of dicts, array mean "OR"
        """
        self.types = types
        self.tags = tags

class Generate:
    def __init__(self, missing_official_fix = True, static = {}, mapping = {}, text = lambda tags, fields: {}):
        """
        How result error file is build.
        @param missing_official_fix: boolean to generate or not new object with quickfix
        @param static: dict of tags apply as is
        @param mapping: dict of tags, if value is string then data set column value is take, else lambda
        @param text: lambda return string, describe this error
        """
        self.missing_official_fix = missing_official_fix
        self.static = static
        self.mapping = mapping
        self.text = text

class Mapping:
    def __init__(self, select = Select(), osmRef = "NULL", conflationDistance = None, extraJoin = None, generate = Generate()):
        """
        How data is mapped with OSM data.
        @param select: fetch OSM data, see Select
        @param osmRef: the osm key for join data on reference
        @param conflationDistance: if no osmRef, do do conflation, use this threshold
        @param extraJoin: additional key condition to join on
        @param generate: build the result, see Generate
        """
        self.select = select
        self.osmRef = osmRef
        self.conflationDistance = conflationDistance
        self.extraJoin = extraJoin
        self.generate = generate


class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger, source = Source(), load = Load(), mapping = Mapping()):
        Analyser_Osmosis.__init__(self, config, logger)
        self.source = source
        self.load = load
        self.mapping = mapping

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

    def float_comma(self, val):
        return float(val.replace(',', '.'))

    def lastUpdate(self):
        if self.source.file:
          csv_file_time = int(os.path.getmtime("merge_data/"+self.source.file)+.5)
        elif self.source.fileUrl:
          csv_file_time = int(downloader.urlmtime(self.source.fileUrl, self.source.fileUrlCache)+.5)
        time = [csv_file_time]
        h = inspect.getmro(self.__class__)
        h = h[:-3]
        for c in h:
            time.append(int(os.path.getmtime(inspect.getfile(c))+.5))
        return max(time)

    def analyser_osmosis(self):
        if not isinstance(self.mapping.select.tags, list):
            self.mapping.select.tags = [self.mapping.select.tags]

        time = self.lastUpdate()
        db_schema = self.config.db_user
        self.data = False
        def setDataTrue():
            self.data=True
        self.run0("SELECT * FROM meta WHERE name='%s' AND update>=%s" % (self.load.table, time), lambda res: setDataTrue())
        if not self.data:
            self.logger.log(u"Load CSV into database")
            if self.source.file:
                f = bz2.BZ2File("merge_data/"+self.source.file)
            elif self.source.fileUrl:
                f = downloader.urlopen(self.source.fileUrl, self.source.fileUrlCache)
            if self.source.encoding not in ("UTF8", "UTF-8"):
                f = io.StringIO(f.read().decode(self.source.encoding))
                f.seek(0)
            if self.load.filter:
                f = io.StringIO(self.load.filter(f.read()))
                f.seek(0)
            self.run("DROP TABLE IF EXISTS %s" % self.load.table)
            if not self.load.create:
                if self.source.csv.header:
                    header = f.readline().strip().strip(self.source.csv.separator)
                    csvf = io.BytesIO(header.encode('utf-8'))
                    f.seek(0)
                    header = csv.reader(csvf, delimiter=self.source.csv.separator, quotechar=self.source.csv.quote).next()
                    self.load.create = ",".join(map(lambda c: "\"%s\" VARCHAR(65534)" % c, header))
                else:
                    raise AssertionError("No table schema provided")
            self.run(sql_schema % {"schema": db_schema})
            self.run("CREATE TABLE %s.%s (%s)" % (db_schema, self.load.table, self.load.create))
            copy = "COPY %s FROM STDIN WITH %s %s %s %s %s" % (
                self.load.table,
                ("DELIMITER AS '%s'" % self.source.csv.separator) if self.source.csv.separator != None else "",
                ("NULL AS '%s'" % self.source.csv.null) if self.source.csv.null != None else "",
                "CSV" if self.source.csv.csv else "",
                "HEADER" if self.source.csv.csv and self.source.csv.header else "",
                ("QUOTE '%s'" % self.source.csv.quote) if self.source.csv.csv and self.source.csv.quote else "")
            self.giscurs.copy_expert(copy, f)

            self.run("DELETE FROM meta WHERE name = '%s'" % self.load.table)
            self.run("INSERT INTO meta VALUES ('%s', %s, NULL)" % (self.load.table, time))
            self.run0("COMMIT")
            self.run0("BEGIN")

        # Convert
        tableOfficial = self.load.table+"_"+self.__class__.__name__.lower()
        if len(tableOfficial) > 63 - 11: # 63 max postgres relation name, 11 is index name prefix
            tableOfficial = tableOfficial[-(63-11-10):]+hashlib.md5(tableOfficial).hexdigest()[-10:]
        self.data = False
        def setDataTrue(res):
            self.data=res
        self.run0("SELECT bbox FROM meta WHERE name='%s' AND bbox IS NOT NULL AND update IS NOT NULL AND update>=%s" % (tableOfficial, time), lambda res: setDataTrue(res))
        if not self.data:
            self.logger.log(u"Convert data to tags")
            self.run(sql_schema % {"schema": db_schema})
            self.run(sql00 % {"schema": db_schema, "official": tableOfficial})
            giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            def insertOfficial(res):
                if self.load.where(res):
                    tags = self.tagFactory(res)
                    giscurs.execute(sql02.replace("%(official)s", tableOfficial), {
                        "ref": tags.get(self.mapping.osmRef) if self.mapping.osmRef != "NULL" else None,
                        "tags": tags,
                        "fields": dict(zip(dict(res).keys(), map(lambda x: unicode(x), dict(res).values()))),
                        "x": self.load.xFunction(res[0]), "y": self.load.yFunction(res[1]), "SRID": self.load.srid
                    })
            if isinstance(self.load.x, tuple):
                self.load.x = self.load.x[0]
            else:
                self.load.x = "\"%s\"" % self.load.x
            if isinstance(self.load.y, tuple):
                self.load.y = self.load.y[0]
            else:
                self.load.y = "\"%s\"" % self.load.y
            self.run0((sql01_ref if self.mapping.osmRef != "NULL" else sql01_geo) % {"table":self.load.table, "x":self.load.x, "y":self.load.y, "where":self.formatCSVSelect(self.load.select)}, insertOfficial)
            if self.load.srid:
                giscurs.execute("SELECT ST_AsText(ST_Envelope(ST_Extent(geom::geometry))::geography) FROM %s" % tableOfficial)
                bbox = giscurs.fetchone()[0]
            else:
                bbox = None
            self.run(sql03 % {"official": tableOfficial})

            self.run("DELETE FROM meta WHERE name='%s'" % tableOfficial)
            if bbox != None:
                self.run("INSERT INTO meta VALUES ('%s', %s, '%s')" % (tableOfficial, time, bbox))
            self.run0("COMMIT")
            self.run0("BEGIN")
        else:
            bbox = self.data[0]

        if self.load.srid and not bbox:
            self.logger.log(u"Empty bbox, abort")
            return # Stop, no data

        if self.load.srid:
          typeGeom = {'N': 'geom', 'W': 'way_locate(linestring)', 'R': 'relation_locate(id)'}
          typeShape = {'N': 'geom', 'W': 'ST_Envelope(linestring)', 'R': 'relation_shape(id)'}
        else:
          typeGeom = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}
          typeShape = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}
        self.logger.log(u"Retrive OSM item")
        where = "(" + (") OR (".join(map(lambda x: self.where(x), self.mapping.select.tags))) + ")"
        self.run("CREATE TABLE osm_item AS" +
            ("UNION".join(
                map(lambda type:
                    ("""(
                    SELECT
                        '%(type)s'::char(1) AS type,
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
                    WHERE""" + ("""
                        %(geom)s IS NOT NULL AND""" if self.load.srid else "") + ("""
                        ST_SetSRID(ST_GeomFromText('%(bbox)s'), 4326) && %(geom)s AND""" if bbox and self.load.srid else "") + """
                        %(where)s)""") % {"type":type[0].upper(), "ref":self.mapping.osmRef, "geom":typeGeom[type[0].upper()], "shape":typeShape[type[0].upper()], "from":type, "bbox":bbox, "where":where},
                    self.mapping.select.types
                )
            ))
        )
        if self.mapping.osmRef != "NULL":
            self.run("CREATE INDEX osm_item_index_ref ON osm_item(ref)")
        self.run("CREATE INDEX osm_item_index_shape ON osm_item USING GIST(shape)")

        joinClause = []
        if self.mapping.osmRef != "NULL":
            joinClause.append("official.ref = osm_item.ref")
        elif self.load.srid:
            joinClause.append("ST_DWithin(official.geom, osm_item.shape, %s)" % self.mapping.conflationDistance)
        if self.mapping.extraJoin:
            joinClause.append("official.tags->'%(tag)s' = osm_item.tags->'%(tag)s'" % {"tag": self.mapping.extraJoin})
        joinClause = " AND\n".join(joinClause) + "\n"

        # Missing official
        self.run(sql10 % {"official": tableOfficial, "joinClause": joinClause})
        self.run(sql11)
        if self.missing_official:
            self.run(sql12, lambda res: {
                "class": self.missing_official["class"],
                "subclass": str(self.stablehash("%s%s"%(res[0],res[1]))),
                "self": lambda r: [0]+r[1:],
                "data": [self.node_new, self.positionAsText],
                "text": self.mapping.generate.text(defaultdict(lambda:None,res[2]), defaultdict(lambda:None,res[3])),
                "fix": {"+": res[2]} if self.mapping.generate.missing_official_fix and res[2] != {} else None,
            } )

        if self.mapping.osmRef == "NULL":
            return # Job done, can't do more in geo mode

        self.run(sql20 % {"official": tableOfficial, "joinClause": joinClause})
        self.run(sql21)
        if self.missing_osm:
            # Missing OSM
            self.run(sql22, lambda res: {
                "class": self.missing_osm["class"],
                "data": [self.typeMapping[res[1]], None, self.positionAsText]
            } )
            # Invalid OSM
            self.run(sql23 % {"official": tableOfficial, "joinClause": joinClause}, lambda res: {
                "class": self.missing_osm["class"],
                "data": [self.typeMapping[res[1]], None, self.positionAsText]
            } )

        # Possible merge
        if self.possible_merge:
            possible_merge_joinClause = []
            possible_merge_orderBy = ""
            if self.load.srid:
                possible_merge_joinClause.append("ST_DWithin(missing_official.geom, missing_osm.shape, %s)" % self.mapping.conflationDistance)
                possible_merge_orderBy = ", ST_Distance(missing_official.geom, missing_osm.shape) ASC"
            if self.mapping.extraJoin:
                possible_merge_joinClause.append("missing_official.tags->'%(tag)s' = missing_osm.tags->'%(tag)s'" % {"tag": self.mapping.extraJoin})
            possible_merge_joinClause = " AND\n".join(possible_merge_joinClause) + "\n"
            self.run(sql30 % {"joinClause": possible_merge_joinClause, "orderBy": possible_merge_orderBy}, lambda res: {
                "class": self.possible_merge["class"],
                "subclass": str(self.stablehash("%s%s"%(res[0],str(res[3])))),
                "data": [self.typeMapping[res[1]], None, self.positionAsText],
                "text": self.mapping.generate.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[4])),
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
                "subclass": str(self.stablehash("%s%s"%(res[0],str(res[4])))),
                "data": [self.typeMapping[res[1]], None, self.positionAsText],
                "text": self.mapping.generate.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[5])),
                "fix": self.mergeTags(res[4], res[3]),
            } )

        self.dumpCSV("SELECT ST_X(geom::geometry) AS lon, ST_Y(geom::geometry) AS lat, tags FROM %s" % tableOfficial, "", ["lon","lat"], lambda r, cc:
            list((r['lon'], r['lat'])) + cc
        )

        self.run(sql40 % {"official": tableOfficial, "joinClause": joinClause})
        self.dumpCSV(sql41, ".byOSM", ["osm_id","osm_type","lon","lat"], lambda r, cc:
            list((r['osm_id'], r['osm_type'], r['lon'], r['lat'])) + cc
        )

        file = io.open("%s/%s.metainfo.csv" % (self.config.dst_dir, self.source.name), "w", encoding="utf8")
        file.write(u"file,origin,osm_date,official_non_merged,osm_non_merged,merged\n")
        if self.missing_official:
            self.giscurs.execute("SELECT COUNT(*) FROM missing_official;")
            official_non_merged = self.giscurs.fetchone()[0]
        else:
            official_non_merged = 0
        self.giscurs.execute("SELECT COUNT(*) FROM missing_osm;")
        osm_non_merged = self.giscurs.fetchone()[0]
        self.giscurs.execute("SELECT COUNT(*) FROM match;")
        merged = self.giscurs.fetchone()[0]
        file.write(u"\"%s\",\"%s\",FIXME,%s,%s,%s\n" % (self.source.name, self.source.fileUrl or self.source.url, official_non_merged, osm_non_merged, merged))
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
                    if k not in column:
                        column[k] = 1
                    else:
                        column[k] += 1
        column = sorted(column, key=column.get, reverse=True)
        column = filter(lambda a: a!=self.mapping.osmRef and not a in self.mapping.select.tags[0], column)
        column = [self.mapping.osmRef] + self.mapping.select.tags[0].keys() + column
        file = bz2.BZ2File(u"%s/%s-%s%s.csv.bz2" % (self.config.dst_dir, self.source.name, self.__class__.__name__, ext), "w")
        file.write((u"%s\n" % ','.join(head + column)).encode("utf-8"))
        for r in row:
            cc = []
            for c in column:
                tags = r['tags']
                if c in tags:
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
                clauses.append("tags->'%s' IN ('%s')" % (k, "','".join(map(lambda i: i.replace("'", "''"), v))))
            elif v:
                clauses.append("tags->'%s' = '%s'" % (k, v.replace("'", "''")))
        return " AND ".join(clauses)

    def tagFactory(self, res):
        tags = dict(self.mapping.generate.static)
        for tag, colomn in self.mapping.generate.mapping.items():
            if inspect.isfunction(colomn) or inspect.ismethod(colomn):
                r = colomn(res)
                if r:
                    tags[tag] = unicode(r)
            elif colomn and res[colomn]:
                tags[tag] = unicode(res[colomn])

        return tags

    def formatCSVSelect(self, csv_select):
        where = []
        for k, v in csv_select.items():
            if isinstance(v, list):
                cond = "\"%s\" IN ('%s')" % (k, "','".join(map(lambda i: i.replace("'", "''"), filter(lambda i: i != None, v))))
                if None in v:
                    cond = "(" + cond + " OR \"%s\" IS NULL)" % k
                where.append(cond)
            elif '%' in v:
                where.append("\"%s\" LIKE '%s'" % (k, v.replace("'", "''")))
            elif v == None:
                where.append("\"%s\" IS NULL" % k)
            else:
                where.append("\"%s\" = '%s'" % (k, v.replace("'", "''")))
        if where == []:
            return "1=1"
        else:
            return " AND ".join(where)
