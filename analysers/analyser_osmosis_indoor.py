#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2022                                         ##
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

sql00 = """
CREATE TEMP TABLE indoor_surfaces AS
SELECT
    id,
    linestring AS geom,
    nodes,
    tags->'indoor' AS indoor,
    tags->'level' AS level,
    tags,
    (NOT tags?'access' OR NOT tags->'access' IN ('no', 'private')) AS public_access
FROM
    ways
WHERE
    is_polygon AND
    tags != ''::hstore AND
    tags?'indoor' AND
    tags->'indoor' in ('room', 'corridor', 'area', 'level')
UNION ALL
SELECT
    relations.id,
    ST_Envelope(ST_Collect(array_agg(inner_ways.linestring) || outer_ways.linestring)) AS geom,
    ARRAY(select unnest(array_agg(inner_ways.nodes))) || outer_ways.nodes as nodes,
    relations.tags->'indoor' AS indoor,
    relations.tags->'level' AS level,
    relations.tags,
    (NOT relations.tags?'access' OR NOT relations.tags->'access' IN ('no', 'private')) AS public_access
FROM
    relations AS relations
    JOIN relation_members AS rel_members ON
        rel_members.relation_id = relations.id AND
        rel_members.member_type = 'W' AND
        rel_members.member_role in ('outer', 'inner')
    JOIN ways AS outer_ways ON
        outer_ways.id = rel_members.member_id AND
        ST_NumPoints(outer_ways.linestring) >= 2
    JOIN ways AS inner_ways ON
        inner_ways.id = rel_members.member_id AND
        ST_NumPoints(inner_ways.linestring) >= 2
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon' AND
    relations.tags?'indoor' AND
    relations.tags->'indoor' in ('room', 'corridor', 'area')
GROUP BY
    relations.id,
    outer_ways.id
"""

sql01 = """
CREATE INDEX indoor_surfaces_idx_geom on indoor_surfaces USING gist(geom)
"""

sql10 = """
SELECT
    public_indoor_rooms.id,
    ST_AsText(way_locate(public_indoor_rooms.geom))
FROM
    indoor_surfaces AS public_indoor_rooms
    LEFT JOIN nodes ON
        public_indoor_rooms.geom && nodes.geom AND
        nodes.id = ANY(public_indoor_rooms.nodes) AND
        nodes.tags != ''::hstore AND
        nodes.tags?'door'
WHERE
    public_indoor_rooms.indoor = 'room' AND
    public_indoor_rooms.public_access AND
    nodes.id IS NULL
"""

sql20 = """
CREATE TEMP TABLE indoor_surfaces_connected_to_highways AS
SELECT DISTINCT
    indoor_surfaces.id,
    indoor_surfaces.geom,
    indoor_surfaces.indoor,
    indoor_surfaces.level AS surface_level,
    highway_ends.nid,
    highway_ends.highway,
    highways.tags->'level' AS connected_highway_level
FROM
    indoor_surfaces
    JOIN nodes ON
        nodes.geom && indoor_surfaces.geom AND
        nodes.id = ANY(indoor_surfaces.nodes)
    JOIN highway_ends ON
        highway_ends.nid = nodes.id
    JOIN highways ON
        highways.id = highway_ends.id
WHERE
    indoor_surfaces.indoor IN ('room', 'corridor', 'area') AND
    highways.highway IN ('steps', 'footway', 'pedestrian')
"""

# TODO : check that all surfaces have at least one connected_highway_level that matches it own surface_level
# (dealing with level="0;1" that occurs on highway=steps
# and assuming than no level on highway is probably implicit level=0)

sql21 = """
CREATE TEMP TABLE indoor_pt_platforms AS
SELECT
    relations.id,
    ST_Envelope(ST_Collect(array_agg(inner_ways.linestring) || outer_ways.linestring)) AS geom,
    ARRAY(select unnest(array_agg(inner_ways.nodes))) || outer_ways.nodes as nodes
FROM
    relations AS relations
    JOIN relation_members AS rel_members ON
        rel_members.relation_id = relations.id AND
        rel_members.member_type = 'W' AND
        rel_members.member_role in ('outer', 'inner')
    JOIN ways AS outer_ways ON
        outer_ways.id = rel_members.member_id AND
        ST_NumPoints(outer_ways.linestring) >= 2
    JOIN ways AS inner_ways ON
        inner_ways.id = rel_members.member_id AND
        ST_NumPoints(inner_ways.linestring) >= 2
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon' AND
    relations.tags?'public_transport' AND
    relations.tags->'public_transport' = 'platform'
GROUP BY
    relations.id,
    outer_ways.id
UNION ALL
SELECT
    id,
    linestring AS geom,
    nodes
FROM
    ways
WHERE
    is_polygon AND
    tags != ''::hstore AND
    tags?'public_transport' AND
    tags->'public_transport'= 'platform'
"""

sql22 = """
SELECT
    indoor_surfaces.id,
    ST_AsText(way_locate(indoor_surfaces.geom))
FROM
    indoor_surfaces
    LEFT JOIN indoor_surfaces AS indoor_surfaces_other ON
        indoor_surfaces_other.id != indoor_surfaces.id AND
        indoor_surfaces_other.indoor IN ('room', 'corridor', 'area') AND
        indoor_surfaces_other.geom && indoor_surfaces.geom AND
        indoor_surfaces_other.nodes && indoor_surfaces.nodes
    LEFT JOIN indoor_pt_platforms ON
        indoor_pt_platforms.geom && indoor_surfaces.geom AND
        indoor_pt_platforms.nodes && indoor_surfaces.nodes
    LEFT JOIN indoor_surfaces_connected_to_highways ON
        indoor_surfaces_connected_to_highways.id = indoor_surfaces.id
WHERE
    indoor_surfaces.indoor IN ('room', 'corridor', 'area') AND
    indoor_surfaces_connected_to_highways.id IS NULL AND
    indoor_pt_platforms.id IS NULL AND
    indoor_surfaces_other.id is NULL
""" # maybe check the levels too to make sure they are actually connected ?


class Analyser_Osmosis_Indoor(Analyser_Osmosis):
    requires_tables_common = ['highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1300, level = 3, tags = ['indoor', 'geom', 'fix:survey'],
            title = T_('This indoor room should have a door'),
            fix = T_(
'''Find out where the entrances of the room are and add them (with a `door=*` tag) so we can actually enter this indoor room.'''))
        self.classs[2] = self.def_class(item = 1300, level = 3, tags = ['indoor', 'geom', 'fix:survey'],
            title = T_('This indoor feature is not reachable'),
            detail = T_(
'''Each indoor feature should be connected to another indoor feature or to some footpath so people can actually go to them.'''))

        self.callback10 = lambda res: {"class": 1, "data": [self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class": 2, "data": [self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql10, self.callback10)
        self.run(sql20)
        self.run(sql21)
        self.run(sql22, self.callback20)
