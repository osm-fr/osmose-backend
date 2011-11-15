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

sql1 = """
CREATE TEMP TABLE buildings AS
SELECT
    ways.id,
    ways.linestring,
    ways.bbox
FROM
    ways
    LEFT JOIN relation_members ON
        relation_members.member_id = ways.id AND
        relation_members.member_type = 'W'
WHERE
    relation_members.member_id IS NULL AND
    ways.tags ? 'building' AND ways.tags->'building' != 'no' AND
    is_polygon AND
    ST_IsValid(ways.linestring) = 't' AND
    ST_IsSimple(ways.linestring) = 't'
;
"""

sql2 = """
CREATE INDEX buildings_bbox_idx ON buildings USING gist(bbox);
"""

sql3 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    AsText(ST_Transform(ST_Centroid(ST_Intersection(b1.linestring, b2.linestring)), 4020))
FROM
    buildings AS b1,
    buildings AS b2
WHERE
    b1.id > b2.id AND
    b1.bbox && b2.bbox AND
    ST_Intersects(b1.linestring, b2.linestring) = 't' AND
    ST_Area(ST_Intersection(b1.linestring, b2.linestring)) <> 0
;
"""

def analyser(config, logger = None):

    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)

    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"0"})
    outxml.Element("classtext", {"lang":"fr", "title":"Intersections de bâtiments"})
    outxml.Element("classtext", {"lang":"en", "title":"Building intersection"})
    outxml.endElement("class")

    ## querries        
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)

    ## gis querries
    giscurs.execute(sql1)
    giscurs.execute(sql2)
    logger.log(u"analyse overlap")
    giscurs.execute(sql3)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        outxml.Element("location", get_points(res[2])[0])
        outxml.WayCreate({"id":res[0], "nd":[], "tag":{}})
        outxml.WayCreate({"id":res[1], "nd":[], "tag":{}})
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
