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
CREATE TEMP TABLE way_ends AS
SELECT
    ends(nodes) AS id
FROM
    {0}ways AS ways
WHERE
    tags?'highway' AND
    tags->'highway' IN ('cycleway', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'link_tertiary')
"""

sql20 = """
SELECT
    way_nodes.node_id,
    ST_AsText(nodes.geom)
FROM
    way_ends
    JOIN way_nodes ON
        way_ends.id = way_nodes.node_id
    JOIN nodes ON
        way_nodes.node_id = nodes.id
GROUP BY
    way_nodes.node_id,
    nodes.geom
HAVING
    COUNT(*) = 1
"""

class Analyser_Osmosis_DeadEnd(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1210", "level": 1, "tag": ["highway"], "desc":{"fr": u"Voie non connectée", "en": u"Unconnected way"} }
        self.callback20 = lambda res: {"class":1, "data":[self.node_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format(""))
        self.run(sql20, self.callback20)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_"))
        self.run(sql20, self.callback20)
