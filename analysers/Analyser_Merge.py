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
import datetime
import gzip
import csv
import psycopg2.extras
import psycopg2.extensions
import os
import os.path
import time
import zipfile
import tempfile
import json
import re
import fnmatch
import shutil
from typing import Optional, Dict, Union, Callable
from collections import defaultdict
from .Analyser_Osmosis import Analyser_Osmosis
from modules.OsmoseTranslation import T_
from modules.Stablehash import stablehash64, hexastablehash
from modules import downloader
from modules import PointInPolygon
from modules import SourceVersion
from modules import DictCursorUnicode
from functools import reduce

try:
    from pyproj import Transformer
except ImportError:
    # No available in pyproj < 2.1
    Transformer = None # type: ignore


GENERATE_DELETE_TAG = u"DELETE TAG aechohve0Eire4ooyeyaey1gieme0xoo"

# Checking existence of schema before CREATE SCHEMA is necessary on databases,
# like france_local_db, where user osmose doesn't have the rights to create a
# schema.
sql_schema = """
DO language 'plpgsql' $$
BEGIN
  IF NOT EXISTS (SELECT * FROM information_schema.schemata WHERE schema_name = '{schema}' ) THEN
    CREATE SCHEMA {schema};
  END IF;
END $$
"""

sql00 = """
CREATE TEMP TABLE {official}_temp (
    ref varchar(65534),
    tags jsonb,
    tags1 jsonb,
    fields jsonb,
    geom geometry(geometry, {proj})
)
"""

sql01_ref = """
SELECT
    {distinct}
    {geom} AS _geom,
    *
FROM
    {table}
WHERE
    {where}
{order_by}
"""

sql01_geo = """
SELECT
    {distinct}
    {geom} AS _geom,
    *
FROM
    {table}
WHERE
    ({validationGeomSQL}) AND
    {where}
{order_by}
"""

sql02 = """
INSERT INTO
    {official}_temp
VALUES (
    %(ref)s,
    %(tags)s::jsonb,
    %(tags1)s::jsonb,
    %(fields)s::jsonb,
    CASE WHEN {geom} IS NOT NULL THEN
        ST_Transform(ST_Force2D({geom}), {proj})
    ELSE NULL END
)
"""

sql02b = """
DROP TABLE IF EXISTS {official} CASCADE;
CREATE TABLE {official} AS
SELECT
  ref,
  tags,
  tags1,
  fields,
  geom
FROM
  {official}_temp
GROUP BY
  ref,
  tags,
  tags1,
  fields,
  geom
"""

sql03a = """
CREATE INDEX ir_{official} ON {official}(ref)
"""

sql03b = """
CREATE INDEX ig_{official} ON {official} USING GIST(geom)
"""

sql10 = """
CREATE TEMP TABLE missing_official AS
SELECT
    official.ref,
    ST_AsText(ST_Transform(official.geom, 4326)),
    official.tags,
    official.fields,
    official.geom
FROM
    {official} AS official
    LEFT JOIN osm_item ON
        {joinClause}
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
CREATE TEMP TABLE missing_osm AS
SELECT
    osm_item.id,
    osm_item.type,
    CASE
        WHEN osm_item.geom IS NOT NULL THEN ST_AsText(ST_Transform(osm_item.geom, 4326))
        ELSE ST_AsText(any_locate(osm_item.type, osm_item.id))
    END,
    osm_item.tags,
    osm_item.geom,
    osm_item.shape
FROM
    osm_item
    LEFT JOIN {official} AS official ON
        {joinClause}
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
        WHEN osm_item.geom IS NOT NULL THEN ST_AsText(ST_Transform(osm_item.geom, 4326))
        ELSE ST_AsText(any_locate(osm_item.type, osm_item.id))
    END,
    osm_item.tags,
    osm_item.geom,
    osm_item.ref
FROM
    osm_item
    LEFT JOIN {official} AS official ON
        {joinClause}
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
        {joinClause}
ORDER BY
    missing_osm.id
    {orderBy}
"""

sql40 = """
CREATE TEMP TABLE match AS
SELECT
    osm_item.id,
    osm_item.type,
    osm_item.tags,
    ST_Transform(osm_item.geom, 4326) AS geom
FROM
    osm_item
    JOIN {official} AS official ON
        {joinClause}
"""

sql41 = """
(
    SELECT
        id::bigint AS osm_id,
        type::varchar AS osm_type,
        tags::jsonb,
        ST_X(geom)::float AS lon,
        ST_Y(geom)::float AS lat
    FROM
        match
) UNION ALL (
    SELECT
        NULL::bigint AS osm_id,
        NULL::varchar AS osm_type,
        tags::jsonb,
        ST_X(geom)::float AS lon,
        ST_Y(geom)::float AS lat
    FROM
        missing_official
) UNION ALL (
    SELECT
        id::bigint AS osm_id,
        type::varchar AS osm_type,
        tags::jsonb,
        ST_X(geom)::float AS lon,
        ST_Y(geom)::float AS lat
    FROM
        missing_osm
)
"""

sql50 = """
SELECT
    osm_item.id,
    ST_AsText(ST_Transform(osm_item.geom, 4326)),
    ST_AsText(ST_Transform(official.geom, 4326))
FROM
    {official} AS official
    JOIN osm_item ON
        {joinClause} AND
        NOT official.geom && osm_item.geom
"""

sql60 = """
SELECT
    osm_item.id,
    osm_item.type,
    ST_AsText(ST_Transform(osm_item.geom, 4326)),
    official.tags,
    osm_item.tags,
    official.fields AS official_fields
FROM
    {official} AS official
    JOIN osm_item ON
        {joinClause}
WHERE
    official.tags1 - (SELECT coalesce(array_agg(key), array[]::text[]) FROM each(official.tags1) WHERE NOT osm_item.tags?key AND value = '""" + GENERATE_DELETE_TAG + """') - osm_item.tags - 'source'::text != ''::jsonb
"""

class Source:
    def __init__(self, attribution = None, millesime = None, encoding = "utf-8", file = None, fileUrl = None, post: Dict[str, str] = None, fileUrlCache = 30, zip = None, extract = None, bz2 = False, gzip = False, filter = None):
        """
        Describe the source file.
        @param attribution: Author of the data, for the OSM source tag
        @param millesime: date of the last release
        @param encoding: file charset encoding
        @param file: file name in storage
        @param urlFile: remote URL of source file
        @param fileUrlCache: days for file in cache
        @param post: post key-value to the URL to get the file to download
        @param zip: extract a file from zip. Unix filename pattern matching.
        @param extract: extract file from any archive format
        @param gzip: uncompress from bz2
        @param gzip: uncompress from gzip
        @param filter: lambda expression applied on text file before loading
        """
        self.attribution = attribution
        self.millesime = millesime
        self.encoding = encoding
        self.file = file
        self.fileUrl = fileUrl
        self.post = post
        self.fileUrlCache = fileUrlCache
        self.zip = zip
        self.extract = extract
        self.bz2 = bz2
        self.gzip = gzip
        self.filter = filter

        if self.file and self.fileUrl:
            raise ValueError("file and fileUrl should not be both set")

        if self.file:
            if not os.path.isabs(self.file):
                self.file = "merge_data/" + self.file

        if self.attribution and "{0}" in self.attribution:
            self.attribution_re = re.compile(self.attribution.replace("{0}", ".*"))

    def zipFile(self):
        if not self.zip:
            return None
        if self.file:
            f = open(self.file, 'rb')
        elif self.fileUrl:
            f = downloader.urlopen(self.fileUrl, self.fileUrlCache, mode='rb', post=self.post)

        z = zipfile.ZipFile(f, 'r')
        print(z.namelist())
        filename = next(filter(lambda zipinfo: fnmatch.fnmatch(zipinfo.filename, self.zip), z.infolist()))
        return filename

    def time(self):
        if self.file:
            return int(os.path.getmtime(self.file)+.5)
        elif self.fileUrl:
            if self.zipFile():
                date_time = self.zipFile().date_time
                return int(time.mktime(date_time + (0, 0, -1))+.5)
            else:
                return int(downloader.urlmtime(self.fileUrl, self.fileUrlCache, self.post)+.5)

    def path(self):
        if self.file:
            return self.file
        elif self.fileUrl:
            # Do nothing about ZIP
            return downloader.path(self.fileUrl, self.fileUrlCache, post=self.post)

    def open(self, binary = False):
        if self.file:
            f = open(self.file, 'rb')
        elif self.fileUrl:
            f = downloader.urlopen(self.fileUrl, self.fileUrlCache, mode='rb', post=self.post)

        if self.zipFile():
            z = zipfile.ZipFile(f, 'r').open(self.zipFile().filename)
            f = io.BytesIO(z.read())
            f.seek(0)
        elif self.extract:
            import libarchive.public # type: ignore
            with libarchive.public.memory_reader(f.read()) as archive:
                f = io.BytesIO()
                for entry in archive:
                    if entry.pathname == self.extract:
                        for block in entry.get_blocks():
                            f.write(block)
                        break
            f.seek(0)
        elif self.bz2:
            f = io.BytesIO(bz2.decompress(f.read()))
            f.seek(0)
        elif self.gzip:
            f = gzip.GzipFile(fileobj=f)

        if not binary:
            f = io.StringIO(f.read().decode(self.encoding, 'ignore'))
            f.seek(0)
            if self.filter:
                f = io.StringIO(self.filter(f.read()))
                f.seek(0)
        return f

    def _get_millesime(self) -> Optional[str]:
        if not self.millesime and self.fileUrl:
            cached_millesime = downloader.get_millesime(self.fileUrl, self.fileUrlCache, self.post)
            if cached_millesime:
                self.millesime = cached_millesime
            else:
                self.millesime = self.get_millesime()
                downloader.set_millesime(self.fileUrl, self.millesime)
        if self.millesime is None or type(self.millesime) == str:
            return self.millesime
        return self.millesime.strftime("%Y-%m")

    def get_millesime(self) -> Optional[datetime.datetime]:
        """To be overwritten by sources with dynamic millesime"""
        return None

    def as_tag_value(self):
        if "{0}" in self.attribution:
            return self.attribution.format(self._get_millesime())
        else:
            return " - ".join(filter(lambda x: x is not None, [self.attribution, self._get_millesime()]))

    def match_attribution(self, s):
        if "{0}" not in self.attribution:
            return self.attribution in s
        else:
            return self.attribution_re.match(s)


class SourceDataGouv(Source):

    def __init__(self, dataset: str, resource: str, data_gouv_api_base: str = "https://www.data.gouv.fr/api/1", data_gouv_dataset_base: str = "https://www.data.gouv.fr/fr/datasets/r/", **kwargs):
        self.dataset = dataset
        self.resource = resource
        self.data_gouv_api_base = data_gouv_api_base
        kwargs.update({
            "fileUrl": data_gouv_dataset_base + resource,
            "millesime": None,
        })
        super().__init__(**kwargs)

    def get_millesime(self) -> datetime.datetime:
        response = downloader.request_get(f"{self.data_gouv_api_base}/datasets/{self.dataset}/resources/{self.resource}/")
        response.raise_for_status()
        return datetime.datetime.fromisoformat(response.json()["last_modified"])


class SourcePublicLu(SourceDataGouv):
    def __init__(self, dataset: str, resource: str, **kwargs):
        super().__init__(dataset, resource, data_gouv_api_base="https://data.public.lu/api/1", data_gouv_dataset_base="https://data.public.lu/fr/datasets/r/", **kwargs)


class SourceOpenDataSoft(Source):

    url_re = re.compile(r"(https?://.+)/explore/dataset/([^/?#]+)")

    def __init__(self,
                 url: str,
                 format: str = "csv",
                 **kwargs):
        url_match = self.url_re.match(url)
        if url_match is None:
            raise ValueError(f"Invalid url: {url}")
        self.base_url, self.dataset = url_match.groups()
        kwargs.update({
            "fileUrl": f"{self.base_url}/explore/dataset/{self.dataset}/download/?format={format}&csv_separator=,&use_labels_for_header=true",
            "millesime": None,
        })
        super().__init__(**kwargs)

    def get_millesime(self) -> datetime.datetime:
        response = downloader.request_get(f"{self.base_url}/api/datasets/1.0/{self.dataset}")
        response.raise_for_status()
        return datetime.datetime.fromisoformat(response.json()["metas"]["data_processed"])


class SourceHttpLastModified(Source):
    """Get URL from Last-Modified HTTP headers"""
    def get_millesime(self):
        return datetime.datetime.strptime(
            downloader.requests_retry_session().head(self.fileUrl).headers['Last-Modified'],
            downloader.HTTP_DATE_FMT,
        )

class SourceIGN(Source):
    """Get millesime from IGN BDTOPO MetaData"""
    def get_millesime(self) -> datetime.datetime:
        response = downloader.request_get("https://files.opendatarchives.fr/professionnels.ign.fr/bdtopo/latest/geopackage/meta.json")
        response.raise_for_status()
        return datetime.datetime.fromisoformat(response.json()["millesime"])

class Parser:
    def header(self):
        pass

    def import_(self, table, osmosis):
        pass

    def close(self):
        pass

    def srid(self):
        pass

class CSV(Parser):
    def __init__(self, source, separator = u',', null = u'', header = True, quote = u'"', csv = True, skip_first_lines = 0):
        """
        Describe the CSV file format, mainly for postgres COPY command in order to load data, but also for other thing, like load header.
        Setting param as None disable parameter into the COPY command.
        @param source: source file reader
        @param separator: one char separator
        @param null: string loaded à NULL
        @param header: CSV have header row
        @param quote: one char string delimiter
        @param csv: load file as CSV on COPY command
        @param skip_first_lines: skip lines before reading CSV content
        """
        self.source = source
        self.separator = separator
        self.null = null
        self.have_header = header
        self.quote = quote
        self.csv = csv
        self.skip_first_lines = skip_first_lines

        self.f = None

    def header(self):
        self.f = self.source.open()
        for _ in range(self.skip_first_lines):
            self.f.__next__()
        if self.have_header:
            return next(csv.reader(self.f, delimiter=self.separator, quotechar=self.quote))

    def import_(self, table, osmosis):
        self.f = self.f or self.source.open()
        for _ in range(self.skip_first_lines):
            self.f.__next__()
        copy = "COPY {0} FROM STDIN WITH {1} {2} {3} {4} {5}".format(
            table,
            ("DELIMITER AS '{0}'".format(self.separator)) if self.separator is not None else "",
            ("NULL AS '{0}'".format(self.null)) if self.null is not None else "",
            "CSV" if self.csv else "",
            "HEADER" if self.csv and self.header else "",
            ("QUOTE '{0}'".format(self.quote)) if self.csv and self.quote else "")
        osmosis.giscurs.copy_expert(copy, self.f)

    def close(self):
        self.f.close()

class GTFS(CSV):
    def __init__(self, source):
        """
        Load GTFS file data.
        @param source: source file reader
        """
        source.zip = "stops.txt"
        CSV.__init__(self, source)

    def srid(self):
        return 4326

def flattenjson(b):
    """
    Converts multi-level JSON properties into single level
    Columns names are separated by a "."
    Based on Alec McGail implementation, see https://stackoverflow.com/a/28246154
    @param b: source JSON object
    @return flattened JSON object
    """
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson(b[i])
            for j in get.keys():
                val[ i + "." + j ] = get[j]
        elif isinstance( b[i], list):
            val[i] = "[" + ",".join(map(str, b[i])) + "]"
        else:
            val[i] = b[i]
    return val

def removequotesjson(s):
    """
    Removes trailing and leading char " if any in given string
    @param s : source string
    @return same string without trailing/leading " char
    """
    try:
        return s.strip('"')
    except AttributeError:
        return s

class JSON(Parser):
    def __init__(self, source, extractor = lambda json: json):
        """
        Load JSON file data.
        @param source: source file reader
        @param extractor: lambda returning an interable
        """
        self.source = source
        self.extractor = extractor

        self.json = None

    def header(self):
        self.json = list(map(flattenjson, self.extractor(json.loads(self.source.open().read()))))
        columns = set()
        # Read all entries because structure can vary
        for feature in self.json:
            columns = columns.union(list(flattenjson(feature).keys()))
        columns = list(columns)
        return columns

    def import_(self, table, osmosis):
        self.json = self.json or map(flattenjson, self.extractor(json.loads(self.source.open().read())))
        for row in self.json:
            osmosis.giscurs.execute("insert into \"{0}\" (\"{1}\") values ({2})".format(
                table, '", "'.join(row.keys()), (u'%s, ' * len(row.keys()))[:-2]),
                list(map(removequotesjson, row.values())))

class GeoJSON(Parser):
    def __init__(self, source, extractor = lambda json: json):
        """
        Load GeoJSON file data.
        @param source: source file reader
        @param extractor: lambda returning an interable
        """
        self.source = source
        self.extractor = extractor

        self.json = None

    def header(self):
        self.json = self.extractor(json.loads(self.source.open().read()))
        columns = set()
        # Read all entries because structure can vary
        for feature in self.json['features']:
            columns = columns.union(list(flattenjson(feature['properties']).keys()))
        columns = list(columns)
        columns.append(u"geom_x")
        columns.append(u"geom_y")
        return columns

    def import_(self, table, osmosis):
        self.json = self.json or self.extractor(json.loads(self.source.open().read()))
        for row in self.json['features']:
            if row['geometry'] and row['geometry']['coordinates'] and len(row['geometry']['coordinates']) > 0:
                row['properties'] = flattenjson(row['properties'])
                columns = list(row['properties'].keys())
                values = list(map(removequotesjson, map(lambda column: row['properties'][column], columns)))
                columns.append(u"geom_x")
                columns.append(u"geom_y")
                if row['geometry']['type'] in ('Point', 'MultiPoint', 'LineString', 'MultiLineString'):
                    if row['geometry']['type'] == 'Point':
                        values.append(row['geometry']['coordinates'][0])
                        values.append(row['geometry']['coordinates'][1])
                    elif row['geometry']['type'] in ('MultiPoint', 'LineString'):
                        npt = len(row['geometry']['coordinates'])//2
                        values.append(row['geometry']['coordinates'][npt][0])
                        values.append(row['geometry']['coordinates'][npt][1])
                    else:
                        npt = len(row['geometry']['coordinates'][0])//2
                        values.append(row['geometry']['coordinates'][0][npt][0])
                        values.append(row['geometry']['coordinates'][0][npt][1])
                    osmosis.giscurs.execute(u"insert into \"{0}\" (\"{1}\") values ({2})".format(
                        table, u'", "'.join(columns), (u'%s, ' * len(columns))[:-2]),
                        values)

    def srid(self):
        return 4326

class GDAL(Parser):
    def __init__(self, source, zip = None, layer = None, fields = None):
        """
        Load any GDAL supported format.
        @param source: source file reader
        @param zip: use path in zip file.
        @param layer: layer to use when source is multi-layer.
        @param fields: array of fields to load. Default to All. Usefull for big dataset.
        """
        self.source = source
        self.zip = zip
        self.layer = layer
        self.fields = fields

    def header(self):
        return True

    def import_(self, table, osmosis):
        try:
            tmp_file = tempfile.NamedTemporaryFile(suffix = '.zip' if self.zip else '', mode = 'wb', delete = False)
            shutil.copyfileobj(self.source.open(binary = True), tmp_file, 20*1024*1024)
            tmp_file.close()

            if self.zip:
                # Resolve pattern filename into the zip archive.
                z = zipfile.ZipFile(tmp_file.name, 'r')
                info = next(filter(lambda zipinfo: fnmatch.fnmatch(zipinfo.filename, self.zip), z.infolist()))
                if info:
                    self.zip = info.filename

            select = "-select '{}'".format(','.join(self.fields)) if self.fields else ''
            gdal = "ogr2ogr -f PostgreSQL 'PG:{}' -lco SCHEMA={} -nln {} -lco OVERWRITE=yes -lco GEOMETRY_NAME=geom -lco LAUNDER=NO {} -t_srs EPSG:{} '{}' {}".format(
                osmosis.config.osmosis_manager.db_string,
                osmosis.config.osmosis_manager.db_user,
                table,
                select,
                self.proj,
                ('/vsizip/' if self.zip else '' ) + tmp_file.name + (('/' + self.zip) if self.zip else ''),
                f"'{self.layer}'" if self.layer else '',
            )
            osmosis.giscurs.execute("DROP TABLE IF EXISTS {} CASCADE".format(table))
            osmosis.giscurs.execute("COMMIT")
            print(gdal)
            if os.system(gdal):
                raise Exception("ogr2ogr error")
            osmosis.giscurs.execute("BEGIN")
        finally:
            os.remove(tmp_file.name)

    def srid(self):
        return self.proj

SHP = GDAL
GPKG = GDAL

class Load(object):
    def __init__(self, geom = ("NULL",), srid = None, table_name = None, create = None,
            select = {}, unique = None, where = lambda res: True, map = lambda i: i, geomFunction = lambda i: i, validationGeomSQL = "1=1", spatialGeom = lambda geom: f"ST_GeomFromEWKT('{geom}')"):
        """
        Describ the conversion of data set loaded with COPY into the database into an other table more usable for processing.
        @param geom: the name of geom column, can be a SQL expression formatted as ("SQL CODE",)
        @param srid: overwrite the projection of geometry, by default projection comes from parsed content, or if no fallback to 4326.
        @param table_name: override the default table name
        @param create: the data base table description, generated by default from file header et format
        @param select: dict reformatted as SQL to filter row import before conversion, prefer this as the where parameter
        @param unique: keep only one distinct record by list of column
        @param where: lambda expression taking row as dict and returning boolean to determine whether or not inserting the row into the table
        @param map: lambda returning adict from adict to replace the record
        @param geomFunction: lambda expression for convert geom content column before reprojection, identity by default
        @param validationGeomSQL: SQL where clause to pre-validate geometry
        @param spatialGeom: SQL to get the geometry
        """
        self.geom = geom
        self.sridOverwrite = srid
        self.table_name = table_name
        self.create = create
        self.select = select
        self.unique = unique
        self.where = where
        self.map = map
        self.geomFunction = geomFunction
        self.validationGeomSQL = validationGeomSQL
        self.spatialGeom = spatialGeom

    def srid(self):
        return self.sridOverwrite if self.sridOverwrite is not None else (self.parser.srid() or 4326)

    def run(self, osmosis, conflate, db_schema, default_table_base_name, version):
        """
        @return if data loaded in data base
        """
        table_base_name = self.table_name or default_table_base_name
        table = DictCursorUnicode.identifier(table_base_name)

        osmosis.run("CREATE TABLE IF NOT EXISTS meta (name character varying(255) NOT NULL, update integer, bbox character varying(1024) )")

        # Official data table cache
        country_hash = osmosis.config.db_schema.split('_')[-1][0:10] + hexastablehash(osmosis.config.db_schema)[-4:]
        if len(default_table_base_name + '_' + country_hash) <= 63-2-3: # 63 max postgres relation name, 3 is index name prefix
            tableOfficial = default_table_base_name + '_' + country_hash + "_o"
        else:
            tableOfficial = (default_table_base_name + '_' + country_hash)[-(63-2-3-4):] + '_o' + hexastablehash(default_table_base_name)[-4:]

        self.data = False
        def setData(res):
            self.data = res
        osmosis.run0("SELECT bbox FROM meta WHERE name='{0}' AND bbox IS NOT NULL AND update IS NOT NULL AND update={1}".format(tableOfficial, version), lambda res: setData(res))

        if not self.data:
            osmosis.logger.log("Load raw data into database")
            if not self.create:
                header = self.parser.header()
                if header:
                    if header is not True:
                        self.create = ",".join(map(lambda c: "\"{0}\" VARCHAR(65534)".format(DictCursorUnicode.identifier(c)), header))
                else:
                    raise AssertionError("No table schema provided")
            osmosis.run(sql_schema.format(schema = db_schema))
            if self.create:
                osmosis.run("CREATE TEMP TABLE {0} ({1})".format(table, self.create))
            self.parser.import_(table, osmosis)
            self.parser.close()

            # Convert
            osmosis.logger.log("Convert raw data to tags")
            osmosis.run(sql_schema.format(schema = db_schema))
            osmosis.run(sql00.format(official = tableOfficial, proj = self.proj))
            giscurs = osmosis.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            mult_space = re.compile(r'\s+')
            def insertOfficial(res):
                if not self.where(res):
                    return
                res = self.map(res)
                geom = self.geomFunction(res['_geom'])
                if geom:
                    for k in res.keys():
                        try:
                            res[k] = mult_space.sub(' ', res[k].strip()) # Strip and remove duplicate space
                        except AttributeError:
                            pass
                    tags = conflate.mapping.tagFactory(res)
                    tags[1].update(tags[0])
                    giscurs.execute(sql02.format(official = tableOfficial, proj = self.proj, geom = self.spatialGeom(geom)), {
                        "ref": tags[1].get(conflate.osmRef) if conflate.osmRef != "NULL" else None,
                        "tags": tags[1],
                        "tags1": tags[0],
                        "fields": dict(zip(dict(res).keys(), map(lambda s: (s is None and None) or u'{0}'.format(s), dict(res).values()))),
                    })
            if isinstance(self.geom, tuple):
                self.geom = self.geom[0]
            else:
                self.geom = "ST_AsEWKT(\"{0}\")".format(self.geom)
            if self.unique:
                l = ','.join(map(lambda v: '"{0}"'.format(v), self.unique))
                distinct = "DISTINCT ON ({0})".format(l)
                order_by = "ORDER BY {0}".format(l)
            else:
                distinct = order_by = ""
            osmosis.run0((sql01_ref if conflate.osmRef != "NULL" else sql01_geo).format(table = table, geom = self.geom, validationGeomSQL = self.validationGeomSQL, where = Select.where_attributes(self.select), distinct = distinct, order_by = order_by), insertOfficial)
            osmosis.run(sql02b.format(official = tableOfficial))
            if self.srid():
                giscurs.execute("SELECT ST_AsText(ST_Envelope(ST_Extent(geom))) FROM {0}".format(tableOfficial))
                self.bbox = giscurs.fetchone()[0]
            else:
                self.bbox = None
            osmosis.run(sql03a.format(official = tableOfficial))
            osmosis.run(sql03b.format(official = tableOfficial))

            giscurs.close()

            osmosis.run("DELETE FROM meta WHERE name='{0}'".format(tableOfficial))
            if self.bbox is not None:
                osmosis.run("INSERT INTO meta VALUES ('{0}', {1}, '{2}')".format(tableOfficial, version, self.bbox))

            osmosis.run("DROP TABLE {0}".format(table))
            osmosis.run0("COMMIT")
            osmosis.run0("BEGIN")
        else:
            self.bbox = self.data[0]

        if not (self.srid() and not self.bbox): # Abort condition
            return tableOfficial

    @staticmethod
    def float_comma(val):
        """Convert decimal comma separeted to dot."""
        if val is not None:
            return float(val.replace(',', '.'))

    @staticmethod
    def degree(val):
        """Convert coordinate in degree, minute, second to decimal degrees."""
        if val is not None and u'°' in val:
            # 01°13'23,8 -> 1,334388
            return reduce(lambda sum, i: sum * 60 + i, map(lambda i: float(i.replace(u',', u'.')), filter(lambda i: i != '', val.replace(u'°', u"'").split(u"'"))), 0) / 3600
        else:
            return val

class Load_XY(Load):
    pip = None

    def __init__(self, x = ("NULL",), y = ("NULL",), srid = None, table_name = None, create = None,
            select = {}, unique = None, where = lambda res: True, map = lambda i: i, xFunction = lambda i: i, yFunction = lambda i: i):
        """
        Describ the conversion of data set loaded with COPY into the database into an other table more usable for processing.
        @param x: the name of x column, as or converted to longitude, can be a SQL expression formatted as ("SQL CODE",)
        @param y: the name of y column, as or converted to latitude, can be a SQL expression formatted as ("SQL CODE",)
        @param srid: overwrite the projection of geometry, by default projection comes from parsed content, or if no fallback to 4326.
        @param table_name: override the default table name
        @param create: the data base table description, generated by default from file header et format
        @param select: dict reformatted as SQL to filter row import before conversion, prefer this as the where parameter
        @param unique: keep only one distinct record by list of column
        @param where: lambda expression taking row as dict and returning boolean to determine whether or not inserting the row into the table
        @param map: lambda returning adict from adict to replace the record
        @param xFunction: lambda expression for convert x content column before reprojection, identity by default
        @param yFunction: lambda expression for convert y content column before reprojection, identity by default
        """
        if isinstance(x, tuple):
            x = x[0]
        else:
            x = "\"{0}\"".format(x)
        if isinstance(y, tuple):
            y = y[0]
        else:
            y = "\"{0}\"".format(y)

        self.xFunction = xFunction
        self.yFunction = yFunction

        validationGeomSQL = f"""
    {x} IS NOT NULL AND
    {y} IS NOT NULL AND
    {x}::varchar NOT IN ('', 'null') AND
    {y}::varchar NOT IN ('', 'null')
"""
        spatialGeom = lambda geom: f"ST_Transform(ST_GeomFromEWKT('SRID={self.srid()};POINT({geom[0]} {geom[1]})'), {self.proj})" if self.srid() else "NULL::geometry"
        super().__init__((f'ARRAY[{x}, {y}]',), srid, table_name, create, select, unique, where, map, self.geomFunctionPoint, validationGeomSQL, spatialGeom)

    def run(self, osmosis, conflate, db_schema, default_table_base_name, version):
        """
        @return if data loaded in data base
        """
        if not self.pip:
            self.pip = PointInPolygon.PointInPolygon(self.polygon_id) if self.srid() and self.polygon_id else None
            if self.pip:
                if Transformer:
                    self.transformer = Transformer.from_crs(self.srid(), 4326, always_xy = True)
                else: # pyproj < 2.1
                    self.transformer = None

        try:
            if self.pip and not self.transformer:
                self.giscurs_getpoint = osmosis.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            return super().run(osmosis, conflate, db_schema, default_table_base_name, version)
        finally:
            if self.pip and not self.transformer and self.giscurs_getpoint:
                self.giscurs_getpoint.close()

    def geomFunctionPoint(self, geom):
        x, y = self.xFunction(geom[0]), self.yFunction(geom[1])
        if not self.pip or (x and y):
            is_pip = False
            if self.pip:
                if self.transformer:
                    lonLat = self.transformer.transform(x, y)
                else:
                    self.giscurs_getpoint.execute("SELECT ST_AsText(ST_Transform(ST_SetSRID(ST_MakePoint({x}, {y}), {srid}), 4326))".format(x=x, y=y, srid=self.srid()))
                    lonLat = self.osmosis.get_points(self.giscurs_getpoint.fetchone()[0])[0]
                    lonLat = [float(lonLat["lon"]), float(lonLat["lat"])]
                is_pip = self.pip.point_inside_polygon(lonLat[0], lonLat[1])
            if not self.pip or is_pip:
                return [x, y]


class LoadGeomCentroid(Load_XY):
    def __init__(self, *args, **kwargs):
        super(LoadGeomCentroid, self).__init__(("ST_X(ST_PointOnSurface(geom))",), ("ST_Y(ST_PointOnSurface(geom))",), *args, **kwargs)

class Select:
    def __init__(self, types = [], tags = {}):
        """
        On witch OSM we try to join data set.
        @param types: object types, array of "relations", "ways" and "nodes"
        @param tags: dict of tags or array of dicts, array mean "OR"
        """
        self.types = types
        self.tags = tags

    @staticmethod
    def where_tags(query):
        return Select._where(query, attribut_not_exists = "NOT tags?'{}'", attribut_value = "tags->'{}'")

    @staticmethod
    def where_attributes(query):
        return Select._where(query, attribut_not_exists = "\"{}\" IS NULL", attribut_value = "\"{}\"")

    @staticmethod
    def _where(query, attribut_not_exists, attribut_value):
        if not isinstance(query, list):
            query = [query]
        return "((" + (") OR (".join(map(lambda x: Select._where_and(x, attribut_not_exists, attribut_value), query))) + "))"

    @staticmethod
    def _where_and(query, attribut_not_exists, attribut_value):
        clauses = []
        for k, v in query.items():
            k_not_exists = attribut_not_exists.format(k)
            k_value = attribut_value.format(k)
            if v is False:
                clauses.append(k_not_exists)
            else:
                if hasattr(v, '__call__'):
                    clauses.append("NOT " + k_not_exists)
                    clauses.append(v(k_value))
                elif isinstance(v, list):
                    cond = k_value + " IN ('{}')".format("', '".join(map(lambda i: i.replace("'", "''"), filter(lambda i: i is not False, v))))
                    if False in v:
                        cond = "(" + cond + " OR " + k_not_exists + ")"
                    else:
                        clauses.append("NOT " + k_not_exists)
                    clauses.append(cond)
                else:
                    clauses.append("NOT " + k_not_exists)
                    if v is None or v is True:
                        pass
                    elif isinstance(v, dict):
                        if "like" in v:
                            clauses.append(k_value + " LIKE '{}'".format(v["like"].replace("'", "''")))
                        elif "regex" in v:
                            clauses.append(k_value + " ~ '{}'".format(v["regex"].replace("'", "''")))
                    else:
                        clauses.append(k_value + " = '{}'".format(v.replace("'", "''")))
        return " AND ".join(clauses) if clauses else "1=1"


MappingStatic = Dict[str, Union[str, Callable[[], str]]]
MappingMapping = Dict[str, Union[str, Callable[[Dict[str, str]], str]]]
MappingText = Callable[[Dict[str, str], Dict[str, str]], Dict[str, str]]

class Mapping:
    def __init__(
        self,
        static1: MappingStatic = {},
        static2: MappingStatic = {},
        mapping1: MappingMapping = {},
        mapping2: MappingMapping = {},
        text: MappingText = lambda tags, fields: {},
    ):
        """
        How fields are mapped to OSM tags.
        @param static1: dict of primary tags apply as is
        @param static2: dict of secondary tags apply as is, not checked on update process
        @param mapping1: dict of primary tags, if value is string then data set column value is take, else lambda
        @param mapping2: dict of secondary tags, if value is string then data set column value is take, else lambda, not checked on update process
        @param text: lambda return string, describe this error
        """
        self.static1: MappingStatic = static1
        self.static2: MappingStatic = static2
        self.mapping1: MappingMapping = mapping1
        self.mapping2: MappingMapping = mapping2
        self.text: MappingText = text

    def eval_staticGroup(self, static: MappingStatic, analyser):
        for tag, colomn in static.items():
            if callable(colomn):
                r = colomn()
                if r:
                    static[tag] = r

    def eval_static(self, analyser):
        self.eval_staticGroup(self.static1, analyser)
        self.eval_staticGroup(self.static2, analyser)

    delete_tag = GENERATE_DELETE_TAG

    def tagFactoryGroup(self, res, static, mapping):
        tags = dict(static)
        for tag, colomn in mapping.items():
            if callable(colomn):
                r = colomn(res)
                if r:
                    tags[tag] = r
            elif colomn and res[colomn]:
                tags[tag] = res[colomn]

        return dict(map(lambda kv: [kv[0], kv[1] is not None and u'{0}'.format(kv[1]) or None], tags.items()))

    def tagFactory(self, res):
        tags = self.tagFactoryGroup(res, self.static1, self.mapping1)
        tags_secondary = self.tagFactoryGroup(res, self.static2, self.mapping2)
        return [tags, tags_secondary]

    @staticmethod
    def date_format(date_string, format='%d/%m/%Y'):
        try:
            dt = datetime.datetime.strptime(date_string, format)
            return str(dt.date())
        except ValueError:
            return None

class Conflate:
    def __init__(self, select = Select(), osmRef = "NULL", conflationDistance = None, extraJoin = None, tag_keep_multiple_values = [], subclass_hash = lambda d: d, mapping = Mapping()):
        """
        How data is mapped with OSM data.
        @param select: fetch OSM data, see Select
        @param osmRef: the OSM key for join data on reference, must refer to mapped tag from OpenData set.
        @param conflationDistance: if no osmRef, do do conflation, use this threshold
        @param extraJoin: an additional OSM key to join on, must refer to mapped tag from OpenData set.
        @param tag_keep_multiple_values: if tags already have value or multiple values just append the new one
        @param subclass_hash: lambda return dict from dict fields to be used in subclass hash computation (to be stable)
        @param mapping: map the fields to OSM tags, see Mapping
        """
        self.select = select
        self.osmRef = osmRef
        self.conflationDistance = conflationDistance
        self.extraJoin = extraJoin
        self.tag_keep_multiple_values = tag_keep_multiple_values
        self.subclass_hash = subclass_hash
        self.mapping = mapping


class Analyser_Merge(Analyser_Osmosis):

    def __init__(self, config, logger):
        Analyser_Osmosis.__init__(self, config, logger)

    doc_master = dict(
        detail = T_(
'''It is from OpenData source, but that not enough to ensure the quality
of the data. Review it before integration. You must not done blind import
into OSM, you must do critical review of data integration.'''),
        fix = T_(
'''If after review you are sure that it is a new data and right for
OpenStreetMap, then you can add it.'''),
        trap = T_(
'''Be sure that it is not already existing in another place.'''))

    def def_class_missing_official(self, **kwargs):
        doc = self.merge_docs(self.doc_master,
            detail = T_(
'''This is reported from an OpenData source, without any prior individual
verification on this data.'''))
        kwargs.update(self.merge_docs(doc, **kwargs))
        self.missing_official = self.def_class(back_in_stack = 3, **kwargs)

    def init(self, url, name, parser, load = Load(), conflate = Conflate()):
        """
        @param url: remote URL of data source, webpage
        @param name: official name of the data set
        """
        self.url = url
        self.name = name
        self.parser = parser
        self.load = load
        self.conflate = conflate

        for (id, c) in self.classs.items():
            c['resource'] = url

        if not isinstance(self.conflate.select.tags, list):
            self.conflate.select.tags = [self.conflate.select.tags]
        self.conflate.mapping.eval_static(self)

        self.load.osmosis = self
        self.load.polygon_id = self.config.polygon_id
        if "proj" in self.config.options:
            self.parser.proj = self.config.options.get("proj")
            self.load.proj = self.config.options.get("proj")

        if hasattr(self, 'missing_official'):
            self.classs[self.missing_official['id']] = self.missing_official
        else:
            self.missing_official = None

    def source(self):
        return self.parser.source.as_tag_value()

    def analyser_version(self):
        return SourceVersion.version(self.parser.source.time(), self.__class__)

    def typeGeom(self):
        typeSelect = {'N': 'geom', 'W': 'linestring', 'R': 'relation_locate(id)'}
        typeGeom = {'N': 'geom', 'W': 'linestring', 'R': 'relation_locate(id)'}
        if self.conflate.osmRef == "NULL" or self.possible_merge:
            typeShape = {'N': 'geom', 'W': 'linestring', 'R': 'relation_shape(id)'}
        else:
            typeShape = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}
        return [typeSelect, typeGeom, typeShape]

    def analyser_osmosis_common(self):
        self.run("SET search_path TO {0}".format(self.config.db_schema_path or ','.join([self.config.db_user, self.config.db_schema, 'public'])))
        self.load.parser = self.parser
        table = self.load.run(self, self.conflate, self.config.db_user, self.__class__.__name__.lower()[15:], self.analyser_version())
        if not table:
            self.logger.log(u"Empty bbox, abort")
            return None

        # Extract OSM objects
        if self.load.srid():
            typeSelect, typeGeom, typeShape = self.typeGeom()
        else:
            typeSelect = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}
            typeGeom = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}
            typeShape = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}

        self.logger.log(u"Retrieve OSM item")
        where = Select.where_tags(self.conflate.select.tags)
        self.run("CREATE TEMP TABLE osm_item AS " +
            ("UNION ALL".join(
                map(lambda type:
                    ("""(
                    SELECT
                        '{type}'::char(1) AS type,
                        id,
                        trim(both from ref) AS ref,
                        ST_Transform({geom}::geometry, {proj}) AS geom,
                        ST_Transform({shape}::geometry, {proj}) AS shape,
                        tags
                    FROM
                        {from_}
                        LEFT JOIN LATERAL regexp_split_to_table(tags->'{ref}', ';') a(ref) ON true
                    WHERE""" + ("""
                        {geomSelect} IS NOT NULL AND""" if self.load.srid() else "") + ("""
                        ST_Transform(ST_Expand(ST_SetSRID(ST_GeomFromText('{bbox}'), {proj}), {distance}), 4326) && {geomSelect} AND""" if self.load.bbox and self.load.srid() else "") + """
                        tags != ''::hstore AND
                        {where})""").format(
                        type = type[0].upper(),
                        ref = self.conflate.osmRef,
                        geomSelect = typeSelect[type[0].upper()],
                        geom = typeGeom[type[0].upper()],
                        shape = typeShape[type[0].upper()],
                        from_ = type,
                        bbox = self.load.bbox,
                        srid = self.load.srid(),
                        proj = self.config.options.get("proj"),
                        distance = self.conflate.conflationDistance or 0, where = where),
                    self.conflate.select.types
                )
            ))
        )

        return table

    def passTags(self, official):
        official = dict(filter(lambda kv: kv[1] != Mapping.delete_tag, official.items()))
        return {"+": official}

    def mergeTags(self, osm, official, ref, keep_multiple):
        fix = {"+": {}, "~": {}, "-": []}
        for o in official:
            if o in osm:
                if official[o] == Mapping.delete_tag:
                    fix["-"].append(o)
                elif osm[o] == official[o]:
                    pass
                else:
                    if o == "source":
                        if self.parser.source.attribution:
                            for s in osm[o].split(";"):
                                if self.parser.source.match_attribution(s):
                                    fix["~"][o] = osm[o].replace(s, self.parser.source.as_tag_value())
                                    break
                        else:
                            fix["~"][o] = osm[o]+";"+official[o]
                    else:
                        fix["~"][o] = official[o]
            else:
                if official[o] != Mapping.delete_tag:
                    fix["+"][o] = official[o]
        for k in [ref] + keep_multiple:
            if fix["~"].get(k) and osm.get(k):
                if fix["~"][k] not in osm[k].split(";"):
                    fix["~"][k] = osm[k] + ";" + fix["~"][k] # Append new value to the list
                else:
                    del fix["~"][k] # Value already in the list, change nothing
        keys = [s for s in (list(fix["+"].keys()) + list(fix["~"].keys())) if s != "name" and not s.startswith("source")]
        if "name" in osm and "name" in official and osm["name"] != official["name"] and len(keys) != 0:
            fix0 = {"+": fix["+"], "~": dict(fix["~"])}
            del fix0["~"]["name"]
            fix = [fix0, fix]
        return fix


class Analyser_Merge_Point(Analyser_Merge):

    def __init__(self, config, logger):
        Analyser_Merge.__init__(self, config, logger)

    def def_class_missing_osm(self, **kwargs):
        doc = self.doc_master
        kwargs.update(self.merge_docs(doc, **kwargs))
        self.missing_osm = self.def_class(back_in_stack = 3, **kwargs)

    def def_class_possible_merge(self, **kwargs):
        doc = self.merge_docs(self.doc_master,
            detail = T_(
'''This is a integration suggestion, mixing OpenData source and
OpenStreetMap.'''))
        kwargs.update(self.merge_docs(doc, **kwargs))
        self.possible_merge = self.def_class(back_in_stack = 3, **kwargs)

    def def_class_moved_official(self, **kwargs):
        doc = self.doc_master
        kwargs.update(self.merge_docs(doc, **kwargs))
        self.moved_official = self.def_class(back_in_stack = 3, **kwargs)

    def def_class_update_official(self, **kwargs):
        doc = self.merge_docs(self.doc_master,
            detail = T_(
'''This is an update suggestion because the same ref can be found on both
OpenData and OSM.'''))
        kwargs.update(self.merge_docs(doc, **kwargs))
        self.update_official = self.def_class(back_in_stack = 3, **kwargs)

    def init(self, url, name, parser, load = Load_XY(), conflate = Conflate()):
        """
        @param url: remote URL of data source, webpage
        @param name: official name of the data set
        """
        super().init(url, name, parser, load, conflate)

        if hasattr(self, 'missing_osm'):
            self.classs[self.missing_osm['id']] = self.missing_osm
        else:
            self.missing_osm = None
        if hasattr(self, 'possible_merge'):
            self.classs[self.possible_merge['id']] = self.possible_merge
        else:
            self.possible_merge = None
        if hasattr(self, 'moved_official'):
            self.classs[self.moved_official['id']] = self.moved_official
        else:
            self.moved_official = None
        if hasattr(self, 'update_official'):
            self.classs[self.update_official['id']] = self.update_official
        else:
            self.update_official = None

    def typeGeom(self):
        typeSelect = {'N': 'geom', 'W': 'linestring', 'R': 'relation_locate(id)'}
        typeGeom = {'N': 'geom', 'W': 'way_locate(linestring)', 'R': 'relation_locate(id)'}
        if self.conflate.osmRef == "NULL" or self.possible_merge:
            typeShape = {'N': 'geom', 'W': 'ST_Envelope(linestring)', 'R': 'relation_shape(id)'}
        else:
            typeShape = {'N': 'NULL', 'W': 'NULL', 'R': 'NULL'}
        return [typeSelect, typeGeom, typeShape]

    def analyser_osmosis_common(self):
        table = super().analyser_osmosis_common()
        if not table:
            return

        if self.conflate.osmRef != "NULL":
            self.run("CREATE INDEX osm_item_index_ref ON osm_item(ref)")
        self.run("CREATE INDEX osm_item_index_shape ON osm_item USING GIST(shape)")

        self.giscurs.execute(f"SELECT COUNT(*) FROM {table}")
        count_official = self.giscurs.fetchone()[0]
        self.giscurs.execute("SELECT COUNT(*) FROM osm_item")
        count_osm = self.giscurs.fetchone()[0]

        joinClause = []
        if self.conflate.osmRef != "NULL":
            joinClause.append("official.ref = osm_item.ref")
        elif self.load.srid():
            joinClause.append("ST_DWithin(official.geom, osm_item.shape, {0})".format(self.conflate.conflationDistance))
        if self.conflate.extraJoin:
            joinClause.append("official.tags->'{tag}' = osm_item.tags->'{tag}'".format(tag=self.conflate.extraJoin))
        joinClause = " AND\n".join(joinClause) + "\n"

        # Missing official
        self.run(sql10.format(official = table, joinClause = joinClause))
        self.run(sql11)
        count_missing_official = None
        if self.missing_official:
            count_missing_official = 0
            def ret(res):
                nonlocal count_missing_official
                count_missing_official = count_missing_official + 1
                return {
                    "class": self.missing_official['id'],
                    "subclass": str(stablehash64("{0}{1}{2}".format(
                        res[0], res[1],
                        sorted(self.conflate.subclass_hash(res[3]).items())) )),
                    "self": lambda r: [0]+r[1:],
                    "data": [self.node_new, self.positionAsText],
                    "text": self.conflate.mapping.text(defaultdict(lambda:None,res[2]), defaultdict(lambda:None,res[3])),
                    "fix": self.passTags(res[2]) if res[2] != {} else None,
                }
            self.run(sql12, ret)

        count_missing_osm = None
        count_invalid_osm_ref = None
        if self.conflate.osmRef != "NULL":
            self.run(sql20.format(official = table, joinClause = joinClause))
            self.run(sql21)
            if self.missing_osm:
                # Missing OSM
                count_missing_osm = 0
                def ret_missing(res):
                    nonlocal count_missing_osm
                    count_missing_osm = count_missing_osm + 1
                    return {
                        "class": self.missing_osm['id'],
                        "data": [self.typeMapping[res[1]], None, self.positionAsText]
                    }
                self.run(sql22, ret_missing)
                # Invalid OSM
                count_invalid_osm_ref = 0
                def ret_invalid(res):
                    nonlocal count_invalid_osm_ref
                    count_invalid_osm_ref = count_invalid_osm_ref + 1
                    return {
                        "class": self.missing_osm['id'],
                        "subclass": str(stablehash64(res[5])) if self.conflate.osmRef != "NULL" else None,
                        "data": [self.typeMapping[res[1]], None, self.positionAsText]
                    }
                self.run(sql23.format(official = table, joinClause = joinClause), ret_invalid)

            # Possible merge
            count_possible_merge = None
            if self.possible_merge:
                possible_merge_joinClause = []
                possible_merge_orderBy = ""
                if self.load.srid():
                    possible_merge_joinClause.append("ST_DWithin(missing_official.geom, missing_osm.shape, {0})".format(self.conflate.conflationDistance))
                    possible_merge_orderBy = ", ST_Distance(missing_official.geom, missing_osm.shape) ASC"
                if self.conflate.extraJoin:
                    possible_merge_joinClause.append("missing_official.tags->'{tag}' = missing_osm.tags->'{tag}'".format(tag=self.conflate.extraJoin))
                possible_merge_joinClause = " AND\n".join(possible_merge_joinClause) + "\n"
                count_possible_merge = 0
                def ret(res):
                    nonlocal count_possible_merge
                    count_possible_merge = count_possible_merge + 1
                    return {
                        "class": self.possible_merge['id'],
                        "subclass": str(stablehash64("{0}{1}".format(
                            res[0],
                            sorted(self.conflate.subclass_hash(res[3]).items())) )),
                        "data": [self.typeMapping[res[1]], None, self.positionAsText],
                        "text": self.conflate.mapping.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[4])),
                        "fix": self.mergeTags(res[5], res[3], self.conflate.osmRef, self.conflate.tag_keep_multiple_values),
                    }
                self.run(sql30.format(joinClause = possible_merge_joinClause, orderBy = possible_merge_orderBy), ret)

            self.dumpCSV("SELECT ST_X(geom::geometry) AS lon, ST_Y(geom::geometry) AS lat, tags FROM {0}".format(table), "", ["lon","lat"], lambda r, cc:
                list((r['lon'], r['lat'])) + cc
            )

            self.run(sql40.format(official = table, joinClause = joinClause))
            self.dumpCSV(sql41, ".byOSM", ["osm_id","osm_type","lon","lat"], lambda r, cc:
                list((r['osm_id'], r['osm_type'], r['lon'], r['lat'])) + cc
            )

            file = io.open("{0}/{1}.metainfo.csv".format(self.config.dst_dir, self.name), "w", encoding="utf8")
            file.write("file,origin,osm_date,count_official,count_osm,count_missing_official_in_osm,count_missing_osm_in_official,count_invalid_osm_ref,count_possible_merge\n")
            file.write(f"\"{self.name}\",\"{self.parser.source.fileUrl or self.url}\",FIXME,{count_official},{count_osm},{count_missing_official},{count_missing_osm},{count_invalid_osm_ref},{count_possible_merge}\n")
            file.close()

        # Moved official
        if self.moved_official:
            self.run(sql50.format(official = table, joinClause = joinClause), lambda res: {
                "class": self.moved_official['id'],
                "data": [self.node_full, self.positionAsText],
            } )

        # Update official
        if self.update_official:
            self.run(sql60.format(official = table, joinClause = joinClause), lambda res: {
                "class": self.update_official['id'],
                "subclass": str(stablehash64("{0}{1}".format(
                    res[0],
                    sorted(self.conflate.subclass_hash(res[5]).items())) )),
                "data": [self.typeMapping[res[1]], None, self.positionAsText],
                "text": self.conflate.mapping.text(defaultdict(lambda:None,res[3]), defaultdict(lambda:None,res[5])),
                "fix": self.mergeTags(res[4], res[3], self.conflate.osmRef, self.conflate.tag_keep_multiple_values),
            } )

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
        column = list(filter(lambda a: a != self.conflate.osmRef and not a in self.conflate.select.tags[0], column))
        column = [self.conflate.osmRef] + list(self.conflate.select.tags[0].keys()) + column
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator=u'\n')
        writer.writerow(head + column)
        for r in row:
            cc = []
            for c in column:
                tags = r['tags']
                if c in tags:
                    cc.append(tags[c])
                else:
                    cc.append(None)
            writer.writerow(callback(r, cc))

        with bz2.BZ2File("{0}/{1}-{2}{3}.csv.bz2".format(self.config.dst_dir, self.name, self.__class__.__name__, ext), mode='w') as csv_bz2_file:
            csv_bz2_file.write(buffer.getvalue().encode('utf-8'))

###########################################################################
from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    from modules import config
    default_xml_res_path = config.dir_tmp + "/tests/osmosis/"

    @classmethod
    def setup_class(cls):
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis.test.osm",
                                         cls.default_xml_res_path + "osmosis.test.xml",
                                         {"test": True,
                                          "addr:city-admin_level": "8,9",
                                          "driving_side": "left",
                                          "proj": 2969})

        cls.analyser_conf.country = "FR"
        cls.analyser_conf.dst_dir = cls.conf.dir_results

        import modules.OsmOsisManager
        cls.conf.osmosis_manager = modules.OsmOsisManager.OsmOsisManager(cls.conf, cls.conf.db_host, cls.conf.db_user, cls.conf.db_password, cls.conf.db_base, cls.conf.db_schema or cls.conf.country, cls.conf.db_persistent, cls.logger)

    # def test_merge(self):
    #     # run all available merge analysers, for basic SQL check
    #     import importlib
    #     import inspect
    #     import os

    #     for fn in sorted(os.listdir("analysers/")):
    #         if not fn.startswith("analyser_merge_") or not fn.endswith(".py"):
    #             continue
    #         analyser = importlib.import_module("analysers." + fn[:-3], package=".")
    #         for name, obj in inspect.getmembers(analyser):
    #             if (inspect.isclass(obj) and obj.__module__ == ("analysers." + fn[:-3]) and
    #                 (name.startswith("Analyser") or name.startswith("analyser"))):

    #                 self.xml_res_file = self.analyser_conf.error_file.dst

    #                 with obj(self.analyser_conf, self.logger) as analyser_obj:
    #                     analyser_obj.analyser()

    #                 self.root_err = self.load_errors()
    #                 self.check_num_err(min=0, max=5)

    def test_date_formatter(self):
        self.assertEqual(Mapping.date_format('27/04/1990'), '1990-04-27')
        self.assertEqual(Mapping.date_format('04/27/1990', '%m/%d/%Y'), '1990-04-27')
        self.assertEqual(Mapping.date_format('31/04/1990'), None)

    def test_where_formatter(self):
        self.assertEqual(Select.where_attributes({}), """((1=1))""")
        self.assertEqual(Select.where_attributes({'a': None}), """((NOT "a" IS NULL))""")
        self.assertEqual(Select.where_attributes({'a': True}), """((NOT "a" IS NULL))""")
        self.assertEqual(Select.where_attributes({'a': False}), """(("a" IS NULL))""")
        self.assertEqual(Select.where_attributes({'a': {'like': 'a%'}}), """((NOT "a" IS NULL AND "a" LIKE 'a%'))""")
        self.assertEqual(Select.where_attributes({'a': '1'}), """((NOT "a" IS NULL AND "a" = '1'))""")
        self.assertEqual(Select.where_attributes({'a': ['1', '2']}), """((NOT "a" IS NULL AND "a" IN ('1', '2')))""")
        self.assertEqual(Select.where_attributes({'a': ['1', False]}), """((("a" IN ('1') OR "a" IS NULL)))""")
        self.assertEqual(Select.where_attributes({'a': '1', 'b': '2'}), """((NOT "a" IS NULL AND "a" = '1' AND NOT "b" IS NULL AND "b" = '2'))""")

        self.assertEqual(Select.where_tags({'a': '1'}), """((NOT NOT tags?'a' AND tags->'a' = '1'))""")
        self.assertEqual(Select.where_tags({'a': None}), """((NOT NOT tags?'a'))""")

        self.assertEqual(Select.where_attributes([{'a': '1'}, {'b': '2'}]), """((NOT "a" IS NULL AND "a" = '1') OR (NOT "b" IS NULL AND "b" = '2'))""")
