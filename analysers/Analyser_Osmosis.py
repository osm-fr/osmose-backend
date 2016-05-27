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

from Analyser import Analyser

import psycopg2
import psycopg2.extras
import psycopg2.extensions
from collections import defaultdict
from modules import OsmOsis


class Analyser_Osmosis(Analyser):

    def __init__(self, config, logger = None):
        Analyser.__init__(self, config, logger)
        self.classs = {}
        self.classs_change = {}
        self.explain_sql = False
        self.FixTypeTable = {
            self.node:"node", self.node_full:"node", self.node_new:"node", self.node_position:"node",
            self.way:"way", self.way_full:"way",
            self.relation:"relation", self.relation_full:"relation",
        }
        self.typeMapping = {'N': self.node_full, 'W': self.way_full, 'R': self.relation_full}

        if hasattr(config, "verbose") and config.verbose:
            self.explain_sql = True

    def __enter__(self):
        Analyser.__enter__(self)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        # open database connections + output file
        self.gisconn = psycopg2.connect(self.config.db_string)
        psycopg2.extras.register_hstore(self.gisconn, unicode=True)
        self.giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.apiconn = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema, dump_sub_elements=False)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections + output file
        self.giscurs.close()
        self.gisconn.close()
        self.apiconn.close()
        Analyser.__exit__(self, exc_type, exc_value, traceback)


    def analyser(self):
        self.init_analyser()
        self.logger.log(u"run osmosis all analyser %s" % self.__class__.__name__)
        self.error_file.analyser()
        self.dump_class(self.classs)
        self.dump_class(self.classs_change)
        self.analyser_osmosis()
        self.analyser_osmosis_all()
        self.error_file.analyser_end()


    def analyser_change(self):
        self.init_analyser()
        if self.classs != {}:
            self.logger.log(u"run osmosis base analyser %s" % self.__class__.__name__)
            self.error_file.analyser()
            self.dump_class(self.classs)
            self.analyser_osmosis()
            self.error_file.analyser_end()
        if self.classs_change != {}:
            self.logger.log(u"run osmosis touched analyser %s" % self.__class__.__name__)
            self.error_file.analyser(change=True)
            self.dump_class(self.classs_change)
            self.dump_delete()
            self.analyser_osmosis_touched()
            self.error_file.analyser_end()


    def init_analyser(self):
        if len(set(self.classs.keys()) & set(self.classs_change.keys())) > 0:
            self.logger.log(u"Warning: duplicate class in %s" % self.__class__.__name__)

        self.giscurs.execute("SET search_path TO %s,public;" % self.config.db_schema)


    def dump_class(self, classs):
        for id_ in classs:
            data = classs[id_]
            self.error_file.classs(
                id_,
                data["item"],
                data.get("level"),
                data.get("tag"),
                data["desc"])


    def analyser_osmosis(self):
        pass

    def analyser_osmosis_all(self):
        pass

    def analyser_osmosis_touched(self):
        pass


    def dump_delete(self, tt = ["node", "way", "relation"]):
        for t in tt:
            sql = "(SELECT id FROM actions WHERE data_type='%s' AND action='D') UNION (SELECT id FROM touched_%ss)" % (t[0].upper(), t)
            self.giscurs.execute(sql)
            for res in self.giscurs.fetchall():
                self.error_file.delete(t, res[0])


    def run0(self, sql, callback = None):
        if self.explain_sql:
            self.logger.log(sql.strip())
        if self.explain_sql and (sql.strip().startswith("SELECT") or sql.strip().startswith("CREATE TABLE")) and not ';' in sql[:-1]:
            sql_explain = "EXPLAIN " + sql.split(";")[0]
            self.giscurs.execute(sql_explain)
            for res in self.giscurs.fetchall():
                self.logger.log(res[0])

        try:
            self.giscurs.execute(sql)
        except:
            self.logger.log(u"sql=%s" % sql)
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
                        print("res=", res)
                        print("ret=", ret)
                        raise

    def run(self, sql, callback = None):
        def callback_package(res):
            ret = callback(res)
            if ret and ret.__class__ == dict:
                if "self" in ret:
                    res = ret["self"](res)
                if "data" in ret:
                    self.geom = defaultdict(list)
                    for (i, d) in enumerate(ret["data"]):
                        if d != None:
                            d(res[i])
                    ret["fixType"] = map(lambda datai: self.FixTypeTable[datai] if datai != None and datai in self.FixTypeTable else None, ret["data"])
                self.error_file.error(
                    ret["class"],
                    ret.get("subclass"),
                    ret.get("text"),
                    res,
                    ret.get("fixType"),
                    ret.get("fix"),
                    self.geom)

        if callback:
            self.logger.log(u"xml generation")
            self.run0(sql, callback_package)
        else:
            self.run0(sql)


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

    def array_full(self, res):
        for type, id in map(lambda r: (r[0], r[1:]), res):
            self.typeMapping[type](int(id))

    def positionAsText(self, res):
        for loc in self.get_points(res):
            self.geom["position"].append(loc)

#    def positionWay(self, res):
#        self.geom["position"].append()

#    def positionRelation(self, res):
#        self.geom["position"].append()


###########################################################################
from Analyser import TestAnalyser

class TestAnalyserOsmosis(TestAnalyser):
    @classmethod
    def teardown_class(cls):
        cls.clean()

    @classmethod
    def load_osm(cls, osm_file, dst, analyser_options=None, skip_db=False):
        import osmose_run
        (conf, analyser_conf) = cls.init_config(osm_file, dst, analyser_options)
        if not skip_db:
            from nose import SkipTest
            try:
                if not osmose_run.check_database(conf, cls.logger):
                    raise SkipTest("database not present")
            except:
                raise SkipTest("database not present")
            osmose_run.init_database(conf, cls.logger)

        # create directory for results
        import os
        dirname = os.path.dirname(dst)
        try:
          os.makedirs(dirname)
        except OSError:
          if os.path.isdir(dirname):
            pass
          else:
            raise

        cls.conf = conf
        cls.xml_res_file = dst

        return analyser_conf

    @classmethod
    def clean(cls):
        # clean database
        import osmose_run
        osmose_run.clean_database(cls.conf, cls.logger, False)

        # clean results file
        import os
        try:
            os.remove(cls.xml_res_file)
        except OSError:
            pass

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis.test.osm",
                                         "tests/out/osmosis.test.xml",
                                         {"test": True,
                                          "addr:city-admin_level": "8,9",
                                          "driving_side": "left",
                                          "proj": 2969})

    def test(self):
        # run all available osmosis analysers, for basic SQL check
        import inspect, os, sys
        sys.path.insert(0, "analysers/")

        for fn in os.listdir("analysers/"):
            if not fn.startswith("analyser_osmosis_") or not fn.endswith(".py"):
                continue
            analyser = __import__(fn[:-3])
            for name, obj in inspect.getmembers(analyser):
                if (inspect.isclass(obj) and obj.__module__ == fn[:-3] and
                    (name.startswith("Analyser") or name.startswith("analyser"))):

                    with obj(self.analyser_conf, self.logger) as analyser_obj:
                        analyser_obj.analyser()

                    self.root_err = self.load_errors()
                    self.check_num_err(min=0, max=5)

    def test_change(self):
        # run all available osmosis analysers, for basic SQL check
        import inspect, os, sys

        cmd  = ["psql"]
        cmd += self.conf.db_psql_args
        cmd += ["-c", "ALTER ROLE %s IN DATABASE %s SET search_path = %s,public;" % (self.conf.db_user, self.conf.db_base, self.conf.db_schema)]
        self.logger.execute_out(cmd)

        for script in self.conf.osmosis_change_init_post_scripts + self.conf.osmosis_change_post_scripts:
            cmd  = ["psql"]
            cmd += self.conf.db_psql_args
            cmd += ["-f", script]
            self.logger.execute_out(cmd)

        sys.path.insert(0, "analysers/")

        for fn in os.listdir("analysers/"):
            if not fn.startswith("analyser_osmosis_") or not fn.endswith(".py"):
                continue
            analyser = __import__(fn[:-3])
            for name, obj in inspect.getmembers(analyser):
                if (inspect.isclass(obj) and obj.__module__ == fn[:-3] and
                    (name.startswith("Analyser") or name.startswith("analyser"))):

                    with obj(self.analyser_conf, self.logger) as analyser_obj:
                        analyser_obj.analyser_change()

                    self.root_err = self.load_errors()
                    self.check_num_err(min=0, max=5)
