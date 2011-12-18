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
    ST_X(ST_Centroid(geom)),
    ST_Y(ST_Centroid(geom))
FROM
(
    SELECT
        (ST_Dump(ST_Union(ST_Buffer(geom, 0.001, 'quad_segs=2')))).geom AS geom
    FROM
        nodes
        LEFT JOIN way_nodes ON
            nodes.id = way_nodes.node_id
    WHERE
        way_nodes.node_id IS NULL AND
        array_length(akeys(tags),1) = 0 AND
        version = 1
) AS t
WHERE
    ST_Area(geom) > 1e-5
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
    outxml.startElement("class", {"id":"1", "item":"1080"})
    outxml.Element("classtext", {"lang":"fr", "title":"Groupe de nœuds orphelins"})
    outxml.Element("classtext", {"lang":"en", "title":"Orphan nodes cluster"})
    outxml.endElement("class")

    ## querries
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1", "subclass":str(abs(int(hash(res[0]*res[1]))))})
        outxml.Element("location", {"lat":str(res[1]), "lon":str(res[0])})
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()

    ## close database connections
    giscurs.close()
    gisconn.close()
    del apiconn
