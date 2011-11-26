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
## some usefull functions

re_points = re.compile("[\(,][^\(,\)]*[\),]")
def get_points(text):
    pts = []
    for r in re_points.findall(text):
        lon, lat = r[1:-1].split(" ")
        pts.append({"lat":lat, "lon":lon})
    return pts

###########################################################################

# ways avec addr:housenumber et sans addr:street et pas membre d'une associatedStreet
sql10 = """
SELECT
    ways.id,
    ST_X(ST_Centroid(linestring)),
    ST_Y(ST_Centroid(linestring))
FROM
    ways
    LEFT JOIN relation_members ON
        ways.id = relation_members.member_id AND
        relation_members.member_type = 'W'
    LEFT JOIN relations ON
        relation_members.relation_id = relations.id AND
        relations.tags?'type' AND
        relations.tags->'type' IN ('associatedStreet', 'street')
WHERE
    ways.tags?'addr:housenumber' AND
    (NOT ways.tags?'addr:street') AND
    relations.id IS NULL
;
"""

# idem nodes
sql11 = """
SELECT
    nodes.id,
    ST_X(geom),
    ST_Y(geom)
FROM
    nodes
    LEFT JOIN relation_members ON
        nodes.id = relation_members.member_id AND
        relation_members.member_type = 'N'
    LEFT JOIN relations ON
        relation_members.relation_id = relations.id AND
        relations.tags?'type' AND
        relations.tags->'type' IN ('associatedStreet', 'street')
WHERE
    nodes.tags?'addr:housenumber' AND
    (NOT nodes.tags?'addr:street') AND
    relations.id IS NULL
;
"""

# pas de rôle street dans la relation
sql20 = """
SELECT
    relations.id,
    ST_AsText((
        SELECT
            ST_Centroid(ST_Collect(geom)) AS geom
        FROM
        ((
            SELECT
                linestring AS geom
            FROM
                relation_members
                JOIN ways ON
                    relation_members.member_id = ways.id
            WHERE
                relations.id = relation_members.relation_id AND
                relation_members.member_type = 'W'
            LIMIT 1
        ) UNION (
            SELECT
                geom
            FROM
                relation_members
                JOIN nodes ON
                    relation_members.member_id = nodes.id
            WHERE
                relations.id = relation_members.relation_id AND
                relation_members.member_type = 'N'
            LIMIT 1
        )) AS a
    )) AS geom
FROM
    relations
    LEFT JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'street'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet' AND
    relation_members.member_role IS NULL
;
"""

# rôle street sans highway
sql30 = """
SELECT
    ways.id,
    relations.id,
    ST_X(ST_Centroid(linestring)),
    ST_Y(ST_Centroid(linestring))
FROM
    relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'street'
    JOIN ways ON
        relation_members.member_id = ways.id AND
        NOT ways.tags?'highway'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
;
"""

# node membre sans rôle dans la relation
sql40 = """
SELECT
    nodes.id,
    relations.id,
    ST_X(geom),
    ST_Y(geom)
FROM
    relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'N' AND
        relation_members.member_role = ''
    JOIN nodes ON
        relation_members.member_id = nodes.id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
;
"""

# way membre sans rôle dans la relation
sql41 = """
SELECT
    ways.id,
    relations.id,
    ST_X(ST_Centroid(linestring)),
    ST_Y(ST_Centroid(linestring))
FROM
    relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = ''
    JOIN ways ON
        relation_members.member_id = ways.id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
;
"""

# node de la relation sans addr:housenumber
sql50 = """
SELECT
    nodes.id,
    relations.id,
    ST_X(geom),
    ST_Y(geom)
FROM
    relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'N'
    JOIN nodes ON
        relation_members.member_id = nodes.id AND
        NOT nodes.tags?'addr:housenumber'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
;
"""

# way role house de la relation sans addr:housenumber
sql51 = """
SELECT
    ways.id,
    relations.id,
    ST_X(ST_Centroid(linestring)),
    ST_Y(ST_Centroid(linestring))
FROM
    relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'house'
    JOIN ways ON
        relation_members.member_id = ways.id AND
        NOT ways.tags?'addr:housenumber' AND
        NOT ways.tags?'addr:interpolation'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
;
"""

# plusiers fois le même numéro dans la rue
sql60 = """
SELECT
    rid,
    ST_X(ST_Centroid(ST_Collect(geom))),
    ST_Y(ST_Centroid(ST_Collect(geom))),
    n
FROM
((
    SELECT
        relations.id AS rid,
        ways.tags->'addr:housenumber' AS n,
        ST_Centroid(ways.linestring) AS geom
    FROM
        relations
        JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role = 'house'
        JOIN ways ON
            relation_members.member_id = ways.id AND
            ways.tags?'addr:housenumber'
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet'
) UNION (
    SELECT
        relations.id AS rid,
        nodes.tags->'addr:housenumber' AS n,
        nodes.geom
    FROM
        relations
        JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'N' AND
            relation_members.member_role = 'house'
        JOIN nodes ON
            relation_members.member_id = nodes.id AND
            nodes.tags?'addr:housenumber'
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet'
)) AS n
GROUP BY
    rid,
    n
HAVING
    COUNT(*) > 1
;
"""

sql70 = """
DROP VIEW IF EXISTS street_name CASCADE;
CREATE VIEW street_name AS
SELECT
    *
FROM
((
    SELECT
        relations.id,
        relations.tags->'name' AS name,
        NULL AS linestring
    FROM
        relations
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet' AND
        relations.tags?'name'
) UNION (
    SELECT
        relations.id,
        ways.tags->'name' AS name,
        linestring AS linestring
    FROM
        relations
        JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role = 'street'
        JOIN ways ON
            relation_members.member_id = ways.id AND
            ways.tags?'name'
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet'
)) As d
;
"""

# Plus d'un nom dans la relation
sql80 = """
SELECT
    id,
    ST_AsText((SELECT ST_Centroid(ST_Union(linestring)) FROM street_name WHERE t.id = street_name.id)) AS geom
FROM
    (SELECT id, name FROM street_name GROUP BY id, name) AS t
GROUP BY
    id
HAVING
    COUNT(*) > 1
;
"""

sql90 = """
DROP VIEW IF EXISTS street_area CASCADE;
CREATE VIEW street_area AS
SELECT
    id,
    name,
    ST_Envelope(ST_Collect(linestring)) AS geom
FROM
    street_name
GROUP BY
    id,
    name
;
"""

# Multiple relation pour la même rue
sqlA0 = """
SELECT
    sa1.id,
    sa2.id,
    ST_X(ST_Centroid(ST_Collect(sa1.geom, sa2.geom))),
    ST_Y(ST_Centroid(ST_Collect(sa1.geom, sa2.geom)))
FROM
    street_area AS sa1
    JOIN street_area AS sa2 ON
        sa1.id < sa2.id AND
        sa1.name = sa2.name AND
        sa1.geom && sa2.geom
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
    outxml.startElement("class", {"id":"1", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"addr:housenumber sans addr:street doit être dans une relation associatedStreet"})
    outxml.Element("classtext", {"lang":"en", "title":"addr:housenumber without addr:street must be in a associatedStreet relation"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"2", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Pas de rôle street"})
    outxml.Element("classtext", {"lang":"en", "title":"No street role"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"3", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Le rôle street n'est pas une highway"})
    outxml.Element("classtext", {"lang":"en", "title":"street role is not an highway"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"4", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Membre sans role"})
    outxml.Element("classtext", {"lang":"en", "title":"Roleless member"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"5", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Membre sans addr:housenumber"})
    outxml.Element("classtext", {"lang":"en", "title":"Member without addr:housenumber"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"6", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Numero en double dans la rue"})
    outxml.Element("classtext", {"lang":"en", "title":"Number twice in the street"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"7", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Plusiers noms pour la rue"})
    outxml.Element("classtext", {"lang":"en", "title":"Many street names"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"8", "item":"2060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Plusieurs relations pour la même rue"})
    outxml.Element("classtext", {"lang":"en", "title":"Many relations on one street"})
    outxml.endElement("class")

    giscurs.execute("SET search_path TO %s,public;" % config.dbp)

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql11)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1", "subclass":"2"})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql20)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"2", "subclass":"1"})
        for loc in get_points(res[1]):
            outxml.Element("location", loc)
        outxml.RelationCreate(apiconn.RelationGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql30)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"3", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.RelationCreate(apiconn.RelationGet(res[1]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql40)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"4", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.RelationCreate(apiconn.RelationGet(res[1]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql41)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"4", "subclass":"2"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.RelationCreate(apiconn.RelationGet(res[1]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql50)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"5", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.NodeCreate(apiconn.NodeGet(res[0]))
        outxml.RelationCreate(apiconn.RelationGet(res[1]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql51)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"5", "subclass":"2"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.RelationCreate(apiconn.RelationGet(res[1]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql60)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"6", "subclass":"1"})
        outxml.Element("text", {"lang":"fr", "value":"Multiple \"%s\" dans la rue" % res[3]})
        outxml.Element("text", {"lang":"en", "value":"Multiple \"%s\" in street" % res[3]})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.RelationCreate(apiconn.RelationGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql70)
    giscurs.execute(sql80)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"7", "subclass":"1"})
        for loc in get_points(res[1]):
            outxml.Element("location", loc)
        outxml.RelationCreate(apiconn.RelationGet(res[0]))
        outxml.endElement("error")

    ## querry
    logger.log(u"requête osmosis")
    giscurs.execute(sql90)
    giscurs.execute(sqlA0)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"8", "subclass":"1"})
        outxml.Element("location", {"lat":str(res[3]), "lon":str(res[2])})
        outxml.RelationCreate(apiconn.RelationGet(res[0]))
        outxml.RelationCreate(apiconn.RelationGet(res[1]))
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
