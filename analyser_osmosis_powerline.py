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
    nodes.id,
    ST_X(nodes.geom),
    ST_Y(nodes.geom)
FROM
    nodes
    LEFT JOIN way_nodes ON
        nodes.id = way_nodes.node_id
    LEFT JOIN ways ON
        way_nodes.way_id = ways.id AND
        ways.tags?'power' AND
        ways.tags->'power' IN ('line', 'minor_line', 'cable')
WHERE
    nodes.tags?'power' AND
    (nodes.tags->'power' = 'pole' OR nodes.tags->'power' = 'tower') AND
    ways.id IS NULL
;
"""

sql20 = """
CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql;

DROP VIEW IF EXISTS line_ends CASCADE;
CREATE VIEW line_ends AS
SELECT
    ends(ways.nodes) AS id
FROM
    ways
WHERE
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line', 'cable')
;

DROP VIEW IF EXISTS line_ends1 CASCADE;
CREATE VIEW line_ends1 AS
SELECT
    line_ends.id
FROM
    line_ends
    JOIN way_nodes ON
        way_nodes.node_id = line_ends.id
    JOIN ways ON
        way_nodes.way_id = ways.id AND
        ways.tags?'power' AND
        ways.tags->'power' IN ('line', 'minor_line', 'cable')
GROUP BY
    line_ends.id
HAVING
    COUNT(*) = 1
;

DROP VIEW IF EXISTS line_terminators CASCADE;
CREATE VIEW line_terminators AS
(
SELECT
    'N' as type,
    id,
    geom
FROM
    nodes
WHERE
    tags?'power' AND
    tags->'power' NOT IN ('pole', 'tower')
)
UNION
(
SELECT
    'W' as type,
    id,
    ST_Centroid(linestring) AS geom
FROM
    ways
WHERE
    tags?'power' AND
    tags->'power' NOT IN ('line', 'minor_line', 'cable')
)
;

SELECT
    nodes.id,
    ST_X(nodes.geom),
    ST_Y(nodes.geom)
FROM
    line_ends1
    JOIN nodes ON
        line_ends1.id = nodes.id
    LEFT JOIN line_terminators ON
        ST_Distance(nodes.geom, line_terminators.geom) < 10e-3
WHERE
    line_terminators.id IS NULL
;
"""

sql30 = """
DROP VIEW IF EXISTS power_line CASCADE;
CREATE VIEW power_line AS
SELECT
    id,
    nodes,
    regexp_split_to_table(tags->'voltage','; *') AS voltage
FROM
    ways
WHERE
    tags?'power' AND
    (tags->'power' = 'line' OR tags->'power' = 'minor_line') AND
    tags?'voltage'
;

CREATE OR REPLACE FUNCTION ends(nodes bigint[]) RETURNS SETOF bigint AS $$
DECLARE BEGIN
    RETURN NEXT nodes[1];
    RETURN NEXT nodes[array_length(nodes,1)];
    RETURN;
END
$$ LANGUAGE plpgsql;


DROP VIEW IF EXISTS power_line_junction CASCADE;
CREATE VIEW power_line_junction AS
SELECT
    nodes.id,
    nodes.geom
FROM
    (SELECT voltage, ends(nodes) AS id FROM power_line) AS v
    JOIN nodes ON
        v.id = nodes.id
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(*) > 1
;

SELECT
    DISTINCT(id),
    ST_X(geom),
    ST_Y(geom)
FROM
    power_line_junction
    NATURAL JOIN (SELECT voltage, ends(nodes) AS id FROM power_line) AS v
GROUP BY
    id,
    voltage,
    geom
HAVING
    COUNT(*) = 1
;
"""

sql40 = """
SELECT
    nodes.id,
    ST_X(nodes.geom),
    ST_Y(nodes.geom)
FROM
    ways
    JOIN way_nodes ON
        ways.id = way_nodes.way_id
    JOIN nodes ON
        way_nodes.node_id = nodes.id
WHERE
    nodes.id != ways.nodes[1] AND
    nodes.id != ways.nodes[array_length(nodes,1)] AND
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line') AND
    not nodes.tags?'power'
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
    outxml.startElement("class", {"id":"1", "item":"7040"})
    outxml.Element("classtext", {"lang":"fr", "title":"Pylône ou poteau électrique isolé"})
    outxml.Element("classtext", {"lang":"en", "title":"Power tower or pole alone"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"2", "item":"7040"})
    outxml.Element("classtext", {"lang":"fr", "title":"Line électrique non terminé"})
    outxml.Element("classtext", {"lang":"en", "title":"Power line non terminated"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"3", "item":"7040"})
    outxml.Element("classtext", {"lang":"fr", "title":"Connexion entre différents voltages"})
    outxml.Element("classtext", {"lang":"en", "title":"Connection between different voltages"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"4", "item":"7040"})
    outxml.Element("classtext", {"lang":"en", "title":"No power node on power way"})
    outxml.endElement("class")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql20)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"2", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql30)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"3", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql40)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"4", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
