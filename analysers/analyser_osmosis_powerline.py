#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011-2014                                 ##
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
from modules.Stablehash import stablehash64

# Power lines nodes with their voltage as array padded up to 99 zeros to cope with non-numerical values
# Lines with no voltage get null voltage instead empty array
sql01 = """
CREATE TEMP TABLE power_lines_nodes AS
SELECT
    w.id as wid,
    unnest('{NULL}' || w.nodes[1:array_length(w.nodes, 1) - 1]) AS nid_prec,
    unnest(w.nodes) AS nid,
    unnest(w.nodes[2:]) AS nid_next,
    w.tags->'cables' AS cables,
    coalesce((w.tags->'circuits')::integer, 1) AS circuits,
    coalesce(w.tags->'location', 'overhead') AS location,
    voltage
FROM
    ways AS w
    JOIN LATERAL (
        SELECT array_agg(lpad(v, 99, '0'))
        FROM (SELECT
            unnest(array_cat(
                array_fill(
                    split_part(w.tags->'voltage', ';', 1)::text, -- voltage1 in voltage1;voltage2
                    ARRAY[greatest(0, coalesce((w.tags->'circuits')::integer, 1) - (1 + length(coalesce(w.tags->'voltage', '')) - length(replace(coalesce(w.tags->'voltage',''), ';', ''))))]
                ),
                regexp_split_to_array(w.tags->'voltage', '; *'))
            ) LIMIT coalesce((w.tags->'circuits')::integer, 1)
        ) AS t(v)) AS t(voltage)
        ON TRUE
WHERE
    w.tags != ''::hstore AND
    w.tags?'power' AND
    w.tags->'power' IN ('line', 'minor_line', 'cable') AND
    w.tags?'voltage' AND
    (
        NOT w.tags?'circuits' OR
        w.tags->'circuits' ~ '^[0-9]+$'
    )

UNION ALL

SELECT
    w.id AS wid,
    unnest('{NULL}' || w.nodes[1:array_length(w.nodes, 1) - 1]) AS nid_prec,
    unnest(w.nodes) AS nid,
    unnest(w.nodes[2:array_length(w.nodes, 1)]) AS nid_next,
    w.tags->'cables' AS cables,
    coalesce((w.tags->'circuits')::integer, 1) AS circuits,
    coalesce(w.tags->'location', 'overhead') AS location,
    NULL AS voltage
FROM
   ways AS w
WHERE
    w.tags != ''::hstore AND
    w.tags?'power' AND
    w.tags->'power' IN ('line', 'minor_line', 'cable') AND
    (
        NOT w.tags?'voltage' OR (
            w.tags?'circuits' AND
            NOT(w.tags->'circuits' ~ '^[0-9]+$')
        )
    )
"""

# Build junctions knowledge
# Topoedges are couples attached to a given node with their neighbors.
# Topoedges are agregated by nodes and location (two *overhead* lines between two node will give a single topoedge)
# Involved nodes are not necessary power, particularly on cables
sql02 = """
CREATE TEMP TABLE power_lines_topoedges AS
WITH topotuples as (
    SELECT
        n.wid,
        n.nid # n.nid_prec AS tid,
        n.nid,
        n.location,
        n.cables,
        n.circuits,
        voltage
    FROM
        power_lines_nodes AS n
    WHERE
        nid_prec IS NOT NULL

    UNION ALL

    SELECT
        n.wid,
        n.nid # n.nid_next as tid,
        n.nid,
        n.location,
        n.cables,
        n.circuits,
        voltage
    FROM
        power_lines_nodes AS n
    WHERE
        nid_next IS NOT NULL
)

SELECT
    p.nid,
    p.tid,
    p.location,
    count(distinct p.wid) AS cw,
    sum(p.circuits::integer) AS circuits,
    regexp_split_to_array(string_agg(array_to_string(p.voltage, ';'), ';'), '; *') AS voltage
FROM
    topotuples p
GROUP BY
    p.nid, p.tid, p.location
HAVING
    array_position(array_agg(p.circuits), NULL) IS NULL
"""

# Lone power supports
# TODO rework by using exclusion from power_lines_nodes, it will save a join and work on a lower amount of pre-selected power nodes
sql10 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    nodes
    LEFT JOIN way_nodes ON
        way_nodes.node_id = nodes.id
    LEFT JOIN ways ON
        ways.id = way_nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags?'power' AND
        ways.tags->'power' IN ('line', 'minor_line', 'cable')
WHERE
    nodes.tags != ''::hstore AND
    nodes.tags?'power' AND
    nodes.tags->'power' IN ('pole', 'tower', 'insulator', 'terminal', 'portal')
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    bool_and(ways.id IS NULL)
"""

# Power lines ends with their voltages as array padded with up to 99 zeros
# TODO rework this analysis with topoedges, find topoedges that end a line and conflate them with terminators.
sql20 = """
CREATE TEMP TABLE power_lines_ends AS
SELECT DISTINCT ON (ends(ways.nodes))
    ways.id AS wid,
    ends(ways.nodes) AS nid,
    ways.tags->'power' AS power,
    (SELECT array_agg(lpad(v, 99, '0')) FROM unnest(regexp_split_to_array(ways.tags->'voltage','; *')) AS t(v)) AS voltage
FROM
    ways
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line', 'cable')
ORDER BY
    ends(ways.nodes)
"""

sql21 = """
CREATE INDEX idx_line_ends_id ON power_lines_ends(nid)
"""

# Unfinished lines ends
sql22 = """
CREATE TEMP TABLE power_lines_unfinished AS
SELECT
    line_ends.wid,
    line_ends.nid,
    line_ends.power,
    line_ends.voltage,
    nodes.geom::geography
FROM
    (
    SELECT
        e.wid,
        e.nid,
        e.power,
        e.voltage
    FROM
        power_lines_ends e
        LEFT JOIN power_lines_ends AS other ON
        e.wid != other.wid AND
            e.nid = other.nid
    WHERE
        other.nid IS NULL
    ) AS line_ends
    JOIN nodes ON
        line_ends.nid = nodes.id
    WHERE
        NOT (nodes.tags?'location:transition' AND nodes.tags->'location:transition' = 'yes') AND
        NOT (nodes.tags?'transformer' AND nodes.tags->'transformer' in ('distribution', 'main')) AND
        NOT (nodes.tags?'substation' AND nodes.tags->'substation' = 'minor_distribution') AND
        NOT (nodes.tags?'line_management' AND nodes.tags->'line_management' IN ('transition','termination')) AND
        NOT (nodes.tags?'power' AND nodes.tags->'power' = 'terminal')
"""

sql23 = """
CREATE INDEX idx_line_ends1_geom ON power_lines_unfinished USING GIST(geom)
"""

sql24 = """
CREATE TEMP TABLE power_lines_terminators AS
(
SELECT
    'N' || id AS type_id,
    geom::geography,
    tags->'power' AS power,
    tags->'substation' AS substation,
    (SELECT array_agg(lpad(v, 99, '0')) FROM unnest(regexp_split_to_array(tags->'voltage','; *')) AS t(v)) AS voltage
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'power' AND
    tags->'power' NOT IN ('pole', 'tower', 'portal')
)
UNION ALL
(
SELECT
    'W' || id AS type_id,
    ST_MakePolygon(linestring)::geography AS geom,
    tags->'power' AS power,
    tags->'substation' AS substation,
    (SELECT array_agg(lpad(v, 99, '0')) FROM unnest(regexp_split_to_array(tags->'voltage','; *')) AS t(v)) AS voltage
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'power' AND
    tags->'power' NOT IN ('line', 'minor_line', 'cable') AND
    is_polygon
)
"""

sql25 = """
CREATE INDEX idx_line_terminators_geom ON power_lines_terminators USING GIST(geom)
"""

# Find every unfinished end that isn't near of any terminator
sql26 = """
SELECT
    t.nid,
    t.wid,
    ST_AsText(t.geom),
    t.power
FROM (
SELECT
    u.nid,
    u.wid,
    u.geom,
    u.power
FROM
    power_lines_unfinished u

EXCEPT

SELECT
    u.nid,
    u.wid,
    u.geom,
    u.power
FROM
    power_lines_unfinished u
    JOIN power_lines_terminators plt ON
        ST_DWithin(u.geom, plt.geom, 50)

EXCEPT

SELECT
    u.nid,
    u.wid,
    u.geom,
    u.power
FROM
    power_lines_unfinished u
    JOIN ways ON
        ways.id != u.wid AND
        ways.tags != ''::hstore AND
        ways.tags?'power' AND
        ways.tags->'power' IN ('line', 'minor_line', 'cable') AND
        ways.linestring && u.geom AND
        u.nid = ANY(ways.nodes)
) AS t
"""

# Every plain line junction that isn't transformers, termination or cross repeated twice (main and / sqrt(3)) (meaning the junction involves different voltages)
# It looks for voltage continuation on every junction. Two (or more) topoedges on a given node with the same voltage means a connection.
# TODO support partial termination (i.e termination|straight) with different voltages involved.
sql30 = """
WITH nodes_voltage AS (
    SELECT
        nid,
        tid,
        unnest(voltage)::varchar AS voltage
    FROM
        power_lines_topoedges
),
nodes_voltage_values AS (
    SELECT
        nid,
        tid,
        voltage,
        round((voltage::numeric / 1000)::numeric,1)::varchar AS voltage_val,
        'numeric' AS origin
    FROM
        nodes_voltage
    WHERE
        voltage ~ '^[0-9.]+$'

    UNION

    SELECT
        nid,
        tid,
        voltage AS voltage,
        round((voltage::numeric / (1000 * sqrt(3)))::numeric,1)::varchar AS voltage_val,
        'numeric' AS origin
    FROM
        nodes_voltage
    WHERE
        voltage ~ '^[0-9.]+$'

    UNION

    SELECT
        nid,
        tid,
        voltage AS voltage,
        voltage AS voltage_val,
        'varchar' AS origin
    FROM
        nodes_voltage
    WHERE
        NOT(voltage ~ '^[0-9.]+$')
),

nodes_selected AS (
    SELECT
        nid
    FROM
        power_lines_topoedges
    GROUP BY
        nid
    HAVING
        count(distinct tid) > 1
),
voltage_groups AS (
    SELECT
        n.nid,
        max(n.voltage) AS voltage,
        n.voltage_val,
        count(n.voltage) AS cv,
        n.origin
    FROM
        nodes_voltage_values AS n
        JOIN nodes_selected AS s ON
            s.nid = n.nid
    GROUP BY
        n.nid, n.voltage_val, n.origin
)

SELECT
    DISTINCT(v.nid),
    ST_AsText(nodes.geom)
FROM
    voltage_groups AS v
    JOIN nodes ON
        v.nid = nodes.id
WHERE
    (
        NOT nodes.tags?'power' OR
        nodes.tags->'power' != 'transformer'
    ) AND
    NOT nodes.tags?'transformer' AND -- example: power=pole + transformer=*
    (
        NOT nodes.tags?'line_management' OR (
            nodes.tags->'line_management' != 'cross' AND
            nodes.tags->'line_management' != 'termination'
        )
    )
GROUP BY
    v.nid,
    nodes.geom,
    v.voltage,
    v.origin
HAVING
    (v.origin='numeric' AND sum(v.cv)=2) OR (v.origin='varchar' AND sum(v.cv)=1)
"""

# Non power nodes on power line and minor_line ways
sql40 = """
SELECT DISTINCT ON (nodes.id)
    nodes.id AS nid,
    ways.id AS wid,
    ST_AsText(nodes.geom)
FROM
    ways
    JOIN nodes ON
        nodes.id = ANY (ways.nodes[2:array_length(nodes,1)-1]) AND
        NOT nodes.tags?'power'
    LEFT JOIN power_lines_terminators t ON
        ST_DWithin(nodes.geom, t.geom, 50)
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line') AND
    (NOT ways.tags?'tunnel' OR NOT ways.tags->'tunnel' IN ('yes', 'true')) AND
    (NOT ways.tags?'submarine' OR NOT ways.tags->'submarine' IN ('yes', 'true')) AND
    t.geom IS NULL
ORDER BY
    nodes.id
"""

sql50 = """
CREATE TEMP TABLE power_segement AS
SELECT
    id,
    ST_MakeLine(p1, p2) AS seg,
    ST_Length(ST_MakeLine(p1, p2)::geography) AS l
FROM
    (
    SELECT
        id,
        generate_series(1,ST_NPoints(linestring)-1) AS n,
        ST_PointN(linestring, generate_series(1,ST_NPoints(linestring)-1)) AS p1,
        ST_PointN(linestring, generate_series(2,ST_NPoints(linestring))) AS p2
    FROM
        {0}ways
    WHERE
        tags != ''::hstore AND
        tags?'power' AND
        tags->'power' = 'line' AND
        (NOT tags ? 'tunnel' OR NOT tags->'tunnel' IN ('yes', 'true')) AND
        (NOT tags ? 'submarine' OR NOT tags->'submarine' IN ('yes', 'true')) AND
        (NOT tags ? 'location' OR NOT tags->'location' IN ('underground')) AND
        array_length(nodes, 1) >= 30
    ) AS d
"""

sql51 = """
CREATE TEMP TABLE power_segement_stddev AS
SELECT
    id,
    stddev(l) AS ll,
    avg(l) AS a
FROM
    power_segement
WHERE
    l > 50 AND l < 800
GROUP BY
    id
HAVING
    stddev(l)/avg(l) < 0.25 AND
    COUNT(*) > 20
"""

sql52 = """
SELECT
    power_segement.id,
    ST_AsText(ST_LineInterpolatePoint(
        power_segement.seg,
        generate_series(1, (power_segement.l / power_segement_stddev.a)::int-1)
            /round(power_segement.l / power_segement_stddev.a)
    ))
FROM
    power_segement
    JOIN power_segement_stddev ON
        power_segement.id = power_segement_stddev.id AND
        power_segement.l / power_segement_stddev.a > 1.8
WHERE
    power_segement.l / power_segement_stddev.a < 8
ORDER BY
    power_segement.id,
    power_segement.l / power_segement_stddev.a
"""

sql60 = """
SELECT DISTINCT ON (u.wid)
    u.wid,
    t.type_id,
    ST_AsText(u.geom)
FROM
    power_lines_unfinished u
    JOIN power_lines_terminators t ON
        ST_Intersects(u.geom, t.geom)
WHERE
    t.power = 'substation' AND
    (t.substation IS NULL OR t.substation != 'minor_distribution') AND
    (SELECT max(v) FROM unnest(u.voltage) AS t(v)) > (SELECT max(v) FROM unnest(t.voltage) AS t(v))
ORDER BY
    u.wid
"""

# Find line_management and location:transition values from power lines nodes
# Two circuits in vertices query means 1 in and 1 out of a given node, so straight.
# Please keep case when ordered
sql70 = """
CREATE TEMP TABLE power_lines_mgmt AS

WITH vertices AS (
    SELECT
        e.nid,
        string_agg(CASE e.location WHEN 'overhead' THEN e.circuits::varchar ELSE NULL END, '-' ORDER BY e.circuits desc) AS circuits_overhead,
        string_agg(CASE WHEN e.location!='overhead' THEN e.circuits::varchar ELSE NULL END, '-' ORDER BY e.circuits desc) AS circuits_elsewhere
    FROM
        power_lines_topoedges e
    GROUP BY
        e.nid
    HAVING
        COUNT(*) > 1 AND SUM(e.circuits) > 2
)

SELECT
    j.nid,
    CASE
    WHEN j.circuits_overhead='1' AND j.circuits_elsewhere IS NULL THEN 'termination'
    WHEN j.circuits_overhead='1' AND j.circuits_elsewhere='1' THEN 'transition'
    WHEN j.circuits_overhead='1-1' AND j.circuits_elsewhere='1' THEN 'branch'
    WHEN j.circuits_overhead='1-1' AND j.circuits_elsewhere='1-1' THEN 'split'
    WHEN j.circuits_overhead='1-1-1' AND j.circuits_elsewhere IS NULL THEN 'branch'
    WHEN j.circuits_overhead='2' AND j.circuits_elsewhere='1-1'  THEN 'transition'
    WHEN j.circuits_overhead='2-1' AND j.circuits_elsewhere='1' THEN 'split|transition'
    WHEN j.circuits_overhead='2-1-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='2-1-1-1' AND j.circuits_elsewhere IS NULL THEN 'straight|branch'
    WHEN j.circuits_overhead='2-2' AND j.circuits_elsewhere='1' THEN 'straight|branch'
    WHEN j.circuits_overhead='2-2' AND j.circuits_elsewhere='1-1' THEN 'split'
    WHEN j.circuits_overhead='2-2' AND j.circuits_elsewhere='2' THEN 'split'
    WHEN j.circuits_overhead='2-2-1' THEN 'straight|branch'
    WHEN j.circuits_overhead='2-2-1-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='2-2-2' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='3-1-1-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='3-2-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='4-1-1-1-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='4-2-1-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='4-2-2' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='4-3-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    WHEN j.circuits_overhead='5-2-2-1' AND j.circuits_elsewhere IS NULL THEN 'split'
    ELSE NULL
    END as line_management,
    CASE
    WHEN j.circuits_overhead='1' AND j.circuits_elsewhere='1' THEN 'yes'
    WHEN j.circuits_overhead='1-1' AND j.circuits_elsewhere='1' THEN 'yes'
    WHEN j.circuits_overhead='1-1' AND j.circuits_elsewhere='1-1' THEN 'yes'
    WHEN j.circuits_overhead='2' AND j.circuits_elsewhere='1-1'  THEN 'yes'
    WHEN j.circuits_overhead='2-1' AND j.circuits_elsewhere='1' THEN 'yes'
    WHEN j.circuits_overhead='2-2' AND j.circuits_elsewhere='1' THEN 'yes'
    WHEN j.circuits_overhead='2-2' AND j.circuits_elsewhere='1-1' THEN 'yes'
    WHEN j.circuits_overhead='2-2' AND j.circuits_elsewhere='2' THEN 'yes'
    ELSE NULL
    END as location_transition
FROM
    vertices j
"""

sql71 = """
SELECT m.nid,
    ST_AsText(nodes.geom),
    m.line_management,
    m.location_transition,
    nodes.tags->'line_management' as current_line_management,
    nodes.tags->'location:transition' as current_location_transition
FROM
    power_lines_mgmt m
    JOIN nodes ON nodes.id=m.nid
WHERE
    (line_management IS NOT NULL AND (NOT nodes.tags ? 'line_management' OR nodes.tags->'line_management' != m.line_management)) OR
    (location_transition IS NOT NULL AND (NOT nodes.tags ? 'location:transition' OR nodes.tags->'location:transition' != m.location_transition))
ORDER BY
    m.nid
"""

class Analyser_Osmosis_Powerline(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:imagery'],
            title = T_('Lone power tower or pole'),
            fix = T_(
'''This tower should probably be connected to a power line.'''),
            trap = T_(
'''It's possible that disused power features could be disconnected from the network.
In which case make use of the `disused:` [lifecycle prefix](https://wiki.openstreetmap.org/wiki/Lifecycle_prefix).'''))
        self.classs[2] = self.def_class(item = 7040, level = 2, tags = ['power', 'fix:imagery'],
            title = T_('Unfinished power transmission line'),
            detail = T_(
'''The line ends in a vacuum, and should be connected to another line or
a transformer (`power=transformer`), a generator (`power=generator`)
or marked as transitioning into ground (`location:transition=yes`).'''),
            trap = T_(
'''It's possible that disused power features could be disconnected from the network.
In which case make use of the `disused:` [lifecycle prefix](https://wiki.openstreetmap.org/wiki/Lifecycle_prefix).'''))
        self.classs[6] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:imagery'],
            title = T_('Unfinished power distribution line'),
            detail = T_(
'''The line ends in a vacuum, and should be connected to another line or
a transformer (`power=transformer`), a generator (`power=generator`)
or marked as transitioning into ground (`location:transition=yes`).'''),
            trap = T_(
'''It's possible that disused power features could be disconnected from the network.
In which case make use of the `disused:` [lifecycle prefix](https://wiki.openstreetmap.org/wiki/Lifecycle_prefix).'''))
        self.classs[3] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:chair'],
            title = T_('Connection between different voltages'),
            detail = T_('Two power lines meet at this point, but have inconsistent voltages (`voltage=*`).'),
            fix = T_(
'''Check if the voltages are really different.
Add a transformer using `power=transformer` (standalone transformers) or `power=pole + transformer=*` (pole mounted transformers).'''))
        self.classs[4] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:imagery'],
            title = T_('Non power node on power way'),
            detail = T_(
'''Power lines can only form a straight line between supports and therefore shouldn't
have additional nodes that aren't tagged as a `power` feature.'''),
            fix = T_(
'''If this node is a tower or pole, use the tag `power=tower` or
`power=pole`. Otherwise remove it.'''))
        self.classs_change[5] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:imagery'],
            title = T_('Missing power tower or pole'),
            detail = T_(
'''Based on the statistical frequency of the poles on this power line,
there's likely an unmapped pole nearby.'''))
        self.classs[7] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:chair'],
            title = T_('Unmatched voltage of line on substation'))
        self.classs[8] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:chair'],
            title = T_('Power support line management suggestion'))

        self.callback50 = lambda res: {"class":5, "subclass": stablehash64(res[1]), "data":[self.way_full, self.positionAsText]}

    def way_power(self, res):
        way_data = self.apiconn.WayGet(res)
        way_tags = {key: way_data["tag"][key] for key in way_data["tag"].keys() & {'power', 'voltage'}}
        self.geom["way"].append({"id":res, "nd":[], "tag":way_tags})

    def analyser_osmosis_common(self):
        self.run(sql01)
        self.run(sql02)
        self.run(sql10, lambda res: {"class":1, "data":[self.node_full, self.positionAsText]} )
        self.run(sql20)
        self.run(sql21)
        self.run(sql22)
        self.run(sql23)
        self.run(sql24)
        self.run(sql25)
        self.run(sql26, lambda res: {"class":6 if res[3] == 'minor_line' else 2, "data":[self.node_full, self.way_power, self.positionAsText]} )
        self.run(sql30, lambda res: {"class":3, "data":[self.node, self.positionAsText]} )
        self.run(sql40, lambda res: {"class":4, "data":[self.node_full, self.way_power, self.positionAsText], "fix":[{"+": {"power": "tower"}}, {"+": {"power": "pole"}}]})
        self.run(sql60, lambda res: {"class":7, "data":[self.way_full, self.any_full, self.positionAsText]} )
        self.run(sql70)
        self.run(sql71, lambda res: {"class":8, "data":[self.node_full, self.positionAsText], "fix":self.__callback80_fix(res)} )

    def analyser_osmosis_full(self):
        self.run(sql50.format(""))
        self.run(sql51)
        self.run(sql52, self.callback50)

    def analyser_osmosis_diff(self):
        self.run(sql50.format("touched_"))
        self.run(sql51)
        self.run(sql52, self.callback50)

    def __callback80_fix(self, res):
        result = []
        if res[2]:
            if res[4] is None:
                result.append({"+": {"line_management": res[2]}})
            elif res[4] != res[2]:
                result.append({"~": {"line_management": res[2]}})
        if res[3]:
            if res[5] is None:
                result.append({"+": {"line_management": res[3]}})
            elif res[5] != res[3]:
                result.append({"~": {"line_management": res[3]}})

        return result


###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_powerline.test.osm",
                                         config.dir_tmp + "/tests/osmosis_powerline.test.xml")

    def test_powergrid(self):
        with Analyser_Osmosis_Powerline(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("node", "26971")])
        self.check_err(cl="2", elems=[("node", "25874"), ("way", "1909")])
        self.check_err(cl="2", elems=[("node", "25883"), ("way", "1918")])
        self.check_err(cl="3", elems=[("node", "25950")])
        self.check_err(cl="4", elems=[("node", "26082"), ("way", "1910")])
        self.check_err(cl="6", elems=[("node", "26191"), ("way", "2088")])
        self.check_err(cl="8", elems=[("node", "25956")])
        self.check_err(cl="8", elems=[("node", "26383")])
        self.check_num_err(11)
