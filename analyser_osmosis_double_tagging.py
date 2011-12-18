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
import psycopg2
from modules import OsmSax
from modules import OsmOsis

###########################################################################

sql10 = """
SELECT
    ways.id,
    nodes.id,
    ST_X(nodes.geom),
    ST_Y(nodes.geom)
FROM
    ways
    JOIN nodes ON
        ways.linestring && nodes.geom
WHERE
    ways.tags?'name' AND
    nodes.tags?'name' AND
    ways.tags->'name' = nodes.tags->'name'
    AND
    (
        (
            ways.tags?'amenity' AND
            nodes.tags?'amenity' AND
            ways.tags->'amenity' = nodes.tags->'amenity'
        ) OR
        (
            ways.tags?'leisure' AND
            nodes.tags?'leisure' AND
            ways.tags->'leisure' = nodes.tags->'leisure'
        )
    )
;
"""

###########################################################################

def analyser(config, logger = None):

    gisconn = psycopg2.connect(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)

    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"4080"})
    outxml.Element("classtext", {"lang":"fr", "title":"Objet marqué comme way et comme nœud"})
    outxml.Element("classtext", {"lang":"en", "title":"Object tagged as way and as node"})
    outxml.endElement("class")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.NodeCreate(apiconn.NodeGet(res[1]))
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()

    ## close database connections
    giscurs.close()
    gisconn.close()
    del apiconn
