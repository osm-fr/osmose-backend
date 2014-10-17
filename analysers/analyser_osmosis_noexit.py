#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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
    nodes.id,
    ST_AsText(nodes.geom),
    COUNT(*) > 1
FROM
    {0}nodes
    JOIN way_nodes ON
        way_nodes.node_id = nodes.id
    JOIN {1}ways ON
        ways.linestring && nodes.geom AND
        ways.id = way_nodes.way_id AND
        ways.tags?'highway'
WHERE
    nodes.tags?'noexit' AND
    nodes.tags->'noexit' = 'yes'
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    COUNT(*) > 1 OR
    nodes.id NOT IN (SELECT ends(MIN(ways.nodes)))
"""

sql20 = """
SELECT
    id,
    ST_AsText(way_locate(linestring))
FROM
    (
    SELECT
        w1.id,
        w1.linestring
    FROM
        ways AS w1
        JOIN ways AS w2 ON
            w2.id != w1.id AND
            w2.tags?'highway' AND
            w1.linestring && w2.linestring AND
                (SELECT COUNT(*) > 0 FROM (SELECT UNNEST(w1.nodes) INTERSECT SELECT UNNEST(w2.nodes)) AS t)
    WHERE
        w1.tags?'highway' AND
        w1.tags?'noexit' = 'yes'
    GROUP BY
        w1.id,
        w1.linestring,
        (SELECT MIN(nid) FROM (SELECT UNNEST(w1.nodes) INTERSECT SELECT UNNEST(w2.nodes)) AS t(nid))
    ) AS t
GROUP BY
    id,
    linestring
HAVING
    COUNT(*) > 1
"""

class Analyser_Osmosis_Noexit(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"3210", "level": 2, "tag": ["highway", "tag", "fix:chair"], "desc": T_(u"noexit on node with exit") }
        self.classs[2] = {"item":"3210", "level": 2, "tag": ["highway", "tag", "fix:chair"], "desc": T_(u"noexit on way with multiple exits") }
        self.callback10 = lambda res: {"class":1, "subclass":1 if res[2] else 2, "data":[self.node_full, self.positionAsText], "fix":{"-":["noexit"]}}
        self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.positionAsText], "fix":{"-":["noexit"]} }

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20, self.callback20)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
        self.run(sql10.format("touched_", "touched_"), self.callback10)
