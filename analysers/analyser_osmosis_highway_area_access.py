#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo <@free.fr> 2016                           ##
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
  nodes.id,
  ways.id,
  ST_AsText(nodes.geom),
  nodes.tags->'motor_vehicle' AS node_motor_vehicle,
  ways.tags->'motor_vehicle' AS way_motor_vehicle
FROM
  {0}nodes AS nodes
  JOIN way_nodes ON
    way_nodes.node_id = nodes.id
  JOIN {1}highways AS ways ON
    ways.id = way_nodes.way_id AND
    ways.highway = 'pedestrian' AND
    NOT ways.is_area AND
    NOT ways.is_construction
WHERE
  nodes.tags != ''::hstore AND
  nodes.tags?'barrier' AND
  nodes.tags->'barrier' = 'bollard' AND
  (NOT ways.tags?'motor_vehicle' OR ways.tags->'motor_vehicle' != 'no') AND
  (
    (ways.tags?'motor_vehicle' AND NOT nodes.tags?'motor_vehicle') OR
    (NOT ways.tags?'motor_vehicle' AND nodes.tags?'motor_vehicle') OR
    (ways.tags?'motor_vehicle' AND nodes.tags?'motor_vehicle' AND (ways.tags->'motor_vehicle') != (nodes.tags->'motor_vehicle'))
  )
"""

sql20 = """
CREATE TEMP TABLE {barriertype} AS
SELECT
  barrier.id AS id,
  barrier.tags AS tags,
  ways.id AS wid,
  barrier.geom AS geom,
  ways.tags AS waytags
FROM
  nodes AS barrier
  JOIN highways AS ways ON
    barrier.id = ANY(ways.nodes) AND
    NOT ways.is_construction AND
    NOT ways.is_area
WHERE
  barrier.tags != ''::hstore AND
  -- barrier.tags?'barrier' AND -- commented to avoid planner to try to use idx_nodes_tags, build bad plan with it. Very slow
  barrier.tags->'barrier' = '{barriertype}' AND
  -- Default of bollard is access=no / bicycle=foot=yes; default of bus_trap is motor_vehicle=no / psv=foot=bicycle=yes.
  -- Hence, the below three lines should cover all cases as long as we don't test for any non-motor_vehicle or vehicles under psv
  (NOT barrier.tags?'access' OR barrier.tags->'access' = 'no') AND
  (NOT barrier.tags?'vehicle' OR barrier.tags->'vehicle' = 'no') AND
  (NOT barrier.tags?'motor_vehicle' OR barrier.tags->'motor_vehicle' = 'no') AND
  barrier.id != ways.nodes[1] AND barrier.id != ways.nodes[array_length(ways.nodes,1)] -- Barrier is not an end node
"""

sql21 = """
SELECT
    barrier.wid,
    barrier.id,
    ST_AsText(barrier.geom),
    barrier.waytags->'{vehicle}'
FROM
    {barriertype} AS barrier
WHERE
    NOT barrier.tags?'{vehicle}' AND
    barrier.waytags?'{vehicle}' AND
    NOT barrier.waytags->'{vehicle}' IN ('no', 'use_sidepath', 'unknown')
"""

sql31 = """
SELECT
  highways.id,
  barrier.id,
  ST_AsText(barrier.geom)
FROM
  highways
  JOIN nodes AS barrier ON
    barrier.tags != ''::hstore AND
    barrier.id = ANY(highways.nodes) AND
    --barrier.tags?'barrier' AND -- commented to prevent slow route
    barrier.tags->'barrier' NOT IN ('border_control', 'cattle_grid', 'entrance', 'height_restrictor', 'toll_booth') AND
    NOT (barrier.tags?'access' OR barrier.tags?'access:conditional') AND
    NOT (barrier.tags?'vehicle' OR barrier.tags?'vehicle:conditional') AND
    NOT (barrier.tags?'motor_vehicle' OR barrier.tags?'motor_vehicle:conditional')
WHERE
  highways.level <= 3 AND
  NOT (highways.tags?'access' OR highways.tags?'access:conditional') AND
  NOT (highways.tags?'vehicle' OR highways.tags?'vehicle:conditional') AND
  NOT (highways.tags?'motor_vehicle' OR highways.tags?'motor_vehicle:conditional')
"""


sql41 = """
SELECT
  ways.id,
  barrier.id,
  ST_AsText(barrier.geom)
FROM
  highways AS ways
  JOIN way_nodes ON
    way_nodes.way_id = ways.id
  JOIN nodes AS barrier ON
    barrier.tags != ''::hstore AND
    barrier.id = way_nodes.node_id AND
    --barrier.id = ANY(ways.nodes) will cause a very slow planning (focused on the X.tags?'Y') on some countries (e.g. japan_chubu)
    barrier.tags?'barrier' AND
    barrier.tags->'barrier' NOT IN ('bollard', 'border_control', 'cattle_grid', 'entrance', 'height_restrictor', 'toll_booth') AND
    barrier.id != ways.nodes[1] AND barrier.id != ways.nodes[array_length(ways.nodes,1)] AND -- Barrier is not an end node
    NOT (barrier.tags?'access' OR barrier.tags?'access:conditional') AND
    NOT (barrier.tags?'vehicle' OR barrier.tags?'vehicle:conditional') AND
    NOT (barrier.tags?'motor_vehicle' OR barrier.tags?'motor_vehicle:conditional')
  JOIN highways AS minor_highway ON
    barrier.id = ANY(minor_highway.nodes) AND
    (minor_highway.level IS NULL OR minor_highway.level > 4)
WHERE
  ways.level = 4 AND
  NOT (ways.tags?'access' OR ways.tags?'access:conditional') AND
  NOT (ways.tags?'vehicle' OR ways.tags?'vehicle:conditional') AND
  NOT (ways.tags?'motor_vehicle' OR ways.tags?'motor_vehicle:conditional')
"""


class Analyser_Osmosis_HighwayAreaAccess(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs_change[1] = self.def_class(item = 2130, level = 3, tags = ['highway', 'routing'],
            title = T_('Inconsistent Access'),
            detail = T_(
'''Inconsistent `motor_vehicle` values.'''))
        self.classs[2] = self.def_class(item = 2130, level = 3, tags = ['highway', 'routing'],
            title = T_('Inconsistent Access'),
            detail = T_(
'''Inconsistent access values between barrier and highway.'''),
            trap = T_(
'''Sometimes a barrier can exist on an (otherwise uninterrupted) highway to prevent vehicles from using it for purposes other than destination traffic.'''),
            fix = T_(
'''Copy the appropriate access tag to the barrier node.'''))
        self.classs[3] = self.def_class(item = 2130, level = 2, tags = ['highway', 'routing'],
            title = T_('Barrier blocking major highway'),
            detail = T_(
'''A barrier is blocking a major highway. Typically, major highways (`tertiary` and above) are meant for passing traffic.'''),
            fix = T_(
'''Check if there is really a barrier on the highway itself (instead of for instance a connecting minor way only).
If there is no such barrier, remove it, or move it to the appropriate connecting way.
If there is a barrier, check if it has the appropriate (conditional) access keys.'''))
        self.classs[4] = self.def_class(item = 2130, level = 3, tags = ['highway', 'routing'],
            title = T_('Barrier blocking highway'),
            detail = T_(
'''A barrier is blocking a residential or unclassified way on a crossing with a minor highway.
Likely the barrier was only supposed to be present on the minor road.'''),
            trap = T_(
'''Sometimes a barrier can exist on an (otherwise uninterrupted) highway to prevent vehicles from using it for purposes other than destination traffic.'''),
            fix = T_(
'''Check if there is really a barrier on the highway itself (instead of for instance a connecting minor way only).
If there is no such barrier, remove it, or move it to the appropriate connecting way.
If there is a barrier, check if it has the appropriate (conditional) access keys.'''))
        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.way_full, self.positionAsText],
            "text": T_("Inconsistent motor_vehicle values ('{0}'!='{1}')", res[3] if res[3] else '', res[4] if res[4] else '') }

    def analyser_osmosis_common(self):
        self.run(sql20.format(barriertype='bollard'))
        self.run(sql20.format(barriertype='bus_trap'))
        for vehicle in ['motorcycle', 'mofa', 'moped', 'emergency', 'motorcar']:
            self.run(sql21.format(barriertype='bollard', vehicle=vehicle), lambda res: {
                "class":2, "data":[self.way_full, self.node_full, self.positionAsText],
                "text": T_("Inconsistent {0} access: '{1}' on highway, not set on barrier", vehicle, res[3])})
        for vehicle in ['motorcycle', 'mofa', 'moped', 'agricultural', 'hgv', 'emergency']:
            self.run(sql21.format(barriertype='bus_trap', vehicle=vehicle), lambda res: {
                "class":2, "data":[self.way_full, self.node_full, self.positionAsText],
                "text": T_("Inconsistent {0} access: '{1}' on highway, not set on barrier", vehicle, res[3])})

        self.run(sql31, lambda res: {
            "class": 3, "data":[self.way, self.node_full, self.positionAsText]
        })
        self.run(sql41, lambda res: {
            "class": 4, "data":[self.way, self.node_full, self.positionAsText]
        })

    def analyser_osmosis_full(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_", "not_touched_"), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)



###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_highway_access_barrier.osm",
                                         config.dir_tmp + "/tests/osmosis_highway_access_barrier.test.xml",
                                         {"proj": 2154}) # Random proj to satisfy highway table generation

    def test_classes(self):
        with Analyser_Osmosis_HighwayAreaAccess(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("node", "24"), ("way", "108")])
        self.check_err(cl="1", elems=[("node", "29"), ("way", "109")])
        self.check_err(cl="1", elems=[("node", "30"), ("way", "110")])
        self.check_err(cl="2", elems=[("node", "20"), ("way", "107")])
        self.check_err(cl="2", elems=[("node", "37"), ("way", "107")])
        self.check_err(cl="3", elems=[("node", "46"), ("way", "116")])
        self.check_err(cl="3", elems=[("node", "47"), ("way", "116")])
        self.check_err(cl="4", elems=[("node", "55"), ("way", "118")])
        self.check_err(cl="4", elems=[("node", "56"), ("way", "118")])
        self.check_num_err(9)
