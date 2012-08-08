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
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    nodes
    JOIN way_nodes AS highway_nodes ON
        nodes.id = highway_nodes.node_id
    JOIN ways AS highway ON
        highway_nodes.way_id = highway.id
WHERE
    nodes.tags?'railway' AND
    nodes.tags->'railway' IN ('level_crossing', 'crossing')
GROUP BY
    nodes.id
HAVING
    NOT BOOL_OR(highway.tags?'highway')
;
"""

sql20 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    nodes
    JOIN way_nodes AS railway_nodes ON
        nodes.id = railway_nodes.node_id
    JOIN ways AS railway ON
        railway_nodes.way_id = railway.id
WHERE
    nodes.tags?'railway' AND
    nodes.tags->'railway' IN ('level_crossing', 'crossing')
GROUP BY
    nodes.id
HAVING
    NOT BOOL_OR(railway.tags?'railway')
;
"""

class Analyser_Osmosis_Crossing(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"7090", "level": 2, "tag": ["railway", "highway"], "desc":{"fr":"Manque une route au passage à niveau", "en":"Missing highway on crossing"} }
        self.classs[2] = {"item":"7090", "level": 2, "tag": ["railway", "highway"], "desc":{"fr":"Manque un chemin de fer au passage à niveau", "en":"Missing railway on crossing"} }
        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
