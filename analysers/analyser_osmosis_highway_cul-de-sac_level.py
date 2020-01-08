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

from .Analyser_Osmosis import Analyser_Osmosis

sql40 = """
SELECT
    way_ends.id,
    way_ends.nid,
    ST_AsText(way_ends.geom),
    way_ends.level
FROM
    highway_ends AS way_ends
    JOIN way_nodes ON
        way_ends.nid = way_nodes.node_id AND
        way_nodes.way_id != way_ends.id
    JOIN highway_ends AS highway_level ON
        highway_level.id = way_nodes.way_id
WHERE
    NOT way_ends.is_roundabout AND
    way_ends.level <= 3
GROUP BY
    way_ends.id,
    way_ends.nid,
    way_ends.geom,
    way_ends.level
HAVING
    BOOL_AND(way_ends.level + 1 < highway_level.level)
"""

class Analyser_Osmosis_Highway_CulDeSac_Level(Analyser_Osmosis):

    requires_tables_common = ['highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''A way connects directly to the street classification much
smaller.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/b/be/Osmose-eg-error-1090.png)

Secondary connecting directly to the residentials.'''))

        self.classs[1] = self.def_class(item = 1090, level = 1, tags = ['highway', 'fix:chair'], **self.merge_docs(doc,
            title = T_f('Sudden highway type change (level {0})', 1),
            detail = {'en':
'''motorway, primary, trunk'''}))
        self.classs[2] = self.def_class(item = 1090, level = 2, tags = ['highway', 'fix:chair'], **self.merge_docs(doc,
            title = T_f('Sudden highway type change (level {0})', 2),
            detail = {'en':
'''motorway_link, primary_link, trunk_link, secondary,
secondary_link'''}))
        self.classs[3] = self.def_class(item = 1090, level = 2, tags = ['highway', 'fix:chair'], **self.merge_docs(doc,
            title = T_f('Sudden highway type change (level {0})', 3),
            detail = {'en':
'''tertiary, tertiary_link'''}))

    def analyser_osmosis_common(self):
        self.run(sql40, lambda res: {"class":res[3], "data":[self.way, self.node, self.positionAsText]} )
