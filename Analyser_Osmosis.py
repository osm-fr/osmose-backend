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

import re
import psycopg2
from modules import OsmSax
from modules import OsmOsis


class Analyser_Osmosis(Analyser):

    def __init__(self, father):
        self.father = father
        self.classs = {}


    def analyser(self, config, logger = None):
        gisconn = psycopg2.connect(config.db_string)
        giscurs = gisconn.cursor()
        apiconn = OsmOsis.OsmOsis(config.db_string, config.db_schema)

        ## output headers
        self.outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
        self.outxml.startDocument()
        self.outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})

        for (id_, data) in self.classs:
            self.outxml.startElement("class", {"id":str(id_), "item":data["item"]})
            for (lang, title) in data["desc"]:
                self.outxml.Element("classtext", {"lang":lang, "title":title})
            self.outxml.endElement("class")

        ## querries
        giscurs.execute("SET search_path TO %s,public;" % config.db_schema)

        logger.log(u"run analyser %s" % __class__.__name__)
        self.analyser_osmosis(config, logger, self.outxml)

        ## output footers
        self.outxml.endElement("analyser")
        self.outxml._out.close()


    re_points = re.compile("[\(,][^\(,\)]*[\),]")

    @staticmethod
    def get_points(text):
        pts = []
        for r in re_points.findall(text):
            lon, lat = r[1:-1].split(" ")
            pts.append({"lat":lat, "lon":lon})
        return pts

    def analyser_osmosis(self, config, logger, giscurs):
        pass

    def run(self, sql, callback = None):
        giscurs.execute(sql)
        if callback:
            logger.log(u"generation du xml")
            for res in giscurs.fetchall():
                ret = callback(res)
                if ret["subclass"]:
                    self.outxml.startElement("error", {"class":str(ret["class"]), "subclass":str(ret["subclass"])})
                else:
                    self.outxml.startElement("error", {"class":str(ret["class"])})
                i = 0
                for d in ret["data"]:
                    d(res[i])
                    i += 1
                for (lang, value) in ret["text"]:
                    outxml.Element("text", {"lang":lang, "value":value})
                self.outxml.endElement("error")

    def node(res):
        self.outxml.NodeCreate({"id":res, "tag":{}})

    def node_full(res):
        self.outxml.NodeCreate(apiconn.NodeGet(res))

    def way(res):
        self.outxml.WayCreate({"id":res, "nd":[], "tag":{}})

    def way_full(res):
        self.outxml.WayCreate(apiconn.WayGet(res))

#    def relation(res):
#        self.outxml.RelationCreate({"id":res, "nd":[], "tag":{}})

    def relation_full(res):
        self.outxml.RelationCreate(apiconn.WayGet(res))

    def positionAsText(res):
        for loc in get_points(res):
            self.outxml.Element("location", loc)

#    def positionWay(res):
#        self.outxml.Element("location", )

#    def positionRelation(res):
#        self.outxml.Element("location", )
