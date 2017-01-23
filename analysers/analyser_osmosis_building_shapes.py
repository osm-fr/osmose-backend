#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Vincent Pottier <@.> 2010                                  ##
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
    id,
    ST_AsText(way_locate(linestring))
FROM
    {1}ways
WHERE
    tags != ''::hstore AND
    tags?'building' AND
    tags->'building' = 'yes' AND
    NOT tags?'wall' AND
    array_length(nodes, 1) > 16 AND
    is_polygon AND
    ST_Area(ST_MakePolygon(ST_Transform(linestring,{0})))/ST_Area(ST_MinimumBoundingCircle(ST_Transform(linestring,{0}))) > 0.95 AND
    ST_MaxDistance(ST_Transform(linestring,{0}), ST_Transform(linestring,{0})) > 5 AND
    tags - ARRAY['created_by', 'source', 'name', 'building', 'note:qadastre'] = ''::hstore
"""

sql20 = """
SELECT
    id,
    ST_AsText(way_locate(linestring))
FROM
    {1}ways
WHERE
    tags != ''::hstore AND
    tags?'building' AND
    tags->'building' = 'yes' AND
    NOT tags?'wall' AND
    is_polygon AND
    ST_MaxDistance(ST_Transform(linestring,{0}), ST_Transform(linestring,{0})) > 300 AND
    tags - ARRAY['created_by', 'source', 'name', 'building', 'note:qadastre'] = ''::hstore
"""

class Analyser_Osmosis_Building_Shapes(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            self.classs_change[1] = {"item":"7011", "level": 3, "tag": ["building", "fix:imagery"], "desc": T_(u"Special building (round)") }
            self.classs_change[2] = {"item":"7011", "level": 3, "tag": ["building", "fix:imagery"], "desc": T_(u"Special building (large)") }
            self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":[
                {"+":{"man_made":"water_tower"}},
                {"+":{"man_made":"reservoir_covered"}},
                {"+":{"man_made":"wastewater_plant"}},
                {"+":{"man_made":"storage_tank"}},
                {"+":{"man_made":"windmill"}},
                {"+":{"man_made":"dovecote"}},
                {"+":{"building":"hut"}},
                ]}
            self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.positionAsText], "fix":[
                {"+":{"man_made":"works"}},
                {"+":{"shop":"mall"}},
                {"+":{"shop":"supermarket"}},
                {"~":{"building":"warehouse"}},
                {"~":{"building":"industrial"}},
                ]}

    def analyser_osmosis_all(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), ""), self.callback10)
            self.run(sql20.format(self.config.options.get("proj"), ""), self.callback20)

    def analyser_osmosis_touched(self):
        if "proj" in self.config.options:
            self.run(sql10.format(self.config.options.get("proj"), "touched_"), self.callback10)
            self.run(sql20.format(self.config.options.get("proj"), "touched_"), self.callback20)
