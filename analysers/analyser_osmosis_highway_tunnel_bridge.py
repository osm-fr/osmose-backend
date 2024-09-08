#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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
    {0}ways
WHERE
    tags != ''::hstore AND
    (
        tags?'railway' OR
        (tags?'highway' AND tags->'highway' IN ('motorway', 'trunk', 'primary', 'secondary'))
    ) AND
    tags?'bridge' AND
    tags->'bridge' = 'yes' AND
    ST_Length(linestring::geography) > 500 AND
    NOT tags?'bridge:structure'
"""

sql20 = """
CREATE TEMP TABLE bridge_cross AS
SELECT
    ways.id,
    ways.tags,
    ways.linestring,
    bridge.id AS bid,
    bridge.tags AS btags,
    bridge.linestring AS blinestring
FROM
    ways AS bridge
    JOIN ways ON
        bridge.id != ways.id AND
        bridge.linestring && ways.linestring AND
        ST_Crosses(bridge.linestring, ways.linestring)
WHERE
    bridge.tags != ''::hstore AND
    bridge.tags ?| ARRAY['highway', 'railway'] AND
    bridge.tags?'bridge' AND
    bridge.tags->'bridge' != 'no' AND
    ST_NPoints(bridge.linestring) > 1 AND
    ways.tags != ''::hstore AND
    ways.tags ?| ARRAY['highway', 'railway', 'waterway'] AND
    ST_NPoints(ways.linestring) > 1
"""

sql21 = """
SELECT
    id,
    bid,
    ST_AsText(ST_Centroid(ST_Intersection(blinestring, linestring)))
FROM
    bridge_cross
WHERE
    tags?'highway' AND
    tags->'highway' IN ('motorway_link', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link')
"""

sql30 = """
SELECT
    bid,
    ST_AsText(way_locate(blinestring))
FROM
    (
        SELECT
            tags->'layer' AS layer,
            btags->'layer' AS blayer,
            bid,
            blinestring
        FROM
            bridge_cross
    ) AS t
GROUP BY
    bid,
    blayer,
    blinestring
HAVING
    0 = SUM(CASE WHEN layer IS NULL THEN 0 ELSE 1 END) + CASE WHEN blayer IS NULL THEN 0 ELSE 1 END
"""

sql40 = """
SELECT
    nodes.id,
    bt_ways.id,
    bt_connections.id,
    ST_AsText(nodes.geom),
    CASE
        WHEN bt_ways.tags?'bridge' AND bt_ways.tags->'bridge'!='no' THEN 'bridge'
        ELSE 'tunnel'
    END,
    nodes.id IN (bt_connections.nodes[1], bt_connections.nodes[array_length(bt_connections.nodes,1)]) OR bt_connections.is_area
FROM
    {0}highways AS bt_ways
    JOIN {1}highways AS bt_connections ON
        bt_connections.linestring && bt_ways.linestring AND
        bt_connections.nodes && bt_ways.nodes AND
        bt_connections.id != bt_ways.id
    JOIN nodes ON
        nodes.geom && bt_connections.linestring AND nodes.geom && bt_ways.linestring AND -- One is redundant, but let the planner choose
        nodes.id = ANY(bt_ways.nodes) AND
        nodes.id = ANY(bt_connections.nodes) AND
        nodes.id != bt_ways.nodes[1] AND
        nodes.id != bt_ways.nodes[array_length(bt_ways.nodes,1)]
WHERE
    (
        (
            bt_ways.highway NOT IN ('steps') AND
            bt_connections.highway NOT IN ('steps') AND
            bt_ways.tags?'bridge' AND bt_ways.tags->'bridge' NOT IN ('no', 'boardwalk') AND
            (NOT bt_connections.tags?'bridge' OR bt_connections.tags->'bridge' = 'no') AND
            (NOT bt_connections.tags?'man_made' OR bt_connections.tags->'man_made' != 'pier')
        ) OR (
            -- Tunnels for 'low level' highways give many false positives, hence only enable for crossing 'car roads'
            bt_ways.level <= 4 AND bt_connections.level <= 4 AND
            bt_ways.tags?'tunnel' AND bt_ways.tags->'tunnel' NOT IN ('no', 'avalanche_protector') AND
            (NOT bt_connections.tags?'tunnel' OR bt_connections.tags->'tunnel' = 'no') AND
            (NOT bt_connections.tags?'covered' OR bt_connections.tags->'covered' = 'no')
        )
    ) AND
    NOT bt_ways.is_area AND -- any point of an area can be an end point
    NOT bt_ways.is_construction AND NOT bt_connections.is_construction AND
    -- Below: filter all cases where one would for instance walk from a building directly onto a bridge
    (NOT bt_connections.tags?'indoor' OR bt_connections.tags->'indoor' = 'no') AND
    NOT bt_connections.tags?'location' AND
    NOT bt_connections.tags?'level'
"""


class Analyser_Osmosis_Highway_Tunnel_Bridge(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['highways', 'touched_highways', 'not_touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 7012, level = 3, tags = ['tag', 'highway', 'fix:survey'],
            title = T_('Bridge structure missing'),
            detail = T_(
'''The length of the bridge makes it deserve a more detailed tag than
`bridge=yes`.'''),
            fix = T_(
'''See the possible [types of
bridges](https://wiki.openstreetmap.org/wiki/Key:bridge).'''))
        #self.classs_change[2] = self.def_class(item = 7130, level = 3, tags = ['tag', 'highway', 'maxheight', "fix:survey"],
        #    title = T_('Missing maxheight tag'))
        #self.classs_change[3] = self.def_class(item = 7130, level = 3, tags = ['tag', 'highway', 'layer', "fix:imagery"],
        #    title = T_('Missing layer tag around bridge'))
        doc = dict(
            detail = T_(
'''A bridge or tunnel is usually not connected to regular highways except at the end points.'''),
            fix = T_(
'''Disconnect the bridge or tunnel from the highway, or add missing bridge or tunnel tags.

If the highway is truely connected to the bridge or tunnel, it may only be by a short section of this highway.
If so, you may have to split the connecting way and add bridge or tunnel tags only on the relevant part.

If the bridge or tunnel actually consists of more than one bridge or tunnel separated by a section of regular highway,
split the bridge or tunnel and adjust the tags accordingly.'''),
            trap = T_(
'''There might be bad detections with connections at the bridge heads or tunnel entrances.''')
        )
        self.classs_change[4] = self.def_class(item = 7012, level = 2, tags = ['highway', 'fix:survey', 'fix:imagery', 'routing'],
            title = T_('Bridge connected to crossing non-bridge highway'), **doc)
        self.classs_change[5] = self.def_class(item = 7012, level = 2, tags = ['highway', 'fix:survey', 'fix:imagery', 'routing'],
            title = T_('Tunnel connected to crossing non-tunnel highway'), **doc)
        self.classs_change[6] = self.def_class(item = 7012, level = 3, tags = ['highway', 'fix:survey', 'fix:imagery'],
            title = T_('Bridge connected to non-bridge highway'), **doc)
        self.classs_change[7] = self.def_class(item = 7012, level = 3, tags = ['highway', 'fix:survey', 'fix:imagery'],
            title = T_('Tunnel connected to non-tunnel highway'), **doc)

        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "fix":[{"+":{"bridge:structure":"beam"}}, {"+":{"bridge:structure":"suspension"}}] }
        #self.callback20 = lambda res: {"class":2, "data":[self.way_full, self.way_full, self.positionAsText] }
        #self.callback30 = lambda res: {"class":3, "data":[self.way_full, self.positionAsText] }
        self.callback40 = lambda res: {"class": (4 if res[4] == 'bridge' else 5) + (2 if res[5] else 0), "data": [self.node_full, self.way_full, self.way_full, self.positionAsText] }

    def analyser_osmosis_full(self):
        self.run(sql10.format(""), self.callback10)
        #self.run(sql20.format("", ""))
        #self.run(sql21, self.callback20)
        #self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format("", ""), self.callback40)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_"), self.callback10)
        #self.run(sql20.format("touched_", ""))
        #self.run(sql21, self.callback20)
        #self.run(sql30, self.callback30)
        #self.run(sql20.format("", "touched_"))
        #self.run(sql21, self.callback20)
        #self.run(sql30, self.callback30)
        self.run(sql40.format("touched_", ""), self.callback40)
        self.run(sql40.format("not_touched_", "touched_"), self.callback40)

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_highway_tunnel_bridge.osm",
                                         config.dir_tmp + "/tests/osmosis_highway_tunnel_bridge.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Highway_Tunnel_Bridge(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "1018")])
        self.check_err(cl="4", elems=[("node", "30"), ("way", "1008"), ("way", "1014")])
        self.check_err(cl="5", elems=[("node", "13"), ("way", "1004"), ("way", "1005")])
        self.check_err(cl="6", elems=[("node", "26"), ("way", "1008"), ("way", "1013")])
        self.check_err(cl="6", elems=[("node", "39"), ("way", "1008"), ("way", "1019")])
        self.check_err(cl="6", elems=[("node", "39"), ("way", "1008"), ("way", "1020")])
        self.check_err(cl="7", elems=[("node", "42"), ("way", "1004"), ("way", "1022")])
        self.check_num_err(7)
