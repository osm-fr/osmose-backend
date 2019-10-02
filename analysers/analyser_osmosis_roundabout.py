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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = u"""
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring)) AS geom
FROM
    {1}highways AS ways
    JOIN {2}highways AS conns ON
        conns.linestring && ways.linestring AND
        conns.nodes && ways.nodes AND
        conns.id != ways.id AND
        conns.level < 5 AND -- it's a car road
        NOT conns.is_area AND
        NOT conns.is_construction
WHERE
    -- tags
    ways.level < 5 AND -- it's a car road
    NOT ways.is_roundabout AND
    NOT ways.is_area AND
    NOT ways.is_construction AND
    (NOT ways.tags?'name' OR ways.tags->'name' LIKE 'Rond%' OR ways.tags->'name' LIKE 'Giratoire%') AND -- no name or start with 'Rond' or 'Giratoire' (French)
    -- geometry
    ways.is_polygon AND -- It's a polygon
    ST_NPoints(ways.linestring) < 24 AND
    ST_MaxDistance(ST_Transform(ways.linestring,{0}),ST_Transform(ways.linestring,{0})) < 70 AND -- The way diameter is less than 70m
    ST_Area(ST_MakePolygon(ST_Transform(ways.linestring,{0})))/ST_Area(ST_MinimumBoundingCircle(ST_Transform(ways.linestring,{0}))) > 0.6 -- 90% of roundabout covert more than 60% bounding circle
GROUP BY
    ways.id,
    geom
HAVING
    COUNT(*) >= 2 -- select roundabout at least connected with two other ways
"""

class Analyser_Osmosis_Roundabout(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            self.classs_change[1] = {"item":"2010", "level": 1, "tag": ["highway", "roundabout", "fix:imagery"], "desc": T_(u"Missing junction=roundabout") }
            self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":{"+":{"junction":"roundabout"}} }

    def analyser_osmosis_full(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), "", ""), self.callback10)

    def analyser_osmosis_diff(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), "touched_", ""), self.callback10)
            self.run(sql10.format(self.config.options.get("proj"), "not_touched_", "touched_"), self.callback10)
