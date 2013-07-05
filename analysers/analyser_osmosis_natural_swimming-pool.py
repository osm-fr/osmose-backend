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

sql10 = """
SELECT
    DISTINCT ON (w.id)
    w.id,
    ST_AsText(way_locate(w.linestring))
FROM
    (
    SELECT
        geom
    FROM
        (
        SELECT
            (ST_Dump(poly)).geom AS geom
        FROM
            (
            SELECT
                ST_Union(ST_Buffer(ways.linestring,5e-3,'quad_segs=2')) AS poly
            FROM
                ways
            WHERE
                ways.tags?'natural' AND ways.tags->'natural' = 'water' AND
                ways.tags?'source' AND ways.tags->'source' ILIKE '%cadastre%' AND
                NOT ways.tags?'name' AND
                NOT ways.tags?'landuse' AND
                array_length(ways.nodes,1) = 5 AND
                is_polygon AND
                ST_Area(ST_MakePolygon(ways.linestring)) < 7e-9
            GROUP BY
                user_id,
                version,
                ways.tags->'source'
            ) AS water
        ) AS buffer
    WHERE
        ST_Area(geom) > 1e-4
    ) AS geom_union
    JOIN ways AS w ON
        w.tags?'natural' AND w.tags->'natural' = 'water' AND
        w.tags?'source' AND w.tags->'source' ILIKE '%cadastre%' AND
        NOT w.tags?'name' AND
        NOT w.tags?'landuse' AND
        is_polygon AND
        ST_Area(ST_MakePolygon(w.linestring)) < 21e-9 AND
        ST_Intersects(w.linestring, geom_union.geom)
;
"""

class Analyser_Osmosis_Natural_SwimmingPool(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"3080", "level": 3, "tag": ["tag", "fix:imagery"], "desc": T_(u"Swimming-pool, reservoir, pond as natural=water") }

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":[
            {"-":["natural"], "+":{"leisure":"swimming_pool"}},
            {"-":["natural"], "+":{"leisure":"swimming_pool", "access":"private"}},
            {"-":["natural"], "+":{"landuse":"reservoir"}},
            {"-":["natural"], "+":{"landuse":"basin"}},
            {"-":["natural"], "+":{"landuse":"pond"}},
            {"+":{"water":"pond"}},
            ]})
