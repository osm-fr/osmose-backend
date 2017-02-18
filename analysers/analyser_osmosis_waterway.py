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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    rb.id,
    ST_AsText(way_locate(rb.linestring))
FROM
    {0}ways AS rb
    LEFT JOIN (
        SELECT
            id,
            linestring
        FROM
            {1}ways
        WHERE
            tags != ''::hstore AND
            tags?'waterway' AND
            tags->'waterway' IN ('river', 'canal', 'stream')
        ) AS ww ON
        ST_Intersects(ST_MakePolygon(rb.linestring), ww.linestring)
WHERE
    rb.tags != ''::hstore AND
    rb.tags?'waterway' AND
    rb.tags->'waterway' = 'riverbank' AND
    rb.is_polygon AND
    ww.id IS NULL
"""

sql20 = """
CREATE TEMP TABLE {0}water_ends AS
SELECT
    id,
    nodes[array_length(nodes,1)] AS start,
    nodes[array_length(nodes,1)] AS end,
    linestring
FROM
    {0}ways AS ways
WHERE
    tags != ''::hstore AND
    tags?'waterway' AND
    tags->'waterway' IN ('stream', 'river')
"""

sql21 = """
CREATE INDEX idx_{0}water_ends_linestring ON {0}water_ends USING GIST(linestring)
"""

sql22 = """
CREATE TEMP TABLE {0}connx AS
SELECT
    ww.id,
    ww.end
FROM
    {0}water_ends AS ww
    JOIN way_nodes ON
        way_nodes.node_id = ww.end AND
        way_nodes.way_id != ww.id
    JOIN ways ON
        ways.id = way_nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags?'waterway' AND
        ways.tags->'waterway' IN ('stream', 'river', 'canal', 'drain')
"""

sql23 = """
CREATE TEMP TABLE {0}_{1}_coastline AS
SELECT
    ww.id,
    ww.end
FROM
    {0}water_ends AS ww
    JOIN way_nodes ON
        way_nodes.node_id = ww.end AND
        way_nodes.way_id != ww.id
    JOIN {1}ways AS ways ON
        ways.id = way_nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags?'natural' AND
        ways.tags->'natural' = 'coastline'
"""

sql24 = """
SELECT
    t.id,
    ST_AsText(nodes.geom)
FROM
    (
        SELECT
            id,
            "end"
        FROM
            {0}water_ends
    EXCEPT
        SELECT
            *
        FROM
            {0}_{1}_coastline
    EXCEPT
        SELECT
            *
        FROM
            {0}connx
    ) AS t
    JOIN nodes ON
        nodes.id = t."end"
"""

class Analyser_Osmosis_Waterway(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1220", "level": 3, "tag": ["waterway", "fix:imagery"], "desc": T_(u"Riverbank without river") }
        self.classs_change[2] = {"item":"1220", "level": 3, "tag": ["waterway", "fix:imagery"], "desc": T_(u"Unconnected waterway or wrong way flow") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback10)

        self.run(sql20.format(""))
        self.run(sql21.format(""))
        self.run(sql22.format(""))
        self.run(sql23.format("", ""))
        self.run(sql24.format("", ""), self.callback20)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("not_touched_", "touched_"), self.callback10)

        self.run(sql20.format("touched_"))
        self.run(sql21.format("touched_"))
        self.run(sql22.format("touched_"))
        self.run(sql23.format("touched_", ""))
        self.run(sql24.format("touched_", ""), self.callback20)

        self.run(sql20.format("not_touched_"))
        self.run(sql21.format("not_touched_"))
        self.run(sql22.format("not_touched_"))
        self.run(sql23.format("not_touched_", "touched_"))
        self.run(sql24.format("not_touched_", "touched_"), self.callback20)
