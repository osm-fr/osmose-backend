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
CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql;

DROP VIEW IF EXISTS links_ends CASCADE;
CREATE VIEW links_ends AS
SELECT
    id,
    ends(nodes) AS nid,
    tags->'highway' AS highway_link,
    linestring
FROM
    ways
WHERE
    tags?'highway' AND
    tags->'highway' LIKE '%_link'
;

SELECT
    bad.id,
    ST_X(ST_Centroid(bad.linestring)),
    ST_X(ST_Centroid(bad.linestring))
FROM
    (
    SELECT
        links_ends.id,
        links_ends.nid,
        links_ends.linestring
    FROM
        links_ends
        JOIN way_nodes ON
            way_nodes.node_id = links_ends.nid
        JOIN ways AS w1 ON
            links_ends.id != w1.id AND
            way_nodes.way_id = w1.id AND
            w1.tags?'highway' AND
            NOT (
                w1.tags->'highway' = links_ends.highway_link OR
                w1.tags->'highway' || '_link' = links_ends.highway_link
            )
    GROUP BY
        links_ends.id,
        links_ends.nid,
        links_ends.linestring
    ) AS bad
    LEFT JOIN
    (
    SELECT
        links_ends.id,
        links_ends.nid,
        links_ends.linestring
    FROM
        links_ends
        JOIN way_nodes ON
            way_nodes.node_id = links_ends.nid
        JOIN ways AS w1 ON
            links_ends.id != w1.id AND
            way_nodes.way_id = w1.id AND
            w1.tags?'highway' AND
            (
                w1.tags->'highway' = links_ends.highway_link OR
                w1.tags->'highway' || '_link' = links_ends.highway_link
            )
    GROUP BY
        links_ends.id,
        links_ends.nid,
        links_ends.linestring
    ) AS good
    ON
        bad.id = good.id AND
        bad.nid = good.nid
WHERE
    good.id IS NULL
GROUP BY
    bad.id,
    bad.linestring
HAVING
    COUNT(*) > 1
;
"""

###########################################################################

re_points = re.compile("[\(,][^\(,\)]*[\),]")
def get_points(text):
    pts = []
    for r in re_points.findall(text):
        lon, lat = r[1:-1].split(" ")
        pts.append({"lat":lat, "lon":lon})
    return pts


def analyser(config, logger = None):

    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)

    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"1100"})
    outxml.Element("classtext", {"lang":"fr", "title":"Highway *_link non corespondant"})
    outxml.Element("classtext", {"lang":"en", "title":"Bad *_link highway"})
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
