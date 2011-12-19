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
    ways.id,
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    ways
    JOIN nodes ON
        ways.linestring && nodes.geom
WHERE
    ways.tags?'name' AND
    nodes.tags?'name' AND
    ways.tags->'name' = nodes.tags->'name'
    AND
    (
        (
            ways.tags?'amenity' AND
            nodes.tags?'amenity' AND
            ways.tags->'amenity' = nodes.tags->'amenity'
        ) OR
        (
            ways.tags?'leisure' AND
            nodes.tags?'leisure' AND
            ways.tags->'leisure' = nodes.tags->'leisure'
        )
    )
;
"""

class Analyser_Osmosis_Double_Tagging(Analyser_Osmosis):

    def __init__(self, father):
        Analyser_Osmosis.__init__(self, father)
        self.classs[1] = {"item":"4080", "desc":{"fr":"Objet marqué comme way et comme nœud", "en":"Object tagged as way and as node"} }

    def analyser_osmosis(config, logger):
        self.run(sql10, lambda res: {"class":1, "data":[self.way_full, self.node_full, self.positionAsText]} )
