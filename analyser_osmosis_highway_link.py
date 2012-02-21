#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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
DROP VIEW IF EXISTS links_ends CASCADE;
CREATE VIEW links_ends AS
SELECT
    id,
    ends(nodes) AS nid,
    tags->'highway' AS highway_link,
    linestring
FROM
    ways
WHERE
    tags?'highway' AND
    tags->'highway' LIKE '%_link'
;
"""

sql20 = """
DROP TABLE IF EXISTS links_conn CASCADE;
CREATE TEMP TABLE links_conn AS
SELECT
    links_ends.id,
    links_ends.nid,
    links_ends.linestring,
    BOOL_OR(
        w1.tags->'highway' = links_ends.highway_link OR
        w1.tags->'highway' || '_link' = links_ends.highway_link
    ) AS has_good,
    BOOL_OR(NOT(
        w1.tags->'highway' = links_ends.highway_link OR
        w1.tags->'highway' || '_link' = links_ends.highway_link
    )) AS has_bad
FROM
    links_ends
    JOIN way_nodes ON
        way_nodes.node_id = links_ends.nid
    JOIN ways AS w1 ON
        links_ends.id != w1.id AND
        way_nodes.way_id = w1.id AND
        w1.tags?'highway'
GROUP BY
    links_ends.id,
    links_ends.nid,
    links_ends.linestring
;
"""

sql21 = """
CREATE INDEX links_conn_idx ON links_conn(id, nid);
CREATE INDEX links_conn_good ON links_conn(has_good);
CREATE INDEX links_conn_bad ON links_conn(has_bad);
"""

sql30 = """
SELECT
    bad.id,
    ST_AsText(ST_Centroid(bad.linestring))
FROM
    (SELECT * FROM links_conn WHERE has_bad) AS bad
    LEFT JOIN (SELECT * FROM links_conn WHERE has_good) AS good
    ON
        bad.id = good.id AND
        bad.nid = good.nid
WHERE
    good.id IS NULL
GROUP BY
    bad.id,
    bad.linestring
HAVING
    COUNT(*) > 1
;
"""

class Analyser_Osmosis_Highway_Link(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1110", "desc":{"fr":"Highway *_link non corespondant", "en":"Bad *_link highway"} }

    def analyser_osmosis(self):
        self.run(sql10)
        self.run(sql20)
        self.run(sql21)
        self.run(sql30, lambda res: {"class":1, "data":[self.way_full, self.positionAsText]} )
