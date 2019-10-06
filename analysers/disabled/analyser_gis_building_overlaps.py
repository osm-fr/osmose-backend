#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

import time
import psycopg2
from modules import OsmSax
from modules import OsmGis

class Analyser_Gis_Building_Overlaps(Analyser):

  def __init__(self, config, logger = None):
    Analyser_Osmosis.__init__(self, config, logger)

  def analyser(self):
    
    apiconn = OsmGis.OsmGis(self.config.db_string, self.config.db_schema)

    ## result file
    
    outxml = OsmSax.OsmSaxWriter(open(self.config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    
    outxml.startElement("class", {"id":"1", "item":"0"})
    outxml.Element("classtext", {"lang":"en", "title":"Building intersection"})
    outxml.endElement("class")

    ## gis connection
    gisconn = psycopg2.connect(self.config.db_string)
    giscurs = gisconn.cursor()
    
    ## sql querries
    sql1 = "CREATE TEMP TABLE %s_building AS SELECT osm_id, way FROM %s_polygon WHERE st_isvalid(way)='t' AND st_issimple(way)='t' AND building='yes';"%(self.config.db_schema,self.config.dbp)
    sql2 = "CREATE INDEX %s_building_idx ON %s_building USING gist(way);"%(self.config.db_schema,self.config.dbp)
    sql3 = "SELECT b1.osm_id AS id1, b2.osm_id AS id2, astext(st_transform(st_pointonsurface(ST_Intersection(b1.way, b2.way)), 4020)) FROM %s_building AS b1, %s_building AS b2 WHERE b1.osm_id>b2.osm_id AND st_intersects(b1.way, b2.way)='t' AND st_area(ST_Intersection(b1.way, b2.way))<>0;"%(self.config.db_schema,self.config.dbp)
    sql4 = "DROP TABLE %s_building;"%(self.config.db_schema)
    
    ## gis querries
    self.logger.log(u"create building table")
    giscurs.execute(sql1)
    self.logger.log(u"create building index")
    giscurs.execute(sql2)
    self.logger.log(u"analyse overlap")
    giscurs.execute(sql3)
        
    ## format results to outxml
    self.logger.log(u"generate xml")
    while True:
        many = giscurs.fetchmany(1000)
        if not many:
            break
        for res in many:
            outxml.startElement("error", {"class":"1"})
            for loc in self.get_points(res[2]):
                outxml.Element("location", loc)
            #outxml.WayCreate(apiconn.WayGet(res[0]))
            #outxml.WayCreate(apiconn.WayGet(res[1]))
            outxml.WayCreate({"id":res[0], "nd":[], "tag":{}})
            outxml.WayCreate({"id":res[1], "nd":[], "tag":{}})
            outxml.endElement("error")
    giscurs.close()

    outxml.endElement("analyser")
    outxml._out.close()

    #self.logger.log(u"delete building table/index")    
    #giscurs.execute(sql4)
