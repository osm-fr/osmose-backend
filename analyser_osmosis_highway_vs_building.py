#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2011                       ##
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

sql10 = """
SELECT
    buildings.id,
    ST_X(ST_Centroid(buildings.linestring)),
    ST_Y(ST_Centroid(buildings.linestring))
FROM
    ways AS buildings,
    ways AS highways
WHERE
    highways.tags ? 'highway' AND
    (
        highways.tags->'highway' = 'primary' OR
        highways.tags->'highway' = 'secondary' OR
        highways.tags->'highway' = 'tertiary'
    ) AND
        buildings.tags ? 'building' AND buildings.tags->'building' != 'no' AND
        NOT buildings.tags ? 'wall' AND
        NOT highways.tags ? 'tunnel' AND
        NOT highways.tags ? 'bridge'
    AND
    ST_Crosses(buildings.linestring, highways.linestring)
    ;
"""

###########################################################################

def analyser(config, logger = None):

    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)

    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"1070"})
    outxml.Element("classtext", {"lang":"fr", "title":"Intersection entre une voie et un bâtiment"})
    outxml.Element("classtext", {"lang":"en", "title":"Way intersecting building"})
    outxml.endElement("class")

    ## querries
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
	outxml.startElement("error", {"class":"1"})
	outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
	outxml.WayCreate(apiconn.WayGet(res[0]))
	outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
