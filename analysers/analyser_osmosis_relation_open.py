#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2020                                      ##
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


sql10 = """
SELECT
    t.id,
    nodes.id AS nid,
    ST_AsText(nodes.geom),
    CASE
        WHEN admin_level IN ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
            THEN 100 + admin_level::int
        WHEN type = 'boundary' THEN 1
        WHEN type = 'multipolygon' THEN 5
    END
FROM (
    SELECT
        relations.id,
        relations.tags->'type' AS type,
        relations.tags->'admin_level' AS admin_level,
        ends(ways.nodes) AS nid
    FROM
        relations
        JOIN relation_members ON
            relation_members.relation_id = relations.id AND
            relation_members.member_type = 'W'
        JOIN ways ON
            ways.id = relation_members.member_id
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' IN ('boundary', 'multipolygon')
    GROUP BY
        relations.id,
        relations.tags->'type',
        relations.tags->'admin_level',
        nid
    HAVING
        count(*) % 2 != 0
) AS t
    JOIN nodes ON
        nodes.id = t.nid
"""


class Analyser_Osmosis_Relation_Multipolygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        detail = T_(
'''A relation that should be a closed polygon and it is not. An issue is
reported at each end of open part.''')
        self.classs[1] = self.def_class(item = 6010, level = 3, tags = ['geom', 'boundary'],
            title = T_('Open relation type=boundary'),
            detail = detail)
        self.classs[5] = self.def_class(item = 1170, level = 2, tags = ['geom'],
            title = T_('Open relation type=multipolygon'))
        for admin_level in range(0, 15):
            if admin_level <= 6:
                level = 1
            elif admin_level <= 8:
                level = 2
            else:
                level = 3
            self.classs[100 + admin_level] = self.def_class(item = 6010, level = level, tags = ['geom', 'boundary'],
                title = T_('Open relation type=boundary admin_level={0}', admin_level),
                detail = detail)

    def analyser_osmosis_full(self):
        self.run(sql10, lambda res: {"class": res[3], "data":[self.relation_full, self.node, self.positionAsText]})
