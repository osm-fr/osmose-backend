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
import time
import string
from modules import OsmSax
from modules import OsmOsis


class Analyser_Osmosis(Analyser):

    def __init__(self, config, logger = None):
        Analyser.__init__(self, config, logger)
        self.classs = {}
        self.classs_change = {}
        self.explain_sql = False
        self.FixTypeTable = { self.node:"node", self.node_full:"node", self.node_new:"node", self.way:"way", self.way_full:"way", self.relation:"relation", self.relation_full:"relation" }

    def __enter__(self):
        # open database connections + output file
        self.gisconn = psycopg2.connect(self.config.db_string)
        self.giscurs = self.gisconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.apiconn = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema)

        self.outxml = OsmSax.OsmSaxWriter(open(self.config.dst, "w"), "UTF-8")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections + output file
        self.giscurs.close()
        self.gisconn.close()
        self.apiconn.close()

        self.outxml._out.close()


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

        self.giscurs.execute("SET search_path TO %s,public;" % self.config.db_schema)

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
        self.outxml.endElement("analysers")



    def dump_delete(self, tt = ["node", "way", "relation"]):
        for t in tt:
            sql = "(SELECT id FROM actions WHERE data_type='%s' AND action='D') UNION (SELECT id FROM touched_%ss)" % (t[0].upper(), t)
            self.giscurs.execute(sql)
            for res in self.giscurs.fetchall():
                self.outxml.Element("delete", {"type": t, "id": str(res[0])})


    def run(self, sql, callback = None):
        if self.explain_sql:
            self.logger.log(sql.strip())
        if self.explain_sql and sql.strip().startswith("SELECT"):
            sql_explain = "EXPLAIN " + sql.split(";")[0]
            self.giscurs.execute(sql_explain)
            for res in self.giscurs.fetchall():
                print res[0]

        self.giscurs.execute(sql)
        if callback:
            self.logger.log(u"generation du xml")
            while True:
                many = self.giscurs.fetchmany(1000)
                if not many:
                    break
                for res in many:
                    try:
                        ret = callback(res)
                        if ret and ret.__class__ == dict:
                            if "subclass" in ret:
                                self.outxml.startElement("error", {"class":str(ret["class"]), "subclass":str(ret["subclass"])})
                            else:
                                self.outxml.startElement("error", {"class":str(ret["class"])})
                            if "self" in ret:
                                res = ret["self"](res)
                            if "data" in ret:
                                for (i, d) in enumerate(ret["data"]):
                                    if d != None:
                                        d(res[i])
                            if "text" in ret:
                                for lang in ret["text"]:
                                    self.outxml.Element("text", {"lang":lang, "value":ret["text"][lang]})
                            if "fix" in ret:
                                self.dumpxmlfix(self.outxml, res, ret, ret["fix"])
                        self.outxml.endElement("error")

                    except:
                        print "res=", res
                        print "ret=", ret
                        raise


    def node(self, res):
        self.outxml.NodeCreate({"id":res, "tag":{}})

    def node_full(self, res):
        self.outxml.NodeCreate(self.apiconn.NodeGet(res))

    def node_new(self, res):
        pass

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

    def dumpxmlfix(self, outxml, res, ret, fixes):
        fixes = self.fixdiff(fixes)
        outxml.startElement("fixes", {})
        for fix in fixes:
            outxml.startElement("fix", {})
            i = 0
            for f in fix:
                if f != None and i < len(ret["data"]) and ret["data"][i] != None and self.FixTypeTable.has_key(ret["data"][i]):
                    type = self.FixTypeTable[ret["data"][i]]
                    outxml.startElement(type, {'id': str(res[i])})
                    for opp, tags in f.items():
                        for k in tags:
                            if opp in '~+':
                                outxml.Element('tag', {'action': self.FixTable[opp], 'k': k, 'v': tags[k]})
                            else:
                                outxml.Element('tag', {'action': self.FixTable[opp], 'k': k})
                    outxml.endElement(type)
                i += 0
            outxml.endElement('fix')
        outxml.endElement('fixes')
