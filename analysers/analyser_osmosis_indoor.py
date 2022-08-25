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

sql10 = """
SELECT
  id,
  ST_AsText(way_locate(linestring))
FROM
  ways
WHERE
  NOT is_polygon
  AND tags?'indoor'
  AND tags->'indoor' in ('room', 'corridor', 'area', 'level')
"""

sql20 = """
SELECT
  id,
  ST_AsText(geom)
FROM
  nodes
WHERE
  tags?'indoor'
  AND tags->'indoor' in ('room', 'corridor', 'area', 'level')
"""

sql30 = """
CREATE TEMP TABLE indoor_rooms_with_door AS
(
SELECT
  ways.id
FROM
  ways
JOIN way_nodes ON ways.id = way_nodes.way_id
JOIN nodes ON nodes.id = way_nodes.node_id
WHERE
  ways.is_polygon
  AND ways.tags?'indoor'
  AND ways.tags->'indoor' = 'room'
  AND nodes.tags?'door'
)
"""

sql31 = """
SELECT
  ways.id,
  ST_AsText(ST_Centroid(ways.linestring))
FROM
  ways
LEFT JOIN indoor_rooms_with_door ON indoor_rooms_with_door.id = ways.id
WHERE
  ways.is_polygon
  AND ways.tags?'indoor'
  AND ways.tags->'indoor' = 'room'
  AND ways.tags?'access'
  AND NOT ways.tags->'access' IN ('no', 'private')
"""

sql00 = """
CREATE TEMP TABLE indoor_surfaces AS
(
SELECT
  ways.id,
  ST_AsText(ST_Centroid(ways.linestring)) as geom,
  ways.tags->'indoor' as indoor,
  ways.tags->'level' as level,
  ways.tags
FROM
  ways
WHERE
  ways.is_polygon
  AND ways.tags?'indoor'
  AND ways.tags->'indoor' in ('room', 'corridor', 'area', 'level')
)
"""

sql40 = """
SELECT
  id,
  geom
FROM
  indoor_surfaces
WHERE
   NOT tags?'level'
"""

sql50 = """
SELECT
  id,
  geom
FROM
  indoor_surfaces
WHERE
  indoor_surfaces.indoor != 'room'
  AND indoor_surfaces.tags?'shop'
"""

sql60 = """
CREATE TEMP TABLE indoor_surfaces_connected_to_highways AS
(
SELECT DISTINCT
  indoor_surfaces.id,
  indoor_surfaces.geom,
  indoor_surfaces.indoor,
  indoor_surfaces.level as surface_level,
  highway_ends.nid,
  highway_ends.highway,
  highways.tags->'level' as connected_highway_level
FROM
  indoor_surfaces
JOIN way_nodes ON indoor_surfaces.id = way_nodes.way_id
JOIN nodes ON nodes.id = way_nodes.node_id
JOIN highway_ends ON nodes.id = highway_ends.nid
JOIN highways ON highway_ends.id = highways.id
WHERE
  indoor_surfaces.tags->'indoor' IN ('room', 'corridor', 'area')
  AND highways.highway IN ('steps', 'footway', 'pedestrian')
)
"""

# TODO : check that all surfaces have at least one connected_highway_level that matches it own surface_level
# (dealing with level="0;1" that occurs on highway=steps
# and assuming than no level on highway is probably implicit level=0)

sql61 = """
CREATE TEMP TABLE indoor_surfaces_connected_to_other_surfaces AS
(
  SELECT DISTINCT
  i1.id as id,
  i1.level as surface_level,
  i2.id as other_surface_id,
  i2.level as other_surface_level
FROM
  way_nodes w2
JOIN way_nodes w1 ON w1.node_id = w2.node_id
JOIN indoor_surfaces i1 ON i1.id = w1.way_id
JOIN indoor_surfaces i2 ON i2.id = w2.way_id
WHERE
  i1.id <> i2.id
  AND i1.tags->'indoor' IN ('room', 'corridor', 'area')
)
""" # maybe check the levels too to make sure they are actually connected ?

sql62 = """
SELECT
  indoor_surfaces.id,
  indoor_surfaces.geom
FROM
  indoor_surfaces
LEFT JOIN indoor_surfaces_connected_to_other_surfaces ON indoor_surfaces_connected_to_other_surfaces.id = indoor_surfaces.id
LEFT JOIN indoor_surfaces_connected_to_highways ON indoor_surfaces_connected_to_highways.id = indoor_surfaces.id
WHERE
  indoor_surfaces.tags->'indoor' IN ('room', 'corridor', 'area')
  AND indoor_surfaces_connected_to_highways.id IS NULL
  AND indoor_surfaces_connected_to_other_surfaces.id is NULL
"""

class Analyser_Osmosis_Indoor(Analyser_Osmosis):
    requires_tables_common = ['highway_ends']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 9999, level = 3, tags = ['indoor', 'geom', 'fix:chair'],
            title = T_('This indoor feature should be a closed and valid polygon'))
        self.classs[2] = self.def_class(item = 9999, level = 3, tags = ['indoor', 'geom', 'fix:chair'],
            title = T_('This indoor feature should be a polygon instead of a point'),
            fix = T_(
'''If this feature is actually an indoor area, try to map it as a closed way.
If this is an indoor object (any kind of feature located inside a building),
consider using indoor=yes instead'''))
        self.classs[3] = self.def_class(item = 9999, level = 3, tags = ['indoor', 'geom', 'fix:survey'],
            title = T_('This indoor room should have a door'),
            fix = T_(
'''Find out where are the entrances of the room and add them (with a door=* tag) so we can actually enter this indoor room'''))
        self.classs[4] = self.def_class(item = 9999, level = 3, tags = ['indoor', 'geom', 'fix:survey'],
            title = T_('This indoor feature should have a level'),
            fix = T_(
'''Find out which level is the room/area/corridor in and add it with the level=* tag'''))
        self.classs[5] = self.def_class(item = 9999, level = 3, tags = ['indoor', 'geom', 'fix:survey', 'shop'],
            title = T_('This indoor shop should probably be inside a room'),
            fix = T_(
'''Indoor shops are usually enclosed by walls, so they should have indoor=room + room=shop'''))
        self.classs[6] = self.def_class(item = 9999, level = 3, tags = ['indoor', 'geom', 'fix:survey'],
            title = T_('This indoor feature is not reachable'),
            detail = T_(
'''Each indoor feature should be connected to an another indoor feature or to some footpath so people can actually go to them.'''))

        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.way_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.way_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":5, "data":[self.way_full, self.positionAsText]}
        self.callback60 = lambda res: {"class":6, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
        self.run(sql30)
        self.run(sql31, self.callback30)
        self.run(sql00)
        self.run(sql40, self.callback40)
        self.run(sql50, self.callback50)
        self.run(sql60)
        self.run(sql61)
        self.run(sql62, self.callback60)
