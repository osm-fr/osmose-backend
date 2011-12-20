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
from modules import OsmSax
from modules import OsmOsis


class Analyser_Osmosis(Analyser):

    def __init__(self, config, logger = None):
        Analyser.__init__(self, config, logger)
        self.classs = {}

    def analyser(self):
        self.gisconn = psycopg2.connect(self.config.db_string)
        self.giscurs = self.gisconn.cursor()
        self.apiconn = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema)

        ## output headers
        self.outxml = OsmSax.OsmSaxWriter(open(self.config.dst, "w"), "UTF-8")
        self.outxml.startDocument()
        self.outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})

        for id_ in self.classs:
            data = self.classs[id_]
            self.outxml.startElement("class", {"id":str(id_), "item":data["item"]})
            for lang in data["desc"]:
                self.outxml.Element("classtext", {"lang":lang, "title":data["desc"][lang]})
            self.outxml.endElement("class")

        ## querries
        self.giscurs.execute("SET search_path TO %s,public;" % self.config.db_schema)

        self.logger.log(u"run analyser %s" % self.__class__.__name__)
        self.analyser_osmosis()

        self.giscurs.close()

        ## output footers
        self.outxml.endElement("analyser")
        self.outxml._out.close()


    def analyser_osmosis(self):
        pass

    def run(self, sql, callback = None):
        self.giscurs.execute(sql)
        if callback:
            self.logger.log(u"generation du xml")
            for res in self.giscurs.fetchall():
                ret = callback(res)
                if ret:
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
        self.outxml.RelationCreate(self.apiconn.WayGet(res))

    def positionAsText(self, res):
        for loc in self.get_points(res):
            self.outxml.Element("location", loc)

#    def positionWay(self, res):
#        self.outxml.Element("location", )

#    def positionRelation(self, res):
#        self.outxml.Element("location", )
