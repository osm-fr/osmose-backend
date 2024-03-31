#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2011                                      ##
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

from .Analyser import Analyser

import os
import psycopg2
import psycopg2.extensions
import re
from modules import DictCursorUnicode
from collections import defaultdict
from inspect import getframeinfo, stack


class Analyser_Osmosis(Analyser):

    sql_create_highways = """
CREATE UNLOGGED TABLE {0}.highways AS
SELECT
    id,
    nodes,
    tags,
    tags->'highway' AS highway,
    linestring,
    ST_Transform(linestring, {1}) AS linestring_proj,
    is_polygon,
    tags->'highway' LIKE '%_link' AS is_link,
    (tags?'junction' AND tags->'junction' = 'roundabout') AS is_roundabout,
    ((tags->'highway' = 'motorway' AND NOT tags?'oneway') OR (tags?'oneway' AND tags->'oneway' IN ('yes', 'true', '1', '-1'))) AS is_oneway,
    CASE
      WHEN tags?'area' THEN tags->'area' != 'no'
      ELSE (is_polygon AND tags->'highway' = 'pedestrian')
    END AS is_area,
    tags->'highway' IN ('planned', 'proposed', 'construction') AS is_construction,
    CASE tags->'highway'
        WHEN 'motorway' THEN 1
        WHEN 'primary' THEN 1
        WHEN 'trunk' THEN 1
        WHEN 'motorway_link' THEN 2
        WHEN 'primary_link' THEN 2
        WHEN 'trunk_link' THEN 2
        WHEN 'secondary' THEN 2
        WHEN 'secondary_link' THEN 2
        WHEN 'tertiary' THEN 3
        WHEN 'tertiary_link' THEN 3
        WHEN 'unclassified' THEN 4
        WHEN 'unclassified_link' THEN 4
        WHEN 'residential' THEN 4
        WHEN 'residential_link' THEN 4
        WHEN 'living_street' THEN 5
        WHEN 'track' THEN 5
        WHEN 'cycleway' THEN 5
        WHEN 'service' THEN 5
        WHEN 'road' THEN 5
        ELSE NULL
    END AS level
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' NOT IN ('services', 'rest_area', 'razed', 'no') AND
    ST_NPoints(linestring) >= 2
;

CREATE INDEX idx_highways_linestring ON {0}.highways USING gist(linestring);
CREATE INDEX idx_highways_linestring_proj ON {0}.highways USING gist(linestring_proj);
CREATE INDEX idx_highways_id ON {0}.highways(id);
CREATE INDEX idx_highways_highway ON {0}.highways(highway);
ANALYZE {0}.highways;
"""

    sql_create_highway_ends = """
CREATE UNLOGGED TABLE {0}.highway_ends AS
SELECT
    id,
    nodes,
    linestring,
    highway,
    is_link,
    is_roundabout,
    (ends_geom(nodes, linestring)).id AS nid,
    (ends_geom(nodes, linestring)).geom AS geom,
    level
FROM
    highways
WHERE
    NOT is_area AND
    NOT is_construction
;

ANALYZE {0}.highway_ends;
"""

    # Multipolygons table is not complete. It does not contain multipolygons across extract border,
    # (some) invalid ones, and some where ST_BuildArea fails to build the full polygon with all inners
    sql_create_multipolygons = """
DO $$
DECLARE
    mp RECORD;
BEGIN
    DROP TABLE IF EXISTS {0}.multipolygons;
    CREATE UNLOGGED TABLE {0}.multipolygons (
        id bigint,
        tags hstore,
        poly geometry(Geometry, 4326) NOT NULL,
        poly_proj geometry(Geometry, {1}) NOT NULL,
        is_valid boolean NOT NULL
    );

    FOR mp in (
        SELECT
            relations.id,
            relations.tags,
            ST_LineMerge(ST_Collect(ways.linestring)) AS linestrings
        FROM
            relations
            JOIN relation_members ON
                relation_members.relation_id = relations.id AND
                relation_members.member_type = 'W' AND
                relation_members.member_role IN ('outer', 'inner', '')
            LEFT JOIN ways ON
                ways.id = relation_members.member_id
        WHERE
            relations.tags->'type' = 'multipolygon'
        GROUP BY
            relations.id
        HAVING
            -- Ensure all ways are downloaded; may be false at extract borders
            -- If false, calculations like ST_Area would give invalid results
            bool_and(ways.id IS NOT NULL) AND
            -- Avoid dealing with very large multi-polygons
            ST_NPoints(ST_Collect(ways.linestring)) < 100000
    ) LOOP
        BEGIN
            IF ST_BuildArea(mp.linestrings) IS NOT NULL AND NOT ST_IsEmpty(ST_BuildArea(mp.linestrings))
            -- Ensure no linestrings are dropped by ST_BuildArea, which would result in e.g. missing inners (see #2169)
            AND ST_CoveredBy(ST_Points(mp.linestrings), ST_Points(ST_BuildArea(mp.linestrings))) THEN
                WITH
                unary AS (
                    SELECT
                        id, tags,
                        (ST_Dump(poly)).geom AS poly
                    FROM (VALUES (
                        mp.id,
                        mp.tags,
                        ST_BuildArea(mp.linestrings)
                    )) AS t(id, tags, poly)
                ),
                simplified AS (
                    SELECT
                        id, tags,
                        ST_BuildArea(ST_Collect(
                            ST_ExteriorRing(poly),
                            (SELECT ST_Union(ST_MakePolygon(ST_InteriorRingN(poly, n))) FROM generate_series(1, ST_NumInteriorRings(poly)) AS t(n)) -- ST_MakePolygon is needed to union touching inner rings #2169
                        )) AS poly
                    FROM
                        unary
                ),
                multi AS (
                    SELECT
                        id, tags,
                        ST_CollectionHomogenize(ST_Collect(poly)) AS poly
                    FROM
                        simplified
                    GROUP BY
                        id, tags
                )
                INSERT INTO
                    {0}.multipolygons
                SELECT
                    *,
                    ST_Transform(poly, {1}) AS poly_proj,
                    ST_IsValid(poly) AND ST_IsValid(ST_Transform(poly, {1})) AS is_valid -- see #2058 sometimes poly is considered valid but poly_proj not
                FROM
                    multi;
            END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'multipolygon fails: %', mp.id;
        END;
    END LOOP;
END;
$$ LANGUAGE 'plpgsql';

CREATE INDEX idx_multipolygons_poly ON {0}.multipolygons USING GIST(poly);
CREATE INDEX idx_multipolygons_poly_proj ON {0}.multipolygons USING gist(poly_proj);
CREATE INDEX idx_multipolygons_tags ON {0}.multipolygons USING gist (tags);
ANALYZE {0}.multipolygons;
"""

    sql_create_buildings = """
CREATE UNLOGGED TABLE {0}.buildings AS
SELECT
    *,
    CASE WHEN polygon_proj IS NOT NULL AND wall THEN ST_Area(polygon_proj) ELSE NULL END AS area
FROM (
SELECT DISTINCT ON (id)
    id,
    tags,
    linestring,
    CASE WHEN ST_IsValid(linestring) = 't' AND ST_IsSimple(linestring) = 't' AND ST_IsValid(ST_MakePolygon(ST_Transform(linestring, {1}))) THEN ST_MakePolygon(ST_Transform(linestring, {1})) ELSE NULL END AS polygon_proj,
    (NOT tags?'wall' OR tags->'wall' != 'no') AND tags->'building' != 'roof' AS wall,
    tags?'layer' AS layer,
    ST_NPoints(linestring) AS npoints,
    relation_members.relation_id IS NOT NULL AS relation
FROM
    ways
    LEFT JOIN relation_members ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = ways.id
WHERE
    tags != ''::hstore AND
    tags?'building' AND
    tags->'building' != 'no' AND
    is_polygon
) AS t
;

CREATE INDEX idx_buildings_linestring ON {0}.buildings USING GIST(linestring);
CREATE INDEX idx_buildings_linestring_wall ON {0}.buildings USING GIST(linestring) WHERE wall;
CREATE INDEX idx_buildings_polygon_proj ON {0}.buildings USING gist(polygon_proj);
ANALYZE {0}.buildings;
"""

    def __init__(self, config, logger = None):
        Analyser.__init__(self, config, logger)
        self.classs = {}
        self.classs_change = {}
        self.explain_sql = False
        self.typeMapping = {'N': self.node_full, 'W': self.way_full, 'R': self.relation_full}
        self.typeMapping_id_only = {'N': self.node, 'W': self.way, 'R': self.relation}
        self.resume_from_timestamp = None
        self.already_issued_objects = None

        if hasattr(config, "verbose") and config.verbose:
            self.explain_sql = True

    def __enter__(self):
        Analyser.__enter__(self)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        # open database connections + output file
        self.apiconn = self.config.osmosis_manager.osmosis()
        self.gisconn = self.apiconn.conn()
        self.giscurs = self.gisconn.cursor(cursor_factory=DictCursorUnicode.DictCursorUnicode63)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections + output file
        self.config.osmosis_manager.osmosis_close()
        Analyser.__exit__(self, exc_type, exc_value, traceback)


    def timestamp(self):
        return self.apiconn.timestamp()


    def analyser(self):
        self.init_analyser()
        if self.classs != {} or self.classs_change != {}:
            self.logger.log(u"run osmosis all analyser {0}".format(self.__class__.__name__))
            self.error_file.analyser(self.timestamp(), self.analyser_version())
            if hasattr(self, 'requires_tables_common'):
                self.requires_tables_build(self.requires_tables_common)
            if hasattr(self, 'requires_tables_full'):
                self.requires_tables_build(self.requires_tables_full)
            self.dump_class(self.classs)
            self.dump_class(self.classs_change)
            try:
                self.analyser_osmosis_common()
                self.analyser_osmosis_full()
            finally:
                self.error_file.analyser_end()


    def analyser_deferred_clean(self):
        if hasattr(self, 'requires_tables_common'):
            self.requires_tables_clean(self.requires_tables_common)
        if hasattr(self, 'requires_tables_full'):
            self.requires_tables_clean(self.requires_tables_full)


    def analyser_change(self):
        self.init_analyser()
        if self.classs != {}:
            self.logger.log(u"run osmosis base analyser {0}".format(self.__class__.__name__))
            self.error_file.analyser(self.timestamp(), self.analyser_version())
            if hasattr(self, 'requires_tables_common'):
                self.requires_tables_build(self.requires_tables_common)
            self.dump_class(self.classs)
            try:
                self.analyser_osmosis_common()
            finally:
                self.error_file.analyser_end()
        if self.classs_change != {}:
            self.logger.log(u"run osmosis change analyser {0}".format(self.__class__.__name__))
            self.error_file.analyser(self.timestamp(), self.analyser_version(), change=True)
            try:
                if hasattr(self, 'requires_tables_diff'):
                    self.requires_tables_build(self.requires_tables_diff)
                self.dump_class(self.classs_change)
                self.dump_delete()
                self.analyser_osmosis_diff()
            finally:
                self.error_file.analyser_end()


    def analyser_change_deferred_clean(self):
        if self.classs != {}:
            if hasattr(self, 'requires_tables_common'):
                self.requires_tables_clean(self.requires_tables_common)
        if self.classs_change != {}:
            if hasattr(self, 'requires_tables_diff'):
                self.requires_tables_clean(self.requires_tables_diff)


    def analyser_resume(self, timestamp, already_issued_objects):
        if not self.resume_from_timestamp or self.resume_from_timestamp != timestamp:
            self.db_setup_resume_from_timestamp(timestamp)
            self.resume_from_timestamp = timestamp
            self.already_issued_objects = already_issued_objects
        self.analyser_change()


    def analyser_resume_deferred_clean(self):
        self.analyser_change_deferred_clean()


    def requires_tables_build(self, tables):
        for table in tables:
            self.giscurs.execute("SELECT 1 FROM pg_tables WHERE schemaname = '{0}' AND tablename = '{1}'".format(self.config.db_schema.split(',')[0], table))
            if not self.giscurs.fetchone():
                self.logger.log(u"requires table {0}".format(table))
                if table == 'highways':
                    self.giscurs.execute(self.sql_create_highways.format(self.config.db_schema.split(',')[0], self.config.options.get("proj")))
                elif table == 'touched_highways':
                    self.requires_tables_build(["highways"])
                    self.create_view_touched('highways', 'W')
                elif table == 'not_touched_highways':
                    self.requires_tables_build(["highways"])
                    self.create_view_not_touched('highways', 'W')
                elif table == 'highway_ends':
                    self.requires_tables_build(["highways"])
                    self.giscurs.execute(self.sql_create_highway_ends.format(self.config.db_schema.split(',')[0]))
                elif table == 'touched_highway_ends':
                    self.requires_tables_build(["highway_ends"])
                    self.create_view_touched('highway_ends', 'W')
                elif table == 'multipolygons':
                    self.giscurs.execute(self.sql_create_multipolygons.format(self.config.db_schema.split(',')[0], self.config.options.get("proj")))
                elif table == 'touched_multipolygons':
                    self.requires_tables_build(['multipolygons'])
                    self.create_view_touched('multipolygons', 'R')
                elif table == 'buildings':
                    self.giscurs.execute(self.sql_create_buildings.format(self.config.db_schema.split(',')[0], self.config.options.get("proj")))
                elif table == 'touched_buildings':
                    self.requires_tables_build(["buildings"])
                    self.create_view_touched('buildings', 'W')
                elif table == 'not_touched_buildings':
                    self.requires_tables_build(["buildings"])
                    self.create_view_not_touched('buildings', 'W')
                else:
                    raise Exception('Unknown table name {0}'.format(table))
                self.giscurs.execute('COMMIT')
                self.giscurs.execute('BEGIN')


    def requires_tables_clean(self, tables):
        for table in tables:
            self.logger.log(u"requires table clean {0}".format(table))
            self.giscurs.execute('DROP TABLE IF EXISTS {0}.{1} CASCADE'.format(self.config.db_schema.split(',')[0], table))
            self.giscurs.execute('COMMIT')
            self.giscurs.execute('BEGIN')

    def db_setup_resume_from_timestamp(self, timestamp):
        self.giscurs.execute("SELECT tstamp_action FROM metainfo")
        tstamp_action = self.giscurs.fetchone()[0]
        if tstamp_action != timestamp:
            self.logger.log("osmosis resume post scripts")
            osmosis_resume_post_scripts = [ # Scripts to run each time the database is updated
                "/osmosis/ActionFromTimestamp.sql",
                "/osmosis/CreateTouched.sql",
            ]
            for script in osmosis_resume_post_scripts: # self.config.analyser_conf.osmosis_resume_post_scripts:
                self.giscurs.execute(open('./' + script, 'r').read().replace(':timestamp', str(timestamp)))
            self.giscurs.execute('COMMIT')
            self.giscurs.execute('BEGIN')

    def init_analyser(self):
        if len(set(self.classs.keys()) & set(self.classs_change.keys())) > 0:
            self.logger.log(u"Warning: duplicate class in {0}".format(self.__class__.__name__))

        self.giscurs.execute("SET LOCAL statement_timeout = '12h';")
        self.giscurs.execute("SET search_path TO {0},public;".format(self.config.db_schema_path or self.config.db_schema))


    def dump_class(self, classs):
        for id_ in classs:
            data = classs[id_]
            self.error_file.classs(
                id = id_,
                item = data['item'],
                level = data['level'],
                tags = data.get('tags'),
                title = data.get('title'),
                detail = data.get('detail'),
                fix = data.get('fix'),
                trap = data.get('trap'),
                example = data.get('example'),
                source = data.get('source'),
                resource = data.get('resource'),
            )


    def analyser_osmosis_common(self):
        """
        Run check not supporting diff mode.
        """
        pass

    def analyser_osmosis_full(self):
        """
        Run check supporting diff mode. Full data check.
        Alternative method of analyser_osmosis_diff().
        """
        pass

    def analyser_osmosis_diff(self):
        """
        Run check supporting diff mode. Checks only on data changed from last run.
        Alternative method of analyser_osmosis_full().
        """
        pass


    def dump_delete(self):
        if self.already_issued_objects:
            # Resume
            types = {'N': 'node', 'W': 'way', 'R': 'relation'}
            for t, ids in self.already_issued_objects.items():
                if ids:
                    sql = """
-- Touched
SELECT id
FROM touched_{1}s
    JOIN (VALUES ({0})) AS v(id) USING (id)
UNION ALL
-- Deleted
SELECT id
FROM (VALUES ({0})) AS v(id)
    LEFT JOIN {1}s AS l USING(id)
WHERE l.id IS NULL
"""
                    sql = sql.format('),('.join(map(str, ids)), types[t])
                    self.giscurs.execute(sql)
                    for res in self.giscurs.fetchall():
                        self.error_file.delete(types[t], res[0])
        else:
            # Change
            for t in ["node", "way", "relation"]:
                sql = """
SELECT id FROM actions WHERE data_type='{0}' AND action IN ('D', 'C')
UNION ALL
SELECT id FROM touched_{1}s
"""
                sql = sql.format(t[0].upper(), t)
                self.giscurs.execute(sql)
                for res in self.giscurs.fetchall():
                    self.error_file.delete(t, res[0])


    def create_view_touched(self, table, type, id = 'id'):
        """
        @param type in 'N', 'W', 'R'
        """
        sql = """
CREATE OR REPLACE TEMPORARY VIEW touched_{0} AS
SELECT
    {0}.*
FROM
    {0}
    JOIN transitive_touched ON
        transitive_touched.data_type = '{1}' AND
        {0}.{2} = transitive_touched.id
"""
        self.giscurs.execute(sql.format(table, type, id))

    def create_view_not_touched(self, table, type, id = 'id'):
        """
        @param type in 'N', 'W', 'R'
        """
        sql = """
CREATE OR REPLACE TEMPORARY VIEW not_touched_{0} AS
SELECT
    {0}.*
FROM
    {0}
    LEFT JOIN transitive_touched ON
        transitive_touched.data_type = '{1}' AND
        {0}.{2} = transitive_touched.id
WHERE
    transitive_touched.id IS NULL
"""
        self.giscurs.execute(sql.format(table, type, id))

    def run00(self, sql, callback = None):
        if self.explain_sql:
            self.logger.log(sql.strip())
        if self.explain_sql and (sql.strip().startswith("SELECT") or sql.strip().startswith("CREATE UNLOGGED TABLE")) and not ';' in sql[:-1] and " AS " in sql:
            sql_explain = "EXPLAIN " + sql.split(";")[0]
            self.giscurs.execute(sql_explain)
            for res in self.giscurs.fetchall():
                self.logger.log(res[0])

        try:
            self.giscurs.execute(sql)
        except:
            self.logger.err("sql={0}".format(sql))
            raise

        if callback:
            while True:
                many = self.giscurs.fetchmany(1000)
                if not many:
                    break
                for res in many:
                    ret = None
                    try:
                        ret = callback(res)
                    except:
                        self.logger.err("res={0}".format(res))
                        self.logger.err("ret={0}".format(ret))
                        raise

    def run0(self, sql, callback = None):
        caller = getframeinfo(stack()[1][0])
        self.logger.log("{0}:{1} sql".format(os.path.basename(caller.filename), caller.lineno))
        self.run00(sql, callback)

    def run(self, sql, callback = None):
        def callback_package(res):
            ret = callback(res)
            if ret and ret.__class__ == dict:
                if "self" in ret:
                    res = ret["self"](res)
                if "data" in ret:
                    self.geom = defaultdict(list)
                    ret["fixType"] = []
                    for (i, d) in enumerate(ret["data"]):
                        if d is not None:
                            d(res[i])
                            ret["fixType"].append(self._typeFromCallback(d, res[i]))
                            if d in (self.any_full, self.any_id):
                                res[i] = int(res[i][1:])
                self.error_file.error(
                    ret["class"],
                    ret.get("subclass"),
                    ret.get("text"),
                    res,
                    ret.get("fixType"),
                    ret.get("fix"),
                    self.geom)

        caller = getframeinfo(stack()[1][0])
        if callback:
            self.logger.log("{0}:{1} xml generation".format(os.path.basename(caller.filename), caller.lineno))
            self.run00(sql, callback_package)
        else:
            self.logger.log("{0}:{1} sql".format(os.path.basename(caller.filename), caller.lineno))
            self.run00(sql)

    def _typeFromCallback(self, fn, input=None):
        if fn in (self.node, self.node_full, self.node_new, self.node_position):
            return "node"
        if fn in (self.way, self.way_full):
            return "way"
        if fn in (self.relation, self.relation_full):
            return "relation"
        if fn == self.any_full:
            return self._typeFromCallback(self.typeMapping[input[0]])
        if fn == self.any_id:
            return self._typeFromCallback(self.typeMapping_id_only[input[0]])

    def node(self, res):
        self.geom["node"].append({"id":res, "tag":{}})

    def node_full(self, res):
        self.geom["node"].append(self.apiconn.NodeGet(res))

    def node_position(self, res):
        node = self.apiconn.NodeGet(res)
        if node:
            self.geom["position"].append({'lat': str(node['lat']), 'lon': str(node['lon'])})

    def node_new(self, res):
        pass

    def way(self, res):
        self.geom["way"].append({"id":res, "nd":[], "tag":{}})

    def way_full(self, res):
        self.geom["way"].append(self.apiconn.WayGet(res))

    def relation(self, res):
        self.geom["relation"].append({"id":res, "member":[], "tag":{}})

    def relation_full(self, res):
        self.geom["relation"].append(self.apiconn.RelationGet(res))

    def any_full(self, res):
        self.typeMapping[res[0]](int(res[1:]))

    def any_id(self, res):
        self.typeMapping_id_only[res[0]](int(res[1:]))

    def array_full(self, res):
        for type, id in map(lambda r: (r[0], r[1:]), res):
            self.typeMapping[type](int(id))

    def array_id(self, res):
        for type, id in map(lambda r: (r[0], r[1:]), res):
            self.typeMapping_id_only[type](int(id))

    re_points = re.compile(r"[\(,][^\(,\)]*[\),]")

    def get_points(self, text):
        pts = []
        for r in self.re_points.findall(text):
            lon, lat = r[1:-1].split(" ")
            pts.append({"lat":lat, "lon":lon})
        return pts

    def positionAsText(self, res):
        if res is None:
            self.logger.warn("NULL location provided")
            return []
        points = self.get_points(res)
        if points == []:
            self.logger.err("Invalid location provided")
            return []
        for loc in points:
            self.geom["position"].append(loc)

#    def positionWay(self, res):
#        self.geom["position"].append()

#    def positionRelation(self, res):
#        self.geom["position"].append()


###########################################################################
from .Analyser import TestAnalyser
from modules import IssuesFileOsmose


class TestAnalyserOsmosis(TestAnalyser):
    @classmethod
    def teardown_class(cls):
        cls.clean()

    @classmethod
    def load_osm(cls, osm_file, dst, analyser_options=None, skip_db=False):
        import modules.OsmOsisManager
        (conf, analyser_conf) = cls.init_config(osm_file, dst, analyser_options)
        class c_options:
            import_tool = "osmosis"
        options = c_options()

        if not skip_db:
            import pytest
            osmosis_manager = modules.OsmOsisManager.OsmOsisManager(conf, conf.db_host, conf.db_user, conf.db_password, conf.db_base, conf.db_schema or conf.country, conf.db_persistent, cls.logger)
            if not osmosis_manager.check_database():
                pytest.skip("database not present")
            osmosis_manager.init_database(conf, options)

        # create directory for results
        import os
        for i in ["normal", "diff_empty", "diff_full"]:
            dirname = os.path.join(os.path.dirname(dst), i)
            try:
                os.makedirs(dirname)
            except OSError:
                if os.path.isdir(dirname):
                    pass
                else:
                    raise

        cls.conf = conf
        cls.xml_res_file = dst

        analyser_conf.osmosis_manager = osmosis_manager
        analyser_conf.db_schema = conf.db_schema
        analyser_conf.db_schema_path = conf.db_schema_path
        return analyser_conf

    @classmethod
    def clean(cls):
        # clean database
        import modules.OsmOsisManager
        osmosis_manager = modules.OsmOsisManager.OsmOsisManager(cls.conf, cls.conf.db_host, cls.conf.db_user, cls.conf.db_password, cls.conf.db_base, cls.conf.db_schema or cls.conf.country, cls.conf.db_persistent, cls.logger)
        osmosis_manager.clean_database(cls.conf, False)

        # clean results file
        import os
        try:
            os.remove(cls.xml_res_file)
        except OSError:
            pass

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

        import modules.OsmOsisManager
        cls.conf.osmosis_manager = modules.OsmOsisManager.OsmOsisManager(cls.conf, cls.conf.db_host, cls.conf.db_user, cls.conf.db_password, cls.conf.db_base, cls.conf.db_schema or cls.conf.country, cls.conf.db_persistent, cls.logger)

    def test(self):
        # run all available osmosis analysers, for basic SQL check
        import importlib
        import inspect
        import os

        for fn in os.listdir("analysers/"):
            if not fn.startswith("analyser_osmosis_") or not fn.endswith(".py"):
                continue
            analyser = importlib.import_module("analysers." + fn[:-3], package=".")
            for name, obj in inspect.getmembers(analyser):
                if (inspect.isclass(obj) and obj.__module__ == ("analysers." + fn[:-3]) and
                    (name.startswith("Analyser") or name.startswith("analyser"))):

                    self.xml_res_file = self.default_xml_res_path + "normal/{0}.xml".format(name)
                    self.analyser_conf.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)

                    with obj(self.analyser_conf, self.logger) as analyser_obj:
                        analyser_obj.analyser()

                    self.root_err = self.load_errors()
                    self.check_num_err(min=0, max=5)

    def test_change_empty(self):
        # run all available osmosis analysers, for basic SQL check
        import importlib
        import inspect
        import os

        self.conf.osmosis_manager.set_pgsql_schema()

        for script in self.conf.osmosis_change_init_post_scripts:
            self.conf.osmosis_manager.psql_f(script)

        self.conf.osmosis_manager.psql_c("TRUNCATE TABLE actions")

        for script in self.conf.osmosis_change_post_scripts:
            self.conf.osmosis_manager.psql_f(script)

        for fn in os.listdir("analysers/"):
            if not fn.startswith("analyser_osmosis_") or not fn.endswith(".py"):
                continue
            analyser = importlib.import_module("analysers." + fn[:-3], package=".")
            for name, obj in inspect.getmembers(analyser):
                if (inspect.isclass(obj) and obj.__module__ == ("analysers." + fn[:-3]) and
                    (name.startswith("Analyser") or name.startswith("analyser"))):

                    self.xml_res_file = self.default_xml_res_path + "diff_empty/{0}.xml".format(name)
                    self.analyser_conf.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)

                    with obj(self.analyser_conf, self.logger) as analyser_obj:
                        analyser_obj.analyser_change()

                    self.root_err = self.load_errors()
                    self.check_num_err(min=0, max=5)

    def test_change_full(self):
        # run all available osmosis analysers, after marking all elements as new
        import importlib
        import inspect
        import os

        self.conf.osmosis_manager.set_pgsql_schema()

        for script in self.conf.osmosis_change_init_post_scripts:
            self.conf.osmosis_manager.psql_f(script)

        self.conf.osmosis_manager.psql_c("TRUNCATE TABLE actions;"
                                         "INSERT INTO actions (SELECT 'R', 'C', id FROM relations);"
                                         "INSERT INTO actions (SELECT 'W', 'C', id FROM ways);"
                                         "INSERT INTO actions (SELECT 'N', 'C', id FROM nodes);")

        for script in self.conf.osmosis_change_post_scripts:
            self.conf.osmosis_manager.psql_f(script)

        for fn in os.listdir("analysers/"):
            if not fn.startswith("analyser_osmosis_") or not fn.endswith(".py"):
                continue
            analyser = importlib.import_module("analysers." + fn[:-3], package=".")
            for name, obj in inspect.getmembers(analyser):
                if (inspect.isclass(obj) and obj.__module__ == ("analysers." + fn[:-3]) and
                    (name.startswith("Analyser") or name.startswith("analyser"))):

                    self.xml_res_file = self.default_xml_res_path + "diff_full/{0}.xml".format(name)
                    self.analyser_conf.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)

                    with obj(self.analyser_conf, self.logger) as analyser_obj:
                        analyser_obj.analyser_change()

                    self.root_err = self.load_errors()
                    self.check_num_err(min=0, max=5)

    def test_cmp_normal_change(self):
        # compare results between normal and change_full
        # must be run after both test() and test_change_full()
        import importlib
        import inspect
        import os

        for fn in os.listdir("analysers/"):
            if not fn.startswith("analyser_osmosis_") or not fn.endswith(".py"):
                continue
            analyser = importlib.import_module("analysers." + fn[:-3], package=".")
            for name, obj in inspect.getmembers(analyser):
                if (inspect.isclass(obj) and obj.__module__ == ("analysers." + fn[:-3]) and
                    (name.startswith("Analyser") or name.startswith("analyser"))):

                    normal_xml = (self.default_xml_res_path +
                                "normal/{0}.xml".format(name))
                    change_xml = (self.default_xml_res_path +
                                "diff_full/{0}.xml".format(name))

                    print(normal_xml, change_xml)
                    self.compare_results(normal_xml, change_xml, convert_checked_to_normal=True)
