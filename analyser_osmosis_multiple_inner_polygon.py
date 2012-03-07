#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    w1.id,
    w2.id,
    ST_AsText(ST_Centroid(ST_Envelope(w1.linestring)))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W'
    JOIN {1}ways AS w1 ON
        w1.id = relation_members.member_id AND
        w1.is_polygon AND
        array_length(akeys(w1.tags), 1) = 0
    JOIN {2}ways AS w2 ON
        w1.id != w2.id AND
        w2.is_polygon AND
        w1.linestring && w2.linestring AND
        w1.linestring = w2.linestring AND
        (w2.tags?'landuse' OR w2.tags?'aeroway' OR w2.tags?'natural' OR w2.tags?'water') AND
        ST_Equals(ST_MakePolygon(w1.linestring), ST_MakePolygon(w2.linestring))
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon'
;
"""

class Analyser_Osmosis_Polygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1070", "desc":{"en":"Double inner polygon"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format("", "", ""), self.callback10)

    def analyser_osmosis_touched(self):
        dup = set()
        self.run(sql10.format("touched_", "", ""), lambda res: dup.add((res[0], res[1])) or self.callback10(res))
        self.run(sql10.format("", "touched_", ""), lambda res: (res[0], res[1]) in dup or dup.add((res[0], res[1])) or self.callback10(res))
        self.run(sql10.format("", "", "touched_"), lambda res: (res[0], res[1]) in dup or dup.add((res[0], res[1])) or self.callback10(res))
