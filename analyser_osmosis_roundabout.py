#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2010                       ##
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
    id,
    x,
    y
FROM
(
    SELECT
        ways.id,
        x,
        y
    FROM
    (
        SELECT
            ways.id,
            st_x(st_centroid(linestring)) AS x,
            st_y(st_centroid(linestring)) AS y
        FROM
            ways
        WHERE
            -- tags
            ways.tags?'highway' AND
            ways.tags->'highway' IN ('primary','secondary','tertiary','residential') AND -- c'est une route pour voiture
            (NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout') AND
            NOT ways.tags?'area' AND
            (NOT ways.tags?'name' OR ways.tags->'name' LIKE 'Rond%') AND -- pas de nom ou commence par 'Rond'
            -- geometry
            ways.is_polygon AND -- C'est un polygone
            ST_NPoints(linestring) < 24 AND
            ST_MaxDistance(st_Transform(linestring,2154),st_Transform(linestring,2154)) < 70 AND -- Le way fait moins de 80m de diametre
            ST_Area(linestring)/ST_Area(ST_MinimumBoundingCircle(linestring)) > 0.6 -- 90% de rp recouvrent plus 60% du cercle englobant
    ) AS ways
        JOIN way_nodes ON
            way_nodes.way_id = ways.id
        JOIN way_nodes AS o ON
            way_nodes.node_id = o.node_id AND
            o.way_id != way_nodes.way_id
    GROUP BY
        ways.id,
        way_nodes.node_id,
        x,
        y
    HAVING
        COUNT(*) >= 2 -- selection des noueds avec ou moins deux voies
) AS t0
GROUP BY
    id,
    x,
    y
HAVING
    COUNT(*) >= 2 -- selection des rond-points connecté a au moins deux voies
ORDER BY
    id
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
    outxml.startElement("class", {"id":"1", "item":"2010"})
    outxml.Element("classtext", {"lang":"fr", "title":"Manque junction=roundabout"})
    outxml.Element("classtext", {"lang":"en", "title":"Missing junction=roundabout"})
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
