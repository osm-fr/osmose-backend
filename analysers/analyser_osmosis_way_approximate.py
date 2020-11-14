#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2020                                 ##
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


#   B   |f
#    /----- C
#   /\  |
#  / r\ |
# /    \|
# A

sql10 = """
WITH
    points AS (
        SELECT
            id,
            tags->'{1}' AS type,
            (ST_DumpPoints(linestring)).geom AS geom4326,
            (ST_DumpPoints(ST_Transform(linestring, {4}))).geom AS geom,
            (ST_DumpPoints(ST_Transform(linestring, {4}))).path[1] AS index
        FROM
            {0}ways AS ways
        WHERE
            tags != ''::hstore AND
            tags?'{1}' AND tags->'{1}' IN ('{2}') AND
            ST_NPoints(linestring) >= 4
    ),
    distances AS (
        SELECT
            id, index, type,
            lead(geom4326) OVER (PARTITION BY id ORDER BY index) AS geom4326,
            lead(geom) OVER (PARTITION BY id ORDER BY index) AS geom,
            ST_Distance(geom, lead(geom) OVER (PARTITION BY id ORDER BY index)) dist,
            ST_Distance(geom, lead(geom, 2) OVER (PARTITION BY id ORDER BY index)) dist_h
        FROM
            points
            {5}
        WHERE
            {6}
            1 = 1
    ),
    distances2 AS (
        SELECT
            id, index, type, geom,
            dist AS dist_a,
            lead(dist) OVER (PARTITION BY id ORDER BY index) AS dist_b,
            dist_h
        FROM
            distances
    ),
    cos AS (
        SELECT
            id, index, type, geom, dist_a, dist_b,
            -- Subtracting π/2, we compute the angle of a radius of a tangential circle of first segment
            cos(
                -- Using cosine law in a triangle we compute the cosine angle of the middle point of way segments
                acos(GREATEST(-1, LEAST(1,
                      (dpow(dist_a, 2) + dpow(dist_b, 2) - dpow(dist_h, 2)) / (2 * dist_a * dist_b)
                )))
                - pi()/2
            ) AS rc
        FROM
            distances2
        WHERE
            index > 1 AND
            dist_h IS NOT NULL AND
            dist_a > 0 AND
            dist_b > 0 AND
            (dist_a > 70 OR dist_b > 70)
    ),
    rc AS (
        SELECT
            id, index, type, geom, dist_a, dist_b,
            -- We compute the radius of the circle tangential to first segment.
            -- Using cosine in a right-angled triangle based on the middle of the second segment.
            -- The hypotenuse of the triangle is the circle radius.
            (dist_a / 2) / rc AS rc_a,
            (dist_b / 2) / rc AS rc_b
        FROM
            cos
    )
SELECT
    id,
    ST_AsText(ST_Transform(geom, 4326)),
    round(GREATEST(
        -- Using Pythagoras we compute the last side of the right-angled triangle.
        -- The difference between this side length and the circle radius.
        rc_a - dsqrt(dpow(rc_a, 2) - dpow(dist_a / 2, 2)),
        rc_b - dsqrt(dpow(rc_b, 2) - dpow(dist_b / 2, 2))
    )) AS d,
    type,
    {3},
    index
FROM
    rc
WHERE
    GREATEST(
        rc_a - dsqrt(dpow(rc_a, 2) - dpow(dist_a / 2, 2)),
        rc_b - dsqrt(dpow(rc_b, 2) - dpow(dist_b / 2, 2))
    ) > 70
"""

sql10water1 = """
        LEFT JOIN (SELECT is_polygon, tags, linestring FROM ways) AS water ON
            water.is_polygon AND
            water.tags != ''::hstore AND
            water.tags?'natural' AND
            water.tags->'natural' = 'water' AND
            water.tags?'water' AND
            water.tags->'water' IN ('lake', 'lagoon', 'basin', 'reservoir') AND
            water.linestring && points.geom4326 AND
            ST_Intersects(ST_MakePolygon(water.linestring), points.geom4326)
"""

sql10water2 = """
        water.is_polygon IS NULL AND
"""

class Analyser_Osmosis_Way_Approximate(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        highway_values = ("motorway", "trunk", "primary", "secondary")
        if self.config.options and "osmosis_way_approximate" in self.config.options and self.config.options["osmosis_way_approximate"].get("highway"):
            highway_values = self.config.options["osmosis_way_approximate"].get("highway")
        self.tags = ( (10, "railway", ("rail",), '', ''),
                      (20, "waterway", ("river",), sql10water1, sql10water2),
                      (30, "highway", highway_values, '', ''),
                    )
        for t in self.tags:
            self.classs_change[t[0]] = self.def_class(item = 1190, level = 3, tags = ['geom', 'highway', 'railway', 'fix:imagery'],
                title = T_('Approximate geometry of {0}', t[1]),
                detail = T_(
'''Geometry seems to be draw crudely, there is a discrepancy between the
drawing and the real way especially in the curve.'''),
                fix = T_(
'''After checking orthophotos, add nodes or move existing nodes.'''),
                trap = T_(
'''On service ways, train stations, train workshops that may be either a
false positive'''),
                example = T_(
'''![](https://wiki.openstreetmap.org/w/images/9/9d/Osmose-eg-error-1190.png)

`railway=rail` crudely drawn.'''))

        self.callback10 = lambda res: {"class":res[4], "subclass":res[5], "data":[self.way_full, self.positionAsText], "text": T_("{0} deviation of {1}m", res[3], res[2])}

    def analyser_osmosis_full(self):
        for t in self.tags:
            self.run(sql10.format("", t[1], "', '".join(t[2]), t[0], self.config.options.get("proj"), t[3], t[4]), self.callback10)

    def analyser_osmosis_diff(self):
        for t in self.tags:
            self.run(sql10.format("touched_", t[1], "', '".join(t[2]), t[0], self.config.options.get("proj"), t[3], t[4]), self.callback10)
