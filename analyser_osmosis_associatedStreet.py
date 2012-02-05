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

from Analyser_Osmosis import Analyser_Osmosis

# ways avec addr:housenumber et sans addr:street et pas membre d'une associatedStreet
sql10 = """
SELECT
    ways.id,
    ST_AsText(ST_Centroid(linestring))
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
    ST_AsText(geom)
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
    *
FROM
(
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
        {0}relations AS relations
        LEFT JOIN relation_members ON
            relations.id = relation_members.relation_id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role = 'street'
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'associatedStreet' AND
        relation_members.member_role IS NULL
) AS t
WHERE
    geom IS NOT NULL
;
"""

# rôle street sans highway
sql30 = """
SELECT
    ways.id,
    relations.id,
    ST_ASText(ST_Centroid(linestring))
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
;
"""

# node membre sans rôle dans la relation
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
;
"""

# way membre sans rôle dans la relation
sql41 = """
SELECT
    ways.id,
    relations.id,
    ST_AsText(ST_Centroid(linestring))
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
;
"""

# node de la relation sans addr:housenumber
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
    ST_AsText(ST_Centroid(linestring))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'house'
    JOIN {1}ways AS ways ON
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
    ST_AsText(ST_Centroid(ST_Collect(geom))),
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
    ST_AsText(ST_Centroid(ST_Collect(sa1.geom, sa2.geom)))
FROM
    street_area AS sa1
    JOIN street_area AS sa2 ON
        sa1.id < sa2.id AND
        sa1.name = sa2.name AND
        sa1.geom && sa2.geom
;
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
            ways.tags?'addr:housenumber'
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
            nodes.tags?'addr:housenumber'
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
;
"""

class Analyser_Osmosis_AssociatedStreet(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"2060", "desc":{"fr":"addr:housenumber sans addr:street doit être dans une relation associatedStreet", "en":"addr:housenumber without addr:street must be in a associatedStreet relation"} }
        self.classs_change[2] = {"item":"2060", "desc":{"fr":"Pas de rôle street", "en":"No street role"} }
        self.classs_change[3] = {"item":"2060", "desc":{"fr":"Le rôle street n'est pas une highway", "en":"street role is not an highway"} }
        self.classs_change[4] = {"item":"2060", "desc":{"fr":"Membre sans role", "en":"Roleless member"} }
        self.classs_change[5] = {"item":"2060", "desc":{"fr":"Membre sans addr:housenumber", "en":"Member without addr:housenumber"} }
        self.classs[6] = {"item":"2060", "desc":{"fr":"Numero en double dans la rue", "en":"Number twice in the street"} }
        self.classs[7] = {"item":"2060", "desc":{"fr":"Plusiers noms pour la rue", "en":"Many street names"} }
        self.classs[8] = {"item":"2060", "desc":{"fr":"Plusieurs relations pour la même rue", "en":"Many relations on one street"} }
        self.classs[9] = {"item":"2060", "desc":{"fr":"Trop grande distance a la rue", "en":"House away from street"} }
        self.callback20 = lambda res: {"class":2, "subclass":1, "data":[self.relation_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "subclass":1, "data":[self.node_full, self.relation, self.positionAsText]}
        self.callback41 = lambda res: {"class":4, "subclass":2, "data":[self.way_full, self.relation, self.positionAsText]}
        self.callback50 = lambda res: {"class":5, "subclass":1, "data":[self.node_full, self.relation, self.positionAsText]}
        self.callback51 = lambda res: {"class":5, "subclass":1, "data":[self.way_full, self.relation, self.positionAsText]}

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {"class":1, "subclass":1, "data":[self.way_full, self.positionAsText]} )
        self.run(sql11, lambda res: {"class":1, "subclass":2, "data":[self.node_full, self.positionAsText]} )
        self.run(sql60, lambda res: {"class":6, "subclass":1,
            "data":[self.relation, self.positionAsText],
            "text":{"fr":"Multiple \"%s\" dans la rue" % res[2], "en":"Multiple \"%s\" in street" % res[2]} } )
        self.run(sql70)
        self.run(sql80, lambda res: {"class":7, "subclass":1, "data":[self.relation_full, self.positionAsText]} )
        self.run(sql90)
        self.run(sqlA0, lambda res: {"class":8, "subclass":1, "data":[self.relation_full, self.relation_full, self.positionAsText]} )
        byType = {'N':self.node_full, 'W':self.way_full}
        self.run(sqlB0, lambda res: {"class":9, "subclass":1, "data":[lambda t: byType[res[1]], None, self.positionAsText, self.relation_full]} )

    def analyser_osmosis_all(self):
        self.run(sql20.format(""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)
        self.run(sql41.format(""), self.callback41)
        self.run(sql50.format("", ""), self.callback50)
        self.run(sql51.format("", ""), self.callback51)

    def analyser_osmosis_touched(self):
        self.run(sql20.format("touched_"), self.callback20)
        dup30 = set()
        self.run(sql30.format("touched_", ""), lambda res: dup30.add(res[0]) or self.callback30(res))
        self.run(sql30.format("", "touched_"), lambda res: res[0] in dup30 or dup30.add(res[0]) or self.callback30(res))
        self.run(sql40.format("touched_"), self.callback40)
        self.run(sql41.format("touched_"), self.callback41)
        dup50 = set()
        self.run(sql50.format("touched_", ""), lambda res: dup50.add(res[0]) or self.callback50(res))
        self.run(sql50.format("", "touched_"), lambda res: res[0] in dup50 or dup50.add(res[0]) or self.callback50(res))
        dup51 = set()
        self.run(sql51.format("touched_", ""), lambda res: dup51.add(res[0]) or self.callback51(res))
        self.run(sql51.format("", "touched_"), lambda res: res[0] in dup51 or dup51.add(res[0]) or self.callback51(res))
