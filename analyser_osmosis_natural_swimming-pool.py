#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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
    ST_X(ST_Centroid(geom)),
    ST_Y(ST_Centroid(geom))
FROM
(
SELECT
    (ST_Dump(ST_Union(ST_Buffer(poly,5e-2)))).geom AS geom
FROM
(
SELECT
    ways.linestring AS poly
FROM
    ways
WHERE
    ways.tags?'natural' AND ways.tags->'natural' = 'water' AND
    ways.tags?'source' AND ways.tags->'source' ILIKE '%cadastre%' AND
--    array_length(ways.nodes,1) <= 7 AND array_length(ways.nodes,1) > 4 AND
    array_length(ways.nodes,1) = 5 AND
--    is_polygon AND
    ST_Area(ways.linestring) < 7e-9
) AS water
) AS buffer
WHERE
    ST_Area(geom) > 1e-2
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
    outxml.startElement("class", {"id":"1", "item":"3080"})
    outxml.Element("classtext", {"lang":"fr", "title":"Piscines avec natural=water"})
    outxml.Element("classtext", {"lang":"en", "title":"Swimming-pools as natural=water"})
    outxml.endElement("class")

    ## querries
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        outxml.Element("location", {"lat":str(res[1]), "lon":str(res[0])})
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
