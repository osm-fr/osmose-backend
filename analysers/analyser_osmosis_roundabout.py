#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo 2010-2015                                 ##
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

sql10 = u"""
SELECT
    id,
    ST_AsText(way_locate(linestring)) AS geom
FROM
    {1}ways AS ways
    JOIN way_nodes ON
        way_nodes.node_id = ANY (ways.nodes[2:array_length(ways.nodes, 1)]) AND -- not join twice the start/end node
        way_nodes.way_id != ways.id
WHERE
    -- tags
    ways.tags != ''::hstore AND
    ways.tags?'highway' AND
    ways.tags->'highway' IN ('primary', 'secondary', 'tertiary', 'residential', 'unclassified') AND -- it's a car road
    (NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout') AND
    NOT ways.tags?'area' AND
    (NOT ways.tags?'name' OR ways.tags->'name' LIKE 'Rond%' OR ways.tags->'name' LIKE 'Giratoire%') AND -- no name or start with 'Rond' or 'Giratoire' (French)
    -- geometry
    ways.is_polygon AND -- It's a polygon
    ST_NPoints(linestring) < 24 AND
    ST_MaxDistance(ST_Transform(linestring,{0}),ST_Transform(linestring,{0})) < 70 AND -- The way diameter is less than 70m
    ST_Area(ST_MakePolygon(ST_Transform(linestring,{0})))/ST_Area(ST_MinimumBoundingCircle(ST_Transform(linestring,{0}))) > 0.6 -- 90% of roundabout covert more than 60% bounding circle
GROUP BY
    ways.id,
    geom
HAVING
    COUNT(*) >= 2 -- select roundabout at least connected with two other ways
"""

class Analyser_Osmosis_Roundabout(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            self.classs_change[1] = {"item":"2010", "level": 1, "tag": ["highway", "roundabout", "fix:imagery"], "desc": T_(u"Missing junction=roundabout") }
            self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":{"+":{"junction":"roundabout"}} }

    def analyser_osmosis_all(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), ""), self.callback10)

    def analyser_osmosis_touched(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), "touched_"), self.callback10)
