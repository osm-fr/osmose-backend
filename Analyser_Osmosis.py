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
import time
import string
from modules import OsmSax
from modules import OsmOsis


class Analyser_Osmosis(Analyser):

    def __init__(self, config, logger = None):
        Analyser.__init__(self, config, logger)
        self.classs = {}
        self.classs_change = {}
        self.explain_sql = True

    def analyser(self):
        self.init_analyser()
        self.logger.log(u"run osmosis all analyser %s" % self.__class__.__name__)
        self.pre_analyser("analyser")
        self.dump_class(self.classs)
        self.dump_class(self.classs_change)
        self.analyser_osmosis()
        self.analyser_osmosis_all()
        self.post_analyser("analyser")
        self.finish_analyser()


    def analyser_change(self):
        self.init_analyser()
        if self.classs != {}:
            self.logger.log(u"run osmosis base analyser %s" % self.__class__.__name__)
            self.pre_analyser("analyser")
            self.dump_class(self.classs)
            self.analyser_osmosis()
            self.post_analyser("analyser")
        if self.classs_change != {}:
            self.logger.log(u"run osmosis touched analyser %s" % self.__class__.__name__)
            self.pre_analyser("analyserChange")
            self.dump_class(self.classs_change)
            self.dump_delete()
            self.analyser_osmosis_touched()
            self.post_analyser("analyserChange")
        self.finish_analyser()


    def init_analyser(self):
        if len(set(self.classs.keys()) & set(self.classs_change.keys())) > 0:
            self.logger.log(u"Warning: duplicate class in %s" % self.__class__.__name__)

        self.gisconn = psycopg2.connect(self.config.db_string)
        self.giscurs = self.gisconn.cursor()
        self.giscurs.execute("SET search_path TO public,%s,public;" % self.config.db_schema)

        self.apiconn = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema)

        self.outxml = OsmSax.OsmSaxWriter(open(self.config.dst, "w"), "UTF-8")
        self.outxml.startDocument()
        self.outxml.startElement("analysers", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})


    def pre_analyser(self, mode):
        self.outxml.startElement(mode, {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})


    def dump_class(self, classs):
        for id_ in classs:
            data = classs[id_]
            self.outxml.startElement("class", {"id":str(id_), "item":data["item"]})
            for lang in data["desc"]:
                self.outxml.Element("classtext", {"lang":lang, "title":data["desc"][lang]})
            self.outxml.endElement("class")


    def analyser_osmosis(self):
        pass

    def analyser_osmosis_all(self):
        pass

    def analyser_osmosis_touched(self):
        pass


    def post_analyser(self, mode):
        self.outxml.endElement(mode)


    def finish_analyser(self):
        self.giscurs.close()

        self.outxml.endElement("analysers")
        self.outxml._out.close()


    def dump_delete(self, tt = ["node", "way", "relation"]):
        for t in tt:
            sql = "(SELECT id FROM actions WHERE data_type='%s' AND action='D') UNION (SELECT id FROM touched_%ss)" % (t[0].upper(), t)
            self.giscurs.execute(sql)
            for res in self.giscurs.fetchall():
                self.outxml.Element("delete", {"type": t, "id": str(res[0])})


    def run(self, sql, callback = None):
        print sql.strip()
        if self.explain_sql and sql.strip().startswith("SELECT"):
            sql_explain = "EXPLAIN " + sql.split(";")[0]
            self.giscurs.execute(sql_explain)
            for res in self.giscurs.fetchall():
                print res[0]

        self.giscurs.execute(sql)
        if callback:
            self.logger.log(u"generation du xml")
            for res in self.giscurs.fetchall():
                ret = callback(res)
                if ret and ret.__class__ == dict:
                    if "subclass" in ret:
                        self.outxml.startElement("error", {"class":str(ret["class"]), "subclass":str(ret["subclass"])})
                    else:
                        self.outxml.startElement("error", {"class":str(ret["class"])})
                    i = 0
                    if "data" in ret:
                        for d in ret["data"]:
                            if d != None:
                                d(res[i])
                            i += 1
                    if "text" in ret:
                        for lang in ret["text"]:
                            self.outxml.Element("text", {"lang":lang, "value":ret["text"][lang]})
                    if "self" in ret:
                        ret["self"](res)
                self.outxml.endElement("error")


    def node(self, res):
        self.outxml.NodeCreate({"id":res, "tag":{}})

    def node_full(self, res):
        self.outxml.NodeCreate(self.apiconn.NodeGet(res))

    def way(self, res):
        self.outxml.WayCreate({"id":res, "nd":[], "tag":{}})

    def way_full(self, res):
        self.outxml.WayCreate(self.apiconn.WayGet(res))

    def relation(self, res):
        self.outxml.RelationCreate({"id":res, "member":[], "tag":{}})

    def relation_full(self, res):
        self.outxml.RelationCreate(self.apiconn.RelationGet(res))

    def positionAsText(self, res):
        for loc in self.get_points(res):
            self.outxml.Element("location", loc)

#    def positionWay(self, res):
#        self.outxml.Element("location", )

#    def positionRelation(self, res):
#        self.outxml.Element("location", )
