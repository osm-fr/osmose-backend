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
import psycopg2
from modules import OsmSax
from modules import OsmOsis

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

    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)

    ## result file

    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})

    outxml.startElement("class", {"id":"1", "item":"1050"})
    outxml.Element("classtext", {"lang":"fr", "title":"Rond-point à l'envers", "menu":"rond-point à l'envers"})
    outxml.Element("classtext", {"lang":"en", "title":"Reverse roundabout", "menu":"reverse roundabout"})
    outxml.endElement("class")

    ## sql querry

    sql = """
    SELECT
        id,
        AsText(ST_Transform(ST_Centroid(linestring),4020)) AS center
    FROM
        ways
    WHERE
        tags ? 'junction' AND
        tags->'junction' = 'roundabout' AND
        is_polygon AND
        ST_IsSimple(linestring) AND
        ST_OrderingEquals(linestring, st_forceRHR(linestring))
    ;
    """

    gisconn = psycopg2.connect(config.dbs)
    giscurs = gisconn.cursor()
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql)

    ## format results to outxml

    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        for loc in get_points(res[1]):
            outxml.Element("location", loc)
        #outxml.Element("text", {"lang":"en", "value":get_error_text(res[0])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.endElement("error")

    outxml.endElement("analyser")
    outxml._out.close()
