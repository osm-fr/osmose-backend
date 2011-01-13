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

import sys, re, popen2, urllib, time
from pyPgSQL import PgSQL
from modules import OsmSax
from modules import OsmGis

###########################################################################
## some usefull functions

re_points = re.compile("[\(,][^\(,\)]*[\),]")
def get_points(text):
    pts = []
    for r in re_points.findall(text):
        lon, lat = r[1:-1].split(" ")
        pts.append({"lat":lat, "lon":lon})
    return pts
        
###########################################################################

def analyser(config, logger = None):
    
    apiconn = OsmGis.OsmGis(config.dbs, config.dbp)

    ## result file
    
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    
    outxml.startElement("class", {"id":"1", "item":"1060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Croisement de frontières", "menu":"boundary intersect"})
    outxml.Element("classtext", {"lang":"en", "title":"Boundary intersection", "menu":"boundary intersect"})
    outxml.endElement("class")

    ## sql querry

    sql = """
    select ligne1.osm_id, ligne2.osm_id, astext(st_transform(st_intersection(ligne1.way, ligne2.way),4020))
    from %s_roads as ligne1, %s_roads as ligne2
    where st_crosses(ligne1.way,ligne2.way) = 't'
      and ST_touches(ligne1.way,ligne2.way) = 'f'
      and ligne1.boundary='administrative'
      and ligne2.boundary='administrative'
      and ligne1.osm_id > 0
      and ligne2.osm_id > 0
      and ligne1.osm_id > ligne2.osm_id
    ;
    """ % (config.dbp, config.dbp)

    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    giscurs.execute(sql)
    
    ## format results to outxml
    
    while True:
        many = giscurs.fetchmany(1000)
        if not many:
            break
        for res in many:
            outxml.startElement("error", {"class":"1"})
            for loc in get_points(res[2]):
                outxml.Element("location", loc)
            outxml.WayCreate(apiconn.WayGet(res[0]))
            outxml.WayCreate(apiconn.WayGet(res[1]))
            outxml.endElement("error")

    outxml.endElement("analyser")
    outxml._out.close()

    ## update front-end
    #logger.log("update front-end")
    #urllib.urlretrieve(config.updt, "/dev/null")
