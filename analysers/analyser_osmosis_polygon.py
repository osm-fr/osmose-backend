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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    id,
    regexp_replace(ST_IsValidReason(ST_MakePolygon(linestring)), '[^[]+\\[([^]]+).*', 'POINT(\\1)'),
    ST_IsValidReason(ST_MakePolygon(linestring)) AS detail
FROM
    {0}ways
WHERE
    NOT is_polygon AND
    NOT (tags?'attraction' AND tags->'attraction' = 'roller_coaster') AND
    nodes[1] = nodes[array_length(nodes,1)] AND
    ST_NumPoints(linestring) > 3 AND
    ST_IsClosed(linestring) AND
    NOT ST_IsValid(ST_MakePolygon(linestring))
"""

sql20 = """
DROP TABLE IF EXISTS relation_linestrings;
CREATE TEMP TABLE relation_linestrings AS
SELECT
  relations.id,
  ST_LineMerge(ST_Collect(linestring)) AS linestring
FROM
  {0}relations AS relations
  JOIN relation_members ON
    relation_members.relation_id = relations.id AND
    relation_members.member_type = 'W' AND
    relation_members.member_role = 'outer'
  JOIN {1}ways AS ways ON
    ways.id = relation_members.member_id AND
    ST_NumPoints(ways.linestring) >= 2
WHERE
  relations.tags?'type' AND
  relations.tags->'type' IN ('multipolygon', 'boundary')
GROUP BY
  relations.id
"""

sql21 = """
SELECT
    id,
    regexp_replace(ST_IsValidReason(ST_MakePolygon(linestring)), '[^[]+\\[([^]]+).*', 'POINT(\\1)') AS detail,
    ST_IsValidReason(ST_MakePolygon(linestring)) AS detail
FROM
    relation_linestrings
WHERE
    (ST_NumGeometries(linestring) IS NULL OR ST_NumGeometries(linestring) = 1) AND
    ST_NumPoints(linestring) > 3 AND
    ST_IsClosed(linestring) AND
   NOT ST_IsValid(ST_MakePolygon(linestring))
"""

class Analyser_Osmosis_Polygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1040", "level": 1, "tag": ["geom", "fix:chair"], "desc": T_(u"Invalid polygon") }
        self.classs_change[2] = {"item":"1040", "level": 1, "tag": ["geom", "fix:chair"], "desc": T_(u"Invalid multipolygon") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText], "text": {"en": res[2]}}
        self.callback20 = lambda res: {"class":2, "data":[self.relation, self.positionAsText], "text": {"en": res[2]}}

    def analyser_osmosis_full(self):
        self.run(sql10.format(""), self.callback10)
        self.run(sql20.format("", ""))
        self.run(sql21, self.callback20)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_"), self.callback10)
        self.run(sql20.format("touched_", ""))
        self.run(sql21, self.callback20)
        self.run(sql20.format("not_touched_", "touched_"))
        self.run(sql21, self.callback20)
