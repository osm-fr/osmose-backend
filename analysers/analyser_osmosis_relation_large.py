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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    id,
    ST_AsText(ST_Centroid(ST_LongestLine(bbox, bbox))),
    type
FROM
    (
    SELECT
        relations.id,
        relations.tags->'type' AS type,
        CASE
            WHEN ST_Envelope(ST_Collect(linestring)) IS NULL THEN
                ST_Envelope(ST_Collect(geom))
            WHEN ST_Envelope(ST_Collect(geom)) IS NULL THEN
                ST_Envelope(ST_Collect(linestring))
            ELSE
                ST_Envelope(ST_Union(
                    ST_Envelope(ST_Collect(linestring)),
                    ST_Envelope(ST_Collect(geom))
                ))
        END AS bbox
    FROM
        relations
        LEFT JOIN relation_members AS rmw ON
            relations.id = rmw.relation_id AND
            rmw.member_type = 'W'
        LEFT JOIN ways ON
            rmw.member_id = ways.id
        LEFT JOIN relation_members AS rmn ON
            relations.id = rmn.relation_id AND
            rmn.member_type = 'N'
        LEFT JOIN nodes ON
            rmn.member_id = nodes.id
    WHERE
        relations.tags->'type' NOT IN ('multipolygon', 'route', 'boundary', 'public_transport', 'TMC', 'route_master', 'collection', 'waterway', 'tmc', 'network', 'line', 'watershed', 'river', 'superroute', 'boundary_segment', 'railway', 'dual_carriageway', 'bridge', 'tunnel', 'restriction', 'multilinestring', 'pipeline') AND
        NOT (relations.tags->'type' = 'enforcement' AND relations.tags->'enforcement' = 'average_speed') AND
        NOT (relations.tags->'type' = 'site' AND relations.tags?'power' AND relations.tags->'power' = 'plant' AND relations.tags->'plant:source' = 'wind') -- wind farm
    GROUP BY
        relations.id,
        relations.tags->'type'
    ) AS t
WHERE
    ST_Length(ST_LongestLine(bbox, bbox)) > 1e-1
"""

class Analyser_Osmosis_Relation_Large(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1160, level = 1, tags = ['relation', 'geom', 'fix:chair'],
            title = T_('Large relation'),
            detail = T_(
'''A relation whose members should be close is geographically
spread.'''),
            trap = T_(
'''[The relationships are not
classes](https://wiki.openstreetmap.org/wiki/Relations/Relations_are_not_Categories).'''))

    def analyser_osmosis_common(self):
        self.run(sql10, lambda res: {
            "class":1,
            "data":[self.relation, self.positionAsText],
            "text": T_("Large relation of type {0}", res[2]) })
