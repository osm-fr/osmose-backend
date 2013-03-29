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
import string
from collections import defaultdict
from modules import OsmSax
from modules import OsmOsis
from modules import OsmoseErrorFile


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

    def __enter__(self):
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        # open database connections + output file
        self.gisconn = psycopg2.connect(self.config.db_string)
        psycopg2.extras.register_hstore(self.gisconn, unicode=True)
        self.giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.apiconn = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema)

        self.error_file = OsmoseErrorFile.ErrorFile(self.config)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections + output file
        self.giscurs.close()
        self.gisconn.close()
        self.apiconn.close()


    def analyser(self):
        self.init_analyser()
        self.logger.log(u"run osmosis all analyser %s" % self.__class__.__name__)
        self.error_file.analyser()
        self.dump_class(self.classs)
        self.dump_class(self.classs_change)
        self.analyser_osmosis()
        self.analyser_osmosis_all()
        self.error_file.analyser_end()
        self.finish_analyser()


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
        self.finish_analyser()


    def init_analyser(self):
        if len(set(self.classs.keys()) & set(self.classs_change.keys())) > 0:
            self.logger.log(u"Warning: duplicate class in %s" % self.__class__.__name__)

        self.giscurs.execute("SET search_path TO %s,public;" % self.config.db_schema)

        self.error_file.begin()


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


    def finish_analyser(self):
        self.error_file.end()



    def dump_delete(self, tt = ["node", "way", "relation"]):
        for t in tt:
            sql = "(SELECT id FROM actions WHERE data_type='%s' AND action='D') UNION (SELECT id FROM touched_%ss)" % (t[0].upper(), t)
            self.giscurs.execute(sql)
            for res in self.giscurs.fetchall():
                self.error_file.delete(t, res[0])


    def run0(self, sql, callback = None):
        if self.explain_sql:
            self.logger.log(sql.strip())
        if self.explain_sql and sql.strip().startswith("SELECT"):
            sql_explain = "EXPLAIN " + sql.split(";")[0]
            self.giscurs.execute(sql_explain)
            for res in self.giscurs.fetchall():
                print res[0]

        self.giscurs.execute(sql)

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
                        print "res=", res
                        print "ret=", ret
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
                    ret["fixType"] = map(lambda datai: self.FixTypeTable[datai] if datai != None and self.FixTypeTable.has_key(datai) else None, ret["data"])
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

    def positionAsText(self, res):
        for loc in self.get_points(res):
            self.geom["position"].append(loc)

#    def positionWay(self, res):
#        self.geom["position"].append()

#    def positionRelation(self, res):
#        self.geom["position"].append()
