#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Vincent Pottier <@.> 2010                                  ##
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

sqlbase = """
DROP TABLE IF EXISTS kw_tmp;
SELECT DISTINCT ON (nodes.geom)
    nodes.id,
    astext(st_transform(nodes.geom, 4020)) AS way,
    substring(nodes.tags -> 'description' from '#"%#" -%' for '#') AS desc
FROM
    nodes
        JOIN (VALUES
            ('bâtiment'),
            ('blockhaus'),
            ('château'),
            ('chapelle'),
            ('cheminée'),
            ('clocher'),
            ('croix'),
            ('église'),
            ('mairie'),
            ('maison'),
            ('phare'),
            ('réservoir'),
            ('silo'),
            ('tour')
        ) AS k(kw) ON
            nodes.tags ? 'man_made' AND
            nodes.tags->'man_made' = 'survey_point' AND
            nodes.tags ? 'description' AND
            position(k.kw in lower(nodes.tags->'description')) > 0 AND
            position('point constaté détruit' in lower(nodes.tags->'description')) = 0
        LEFT OUTER JOIN ways ON
            ways.tags ? 'building' AND
            is_polygon AND
            ST_Within(nodes.geom, ways.linestring)
WHERE
    ways.id IS NULL
;
"""

###########################################################################

def analyser(config, logger = None):

    apiconn = OsmOsis.OsmOsis(config.db_string, config.db_schema)

    ## result file
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})

    outxml.startElement("class", {"id":"1", "item":"7010"})
    outxml.Element("classtext", {"lang":"fr", "title":"Repère géodésique sans bâtiment"})
    outxml.Element("classtext", {"lang":"en", "title":"Geodesic mark without building"})
    outxml.endElement("class")

    ## sql querry
    gisconn = psycopg2.connect(config.db_string)
    giscurs = gisconn.cursor()
    giscurs.execute("SET search_path TO %s,public;" % config.db_schema)
    giscurs.execute(sqlbase)

    ## format results to outxml
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        for loc in get_points(res[1]):
            outxml.Element("location", loc)
        outxml.Element("text", {"lang":"fr", "value":res[2]})
        outxml.Element("text", {"lang":"en", "value":res[2]})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.endElement("error")

    outxml.endElement("analyser")
    outxml._out.close()

    ## close database connections
    giscurs.close()
    gisconn.close()
    del apiconn
