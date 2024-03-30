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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    id,
    ST_AsText((ST_IsValidDetail(ST_MakePolygon(linestring))).location),
    (ST_IsValidDetail(ST_MakePolygon(linestring))).reason
FROM
    {0}ways
WHERE
    NOT is_polygon AND
    NOT (tags?'roller_coaster' AND tags->'roller_coaster' = 'track') AND -- permit self-intersecting ways
    NOT (tags?'highway' AND tags->'highway' = 'raceway') AND -- permit self-intersecting ways
    nodes[1] = nodes[array_length(nodes,1)] AND
    ST_NumPoints(linestring) > 3 AND
    ST_IsClosed(linestring) AND
    NOT ST_IsValid(ST_MakePolygon(linestring))
"""

sql20 = """
CREATE TEMP TABLE {0}_{1}_relation_linestrings AS
SELECT
  relations.id,
  ST_LineMerge(ST_Collect(linestring)) AS linestring
FROM
  {0}relations AS relations
  JOIN relation_members ON
    relation_members.relation_id = relations.id AND
    relation_members.member_type = 'W' AND
    relation_members.member_role = 'outer'
  JOIN {1}ways AS ways ON
    ways.id = relation_members.member_id AND
    ST_NumPoints(ways.linestring) >= 2
WHERE
  relations.tags?'type' AND
  relations.tags->'type' IN ('multipolygon', 'boundary')
GROUP BY
  relations.id
"""

sql21 = """
SELECT
    id,
    ST_AsText((ST_IsValidDetail(ST_MakePolygon(linestring))).location),
    (ST_IsValidDetail(ST_MakePolygon(linestring))).reason
FROM
    {0}_{1}_relation_linestrings
WHERE
    (ST_NumGeometries(linestring) IS NULL OR ST_NumGeometries(linestring) = 1) AND
    ST_NumPoints(linestring) > 3 AND
    ST_IsClosed(linestring) AND
    NOT ST_IsValid(ST_MakePolygon(linestring))
"""


sql30 = """
SELECT
    id,
    ST_AsText((ST_IsValidDetail(poly)).location),
    (ST_IsValidDetail(poly)).reason
FROM
    {0}multipolygons
WHERE
    NOT is_valid
"""


class Analyser_Osmosis_Polygon(Analyser_Osmosis):

    requires_tables_full = ['multipolygons']
    requires_tables_diff = ['touched_multipolygons']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''The polygon intersects itself. The marker points directly to the
error area of the crossing.'''),
            fix = T_(
'''Find where the polygon intersects itself (i.e. it forms an '8') and
correct geometry for a single loop (a '0') or by removing nodes or
changing the order of these nodes, by adding new nodes or by creating
multiple polygons.'''),
            trap = T_(
'''Make sure the nodes to move do not belong to other way.'''),
            example = {"en": "![](https://wiki.openstreetmap.org/w/images/9/9a/Osmose-eg-error-1040.png)"})
        self.classs_change[1] = self.def_class(item = 1040, level = 1, tags = ['geom', 'fix:chair'], title = T_('Invalid polygon'), **doc)
        self.classs_change[2] = self.def_class(item = 1040, level = 1, tags = ['geom', 'fix:chair'], title = T_('Invalid multipolygon'), **doc)
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "text": {"en": res[2]}}
        self.callback20 = lambda res: {"class":2, "subclass": 0, "data":[self.relation, self.positionAsText], "text": {"en": res[2]}}
        self.callback30 = lambda res: {"class":2, "subclass": 1, "data":[self.relation, self.positionAsText], "text": {"en": res[2]}}

    def analyser_osmosis_full(self):
        self.run(sql10.format(""), self.callback10)
        self.run(sql20.format("", ""))
        self.run(sql21.format("", ""), self.callback20)
        self.run(sql30.format(""), self.callback30)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_"), self.callback10)
        self.run(sql20.format("touched_", ""))
        self.run(sql21.format("touched_", ""), self.callback20)
        self.run(sql20.format("not_touched_", "touched_"))
        self.run(sql21.format("not_touched_", "touched_"), self.callback20)
        self.run(sql30.format("touched_"), self.callback30)
