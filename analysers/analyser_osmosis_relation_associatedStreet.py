#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011-2014                                 ##
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

from Analyser_Osmosis import Analyser_Osmosis

sql00 = """
CREATE TEMP TABLE ways_addr AS
SELECT
    'W'::CHAR(1) AS type,
    ways.id,
    linestring,
    relations.id AS rid,
    relation_members.member_role AS role,
    ways.tags?'addr:flats' AS flats,
    coalesce(ways.tags->'addr:housenumber', ways.tags->'addr:housename') AS number,
    ways.tags->'addr:door' AS door,
    ways.tags->'addr:unit' AS unit,
    coalesce(relations.tags->'name', ways.tags->'addr:street', ways.tags->'addr:district', ways.tags->'addr:neighbourhood', ways.tags->'addr:quarter', ways.tags->'addr:suburb', ways.tags->'addr:place', ways.tags->'addr:hamlet') AS street
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
    ways.tags != ''::hstore AND
    ways.tags ?| ARRAY['addr:housenumber', 'addr:housename'] AND
    NOT ways.tags ?| ARRAY['addr:street', 'addr:district', 'addr:neighbourhood', 'addr:quarter', 'addr:suburb', 'addr:place', 'addr:hamlet']
"""

sql01 = """
CREATE TEMP TABLE nodes_addr AS
SELECT
    'N'::CHAR(1) AS type,
    nodes.id,
    geom,
    relations.id AS rid,
    relation_members.member_role AS role,
    nodes.tags?'addr:flats' AS flats,
    coalesce(nodes.tags->'addr:housenumber', nodes.tags->'addr:housename') AS number,
    nodes.tags->'addr:door' AS door,
    nodes.tags->'addr:unit' AS unit,
    coalesce(relations.tags->'name', nodes.tags->'addr:street', nodes.tags->'addr:district', nodes.tags->'addr:neighbourhood', nodes.tags->'addr:quarter', nodes.tags->'addr:suburb', nodes.tags->'addr:place', nodes.tags->'addr:hamlet') AS street
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
    nodes.tags != ''::hstore AND
    nodes.tags ?| ARRAY ['addr:housenumber', 'addr:housename'] AND
    NOT nodes.tags ?| ARRAY['addr:street', 'addr:district', 'addr:neighbourhood', 'addr:quarter', 'addr:suburb', 'addr:place', 'addr:hamlet']
"""

# ways with addr:housenumber or addr:housename and without addr:street and not member of a associatedStreet
sql10 = """
SELECT
    id,
    ST_AsText(way_locate(linestring))
FROM
    ways_addr
WHERE
    rid IS NULL
"""

# same for nodes
sql11 = """
SELECT
    id,
    ST_AsText(geom)
FROM
    nodes_addr
WHERE
    rid IS NULL
"""

# No role street in relation
sql20 = """
SELECT
    relations.id,
    ST_AsText(relation_locate(relations.id)) AS geom
FROM
    {0}relations AS relations
    LEFT JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'street'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet' AND
    relation_members.member_role IS NULL
"""

# role street without highway
sql30 = """
SELECT
    ways.id,
    relations.id,
    ST_ASText(way_locate(linestring))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'street'
    JOIN {1}ways AS ways ON
        relation_members.member_id = ways.id AND
        NOT ways.tags?'highway'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
"""

# roleless member node in relation
sql40 = """
SELECT
    nodes.id,
    relations.id,
    ST_AsText(geom)
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'N' AND
        relation_members.member_role = ''
    JOIN nodes ON
        relation_members.member_id = nodes.id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
"""

# roleless member way in relation
sql41 = """
SELECT
    ways.id,
    relations.id,
    ST_AsText(way_locate(linestring))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = ''
    JOIN ways ON
        relation_members.member_id = ways.id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
"""

# node of relation without addr:housenumber nor addr:housename
sql50 = """
SELECT
    nodes.id,
    relations.id,
    ST_AsText(geom)
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'N'
    JOIN {1}nodes AS nodes ON
        relation_members.member_id = nodes.id AND
        NOT nodes.tags ?| ARRAY['addr:housenumber', 'addr:housename']
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
"""

# house role way of relation without addr:housenumber nor addr:housename
sql51 = """
SELECT
    ways.id,
    relations.id,
    ST_AsText(way_locate(linestring))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'house'
    JOIN {1}ways AS ways ON
        relation_members.member_id = ways.id AND
        NOT ways.tags ?| ARRAY['addr:housenumber', 'addr:housename', 'addr:interpolation']
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
"""

# many time same number in street
sql60 = """
CREATE TEMP TABLE housenumber AS (
SELECT
    type,
    id,
    ST_Transform(geom, {0}) AS geom,
    number,
    door,
    unit,
    street
FROM
    nodes_addr
WHERE
    role = 'house' AND
    NOT flats
) UNION (
SELECT
    type,
    id,
    ST_Transform(ST_Centroid(linestring), {0}) AS geom,
    number,
    door,
    unit,
    street
FROM
    ways_addr
WHERE
    role = 'house' AND
    NOT flats
)
"""

sql61 = """
CREATE INDEX idx_housenumber_street_number ON housenumber(street, number)
"""

sql62 = """
CREATE INDEX idx_housenumber_geom ON housenumber USING gist(geom)
"""

sql63 = """
SELECT
    CAST(substr(LEAST(hn1.type || hn1.id, hn2.type || hn2.id), 2) AS BIGINT) AS id,
    substr(LEAST(hn1.type || hn1.id, hn2.type || hn2.id), 1, 1) AS type,
    ST_AsText(ST_Transform(hn1.geom, 4326)),
    hn1.street,
    hn1.number,
    hn1.door,
    hn1.unit
FROM
    housenumber AS hn1
    JOIN housenumber AS hn2 ON
        hn1.type || hn1.id < hn2.type || hn2.id AND
        hn1.street = hn2.street AND
        hn1.number = hn2.number AND
        ((hn1.door IS NULL AND hn2.door IS NULL) OR hn1.door = hn2.door) AND
        ((hn1.unit IS NULL AND hn2.unit IS NULL) OR hn1.unit = hn2.unit) AND
        ST_DWithin(hn1.geom, hn2.geom, 1000)
GROUP BY
    LEAST(hn1.type || hn1.id, hn2.type || hn2.id),
    hn1.street,
    hn1.number,
    hn1.door,
    hn1.unit,
    hn1.geom
"""

sql70 = """
CREATE TEMP TABLE street_name AS (
SELECT
    relations.id,
    relations.tags->'name' AS name,
    relations.tags->'ref:FR:FANTOIR' AS ref,
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
    ways.tags->'ref:FR:FANTOIR' AS ref,
    linestring AS linestring
FROM
    relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'street'
    JOIN ways ON
        relation_members.member_id = ways.id AND
        ways.tags != ''::hstore AND
        ways.tags?'name'
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet'
)
"""

# Many name in relation
sql80 = """
SELECT
    id,
    ST_AsText((SELECT ST_Centroid(ST_Union(linestring)) FROM street_name WHERE t.id = street_name.id)) AS geom,
    string_agg(name, ', ') AS names
FROM
    (SELECT id, name FROM street_name GROUP BY id, name) AS t
GROUP BY
    id
HAVING
    COUNT(*) > 1
"""

sql90 = """
CREATE TEMP TABLE street_area AS
SELECT
    id,
    MIN(name) AS name,
    MIN(ref) AS ref,
    ST_Envelope(ST_Collect(linestring)) AS geom
FROM
    street_name
GROUP BY
    id
"""

sql91 = """
CREATE INDEX idx_street_area ON street_area USING GIST(geom)
"""

# Many relations for same street
sqlA0 = """
SELECT
    sa1.id,
    sa2.id,
    ST_AsText(ST_Centroid(ST_Collect(sa1.geom, sa2.geom)))
FROM
    street_area AS sa1
    JOIN street_area AS sa2 ON
        sa1.id < sa2.id AND
        sa1.name = sa2.name AND
        ((sa1.ref IS NULL and sa2.ref IS NULL) OR sa1.ref = sa2.ref) AND
        sa1.geom && sa2.geom
WHERE
    sa1.name IS NOT NULL AND
    sa2.name IS NOT NULL
"""

# House away from street
sqlB0 = """
SELECT
    house.id,
    house.type,
    ST_AsText(ST_Centroid(house.geom)),
    house.rid
FROM
((
    SELECT
        relations.id AS rid,
        'W' AS type,
        ways.id,
        ways.linestring AS geom
    FROM
        relations
        JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role = 'house'
        JOIN ways ON
            relation_members.member_id = ways.id AND
            ways.tags ?| ARRAY['addr:housenumber', 'addr:housename']
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet'
) UNION (
    SELECT
        relations.id AS rid,
        'N' AS type,
        nodes.id,
        nodes.geom
    FROM
        relations
        JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'N' AND
            relation_members.member_role = 'house'
        JOIN nodes ON
            relation_members.member_id = nodes.id AND
            nodes.tags != ''::hstore AND
            nodes.tags ?| ARRAY['addr:housenumber', 'addr:housename']
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet'
)) AS house,
(
    SELECT
        relations.id AS rid,
        ways.linestring AS geom
    FROM
        relations
        JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role = 'street'
    JOIN ways ON
        relation_members.member_id = ways.id
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet'
) AS street
WHERE
    house.rid = street.rid
GROUP BY
    house.rid,
    house.id,
    house.type,
    house.geom
HAVING
    MIN(ST_Distance_Sphere(house.geom, street.geom)) > 200
"""

sqlC0 = """
CREATE TABLE addr_city AS (
SELECT
    'N'::char(1) AS type,
    id,
    tags->'addr:city' AS city
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'addr:city'
) UNION (
SELECT
    'W'::char(1) AS type,
    id,
    tags->'addr:city' AS city
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'addr:city'
)
"""

sqlC1 = """
CREATE TABLE {1}admin_8 AS
SELECT
    'R'::char(1) AS type,
    id,
    tags->'name' AS city
FROM
    {1}relations
WHERE
    tags?'type' AND
    tags->'type' = 'boundary' AND
    tags?'boundary' AND
    tags->'boundary' = 'administrative' AND
    tags->'admin_level' IN ('{0}') AND
    tags?'name'
"""

sqlC2 = """
SELECT
    id,
    type,
    ST_AsText(any_locate(type, id))
FROM
    (
    SELECT
        c.city
    FROM
        (SELECT city FROM addr_city GROUP BY city) AS c
        NATURAL LEFT JOIN {0}admin_8
    WHERE
        {0}admin_8.city IS NULL
    ) AS t
    NATURAL JOIN addr_city
"""

sqlD0 = """
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring)),
    string_agg(DISTINCT nodes.tags->'addr:street', ', ')
FROM
    {0}ways AS ways
    JOIN way_nodes ON
        way_nodes.way_id = ways.id
    JOIN {1}nodes AS nodes on
        nodes.id = way_nodes.node_id AND
        nodes.tags != ''::hstore AND
        nodes.tags?'addr:street'
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'addr:interpolation'
GROUP BY
    ways.id,
    ways.linestring
HAVING
    COUNT(DISTINCT nodes.tags->'addr:street') != 1
"""

sqlE0 = """
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring)),
    string_agg(DISTINCT relations.tags->'name', ', ')
FROM
    ways
    JOIN way_nodes ON
        way_nodes.way_id = ways.id
    JOIN nodes on
        nodes.id = way_nodes.node_id AND
        nodes.tags != ''::hstore AND
        nodes.tags ?| ARRAY['addr:housenumber', 'addr:housename']
    JOIN relation_members ON
        relation_members.member_type = 'N' AND
        relation_members.member_id = nodes.id
    JOIN relations ON
        relations.id = relation_members.relation_id AND
        relations.tags->'type' = 'associatedStreet'
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'addr:interpolation'
GROUP BY
    ways.id,
    ways.linestring
HAVING
    COUNT(DISTINCT relations.id) != 1
"""

class Analyser_Osmosis_Relation_AssociatedStreet(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"2060", "level": 3, "tag": ["addr", "relation", "fix:chair"], "desc": T_(u"addr:housenumber or addr:housename without addr:street, addr:district, addr:neighbourhood, addr:quarter, addr:suburb, addr:place or addr:hamlet must be in a associatedStreet relation") }
        self.classs_change[2] = {"item":"2060", "level": 2, "tag": ["addr", "relation", "fix:chair"], "desc": T_(u"No street role") }
        self.classs_change[3] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"street role is not an highway") }
        self.classs_change[4] = {"item":"2060", "level": 3, "tag": ["addr", "relation", "fix:chair"], "desc": T_(u"Roleless member") }
        self.classs_change[5] = {"item":"2060", "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Member without addr:housenumber nor addr:housename") }
        self.classs[6] = {"item":"2060", "level": 3, "tag": ["addr", "fix:survey"], "desc": T_(u"Number twice in the street") }
        self.classs[7] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Many street names") }
        self.classs[8] = {"item":"2060", "level": 2, "tag": ["addr", "relation", "fix:chair"], "desc": T_(u"Many relations on one street") }
        self.classs[9] = {"item":"2060", "level": 2, "tag": ["addr", "geom", "fix:chair"], "desc": T_(u"House too far away from street") }
        if self.config.options.get("addr:city-admin_level"):
            self.classs[12] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Tag \"addr:city\" not matching a city") }
        self.classs_change[16] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation on nodes of multiple street names") }
        self.classs[17] = {"item":"2060", "level": 2, "tag": ["addr", "fix:chair"], "desc": T_(u"Interpolation on nodes of multiple street names") }
        self.callback20 = lambda res: res[1] and {"class":2, "subclass":1, "data":[self.relation_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "subclass":1, "data":[self.node_full, self.relation, self.positionAsText]}
        self.callback41 = lambda res: {"class":4, "subclass":2, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callback50 = lambda res: {"class":5, "subclass":1, "data":[self.node_full, self.relation, self.positionAsText]}
        self.callback51 = lambda res: {"class":5, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callbackC2 = lambda res: {"class":12, "subclass":1, "data":[lambda t: self.typeMapping[res[1]](t), None, self.positionAsText]}
        self.callbackD0 = lambda res: {"class":16, "subclass":1, "data":[self.way_full, self.positionAsText], "text": T_(u"Interpolation span on streets: %s", res[2]) }
        self.callbackE0 = lambda res: {"class":17, "subclass":1, "data":[self.relation_full, self.positionAsText], "text": T_(u"Interpolation span on streets: %s", res[2]) }

    def analyser_osmosis_common(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql10, lambda res: {"class":1, "subclass":1, "data":[self.way_full, self.positionAsText]} )
        self.run(sql11, lambda res: {"class":1, "subclass":2, "data":[self.node_full, self.positionAsText]} )
        if "proj" in self.config.options:
            self.run(sql60.format(self.config.options.get("proj")))
            self.run(sql61)
            self.run(sql62)
            self.run(sql63, lambda res: {"class":6, "subclass":1,
                "data":[lambda t: self.typeMapping[res[1]](t), None, self.positionAsText],
                "text": T_(u"Multiple numbers \"%(numbers)s\" in way \"%(way)s\"", {"numbers":",  ".join(filter(lambda z: z, res[4:])), "way": res[3]}),
                } )
        self.run(sql70)
        self.run(sql80, lambda res: {"class":7, "subclass":1, "data":[self.relation_full, self.positionAsText], "text":{"en": res[2]}} )
        self.run(sql90)
        self.run(sql91)
        self.run(sqlA0, lambda res: {"class":8, "subclass":1, "data":[self.relation_full, self.relation_full, self.positionAsText]} )
        self.run(sqlB0, lambda res: {"class":9, "subclass":1, "data":[lambda t: self.typeMapping[res[1]](t), None, self.positionAsText, self.relation_full]} )
        self.run(sqlE0.format("", ""), self.callbackE0)

    def analyser_osmosis_full(self):
        self.run(sql20.format(""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)
        self.run(sql41.format(""), self.callback41)
        self.run(sql50.format("", ""), self.callback50)
        self.run(sql51.format("", ""), self.callback51)
        if self.config.options.get("addr:city-admin_level"):
            self.run(sqlC0)
            self.run(sqlC1.format("','".join(self.config.options.get("addr:city-admin_level").split(',')), ""))
            self.run(sqlC2.format(""), self.callbackC2)
        self.run(sqlD0.format("", ""), self.callbackD0)

    def analyser_osmosis_diff(self):
        self.run(sql20.format("touched_"), self.callback20)
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("not_touched_", "touched_"), self.callback30)
        self.run(sql40.format("touched_"), self.callback40)
        self.run(sql41.format("touched_"), self.callback41)
        self.run(sql50.format("touched_", ""), self.callback50)
        self.run(sql50.format("not_touched_", "touched_"), self.callback50)
        self.run(sql51.format("touched_", ""), self.callback51)
        self.run(sql51.format("not_touched_", "touched_"), self.callback51)
        if self.config.options.get("addr:city-admin_level"):
            # TODO: not all touched cases are covered here
            self.run(sqlC0)
            self.run(sqlC1.format("','".join(self.config.options.get("addr:city-admin_level").split(',')), "touched_"))
            self.run(sqlC2.format("touched_"), self.callbackC2)
        self.run(sqlD0.format("touched_", ""), self.callbackD0)
        self.run(sqlD0.format("not_touched_", "touched_"), self.callbackD0)
