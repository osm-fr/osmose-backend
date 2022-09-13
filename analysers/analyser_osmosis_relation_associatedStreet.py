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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql00 = """
CREATE TEMP TABLE ways_addr AS
SELECT
    'W'::CHAR(1) AS type,
    ways.id,
    ST_Transform(linestring, {0}) AS linestring_proj,
    relations.id AS rid,
    relation_members.member_role AS role,
    ways.tags?'addr:flats' AS flats,
    coalesce(ways.tags->'addr:housenumber', ways.tags->'addr:housename') AS number,
    ways.tags->'addr:door' AS door,
    ways.tags->'addr:unit' AS unit,
    relations.tags->'name' AS r_name,
    ways.tags->'addr:street' AS addr_street,
    coalesce(ways.tags->'addr:street', ways.tags->'addr:district', ways.tags->'addr:neighbourhood', ways.tags->'addr:quarter', ways.tags->'addr:suburb', ways.tags->'addr:place', ways.tags->'addr:hamlet') AS name
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
    ways.tags ?| ARRAY['addr:housenumber', 'addr:housename']
"""

sql01 = """
CREATE TEMP TABLE nodes_addr AS
SELECT
    'N'::CHAR(1) AS type,
    nodes.id,
    ST_Transform(geom, {0}) AS geom_proj,
    relations.id AS rid,
    relation_members.member_role AS role,
    nodes.tags?'addr:flats' AS flats,
    coalesce(nodes.tags->'addr:housenumber', nodes.tags->'addr:housename') AS number,
    nodes.tags->'addr:door' AS door,
    nodes.tags->'addr:unit' AS unit,
    relations.tags->'name' AS r_name,
    nodes.tags->'addr:street' AS addr_street,
    coalesce(nodes.tags->'addr:street', nodes.tags->'addr:district', nodes.tags->'addr:neighbourhood', nodes.tags->'addr:quarter', nodes.tags->'addr:suburb', nodes.tags->'addr:place', nodes.tags->'addr:hamlet') AS name
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
    nodes.tags ?| ARRAY ['addr:housenumber', 'addr:housename']
"""

# ways with addr:housenumber or addr:housename and without addr:street and not member of a associatedStreet
sql10 = """
SELECT
    id,
    ST_AsText(ST_Transform(way_locate(linestring_proj), 4326))
FROM
    ways_addr
WHERE
    name IS NULL
GROUP BY
    id,
    linestring_proj
HAVING
    BOOL_AND(rid IS NULL)
"""

# same for nodes
sql11 = """
SELECT
    id,
    ST_AsText(ST_Transform(geom_proj, 4326))
FROM
    nodes_addr
WHERE
    name IS NULL
GROUP BY
    id,
    geom_proj
HAVING
    BOOL_AND(rid IS NULL)
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
SELECT DISTINCT ON (ways.id)
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
ORDER BY
    ways.id
"""

# roleless member node in relation
sql40 = """
SELECT DISTINCT ON (nodes.id)
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
ORDER BY
    nodes.id
"""

# roleless member way in relation
sql41 = """
SELECT DISTINCT ON (ways.id)
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
ORDER BY
    ways.id
"""

# node of relation without addr:housenumber nor addr:housename
sql50 = """
SELECT DISTINCT ON (nodes.id)
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
ORDER BY
    nodes.id
"""

# house role way of relation without addr:housenumber nor addr:housename
sql51 = """
SELECT DISTINCT ON (ways.id)
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
ORDER BY
    ways.id
"""

# many time same number in street
sql60 = """
CREATE TEMP TABLE housenumber AS (
SELECT DISTINCT ON (id)
    type,
    id,
    geom_proj,
    number,
    door,
    unit,
    r_name
FROM
    nodes_addr
WHERE
    role = 'house' AND
    NOT flats
ORDER BY
    id
) UNION ALL (
SELECT DISTINCT ON (id)
    type,
    id,
    ST_Centroid(linestring_proj) AS geom_proj,
    number,
    door,
    unit,
    r_name
FROM
    ways_addr
WHERE
    role = 'house' AND
    NOT flats
ORDER BY
    id
)
"""

sql61 = """
CREATE INDEX idx_housenumber_r_name_number ON housenumber(r_name, number)
"""

sql62 = """
CREATE INDEX idx_housenumber_geom ON housenumber USING gist(geom_proj)
"""

sql63 = """
SELECT
    CAST(substr(LEAST(hn1.type || hn1.id, hn2.type || hn2.id), 2) AS BIGINT) AS id,
    substr(LEAST(hn1.type || hn1.id, hn2.type || hn2.id), 1, 1) AS type,
    ST_AsText(ST_Transform(hn1.geom_proj, 4326)),
    hn1.r_name,
    hn1.number,
    hn1.door,
    hn1.unit
FROM
    housenumber AS hn1
    JOIN housenumber AS hn2 ON
        hn1.type || hn1.id < hn2.type || hn2.id AND
        hn1.r_name = hn2.r_name AND
        hn1.number = hn2.number AND
        ((hn1.door IS NULL AND hn2.door IS NULL) OR hn1.door = hn2.door) AND
        ((hn1.unit IS NULL AND hn2.unit IS NULL) OR hn1.unit = hn2.unit) AND
        ST_DWithin(hn1.geom_proj, hn2.geom_proj, 1000)
GROUP BY
    LEAST(hn1.type || hn1.id, hn2.type || hn2.id),
    hn1.r_name,
    hn1.number,
    hn1.door,
    hn1.unit,
    hn1.geom_proj
"""

# Many name in relation
sql70 = """
CREATE TEMP TABLE street_name AS (
SELECT
    relations.id,
    relations.tags->'name' AS name,
    relations.tags->'ref:FR:FANTOIR' AS ref,
    NULL AS linestring,
    NULL AS wid
FROM
    relations
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'associatedStreet' AND
    relations.tags?'name'
) UNION ALL (
SELECT
    relations.id,
    ways.tags->'name' AS name,
    ways.tags->'ref:FR:FANTOIR' AS ref,
    linestring AS linestring,
    ways.id AS wid
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

# Many relations for same street
sql90 = """
CREATE TEMP TABLE street_area AS
SELECT
    id,
    MIN(name) AS name,
    MIN(ref) AS ref,
    ST_Envelope(ST_Collect(linestring)) AS geom,
    array_agg(wid) AS wids
FROM
    street_name
GROUP BY
    id
"""

sql91 = """
CREATE INDEX idx_street_area ON street_area USING GIST(geom)
"""

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
) UNION ALL (
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
    MIN(ST_DistanceSphere(house.geom, street.geom)) > 200
"""

# Check addr:city
sqlC0 = """
CREATE TEMP TABLE addr_city AS (
SELECT
    'N'::char(1) AS type,
    id,
    tags->'addr:city' AS city
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'addr:city'
) UNION ALL (
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
CREATE TEMP TABLE admin_8 AS
SELECT
    'R'::char(1) AS type,
    id,
    tags->'name' AS city
FROM
    relations
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
        NATURAL LEFT JOIN admin_8
    WHERE
        admin_8.city IS NULL
    ) AS t
    NATURAL JOIN addr_city
"""

# Check addr:street
sqlD0 = """
CREATE TEMP TABLE addr_street AS (
SELECT DISTINCT ON (id)
    'N'::char(1) AS type,
    id,
    addr_street,
    geom_proj
FROM
    nodes_addr
WHERE
    addr_street IS NOT NULL
ORDER BY
    id
) UNION ALL (
SELECT DISTINCT ON (id)
    'W'::char(1) AS type,
    id,
    addr_street,
    linestring_proj AS geom_proj
FROM
    ways_addr
WHERE
    addr_street IS NOT NULL
ORDER BY
    id
)
"""

sqlD1 = """
SELECT
    id,
    type,
    addr_street,
    ST_AsText(ST_Transform(geom, 4326))
FROM (
SELECT
    addr_street.id,
    addr_street.type,
    addr_street.addr_street,
    any_locate(addr_street.type, addr_street.id) AS geom
FROM
    addr_street
    LEFT JOIN highways ON
        highways.tags ?| ARRAY['name', 'name:left', 'name:right'] AND
        (
            highways.tags->'name' = addr_street.addr_street OR
            highways.tags->'name:left' = addr_street.addr_street OR
            highways.tags->'name:right' = addr_street.addr_street
        ) AND
        ST_DWithIn(highways.linestring_proj, addr_street.geom_proj, {0})
WHERE
    highways.id IS NULL
) AS t
WHERE
    geom IS NOT NULL
"""

# Missing highway in associatedStreet
sqlF0 = """
SELECT
    highways.id,
    street_area.id AS rid,
    ST_AsText(way_locate(highways.linestring))
FROM
    street_area
    JOIN highways on
        ST_DWithin(highways.linestring_proj, ST_Transform(street_area.geom, {0}), 500) AND
        highways.id != ALL(street_area.wids) AND
        highways.tags ?| ARRAY['name', 'name:left', 'name:right'] AND
        (
            highways.tags->'name' = street_area.name OR
            highways.tags->'name:left' = street_area.name OR
            highways.tags->'name:right' = street_area.name
        )
"""

class Analyser_Osmosis_Relation_AssociatedStreet(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs[1] = self.def_class(item = 2060, level = 3, tags = ['addr', 'relation', 'fix:chair'],
            title = T_('addr:housenumber or addr:housename without addr:street, addr:district, addr:neighbourhood, addr:quarter, addr:suburb, addr:place or addr:hamlet must be in a associatedStreet relation'),
            detail = T_(
'''There is only a part of the required tag `addr:*=*`. They do not
provide a consistent address.'''))
        self.classs_change[2] = self.def_class(item = 2060, level = 2, tags = ['addr', 'relation', 'fix:chair'],
            title = T_('No street role'),
            detail = T_(
'''The street is not present in relation with the role `street`.'''))
        self.classs_change[3] = self.def_class(item = 2060, level = 2, tags = ['addr', 'fix:chair'],
            title = T_('street role is not an highway'),
            detail = T_(
'''The street must be a highway.'''))
        self.classs_change[4] = self.def_class(item = 2060, level = 3, tags = ['addr', 'relation', 'fix:chair'],
            title = T_('Roleless member'),
            detail = T_(
'''A member without role is present in the relation.'''))
        self.classs_change[5] = self.def_class(item = 2060, level = 3, tags = ['addr', 'fix:chair'],
            title = T_('Member without addr:housenumber nor addr:housename'),
            detail = T_(
'''Address without number is present.'''))
        self.classs[6] = self.def_class(item = 2060, level = 3, tags = ['addr', 'fix:survey'],
            title = T_('Number twice in the street'))
        self.classs[7] = self.def_class(item = 2060, level = 2, tags = ['addr', 'fix:chair'],
            title = T_('Many street names'))
        self.classs[8] = self.def_class(item = 2060, level = 2, tags = ['addr', 'relation', 'fix:chair'],
            title = T_('Many relations on one street'))
        self.classs[9] = self.def_class(item = 2060, level = 2, tags = ['addr', 'geom', 'fix:chair'],
            title = T_('House too far away from street'))
        if self.config.options.get("addr:city-admin_level"):
            self.classs[12] = self.def_class(item = 2060, level = 2, tags = ['addr', 'fix:chair'],
                title = T_('Tag "addr:city" not matching a city'))
        self.classs[18] = self.def_class(item ="2060", level = 2, tags = ['addr', 'fix:chair'],
            title = T_('Missing highway in associatedStreet relation'),
            fix = T_(
'''Extend the relation to include the way with the same name.'''))
        self.classs[19] = self.def_class(item ="2060", level = 2, tags = ['addr', 'fix:chair'],
            title = T_('Tag "addr:street" not matching a street name around'))

        self.callback20 = lambda res: res[1] and {"class":2, "subclass":1, "data":[self.relation_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "subclass":1, "data":[self.node_full, self.relation, self.positionAsText]}
        self.callback41 = lambda res: {"class":4, "subclass":2, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callback50 = lambda res: {"class":5, "subclass":1, "data":[self.node_full, self.relation, self.positionAsText]}
        self.callback51 = lambda res: {"class":5, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callbackC2 = lambda res: {"class":12, "subclass":1, "data":[lambda t: self.typeMapping[res[1]](t), None, self.positionAsText]}
        self.callbackD1 = lambda res: {"class":19, "subclass":1, "data":[lambda t: self.typeMapping[res[1]](t), None, None, self.positionAsText], "text": T_("No street with name \"{0}\" found around", res[2])}
        self.callbackF0 = lambda res: {"class":18, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql00.format(self.config.options.get("proj", 4326)))
        self.run(sql01.format(self.config.options.get("proj", 4326)))
        self.run(sql10, lambda res: {"class":1, "subclass":1, "data":[self.way_full, self.positionAsText]} )
        self.run(sql11, lambda res: {"class":1, "subclass":2, "data":[self.node_full, self.positionAsText]} )
        self.run(sql60.format(self.config.options.get("proj")))
        self.run(sql61)
        self.run(sql62)
        self.run(sql63, lambda res: {"class":6, "subclass":1,
            "data":[lambda t: self.typeMapping[res[1]](t), None, self.positionAsText],
            "text": T_("Multiple numbers \"{numbers}\" in way \"{way}\"", numbers = ",  ".join(filter(lambda z: z, res[4:])), way = res[3]),
        })
        self.run(sql70)
        self.run(sql80, lambda res: {"class":7, "subclass":1, "data":[self.relation_full, self.positionAsText], "text":{"en": res[2]}} )
        self.run(sql90)
        self.run(sql91)
        self.run(sqlA0, lambda res: {"class":8, "subclass":1, "data":[self.relation_full, self.relation_full, self.positionAsText]} )
        self.run(sqlB0, lambda res: {"class":9, "subclass":1, "data":[lambda t: self.typeMapping[res[1]](t), None, self.positionAsText, self.relation_full]} )
        if self.config.options.get("addr:city-admin_level"):
            self.run(sqlC0)
            self.run(sqlC1.format( "','".join(self.config.options.get("addr:city-admin_level").split(','))))
            self.run(sqlC2, self.callbackC2)
        self.run(sqlD0)
        self.run(sqlD1.format(self.config.options.get("addr:street_distance", 500)), self.callbackD1)
        self.run(sqlF0.format(self.config.options.get("proj")), self.callbackF0)

    def analyser_osmosis_full(self):
        self.run(sql20.format(""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)
        self.run(sql41.format(""), self.callback41)
        self.run(sql50.format("", ""), self.callback50)
        self.run(sql51.format("", ""), self.callback51)

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
