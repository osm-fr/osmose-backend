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

from .Analyser_Osmosis import Analyser_Osmosis
from modules.Stablehash import stablehash64

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
    nodes.tags->'power' IN ('pole', 'tower')
GROUP BY
    nodes.id,
    nodes.geom
HAVING
    bool_and(ways.id IS NULL)
"""

sql20 = """
CREATE TEMP TABLE line_ends AS
SELECT DISTINCT ON (ends(ways.nodes))
    ways.id AS wid,
    ends(ways.nodes) AS id,
    ways.tags->'power' AS power,
    regexp_split_to_array(ways.tags->'voltage','; *') AS voltage
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
CREATE INDEX idx_line_ends_id ON line_ends(id)
"""

sql22 = """
CREATE TEMP TABLE line_ends1 AS
SELECT
    line_ends.wid,
    line_ends.id,
    line_ends.power,
    line_ends.voltage,
    nodes.geom::geography
FROM
    (
    SELECT
        line_ends.wid,
        line_ends.id,
        line_ends.power,
        line_ends.voltage
    FROM
        line_ends
        LEFT JOIN line_ends AS other ON
        line_ends.wid != other.wid AND
            line_ends.id = other.id
    WHERE
        other.id IS NULL
    ) AS line_ends
    JOIN nodes ON
        line_ends.id = nodes.id AND
        NOT (tags?'pole' AND tags->'pole' = 'transition') AND -- deprecated
        NOT (tags?'location:transition' AND tags->'location:transition' = 'yes') AND
        NOT (tags?'transformer' AND tags->'transformer' in ('distribution', 'minor_distribution')) AND
        NOT (tags?'power' AND tags->'power' = 'terminal')
"""

sql23 = """
CREATE INDEX idx_line_ends1_geom ON line_ends1 USING GIST(geom)
"""

sql24 = """
CREATE TEMP TABLE line_terminators AS
(
SELECT
    'N' || id AS type_id,
    geom::geography,
    tags->'power' AS power,
    tags->'substation' AS substation,
    regexp_split_to_array(tags->'voltage','; *') AS voltage
FROM
    nodes
WHERE
    tags != ''::hstore AND
    tags?'power' AND
    tags->'power' NOT IN ('pole', 'tower')
)
UNION ALL
(
SELECT
    'W' || id AS type_id,
    linestring::geography AS geom,
    tags->'power' AS power,
    tags->'substation' AS substation,
    regexp_split_to_array(tags->'voltage','; *') AS voltage
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'power' AND
    tags->'power' NOT IN ('line', 'minor_line', 'cable')
)
"""

sql25 = """
CREATE INDEX idx_line_terminators_geom ON line_terminators USING GIST(geom)
"""

sql26 = """
SELECT
    line_ends1.id,
    ST_AsText(line_ends1.geom),
    line_ends1.power
FROM
    line_ends1
    LEFT JOIN line_terminators ON
        ST_DWithin(line_ends1.geom, line_terminators.geom, 150)
    LEFT JOIN ways ON
        ways.id != line_ends1.wid AND
        tags != ''::hstore AND
        tags?'power' AND
        tags->'power' IN ('line', 'minor_line', 'cable') AND
        ways.linestring && line_ends1.geom AND
        line_ends1.id = ANY(ways.nodes)
WHERE
    line_terminators.geom IS NULL AND
    ways.id IS NULL
"""

sql30 = """
CREATE TEMP TABLE power_line AS
SELECT
    id,
    ends(nodes) AS nid,
    regexp_split_to_table(tags->'voltage','; *') AS voltage
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'power' AND
    tags->'power' IN ('line', 'minor_line') AND
    tags?'voltage'
"""

sql31 = """
CREATE VIEW power_line_junction AS
SELECT
    nid
FROM
    (SELECT nid FROM power_line GROUP BY id, nid) AS p
GROUP BY
    nid
HAVING
    COUNT(*) > 1
"""

sql32 = """
SELECT
    DISTINCT(nid),
    ST_AsText(geom)
FROM
    power_line_junction
    NATURAL JOIN power_line
    JOIN nodes ON
        power_line.nid = nodes.id AND
        (
            NOT nodes.tags?'power' OR
            nodes.tags->'power' != 'transformer'
        )
GROUP BY
    nid,
    voltage,
    geom
HAVING
    COUNT(*) = 1
"""

sql40 = """
SELECT DISTINCT ON (nodes.id)
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    {0}ways AS ways
    JOIN nodes ON
        nodes.id = ANY (ways.nodes[2:array_length(nodes,1)-1]) AND
        NOT nodes.tags?'power'
    LEFT JOIN line_terminators ON
        ST_DWithin(nodes.geom, line_terminators.geom, 150)
WHERE
    ways.tags != ''::hstore AND
    ways.tags?'power' AND
    ways.tags->'power' IN ('line', 'minor_line') AND
    (NOT ways.tags?'tunnel' OR NOT ways.tags->'tunnel' IN ('yes', 'true')) AND
    (NOT ways.tags?'submarine' OR NOT ways.tags->'submarine' IN ('yes', 'true')) AND
    line_terminators.geom IS NULL
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
        (NOT tags?'tunnel' OR NOT tags->'tunnel' IN ('yes', 'true')) AND
        (NOT tags?'submarine' OR NOT tags->'submarine' IN ('yes', 'true')) AND
        (NOT tags?'location' OR NOT tags->'location' IN ('underground')) AND
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
SELECT DISTINCT ON (line_ends1.wid)
    line_ends1.wid,
    line_terminators.type_id,
    ST_AsText(line_ends1.geom)
FROM
    line_ends1
    JOIN line_terminators ON
        ST_DWithin(line_ends1.geom, line_terminators.geom, 30)
WHERE
    line_terminators.power = 'substation' AND
    (line_terminators.substation IS NULL OR line_terminators.substation != 'minor_distribution') AND
    NOT line_ends1.voltage <@ line_terminators.voltage
ORDER BY
    line_ends1.wid
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
            title = T_('Unfinished power major line'),
            detail = T_(
'''The line ends in a vacuum, and should be connected to another line or
a transformer (`power=transformer`) or a generator (`power=generator`).'''),
            trap = T_(
'''It's possible that disused power features could be disconnected from the network.
In which case make use of the `disused:` [lifecycle prefix](https://wiki.openstreetmap.org/wiki/Lifecycle_prefix).'''))
        self.classs[6] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:imagery'],
            title = T_('Unfinished power minor line'),
            detail = T_(
'''The line ends in a vacuum, and should be connected to another line or
a transformer (`power=transformer`) or a generator (`power=generator`).'''),
            trap = T_(
'''It's possible that disused power features could be disconnected from the network.
In which case make use of the `disused:` [lifecycle prefix](https://wiki.openstreetmap.org/wiki/Lifecycle_prefix).'''))
        self.classs[3] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:chair'],
            title = T_('Connection between different voltages'),
            detail = T_('Two power lines meet at this point, but have inconsistent voltages (`voltage=*`).'))
        self.classs_change[4] = self.def_class(item = 7040, level = 3, tags = ['power', 'fix:imagery'],
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

        self.callback40 = lambda res: {"class":4, "data":[self.node_full, self.positionAsText], "fix":[{"+": {"power": "tower"}}, {"+": {"power": "pole"}}]}
        self.callback50 = lambda res: {"class":5, "subclass": stablehash64(res[1]), "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.node_full, self.positionAsText]} )
        self.run(sql20)
        self.run(sql21)
        self.run(sql22)
        self.run(sql23)
        self.run(sql24)
        self.run(sql25)
        self.run(sql26, lambda res: {"class":6 if res[2] == 'minor_line' else 2, "data":[self.node_full, self.positionAsText]} )
        self.run(sql30)
        self.run(sql31)
        self.run(sql32, lambda res: {"class":3, "data":[self.node_full, self.positionAsText]} )
        self.run(sql60, lambda res: {"class":7, "data":[self.way_full, self.any_full, self.positionAsText]} )

    def analyser_osmosis_full(self):
        self.run(sql40.format(""), self.callback40)
        self.run(sql50.format(""))
        self.run(sql51)
        self.run(sql52, self.callback50)

    def analyser_osmosis_diff(self):
        self.run(sql40.format("touched_"), self.callback40)
        self.run(sql50.format("touched_"))
        self.run(sql51)
        self.run(sql52, self.callback50)
