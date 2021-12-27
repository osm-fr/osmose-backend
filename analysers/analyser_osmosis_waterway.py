#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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
    rb.id,
    ST_AsText(way_locate(rb.linestring))
FROM
    ways AS rb
    LEFT JOIN (
        SELECT
            id,
            linestring
        FROM
            ways
        WHERE
            tags != ''::hstore AND
            tags?'waterway' AND
            tags->'waterway' IN ('river', 'canal', 'stream')
        ) AS ww ON
        ST_Intersects(ST_MakePolygon(rb.linestring), ww.linestring)
WHERE
    rb.tags != ''::hstore AND
    (
        (rb.tags?'waterway' AND rb.tags->'waterway' = 'riverbank') OR
        (rb.tags?'water' AND rb.tags->'water' = 'river')
    ) AND
    rb.is_polygon AND
    ww.id IS NULL
"""

sql20 = """
CREATE TEMP TABLE water_ends AS
SELECT
    id,
    nodes[array_length(nodes,1)] AS start,
    nodes[array_length(nodes,1)] AS end,
    tags->'waterway' AS waterway,
    linestring
FROM
    ways AS ways
WHERE
    tags != ''::hstore AND
    tags?'waterway' AND
    tags->'waterway' IN ('stream', 'river')
"""

sql21 = """
CREATE INDEX idx_water_ends_linestring ON water_ends USING GIST(linestring)
"""

sql22 = """
CREATE TEMP TABLE connx AS
SELECT
    ww.id,
    ww.end,
    ww.waterway
FROM
    water_ends AS ww
    JOIN way_nodes ON
        way_nodes.node_id = ww.end AND
        way_nodes.way_id != ww.id
    JOIN ways ON
        ways.id = way_nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags?'waterway' AND
        ways.tags->'waterway' IN ('stream', 'river', 'canal', 'drain', 'ditch')
"""

sql23 = """
CREATE TEMP TABLE coastline_sinkhole AS
SELECT
    ww.id,
    ww.end,
    ww.waterway
FROM
    water_ends AS ww
    JOIN way_nodes ON
        way_nodes.node_id = ww.end AND
        way_nodes.way_id != ww.id
    JOIN ways AS ways ON
        ways.id = way_nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags?'natural' AND
        ways.tags->'natural' IN ('coastline', 'sinkhole')
UNION ALL
SELECT
    ww.id,
    ww.end,
    ww.waterway
FROM
    water_ends AS ww
    JOIN nodes ON
        nodes.id = ww.end AND
        nodes.tags != ''::hstore AND
        nodes.tags?'natural' AND
        nodes.tags->'natural' IN ('sinkhole')
"""

sql24 = """
SELECT
    t.id,
    ST_AsText(nodes.geom),
    waterway
FROM
    (
        SELECT
            id,
            "end",
            waterway
        FROM
            water_ends
    EXCEPT
        SELECT
            *
        FROM
            coastline_sinkhole
    EXCEPT
        SELECT
            *
        FROM
            connx
    ) AS t
    JOIN nodes ON
        nodes.id = t."end"
"""

class Analyser_Osmosis_Waterway(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1220, level = 3, tags = ['waterway', 'fix:imagery'],
            title = T_('River bank without river'),
            detail = T_(
'''There is one `natural=water` + `water=river` (or `waterway=riverbank`)
but there is no `waterway=river|canal|stream` inside it.'''),
            fix = T_(
'''After checking, create a "river" line inside the river bank polygon or
eliminate the river bank polygon.'''))
        detail = T_(
'''A `waterway=river` or a `waterway=stream` is an oriented way. The
water must flow into another waterway or meet a `natural=coastline`.''')
        fix = T_(
'''Link the waterway or invert its flow direction.''')
        self.classs[2] = self.def_class(item = 1220, level = 2, tags = ['waterway', 'fix:imagery'],
            title = T_('Unconnected river or wrong way flow'),
            detail = detail,
            fix = fix)
        self.classs[3] = self.def_class(item = 1220, level = 3, tags = ['waterway', 'fix:imagery'],
            title = T_('Unconnected stream or wrong way flow'),
            detail = detail,
            fix = fix)

        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2 if res[2] == "river" else 3, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10, self.callback10)
        self.run(sql20)
        self.run(sql21)
        self.run(sql22)
        self.run(sql23)
        self.run(sql24, self.callback20)
