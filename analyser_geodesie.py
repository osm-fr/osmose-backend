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

sqlbase = """
DROP TABLE IF EXISTS kw_tmp;
SELECT      DISTINCT ON (g.way)
            g.osm_id,
            astext(st_transform(g.way, 4020)) AS way,
            substring(g.description from '#\"%%#\" -%%' for '#') AS desc
FROM        %s_point AS g
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
                    ) AS k(kw)
                    ON g.man_made='survey_point'
                        AND g.description ILIKE '%%' || k.kw || '%%'
                LEFT OUTER JOIN %s_polygon AS p
                    ON ST_Intersects(g.way, p.way)
                        AND p.building IS NOT NULL
WHERE       p.osm_id IS NULL
;
"""

###########################################################################

def analyser(config, logger = None):

    apiconn = OsmGis.OsmGis(config.dbs, config.dbp)

    ## result file
    
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    
    outxml.startElement("class", {"id":"1", "item":"7010"})
    outxml.Element("classtext", {"lang":"fr", "title":"Repère géodésique sans bâtit"})
    outxml.Element("classtext", {"lang":"en", "title":"Geodesic mark without building"})
    outxml.endElement("class")
    
    ## sql querry
    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    giscurs.execute(sqlbase % (config.dbp, config.dbp))

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
