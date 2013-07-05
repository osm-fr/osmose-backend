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
        )
    )
;
"""

class Analyser_Osmosis_Double_Tagging(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"4080", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Object tagged twice as node, way or relation") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.node_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        def f(o1, o2, geom1, geom2, ret1, ret2):
            self.run(sql10.format("", "", o1, o2, geom1, geom2), lambda res: {"class":1, "data":[ret1, ret2, self.positionAsText]})
        self.apply(f)

    def analyser_osmosis_touched(self):
        def f(o1, o2, geom1, geom2, ret1, ret2):
            self.run(sql10.format("touched_", "", o1, o2, geom1, geom2), lambda res: dup.add(res[0]) or
                {"class":1, "data":[ret1, ret2, self.positionAsText]})
            self.run(sql10.format("", "touched_", o1, o2, geom1, geom2), lambda res: res[0] in dup or dup.add(res[0]) or
                {"class":1, "data":[ret1, ret2, self.positionAsText]})
        self.apply(f)

    def apply(self, callback):
        type = {"nodes": "nodes.geom", "ways": "ways.linestring", "relations": "relation_bbox(relations.id)"}
        ret = {"nodes": self.node_full, "ways": self.way_full, "relations": self.relation_full}
        for c in [["ways", "nodes"], ["ways", "relations"], ["relations", "nodes"]]:
            callback(c[0], c[1], type[c[0]], type[c[1]], ret[c[0]], ret[c[1]])
