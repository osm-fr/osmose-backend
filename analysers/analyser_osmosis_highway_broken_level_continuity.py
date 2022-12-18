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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql13 = """
CREATE TEMP TABLE orphan_endin AS
SELECT
    network.id,
    network.nid,
    network.level,
    network.geom,
    CASE network.level
        WHEN 1 THEN (ways.highway IN ('construction', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link'))
        WHEN 2 THEN (ways.highway IN ('construction', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link'))
        WHEN 3 THEN (ways.highway IN ('construction', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link'))
    END AS endin
FROM
    highway_ends AS network
    JOIN way_nodes ON
        way_nodes.node_id = network.nid AND
        way_nodes.way_id != network.id
    JOIN highways AS ways ON
        ways.id = way_nodes.way_id AND
        NOT ways.is_construction
WHERE
    network.nodes[1] != network.nodes[array_length(network.nodes,1)] AND
    network.highway IN ('primary', 'secondary', 'tertiary')
GROUP BY
    1,
    2,
    3,
    4,
    5
"""

sql14 = """
CREATE TEMP TABLE orphan AS
SELECT
    id,
    nid,
    level,
    geom
FROM
    orphan_endin
GROUP BY
    id,
    nid,
    level,
    geom
HAVING
    NOT BOOL_OR(orphan_endin.endin)
"""

sql16 = """
CREATE INDEX orphan_level_idx ON orphan(level)
"""

sql17 = """
CREATE INDEX orphan_geom_idx ON orphan USING gist(geom)
"""

sql18 = """
SELECT
    o1.id,
    o1.nid,
    ST_AsText(o1.geom),
    o1.level
FROM
    orphan AS o1,
    orphan AS o2
WHERE
    o1.nid != o2.nid AND
    o1.level = o2.level AND
    ST_DistanceSphere(o1.geom, o2.geom) < 1000
GROUP BY
    o1.id,
    o1.nid,
    o1.level,
    o1.geom
"""

class Analyser_Osmosis_Highway_Broken_Level_Continuity(Analyser_Osmosis):

    requires_tables_common = ['highways', 'highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        doc = dict(
            title = T_('Broken highway level continuity'),
            detail = T_(
'''Check the continuity of the highway types. The classification of a
highway should normally be consistent along the entire path. For example
a `highway=tertiary` should remain `highway=tertiary` until it intersects
with a road of higher classification.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/e/e8/Osmose-eg-error-1120.png)

`highway=secondary` should not become a residential.'''))
        self.classs[1] = self.def_class(item = 1120, level = 1, tags = ['highway', 'fix:chair'], **self.merge_docs(doc,
            detail = {'en':
'''motorway, motorway_link, trunk, trunk_link, primary,
primary_link'''}))
        self.classs[2] = self.def_class(item = 1120, level = 2, tags = ['highway', 'fix:chair'], **self.merge_docs(doc,
            detail = {'en':
'''secondary, secondary_link'''}))
        self.classs[3] = self.def_class(item = 1120, level = 2, tags = ['highway', 'fix:chair'], **self.merge_docs(doc,
            detail = {'en':
'''tertiary, tertiary_link'''}))

    def analyser_osmosis_common(self):
        self.run(sql13)
        self.run(sql14)
        self.run(sql16)
        self.run(sql17)
        self.run(sql18, lambda res: {"class":res[3], "data":[self.way_full, self.node, self.positionAsText]} )
