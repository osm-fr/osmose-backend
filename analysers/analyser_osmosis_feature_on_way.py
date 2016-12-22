#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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
    MIN(ways.id)
FROM
    {0}nodes AS nodes
    JOIN {1}ways AS ways ON
        ways.linestring && nodes.geom AND
        (ways.tags?'highway' OR ways.tags?'railway') AND
        nodes.id = ANY (ways.nodes)
WHERE
    nodes.tags?'railway' AND
    nodes.tags->'railway' IN ('level_crossing', 'crossing')
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    NOT BOOL_OR(ways.tags?'highway') OR NOT BOOL_OR(ways.tags?'railway')
"""

sql30 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    nodes
    LEFT JOIN way_nodes ON
        nodes.id = way_nodes.node_id
    LEFT JOIN ways ON
        way_nodes.way_id = ways.id AND
        (ways.tags?'highway' OR ways.tags?'railway')
WHERE
    nodes.tags?'highway' AND
    nodes.tags->'highway' IN ('crossing', 'turning_circle', 'traffic_signals', 'stop', 'give_way', 'motorway_junction', 'mini_roundabout', 'passing_place', 'ford', 'elevator', 'turning_loop', 'incline_steep', 'stile', 'incline', 'traffic_calming', 'junction')
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    BOOL_AND(ways.id IS NULL)
"""


class Analyser_Osmosis_Feature_On_Way(Analyser_Osmosis):
    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"7090", "level": 2, "tag": ["railway", "highway", "fix:imagery"], "desc": T_(u"Missing way on level crossing") }
        self.classs[3] = {"item":"7090", "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Lone highway or barrier node") }
        self.callback10 = lambda res: {"class":1, "subclass":1, "data":[self.node_full, self.positionAsText, self.way_full]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.positionAsText]}

    def analyser_osmosis(self):
        self.run(sql30, self.callback30)

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("_touched", ""), self.callback10)
        self.run(sql10.format("", "_touched"), self.callback10)
