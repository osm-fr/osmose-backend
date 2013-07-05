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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
DROP TABLE IF EXISTS traffic_signals;
CREATE TABLE traffic_signals AS
SELECT
    id,
    ST_Buffer(traffic_signals.geom::geography, 30)::geometry AS geom
FROM
    {0}nodes AS traffic_signals
WHERE
    traffic_signals.tags?'highway' AND
    traffic_signals.tags->'highway' = 'traffic_signals' AND
    traffic_signals.tags?'crossing' AND
    traffic_signals.tags?'crossing' != 'no'
"""

sql11 = """
CREATE INDEX traffic_signals_geom ON traffic_signals USING GIST(geom)
"""

sql12 = """
DROP TABLE IF EXISTS crossing;
CREATE TABLE crossing AS
SELECT
    id,
    geom
FROM
    {0}nodes AS crossing
WHERE
    crossing.tags?'highway' AND
    crossing.tags->'highway' = 'crossing' AND
    NOT crossing.tags?'crossing'
"""

sql13 = """
CREATE INDEX crossing_geom ON crossing USING GIST(geom)
"""

sql14 = """
SELECT
    DISTINCT ON(crossing.id)
    crossing.id AS crossing_id,
    traffic_signals.id AS traffic_signals_id,
    ST_AsText(crossing.geom)
FROM
    traffic_signals
    JOIN crossing ON
        crossing.geom && traffic_signals.geom AND
        ST_DWithin(crossing.geom::geography, traffic_signals.geom::geography, 30)
ORDER BY
    crossing.id
"""

class Analyser_Osmosis_Highway_Crossing(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item": 2090, "level": 3, "tag": ["tag", "highway", "fix:imagery"], "desc": T_(u"Possible crossing=traffic_signals") }
        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.node_full, self.positionAsText], "fix":[
            [{"+":{"crossing":"traffic_signals"}}],
            [{"+":{"crossing":"traffic_signals"}}, {"-":["crossing"]}]
        ] }

    def analyser_osmosis_all(self):
        self.run(sql10.format(""))
        self.run(sql11)
        self.run(sql12.format(""))
        self.run(sql13)
        self.run(sql14, self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_"))
        self.run(sql11)
        self.run(sql12.format(""))
        self.run(sql13)
        self.run(sql14, self.callback10)

        self.run(sql10.format(""))
        self.run(sql11)
        self.run(sql12.format("touched_"))
        self.run(sql13)
        self.run(sql14, self.callback10)
