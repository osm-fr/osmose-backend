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
    ST_AsText(ST_Centroid(geom))
FROM
(
    SELECT
        (ST_Dump(ST_Union(ST_Buffer(geom, 0.001, 'quad_segs=2')))).geom AS geom
    FROM
        nodes
        LEFT JOIN way_nodes ON
            nodes.id = way_nodes.node_id
    WHERE
        way_nodes.node_id IS NULL AND
        array_length(akeys(tags),1) = 0 AND
        version = 1
) AS t
WHERE
    ST_Area(geom) > 1e-5
;
"""

class Analyser_Osmosis_Orphan_Nodes_Cluster(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1080", "level": 1, "tag": ["geom", "building"], "desc":{"fr":"Groupe de nœuds orphelins", "en":"Orphan nodes cluster"} }

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {"class":1, "subclass":abs(int(hash(res[0]))), "data":[self.positionAsText]} )
