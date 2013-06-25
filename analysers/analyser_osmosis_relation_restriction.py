#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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
CREATE TEMP TABLE restrictions AS
SELECT
    id,
    tags,
    SUM(CASE WHEN member_role = 'from' AND member_type = 'W' THEN 1 ELSE 0 END) AS nwfrom,
    SUM(CASE WHEN member_role = 'from' AND member_type != 'W' THEN 1 ELSE 0 END) AS nofrom,
    SUM(CASE WHEN member_role = 'to' AND member_type = 'W' THEN 1 ELSE 0 END) AS nwto,
    SUM(CASE WHEN member_role = 'to' AND member_type != 'W' THEN 1 ELSE 0 END) AS noto,
    SUM(CASE WHEN member_role = 'via' AND member_type = 'N' THEN 1 ELSE 0 END) AS nnvia,
    SUM(CASE WHEN member_role = 'via' AND member_type = 'W' THEN 1 ELSE 0 END) AS nwvia,
    SUM(CASE WHEN member_role = 'via' AND member_type = 'R' THEN 1 ELSE 0 END) AS nrvia,
    FALSE AS bad_member,
    FALSE AS bad_continuity,
    NULL::INTEGER AS direction
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_members.relation_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'restriction' AND
    relations.tags?'restriction'
GROUP BY
    relations.id,
    relations.tags
"""

sql10 = """
(
SELECT
    id,
    ST_AsText(relation_locate(id))
FROM
    restrictions
WHERE
    tags->'restriction' NOT IN ('no_entry', 'no_exit') AND
    NOT (
        nwfrom = 1 AND
        nofrom = 0 AND
        nwto = 1 AND
        noto = 0 AND
        ((nnvia = 1 AND nwvia = 0) OR (nnvia = 0 AND nwvia > 0)) AND
        nrvia = 0
    )
) UNION (
SELECT
    id,
    ST_AsText(relation_locate(id))
FROM
    restrictions
WHERE
    tags->'restriction' = 'no_entry' AND
    NOT (
        nwfrom >= 1 AND
        nofrom = 0 AND
        nwto = 1 AND
        noto = 0 AND
        ((nnvia = 1 AND nwvia = 0) OR (nnvia = 0 AND nwvia > 0)) AND
        nrvia = 0
    )
) UNION (
SELECT
    id,
    ST_AsText(relation_locate(id))
FROM
    restrictions
WHERE
    tags->'restriction' = 'no_exit' AND
    NOT (
        nwfrom = 1 AND
        nofrom = 0 AND
        nwto >= 1 AND
        noto = 0 AND
        ((nnvia = 1 AND nwvia = 0) OR (nnvia = 0 AND nwvia > 0)) AND
        nrvia = 0
    )
)
"""

sql20 = """
CREATE TEMP TABLE bad_member AS
SELECT
    restrictions.id AS rid,
    ways.id AS wid,
    ways.linestring
FROM
    restrictions
    JOIN relation_members ON
        restrictions.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role IN ('from', 'via', 'to')
    JOIN ways ON
        ways.id = relation_members.member_id AND
        NOT ways.tags?'highway'
WHERE
    nwfrom = 1 AND
    nofrom = 0 AND
    nwto = 1 AND
    noto = 0 AND
    ((nnvia = 1 AND nwvia = 0) OR (nnvia = 0 AND nwvia > 0)) AND
    nrvia = 0
"""

sql21 = """
UPDATE
    restrictions
SET
    bad_member = TRUE
FROM
    bad_member
WHERE
    restrictions.id = bad_member.rid
"""

sql22 = """
SELECT
    rid,
    wid,
    ST_AsText(way_locate(linestring))
FROM
    bad_member
"""

sql30 = """
CREATE TEMP TABLE bad_continuity AS
SELECT
    restrictions.id AS rid
FROM
    restrictions
    JOIN relation_members ON
        restrictions.id = relation_members.relation_id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role IN ('from', 'via', 'to')
    JOIN ways ON
        ways.id = relation_members.member_id AND
        ways.tags?'highway'
WHERE
    nwfrom = 1 AND
    nofrom = 0 AND
    nwto = 1 AND
    noto = 0 AND
    ((nnvia = 1 AND nwvia = 0) OR (nnvia = 0 AND nwvia > 0)) AND
    nrvia = 0 AND
    NOT bad_member
GROUP BY
    restrictions.id
HAVING
    ST_NumGeometries(ST_LineMerge(ST_Collect(ways.linestring))) > 1
"""

sql31 = """
UPDATE
    restrictions
SET
    bad_continuity = TRUE
FROM
    bad_continuity
WHERE
    restrictions.id = bad_continuity.rid
"""

sql32 = """
SELECT
    rid,
    ST_AsText(relation_locate(rid))
FROM
    bad_continuity
"""

sql40 = """
SELECT
    restrictions.id,
    ways.id,
    ST_AsText(way_locate(ways.linestring))
FROM
    restrictions
    JOIN relation_members AS rmfrom ON
        restrictions.id = rmfrom.relation_id AND
        rmfrom.member_role = 'from'
    JOIN ways ON
        ways.id = rmfrom.member_id AND
        ways.tags?'oneway' AND
        ways.tags->'oneway' = 'yes'
    JOIN relation_members AS rmvia ON
        restrictions.id = rmvia.relation_id AND
        rmvia.member_role = 'via'
    JOIN nodes AS via ON
        via.id = rmvia.member_id
WHERE
    nwfrom = 1 AND
    nofrom = 0 AND
    nwto = 1 AND
    noto = 0 AND
    (nnvia = 1 AND nwvia = 0) AND
    nrvia = 0 AND
    NOT bad_member AND
    NOT bad_continuity AND
    ways.nodes[array_length(ways.nodes,1)] != via.id
"""

sql50 = """
CREATE TEMP TABLE direction AS
SELECT
    restrictions.id AS rid,
    restrictions.tags->'restriction' AS type,
    (CAST(degrees(
        CASE
            WHEN
                ST_Distance(COALESCE(nodes.geom, ways.linestring), ST_PointN(from_.linestring,1)) <
                ST_Distance(COALESCE(nodes.geom, ways.linestring), ST_PointN(from_.linestring,ST_NPoints(from_.linestring)))
            THEN
                ST_Azimuth(ST_PointN(from_.linestring,2), ST_PointN(from_.linestring,1))
            ELSE
                ST_Azimuth(ST_PointN(from_.linestring,ST_NPoints(from_.linestring)-1), ST_PointN(from_.linestring,ST_NPoints(from_.linestring)))
        END -
        CASE
            WHEN
                ST_Distance(COALESCE(nodes.geom, ways.linestring), ST_PointN(to_.linestring,1)) <
                ST_Distance(COALESCE(nodes.geom, ways.linestring), ST_PointN(to_.linestring,ST_NPoints(to_.linestring)))
            THEN
                ST_Azimuth(ST_PointN(to_.linestring,1), ST_PointN(to_.linestring,2))
            ELSE
                ST_Azimuth(ST_PointN(to_.linestring,ST_NPoints(to_.linestring)), ST_PointN(to_.linestring,ST_NPoints(to_.linestring)-1))
        END
    ) AS INTEGER) + 360*2) % 360 - 180 AS a
FROM
    restrictions
    JOIN relation_members AS rmfrom ON
        restrictions.id = rmfrom.relation_id AND
        rmfrom.member_role = 'from'
    JOIN ways AS from_ ON
        from_.id = rmfrom.member_id
    JOIN relation_members AS rmto ON
        restrictions.id = rmto.relation_id AND
        rmto.member_role = 'to'
    JOIN ways AS to_ ON
        to_.id = rmto.member_id
    LEFT JOIN relation_members AS rmwvia ON
        restrictions.id = rmwvia.relation_id AND
        rmwvia.member_role = 'via' AND
        rmwvia.member_type = 'W'
    LEFT JOIN ways ON
        ways.id = rmwvia.member_id
    LEFT JOIN relation_members AS rmnvia ON
        restrictions.id = rmnvia.relation_id AND
        rmnvia.member_role = 'via' AND
        rmnvia.member_type = 'N'
    LEFT JOIN nodes ON
        nodes.id = rmnvia.member_id
WHERE
    nwfrom = 1 AND
    nofrom = 0 AND
    nwto = 1 AND
    noto = 0 AND
    (nnvia = 1 AND nwvia = 0) AND
    nrvia = 0 AND
    NOT bad_member
"""

sql51 = """
UPDATE
    restrictions
SET
    direction = a
FROM
    direction
WHERE
    restrictions.id = direction.rid
"""

sql52 = """
SELECT
    rid,
    ST_AsText(relation_locate(rid))
FROM
    direction
WHERE
    (type IN ('only_straight_on', 'no_straight_on') AND abs(a) < 180-60) OR
    (type IN ('only_left_turn', 'no_left_turn') AND (a > 0 OR a < -170)) OR
    (type IN ('only_right_turn', 'no_right_turn') AND (a < 0 OR a > 170)) OR
    (type IN ('no_u_turn') AND abs(a) > 100)
ORDER BY
    type
"""

class Analyser_Osmosis_Relation_Restriction(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item": 3180, "level": 2, "tag": ["relation", "restriction", "fix:survey"], "desc":{"fr": u"Relation restriction, nombre de membres incorrect", "en": u"Restriction relation, number of members incorrect", "es": u"Restricción de relación, número de miembros incorrecto"} }
        self.classs_change[2] = {"item": 3180, "level": 2, "tag": ["relation", "restriction", "fix:chair"], "desc":{"fr": u"Relation restriction, membre de mauvais type", "en": u"Restriction relation, Bad member type", "es": u"Restricción de relación, tipo de miembros incorrecto"} }
        self.classs_change[3] = {"item": 3180, "level": 2, "tag": ["relation", "restriction", "fix:chair"], "desc":{"fr": u"Chemin de la relation restriction non connexe", "en": u"Unconnected restriction relation ways", "es": u"Vías de restricción de relación inconexas"} }
        self.classs_change[4] = {"item": 3180, "level": 2, "tag": ["relation", "restriction", "fix:survey"], "desc":{"fr": u"Relation restriction, mauvais sens de sens unique sur le membre from", "en": u"Restriction relation, bad oneway direction on from member", "es": u"Restricción de relación, dirección en un sentido incorrecta de un miembro"} }
        self.classs_change[5] = {"item": 3180, "level": 2, "tag": ["relation", "restriction", "fix:survey"], "desc":{"fr": u"La restriction ne correspond pas à la topologie", "en": u"Restriction doesn't match topology", "es": u"La restricción no concuerda con la tipología"} }
        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText] }
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.way_full, self.positionAsText] }
        self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.positionAsText] }
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.way_full, self.positionAsText] }
        self.callback50 = lambda res: {"class":5, "data":[self.relation_full, self.positionAsText] }

    def analyser_osmosis_all(self):
        self.run(sql00.format(""))
        self.run(sql10, self.callback10)
        self.run(sql20)
        self.run(sql21)
        self.run(sql22, self.callback20)
        self.run(sql30)
        self.run(sql31)
        self.run(sql32, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50)
        self.run(sql51)
        self.run(sql52, self.callback50)

    def analyser_osmosis_touched(self):
        self.run(sql00.format("touched_"))
        self.run(sql10, self.callback10)
        self.run(sql20)
        self.run(sql21)
        self.run(sql22, self.callback20)
        self.run(sql30)
        self.run(sql31)
        self.run(sql32, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50)
        self.run(sql51)
        self.run(sql52, self.callback50)
