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

import sys, re, popen2, urllib, time
import psycopg2
from modules import OsmSax
from modules import OsmGis

class Analyser_Gis_Roundabout(Analyser):

  def __init__(self, config, logger = None):
    Analyser_Osmosis.__init__(self, config, logger)

  def analyser(self):

    apiconn = OsmGis.OsmGis(self.config.db_string, self.config.db_schema)

    ## result file
    
    outxml = OsmSax.OsmSaxWriter(open(self.config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    
    outxml.startElement("class", {"id":"1", "item":"1050"})
    outxml.Element("classtext", {"lang":"fr", "title":"Rond-point à l'envers", "menu":"rond-point à l'envers"})
    outxml.Element("classtext", {"lang":"en", "title":"Reverse roundabout", "menu":"reverse roundabout"})
    outxml.endElement("class")
    
    ## sql querry
    
    sql = """
    select osm_id, astext(st_transform(st_centroid(way),4020)) as center from %s_line
    where junction = 'roundabout'
      and (st_isclosed(way) and st_isring(way))
      and ((st_azimuth(st_centroid(way),ST_PointN(way,1))-st_azimuth(st_centroid(way),ST_PointN(way,2)))::numeric)%%((pi()*2)::numeric) between pi() and pi()*2
    ;
    """ % self.config.db_schema

    gisconn = psycopg2.connect(self.config.db_string)
    giscurs = gisconn.cursor()
    giscurs.execute(sql)

    ## format results to outxml

    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        for loc in self.get_points(res[1]):
            outxml.Element("location", loc)
        #outxml.Element("text", {"lang":"en", "value":get_error_text(res[0])})
        if res[0] < 0:
            outxml.RelationCreate(apiconn.RelationGet(-res[0]))
        else:
            outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.endElement("error")

    outxml.endElement("analyser")
    outxml._out.close()

    ## update front-end
    #self.logger.log("update front-end")
    #urllib.urlretrieve(self.config.updt, "/dev/null")
