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
DROP TABLE IF EXISTS {0}relations_with_bbox;
CREATE TEMP TABLE {0}relations_with_bbox AS
SELECT
  id AS id,
  relation_bbox(id) AS bbox,
  tags AS tags
FROM
  {0}relations
WHERE
  tags?'amenity' OR tags?'leisure' OR tags?'building'
"""

sql20 = """
SELECT
    {2}.id,
    {3}.id,
    ST_AsText(ST_Centroid({5}))
FROM
    {0}{2} AS {2}
    JOIN {1}{3} AS {3} ON
        {4} && {5}
WHERE
    {2}.tags?'name' AND
    {3}.tags?'name' AND
    {2}.tags->'name' = {3}.tags->'name'
    AND
    (
        (
            {2}.tags?'amenity' AND
            {3}.tags?'amenity' AND
            {2}.tags->'amenity' = {3}.tags->'amenity'
        ) OR
        (
            {2}.tags?'leisure' AND
            {3}.tags?'leisure' AND
            {2}.tags->'leisure' = {3}.tags->'leisure'
        ) OR
        (
            {2}.tags?'building' AND
            {3}.tags?'building' AND
            {2}.tags->'building' = {3}.tags->'building'
        )
    )
"""

class Analyser_Osmosis_Double_Tagging(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"4080", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Object tagged twice as node and way") }
        self.classs_change[2] = {"item":"4080", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Object tagged twice as way and relation") }
        self.classs_change[3] = {"item":"4080", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Object tagged twice as node and relation") }

    def analyser_osmosis_all(self):
        self.run(sql10.format(""))
        def f(o1, o2, geom1, geom2, ret1, ret2, class_):
            self.run(sql20.format("", "", o1, o2, geom1, geom2), lambda res: {"class":class_, "data":[ret1, ret2, self.positionAsText]})
        self.apply(f)

    def analyser_osmosis_touched(self):
        self.run(sql10.format(""))
        self.run(sql10.format("touched_"))
        def f(o1, o2, geom1, geom2, ret1, ret2, class_):
            dup = set()
            self.run(sql20.format("touched_", "", o1, o2, geom1, geom2), lambda res: dup.add(res[0]) or
                {"class":class_, "data":[ret1, ret2, self.positionAsText]})
            self.run(sql20.format("", "touched_", o1, o2, geom1, geom2), lambda res: res[0] in dup or dup.add(res[0]) or
                {"class":class_, "data":[ret1, ret2, self.positionAsText]})
        self.apply(f)

    def apply(self, callback):
        type = {"nodes": "nodes.geom", "ways": "ways.linestring", "relations_with_bbox": "relations_with_bbox.bbox"}
        ret = {"nodes": self.node_full, "ways": self.way_full, "relations_with_bbox": self.relation_full}
        for c in [["ways", "nodes", 1], ["ways", "relations_with_bbox", 2], ["relations_with_bbox", "nodes", 3]]:
            callback(c[0], c[1], type[c[0]], type[c[1]], ret[c[0]], ret[c[1]], c[2])
