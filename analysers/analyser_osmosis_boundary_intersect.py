#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
CREATE TEMP TABLE boundary AS
(
SELECT
    ways.id,
    ways.linestring,
    relations.tags->'boundary' AS boundary
FROM
    relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W'
    JOIN ways ON
        ways.id = relation_members.member_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'boundary' AND
    relations.tags?'boundary'
)
UNION ALL
(
SELECT
    ways.id,
    ways.linestring,
    tags->'boundary' AS boundary
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags?'type' AND
    tags->'type' = 'boundary' AND
    tags?'boundary'
)
"""

sql11 = """
CREATE INDEX boundary_boundary ON boundary(boundary)
"""

sql12 = """
CREATE INDEX boundary_linestring ON boundary USING GIST(linestring)
"""

sql20 = """
SELECT
    b1.id,
    b2.id,
    ST_ASText(ST_GeometryN(ST_Multi(ST_Intersection(b1.linestring, b2.linestring)), 1))
FROM
    boundary AS b1
    JOIN boundary AS b2 ON
        b1.boundary = b2.boundary AND
        b1.linestring && b2.linestring AND
        b1.id < b2.id AND
        -- Ways not linked
        NOT ST_Touches(b1.linestring, b2.linestring) AND
        -- Ways share inner space
        ST_Crosses(b1.linestring, b2.linestring)
"""

class Analyser_Osmosis_Boundary_Intersect(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1060", "level": 2, "tag": ["boundary", "geom", "fix:chair"], "desc": T_(u"Boundary intersection") }
        self.callback20 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql20, self.callback20)
