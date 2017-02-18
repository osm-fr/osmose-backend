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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE VIEW links_ends AS
SELECT
    id,
    ends(nodes) AS nid,
    tags->'highway' AS highway_link,
    linestring
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' LIKE '%_link'
"""

sql20 = """
CREATE TEMP TABLE links_conn AS
SELECT
    links_ends.id,
    links_ends.nid,
    links_ends.linestring,
    BOOL_OR(
        ways.tags->'highway' = links_ends.highway_link OR
        ways.tags->'highway' || '_link' = links_ends.highway_link
    ) AS has_good,
    BOOL_OR(NOT(
        ways.tags->'highway' = links_ends.highway_link OR
        ways.tags->'highway' || '_link' = links_ends.highway_link
    )) AS has_bad,
    links_ends.highway_link,
    COUNT(*) AS nways,
    max(ways.tags->'highway') AS highway_conn
FROM
    links_ends
    JOIN way_nodes ON
        way_nodes.node_id = links_ends.nid AND
        way_nodes.way_id != links_ends.id
    JOIN ways ON
        ways.id = way_nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags?'highway'
GROUP BY
    links_ends.id,
    links_ends.nid,
    links_ends.highway_link,
    links_ends.linestring
"""

sql21 = """
CREATE INDEX links_conn_idx ON links_conn(id)
"""

sql30 = """
SELECT
    bad.id,
    ST_AsText(way_locate(bad.linestring))
FROM
    links_conn AS bad
    LEFT JOIN links_conn AS good ON
        good.has_good AND
        bad.id = good.id AND
        bad.nid = good.nid
WHERE
    bad.has_bad AND
    good.id IS NULL
GROUP BY
    bad.id,
    bad.linestring
HAVING
    COUNT(*) > 1
"""

sql40 = """
SELECT
    id,
    ST_AsText(way_locate(linestring))
FROM
    {0}ways AS ways
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' LIKE '%_link' AND
    tags->'highway' NOT IN ('motorway_link', 'trunk_link') AND
    --array_length(nodes) > 4 AND
    ST_Length(linestring::geography) > 1000
"""

sql50 = """
SELECT
    lc1.id,
    ST_AsText(way_locate(lc1.linestring)),
    CASE lc1.highway_conn LIKE '%_link'
        WHEN TRUE THEN lc1.highway_conn
        ELSE lc1.highway_conn || '_link'
    END
FROM
    links_conn AS lc1
    JOIN links_conn AS lc2 ON
        lc1.id = lc2.id AND
        lc1.nid < lc2.nid AND
        ( -- Sides have the same highway type
            lc1.highway_conn = lc2.highway_conn OR
            lc1.highway_conn = (lc2.highway_conn || '_link') OR
            (lc1.highway_conn || '_link') = lc2.highway_conn
        )
WHERE
    lc1.nways = 1 AND
    lc2.nways = 1 AND
    -- link and first side have not the same highway type
    lc1.highway_link != lc1.highway_conn AND
    lc1.highway_link != (lc1.highway_conn || '_link') AND
    (lc1.highway_link || '_link') != lc1.highway_conn
"""

class Analyser_Osmosis_Highway_Link(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1110", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad *_link highway") }
        self.classs_change[2] = {"item":"1110", "level": 1, "tag": ["highway", "fix:imagery"], "desc": T_(u"Highway too long for a *_link") }
        self.classs[3] = {"item":"1110", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad *_link highway") }
        self.callback40 = lambda res: {"class":2, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql20)
        self.run(sql21)
        self.run(sql30, lambda res: {"class":1, "data":[self.way_full, self.positionAsText]} )
        self.run(sql50, lambda res: {"class":3, "data":[self.way_full, self.positionAsText], "fix": {"~": {"highway": res[2]}} })

    def analyser_osmosis_full(self):
        self.run(sql40.format(""), self.callback40)

    def analyser_osmosis_diff(self):
        self.run(sql40.format("touched_"), self.callback40)
