#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Didier Marchand  <****@free.fr> 2013                       ##
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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE cvqnotag AS
SELECT
    ways.id,
    ways.linestring
FROM
    ways
    LEFT JOIN relation_members ON
        relation_members.member_id = ways.id AND
        relation_members.member_type = 'W'
WHERE
    relation_members.member_id IS NULL AND
    ways.tags = ''::hstore AND
    ST_NPoints(ways.linestring) > 1 AND
    ST_IsValid(linestring)
"""

sql11 = """
CREATE INDEX cvqnotag_linestring_idx ON cvqnotag USING gist(linestring)
"""

sql12 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(b1.linestring))
FROM
    {0}cvqnotag AS b1,
    {1}cvqnotag AS b2
WHERE
    ({2} OR b1.id > b2.id) AND
    b1.linestring && b2.linestring AND
    ST_Equals(b1.linestring, b2.linestring)
"""

sql20 = """
CREATE TEMP TABLE cvq AS
SELECT
    id,
    linestring,
    tags - ARRAY['source', 'created_by'] AS lsttag
FROM
    ways AS ways
WHERE
    tags != ''::hstore AND
    tags ?| ARRAY['natural', 'landuse', 'waterway', 'amenity', 'highway', 'leisure', 'barrier', 'railway', 'addr:interpolation', 'man_made', 'power', 'aeroway'] AND
    ST_NPoints(ways.linestring) > 1 AND
    ST_IsValid(linestring)
"""

sql21 = """
CREATE INDEX cvq_linestring_idx ON cvq USING gist(linestring)
"""

sql22 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(b1.linestring)),
--    ((b1.lsttag @> b2.lsttag ) AND (b2.lsttag @> b1.lsttag ))
    b1.lsttag = b2.lsttag
FROM
    {0}cvq AS b1,
    {1}cvq AS b2
WHERE
    ({2} OR b1.id > b2.id) AND
    b1.linestring && b2.linestring AND
    ST_Equals(b1.linestring, b2.linestring) AND
    (
        (b1.lsttag->'natural' = b2.lsttag->'natural') OR
        (b1.lsttag->'landuse' = b2.lsttag->'landuse') OR
        (b1.lsttag->'waterway' = b2.lsttag->'waterway') OR
        (b1.lsttag->'amenity' = b2.lsttag->'amenity') OR
        (b1.lsttag->'highway' = b2.lsttag->'highway') OR
        (b1.lsttag->'leisure' = b2.lsttag->'leisure') OR
        (b1.lsttag->'barrier' = b2.lsttag->'barrier') OR
        (b1.lsttag->'railway' = b2.lsttag->'railway') OR
        (b1.lsttag->'addr:interpolation' = b2.lsttag->'addr:interpolation') OR
        (b1.lsttag->'man_made' = b2.lsttag->'man_made') OR
        (b1.lsttag->'aeroway' = b2.lsttag->'aeroway') OR
        (b1.lsttag->'power' = b2.lsttag->'power')
    ) AND
    (NOT b1.lsttag?'layer' AND NOT b2.lsttag?'layer' OR b1.lsttag->'layer' = b2.lsttag->'layer') AND
    (NOT b1.lsttag?'level' AND NOT b2.lsttag?'level' OR b1.lsttag->'level' = b2.lsttag->'level') AND
    (NOT b1.lsttag?'min_height' AND NOT b2.lsttag?'min_height' OR b1.lsttag->'min_height' = b2.lsttag->'min_height') AND
    (NOT b1.lsttag?'ele' AND NOT b2.lsttag?'ele' OR b1.lsttag->'ele' = b2.lsttag->'ele')
"""

sql30 = """
CREATE TEMP TABLE onlynodesfull AS
SELECT
    id,
    nodes.tags - ARRAY['source', 'created_by', 'converted_by', 'attribution'] AS tags,
    geom
FROM
    nodes
WHERE
    nodes.tags != ''::hstore AND
    nodes.tags - ARRAY['source', 'created_by', 'converted_by', 'attribution'] != ''::hstore
"""

sql31 = """
CREATE INDEX onlynodesfull_idx ON onlynodesfull USING gist(geom);
"""

sql32 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(b1.geom),
    b1.tags = b2.tags
FROM
    {0}onlynodesfull AS b1,
    {1}onlynodesfull AS b2
WHERE
    b1.id > b2.id AND
    b1.geom && b2.geom AND
    ST_Equals(b1.geom, b2.geom) AND -- Need ST_Equals as && on bbox is not exact
    -- fix false positive in denmark
    NOT (b1.tags?'osak:identifier' AND b2.tags?'osak:identifier' AND b1.tags->'osak:identifier' != (b2.tags->'osak:identifier')) AND
    (b1.tags @> b2.tags OR b2.tags @> b1.tags) AND
    (NOT b1.tags?'layer' AND NOT b2.tags?'layer' OR b1.tags->'layer' = b2.tags->'layer') AND
    (NOT b1.tags?'level' AND NOT b2.tags?'level' OR b1.tags->'level' = b2.tags->'level') AND
    (NOT b1.tags?'min_height' AND NOT b2.tags?'min_height' OR b1.tags->'min_height' = b2.tags->'min_height') AND
    (NOT b1.tags?'ele' AND NOT b2.tags?'ele' OR b1.tags->'ele' = b2.tags->'ele')
"""

sql40 = """
SELECT
  array_agg('N' || id::text) AS ids,
  ST_AsText(geom)
FROM
  nodes
WHERE
  tags - ARRAY['source', 'created_by', 'converted_by', 'attribution'] = ''::hstore
GROUP BY
  geom
HAVING
  ST_NPoints(ST_Union(geom)) = 1 AND -- recheck geom equality as GROUP BY geom is not excat
  count(*) > 1
"""

class Analyser_Osmosis_Duplicated_Geotag(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 1230, level = 1, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated way geometry and tags'),
            fix = T_(
'''Delete one of the two objects.'''))
        self.classs_change[2] = self.def_class(item = 1230, level = 2, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated way geometry but different tags'),
            fix = T_(
'''Compare tags and delete object or merge them.'''))
        self.classs_change[3] = self.def_class(item = 1230, level = 1, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated node geometry and tags'))
        self.classs_change[4] = self.def_class(item = 1230, level = 2, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated node geometry but different tags'))
        self.classs[5] = self.def_class(item = 1230, level = 3, tags = ['geom', 'fix:chair'],
            title = T_('Duplicated node without tag'))

        self.callback10 = lambda res: {"class":1, "data":[self.way, self.way, self.positionAsText]}
        self.callback20 = lambda res: {"class":1 if res[3] else 2, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3 if res[3] else 4, "data":[self.node_full, self.node_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql40, lambda res: {"class":5, "data":[self.array_full, self.positionAsText]})

    def analyser_osmosis_full(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12.format("", "", "false"), self.callback10)

        self.run(sql20)
        self.run(sql21)
        self.run(sql22.format("","", "false"), self.callback20)

        self.run(sql30)
        self.run(sql31)
        self.run(sql32.format("", ""), self.callback30)

    def analyser_osmosis_diff(self):
        self.run(sql10)
        self.run(sql11)
        self.create_view_touched("cvqnotag", "W")
        self.create_view_not_touched("cvqnotag", "W")
        self.run(sql12.format("touched_", "touched_", "false"), self.callback10)
        self.run(sql12.format("touched_", "not_touched_", "true"), self.callback10)

        self.run(sql20)
        self.run(sql21)
        self.create_view_touched("cvq", "W")
        self.create_view_not_touched("cvq", "W")
        self.run(sql22.format("touched_","touched_", "false"), self.callback20)
        self.run(sql22.format("touched_","not_touched_", "true"), self.callback20)

        self.run(sql30)
        self.run(sql31)
        self.create_view_touched("onlynodesfull", "N")
        self.create_view_not_touched("onlynodesfull", "N")
        self.run(sql32.format("touched_", "not_touched_"), self.callback30)
        self.run(sql32.format("", "touched_"), self.callback30)
