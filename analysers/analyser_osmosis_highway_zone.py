#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2018                                      ##
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

# Cluster Zone with buffer
sql10 = """
CREATE TEMP TABLE a0_{0} AS
SELECT
  (ST_Dump(
    ST_Union(ST_Buffer(linestring_proj, 60))
  )).path[1] AS cid,
  (ST_Dump(
    ST_Union(ST_Buffer(linestring_proj, 60))
  )).geom AS geom
FROM
  highways
WHERE
  NOT is_construction AND
  tags?'zone:maxspeed' AND
  highways.tags->'zone:maxspeed' LIKE '%:{0}'
"""

sql11 = """
CREATE TEMP TABLE a1_{0} AS
SELECT
  cid,
  (ST_DumpRings(geom)).path[1] AS path,
  (ST_DumpRings(geom)).geom
FROM
  a0_{0}
"""

# Remove small inner hole
sql12 = """
CREATE TEMP TABLE a2_{0} AS
SELECT
  cid,
  path,
  ST_ExteriorRing(geom) AS geom
FROM
  a1_{0}
WHERE
  path = 0 OR
  ST_Area(geom) > 100 * 100
"""

# Rebuild cluster and shrink the buffer back
sql13 = """
CREATE TEMP TABLE a3_{0} AS
SELECT
  ST_Buffer(CASE
    WHEN t.inners IS NULL THEN ST_MakePolygon(a.geom)
    ELSE ST_MakePolygon(a.geom, t.inners)
  END, -61) AS geom
FROM
  (SELECT cid, geom FROM a2_{0} WHERE path = 0) AS a
  LEFT JOIN
    (SELECT cid, ST_Accum(geom) AS inners FROM a2_{0} WHERE path > 0 GROUP BY cid) AS t ON
    a.cid = t.cid
"""

# Get candidates ways in the resulting envelope
sql14 = """
SELECT DISTINCT ON (highways.id)
  highways.id,
  ST_AsText(way_locate(linestring))
FROM
  a3_{0} AS a3
  JOIN highways ON
    highways.tags != ''::hstore AND
    highways.tags?'highway' AND
    highways.tags->'highway' IN ('residential', 'unclassified') AND
    NOT highways.is_construction AND
    (NOT highways.tags?'zone:maxspeed' OR NOT highways.tags->'zone:maxspeed' LIKE '%:{0}') AND
    (NOT highways.tags?'maxspeed' OR highways.tags->'maxspeed' = '{0}') AND
    highways.linestring_proj && a3.geom AND
    ST_Length(ST_Intersection(highways.linestring_proj, a3.geom)) / ST_Length(highways.linestring) > 0.8
WHERE
  NOT ST_IsEmpty(a3.geom)
ORDER BY
  highways.id
"""

class Analyser_Osmosis_Highway_Zone(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[20] = self.def_class(item = 2150, level = 1, tags = ['highway', 'fix:survey'],
            title = T_('Probably missing tag zone:maxspeed=XX:%s, according to the neighborhood', 20))
        self.classs[30] = self.def_class(item = 2150, level = 1, tags = ['highway', 'fix:survey'],
            title = T_('Probably missing tag zone:maxspeed=XX:%s, according to the neighborhood', 30))
        self.callback20 = lambda res: {"class":20, "data":[self.way_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":30, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10.format('20'))
        self.run(sql11.format('20'))
        self.run(sql12.format('20'))
        self.run(sql13.format('20'))
        self.run(sql14.format('20'), self.callback20)

        self.run(sql10.format('30'))
        self.run(sql11.format('30'))
        self.run(sql12.format('30'))
        self.run(sql13.format('30'))
        self.run(sql14.format('30'), self.callback30)
