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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE {0}traffic_signals AS
SELECT
    id,
    geom,
    tags,
    tags?'crossing' AND tags->'crossing' != 'no' AS crossing,
    ST_Buffer(geom::geography, 40) AS buffer
FROM
    {0}nodes
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' = 'traffic_signals'
"""

sql11 = """
CREATE INDEX {0}traffic_signals_buffer ON {0}traffic_signals USING GIST(buffer)
"""

sql12 = """
CREATE TEMP TABLE {0}crossing AS
SELECT
    id,
    geom::geography,
    tags->'crossing' AS crossing
FROM
    {0}nodes
WHERE
    tags != ''::hstore AND
    tags?'highway' AND
    tags->'highway' = 'crossing'
"""

sql13 = """
CREATE INDEX {0}crossing_geom ON {0}crossing USING GIST(geom)
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
  ST_AsText(nodes.geom)
FROM
  {0}traffic_signals AS nodes
  JOIN {1}ways AS ways ON
    ways.linestring && nodes.geom AND
    nodes.id = ANY (ways.nodes) AND
    ways.tags != ''::hstore AND
    ways.tags?'highway'
WHERE
  (NOT nodes.tags?'traffic_signals:direction' OR nodes.tags->'traffic_signals:direction' NOT IN('backward', 'forward')) AND
  (NOT nodes.tags?'crossing' OR nodes.tags->'crossing' = 'no')
GROUP BY
  nodes.id,
  nodes.geom
HAVING
  COUNT(*) = 1 AND
  BOOL_AND(NOT ways.tags?'oneway' OR ways.tags->'oneway' IN ('no', 'false')) AND
  BOOL_AND(NOT ways.tags?'junction' OR ways.tags->'junction' != 'roundabout')
"""

class Analyser_Osmosis_Highway_Traffic_Signals(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item": 2090, "level": 3, "tag": ["tag", "highway", "fix:imagery"], "desc": T_(u"Possible crossing=traffic_signals") }
        self.classs[2] = {"item": 2090, "level": 2, "tag": ["tag", "highway", "fix:imagery"], "desc": T_(u"Possible missing highway=traffic_signals nearby") }
        self.classs_change[3] = {"item": 2090, "level": 2, "tag": ["tag", "highway", "fix:chair"], "desc": T_(u"Possible missing traffic_signals:direction or crossing") }
        self.callback10 = lambda res: {"class":1, "data":[self.node_full, self.node_full, self.positionAsText], "fix":[
            [{"+":{"crossing":"traffic_signals"}}],
            [{"+":{"crossing":"traffic_signals"}}, {"-":["crossing"]}]
        ] }
        self.callback20 = lambda res: {"class":2, "data":[self.node_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.node_full, self.positionAsText], "fix":[
            [{"+":{"traffic_signals:direction":"forward"}}],
            [{"+":{"traffic_signals:direction":"backward"}}],
        ] }

    def analyser_osmosis(self):
        self.run(sql10.format(""))
        self.run(sql11.format(""))
        self.run(sql12.format(""))
        self.run(sql13.format(""))
        self.run(sql14.format("", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_"))
        self.run(sql11.format("touched_"))
#        self.run(sql12.format(""))  # already created by analyser_osmosis()
#        self.run(sql13.format(""))  # already created by analyser_osmosis()
        self.run(sql14.format("touched_", ""), self.callback10)

#        self.run(sql10.format(""))  # already created by analyser_osmosis()
#        self.run(sql11.format(""))  # already created by analyser_osmosis()
        self.run(sql12.format("touched_"))
        self.run(sql13.format("touched_"))
        self.run(sql14.format("", "touched_"), self.callback10)

        self.run(sql20.format("touched_", ""), self.callback20)

        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("", "touched_"), self.callback30)
        self.run(sql30.format("touched_", "touched_"), self.callback30)
