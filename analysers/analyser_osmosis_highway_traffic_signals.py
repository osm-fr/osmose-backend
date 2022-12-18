#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013-2016                                 ##
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
CREATE TEMP TABLE traffic_signals AS
SELECT
    id,
    geom,
    tags,
    tags?'crossing' AND tags->'crossing' != 'no' AS crossing,
    ST_Buffer(geom::geography, 40) AS buffer
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' = 'traffic_signals'
"""

sql11 = """
CREATE INDEX traffic_signals_buffer ON traffic_signals USING GIST(buffer)
"""

sql12 = """
CREATE TEMP TABLE crossing AS
SELECT
    id,
    geom::geography,
    tags->'crossing' AS crossing
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' = 'crossing'
"""

sql13 = """
CREATE INDEX crossing_geom ON crossing USING GIST(geom)
"""

sql14 = """
SELECT
    DISTINCT ON(crossing.id)
    crossing.id,
    traffic_signals.id,
    ST_AsText(crossing.geom)
FROM
    {0}traffic_signals AS traffic_signals
    JOIN {1}crossing AS crossing ON
        crossing.geom && traffic_signals.buffer AND
        crossing.crossing IS NULL
WHERE
    traffic_signals.crossing
ORDER BY
    crossing.id
"""

sql20 = """
SELECT
    crossing.id,
    ST_AsText(crossing.geom)
FROM
    {0}crossing AS crossing
    LEFT JOIN traffic_signals AS traffic_signals ON
        crossing.geom && traffic_signals.buffer
WHERE
    crossing.crossing = 'traffic_signals' AND
    traffic_signals.id IS NULL
"""

sql30 = """
SELECT
  nodes.id,
  max(ways.id),
  ST_AsText(nodes.geom)
FROM
  traffic_signals AS nodes
  JOIN way_nodes ON
    way_nodes.node_id = nodes.id
  JOIN highways AS ways ON
    ways.id = way_nodes.way_id
WHERE
  (NOT nodes.tags?'traffic_signals:direction' OR nodes.tags->'traffic_signals:direction' NOT IN('backward', 'forward')) AND
  (NOT nodes.tags?'direction' OR nodes.tags->'direction' NOT IN('backward', 'forward')) AND -- deprecated, move to traffic_signals:direction
  (NOT nodes.tags?'crossing' OR nodes.tags->'crossing' = 'no')
GROUP BY
  nodes.id,
  nodes.geom
HAVING
  COUNT(*) = 1 AND
  BOOL_AND(NOT ways.tags?'oneway' OR ways.tags->'oneway' IN ('no', 'false')) AND
  BOOL_AND(NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout')
"""

sql40 = """
CREATE TEMP TABLE stops AS
SELECT
    id,
    geom,
    tags
FROM
    nodes AS nodes
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' IN ('stop', 'give_way') AND
    (NOT nodes.tags?'direction' OR nodes.tags->'direction' NOT IN('backward', 'forward')) AND
    (NOT nodes.tags?'traffic_sign:direction' OR nodes.tags->'traffic_sign:direction' NOT IN('backward', 'forward')) AND
    NOT nodes.tags?'traffic_sign:forward' AND
    NOT nodes.tags?'traffic_sign:backward'
"""

sql41 = """
SELECT
  nodes.id,
  max(ways.id),
  ST_AsText(nodes.geom)
FROM
  stops AS nodes
  JOIN highways AS ways ON
    ways.linestring && nodes.geom AND
    nodes.id = ANY (ways.nodes)
GROUP BY
  nodes.id,
  nodes.geom
HAVING
  COUNT(*) = 1 AND
  BOOL_AND(NOT ways.tags?'oneway' OR ways.tags->'oneway' IN ('no', 'false')) AND
  BOOL_AND(NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout')
"""

class Analyser_Osmosis_Highway_Traffic_Signals(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''A nearby node already has the `highway=traffic_signals` tag.'''),
            fix = T_(
'''It is very likely that the traffic signals on the junction are
inconsistent with each other, see also
[highway=traffic_signals](https://wiki.openstreetmap.org/wiki/Tag:highway%3Dtraffic_signals).'''))
        self.classs_change[1] = self.def_class(item = 2090, level = 3, tags = ['tag', 'highway', 'fix:imagery'],
            title = T_('Possible crossing=traffic_signals'),
            **doc)
        self.classs_change[2] = self.def_class(item = 2090, level = 2, tags = ['tag', 'highway', 'fix:imagery'],
            title = T_('Possible missing highway=traffic_signals nearby'),
            **doc)
        self.classs[3] = self.def_class(item = 2090, level = 2, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Possible missing traffic_signals:direction tag or crossing on traffic signals'))
        self.classs[4] = self.def_class(item = 2090, level = 2, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Possible missing direction tag on stop or a give way'))

        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.node_full, self.positionAsText], "fix":[
            [{"+":{"crossing":"traffic_signals"}}],
            [{"+":{"crossing":"traffic_signals"}}, {"-":["crossing"]}]
        ] }
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.way, self.positionAsText], "fix":[
            [{"+":{"traffic_signals:direction":"forward"}}],
            [{"+":{"traffic_signals:direction":"backward"}}],
        ] }
        self.callback40 = lambda res: {"class":4, "data":[self.node_full, self.way, self.positionAsText], "fix":[
            [{"+":{"direction":"forward"}}],
            [{"+":{"direction":"backward"}}],
        ] }

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13)

        self.run(sql30, self.callback30)

        self.run(sql40)
        self.run(sql41, self.callback40)

    def analyser_osmosis_full(self):
        self.run(sql14.format("", ""), self.callback10)
        self.run(sql20.format(""), self.callback20)

    def analyser_osmosis_diff(self):
        self.create_view_touched("traffic_signals", "N")
        self.create_view_not_touched("traffic_signals", "N")
        self.create_view_touched("crossing", "N")

        self.run(sql14.format("touched_", ""), self.callback10)
        self.run(sql14.format("not_touched_", "touched_"), self.callback10)

        self.run(sql20.format("touched_"), self.callback20)
