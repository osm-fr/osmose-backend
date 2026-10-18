#!/usr/bin/env python
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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE boundary AS
SELECT
    id,
    linestring,
    array_agg(boundary) AS boundaries,
    array_agg(DISTINCT admin_level ORDER BY admin_level) AS admin_levels
FROM (
(
SELECT
    ways.id,
    ways.linestring,
    relations.tags->'boundary' AS boundary,
    relations.tags->'admin_level' AS admin_level
FROM
    relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W'
    JOIN ways ON
        ways.id = relation_members.member_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'boundary' AND
    relations.tags?'boundary'
)
UNION ALL
(
SELECT
    ways.id,
    ways.linestring,
    tags->'boundary' AS boundary,
    tags->'admin_level' AS admin_level
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'type' AND
    tags->'type' = 'boundary' AND
    tags?'boundary'
)
) AS t
GROUP BY
    id,
    linestring
"""

sql12 = """
CREATE INDEX boundary_linestring ON boundary USING GIST(linestring)
"""

sql20 = """
SELECT
    b1.id,
    b2.id,
    ST_ASText(ST_GeometryN(ST_Multi(ST_Intersection(b1.linestring, b2.linestring)), 1))
FROM
    boundary AS b1
    JOIN boundary AS b2 ON
        b1.boundaries && b2.boundaries AND
        b1.linestring && b2.linestring AND
        b1.id < b2.id AND
        -- Ways not linked
        NOT ST_Touches(b1.linestring, b2.linestring) AND
        -- Ways share inner space
        ST_Crosses(b1.linestring, b2.linestring) AND
        -- Allowed intersections
        ({0} IS NULL OR NOT {0} <@ (SELECT array_agg(DISTINCT a ORDER BY a) FROM (SELECT unnest(b1.admin_levels) UNION SELECT unnest(b2.admin_levels)) AS t(a)))
"""

class Analyser_Osmosis_Boundary_Intersect(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        admin_level_intersection = self.config.options and self.config.options.get("allow_boundary_admin_level_intersection", None)
        self.admin_level_intersection = "array['{}']".format("','".join(map(str, admin_level_intersection))) if admin_level_intersection else "NULL"
        self.classs[1] = self.def_class(item = 1060, level = 2, tags = ['boundary', 'geom', 'fix:chair'],
            title = T_('Boundary intersection'),
            detail = T_(
'''Borders crossing each other.'''),
            fix = T_(
'''Check the type of border and keep the best one or merge them.'''),
            trap = T_(
'''The borders are part of relations which normally form a loop.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/6/69/Osmose-eg-error-1060.png)

Two definitions of the same border.'''))
        self.callback20 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql12)
        self.run(sql20.format(self.admin_level_intersection), self.callback20)
