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

from modules.Stablehash import stablehash64
from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    ST_AsText(ST_Centroid(geom))
FROM
(
    SELECT
        (ST_Dump(ST_MemUnion(ST_Buffer(geom, 0.001, 'quad_segs=2')))).geom AS geom
    FROM
    (
        SELECT geom
        FROM nodes
        LEFT JOIN way_nodes ON
            nodes.id = way_nodes.node_id
        WHERE
            way_nodes.node_id IS NULL AND
            tags = ''::hstore AND
            version = 1
        LIMIT 3000
    ) AS n
) AS t
WHERE
    ST_Area(geom) > 1e-5
"""

class Analyser_Osmosis_Orphan_Nodes_Cluster(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1080, level = 1, tags = ['geom', 'building', 'fix:chair'],
            title = T_('Orphan nodes cluster'),
            detail = T_(
'''Nodes in the vicinity without tag and not part of a way.'''),
            fix = T_(
'''Find the origin of these nodes. They probably result from a bad import.
Contact the contributor submitting the nodes or remove them.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/0/0c/Osmose-eg-error-1080.png)

Group of orphan nodes.'''))

    def analyser_osmosis_common(self):
        self.run(sql10, lambda res: {"class":1, "subclass":stablehash64(res[0]), "data":[self.positionAsText]} )
