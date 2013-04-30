#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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
    ways.id,
    AsText(way_locate(linestring))
FROM
    {0}ways AS ways
WHERE
    (
        ways.tags?'railway' OR
        (ways.tags?'highway' AND ways.tags->'highway' IN ('motorway', 'trunk', 'primary', 'secondary'))
    ) AND
    ways.tags?'bridge' AND
    ways.tags->'bridge' = 'yes' AND
    ST_Length(ways.linestring::geography) > 500
"""

sql20 = """
SELECT
    ways.id,
    bridge.id,
    ST_Centroid(ST_Intersection(bridge.linestring, ways.linestring))
FROM
    {0}ways AS bridge
    JOIN {1}ways AS ways ON
        ST_Intersects(bridge.linestring, ways.linestring)
WHERE
    bridge.tags?'bridge' AND
    bridge.tags->'bridge' != 'no' AND
    ST_NPoints(bridge.linestring) > 1 AND
    ways.tags?'highway' AND
    ways.tags->'highway' IN ('motorway_link', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link') AND
    NOT ways.tags?'maxheight' AND
    ST_NPoints(ways.linestring) > 1 AND
    bridge.nodes[1] != ways.nodes[1] AND
    bridge.nodes[1] != ways.nodes[array_length(ways.nodes, 1)] AND
    bridge.nodes[array_length(bridge.nodes, 1)] != ways.nodes[1] AND
    bridge.nodes[array_length(bridge.nodes, 1)] != ways.nodes[array_length(ways.nodes, 1)]
"""

class Analyser_Osmosis_Tunnel_Bridge(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item": 7012, "level": 3, "tag": ["tag", "highway"], "desc":{"fr": u"Type de pont à qualifier", "en": u"Bridge type"} }
        self.classs_change[2] = {"item": 7120, "level": 3, "tag": ["tag", "highway"], "desc": {"en": u"Mising maxheight tag", "fr": u"Manque le tag maxheight"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":[{"~":{"bridge":"aqueduct"}}, {"~":{"bridge":"viaduct"}}, {"~":{"bridge":"suspension"}}] }
        self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.way_full, self.positionAsText] }

    def analyser_osmosis_all(self):
        self.run(sql10.format(""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_"), self.callback10)
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("", "touched_"), self.callback20)
