#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

sql10 = """
SELECT
    w1.id,
    w2.id,
    ST_AsText(ST_Centroid(ST_Envelope(w1.linestring)))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'inner'
    JOIN {1}ways AS w1 ON
        w1.id = relation_members.member_id AND
        w1.is_polygon AND
        w1.tags = ''::hstore
    JOIN {2}ways AS w2 ON
        w1.id != w2.id AND
        w2.is_polygon AND
        w1.linestring && w2.linestring AND
        w2.tags ?| ARRAY['landuse', 'aeroway', 'natural', 'water'] AND
        w1.nodes @> w2.nodes AND w1.nodes <@ w2.nodes  -- check that both ways contain the same nodes
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon'
"""

sql20 = """
SELECT
    relations.id,
    ways.id,
    ST_AsText(way_locate(ways.linestring)),
    relations.tags->'landuse' rl,
    ways.tags->'landuse' wl,
    relations.tags->'natural' rn,
    ways.tags->'natural' wn,
    relations.tags->'waterway' rw,
    ways.tags->'waterway' ww,
    relations.tags->'building' rb,
    ways.tags->'building' wb,
    COALESCE(relations.tags->'landuse', relations.tags->'natural', relations.tags->'waterway', relations.tags->'building')
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role IN ('', 'outer')
    JOIN {1}ways AS ways ON
        ways.id = relation_members.member_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon' AND
    (
        relations.tags?'landuse' AND
        ways.tags?'landuse' AND
        ways.tags->'landuse' != (relations.tags->'landuse')
    ) OR (
        relations.tags?'natural' AND
        relations.tags->'natural' IN ('bay', 'beach', 'fell', 'grassland', 'glacier', 'heath', 'mud', 'sand', 'scree', 'scrub', 'sinkhole', 'water', 'wetland', 'wood') AND
        ways.tags?'natural' AND
        ways.tags->'natural' IN ('bay', 'beach', 'fell', 'grassland', 'glacier', 'heath', 'mud', 'sand', 'scree', 'scrub', 'sinkhole', 'water', 'wetland', 'wood') AND
        ways.tags->'natural' != (relations.tags->'natural')
    ) OR (
        relations.tags?'waterway' AND
        relations.tags->'waterway' IN ('boatyard', 'dock', 'riverbank') AND
        ways.tags?'waterway' AND
        ways.tags->'waterway' IN ('boatyard', 'dock', 'riverbank') AND
        ways.tags->'waterway' != (relations.tags->'waterway')
    ) OR (
        relations.tags?'building' AND
        ways.tags?'building' AND
        ways.tags->'building' != (relations.tags->'building')
    )
"""

sql30 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    string_agg(landuse, ',') AS landuse,
    string_agg("natural", ',') AS "natural",
    string_agg(waterway, ',') AS waterway,
    string_agg(building, ',') AS building
FROM
(
    SELECT
        relations.id,
        ways.tags->'landuse' AS landuse,
        ways.tags->'natural' AS "natural",
        ways.tags->'waterway' AS waterway,
        ways.tags->'building' AS building
    FROM
        {0}relations AS relations
        JOIN relation_members ON
            relation_members.relation_id = relations.id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role IN ('', 'outer')
        JOIN {1}ways AS ways ON
            ways.id = relation_members.member_id
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'multipolygon' AND
        NOT relations.tags?'landuse' AND
        NOT relations.tags?'natural' AND
        NOT relations.tags?'waterway' AND
        NOT relations.tags?'building' AND
        ((ways.tags->'landuse') IS NOT NULL OR (ways.tags->'natural') IS NOT NULL OR (ways.tags->'waterway') IS NOT NULL OR (ways.tags->'building') IS NOT NULL)
    GROUP BY
        relations.id,
        ways.tags->'landuse',
        ways.tags->'natural',
        ways.tags->'waterway',
        ways.tags->'building'
) AS t
GROUP BY
    id
HAVING
    COUNT(*) > 1
"""

sql40 = """
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring)),
    ways.tags->'landuse',
    ways.tags->'natural',
    ways.tags->'waterway',
    ways.tags->'building',
    COALESCE(ways.tags->'landuse', ways.tags->'natural', ways.tags->'waterway', ways.tags->'building')
FROM
    {0}ways AS ways
    LEFT JOIN relation_members ON
        relation_members.member_id = ways.id AND
        relation_members.member_type = 'W'
WHERE
    (
        ways.tags?'landuse' OR
        (ways.tags?'natural' AND ways.tags->'natural' in ('bay', 'beach', 'fell', 'grassland', 'glacier', 'heath', 'mud', 'sand', 'scree', 'scrub', 'sinkhole', 'water', 'wetland', 'wood')) OR
        (ways.tags?'waterway' AND ways.tags->'waterway' in ('boatyard', 'dock', 'riverbank')) OR
        ways.tags?'building'
    ) AND
    NOT ways.is_polygon AND
    relation_members.member_id IS NULL
"""

class Analyser_Osmosis_Relation_Multipolygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1170", "level": 3, "tag": ["relation", "geom", "fix:chair"], "desc": T_(u"Double inner polygon") }
        self.classs_change[2] = {"item":"1170", "level": 2, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"Inconsistant multipolygon nature with members nature") }
        self.classs_change[3] = {"item":"1170", "level": 2, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"Inconsistant multipolygon member nature") }
        self.classs_change[4] = {"item":"1170", "level": 1, "tag": ["relation", "geom", "fix:chair"], "desc": T_(u"Should be polygon or part of multipolygon") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "subclass":self.stablehash(res[11]), "data":[self.relation_full, self.way_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "%s=(%s,%s)"%k, filter(lambda k: k[1], (("landuse",res[3],res[4]), ("natural",res[5],res[6]), ("waterway",res[7],res[8]), ("building",res[9],res[10])))))}
        }
        self.callback30 = lambda res: {"class":3, "subclass":1, "data":[self.relation_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "%s=(%s)"%k, filter(lambda k: k[1], (("landuse",res[2]), ("natural",res[3]), ("waterway",res[4]), ("building",res[5])))))}
        }
        self.callback40 = lambda res: {"class":4, "subclass":self.stablehash(res[6]), "data":[self.way_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "%s=%s"%k, filter(lambda k: k[1], (("landuse",res[2]), ("natural",res[3]), ("waterway",res[4]), ("building",res[5])))))}
        }

    def analyser_osmosis_all(self):
        self.run(sql10.format("", "", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)

    def analyser_osmosis_touched(self):
        dup = set()
        self.run(sql10.format("touched_", "", ""), lambda res: dup.add((res[0], res[1])) or self.callback10(res))
        self.run(sql10.format("", "touched_", ""), lambda res: (res[0], res[1]) in dup or dup.add((res[0], res[1])) or self.callback10(res))
        self.run(sql10.format("", "", "touched_"), lambda res: (res[0], res[1]) in dup or dup.add((res[0], res[1])) or self.callback10(res))
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("", "touched_"), self.callback20)
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("", "touched_"), self.callback30)
        self.run(sql40.format("touched_"), self.callback40)
