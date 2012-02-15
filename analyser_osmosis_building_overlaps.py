#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

sql1 = """
CREATE TEMP TABLE buildings AS
SELECT
    ways.id,
    ST_MakePolygon(ways.linestring) AS linestring
FROM
    ways
    LEFT JOIN relation_members ON
        relation_members.member_id = ways.id AND
        relation_members.member_type = 'W'
WHERE
    relation_members.member_id IS NULL AND
    ways.tags ? 'building' AND ways.tags->'building' != 'no' AND
    is_polygon AND
    ST_IsValid(ways.linestring) = 't' AND
    ST_IsSimple(ways.linestring) = 't'
;
"""

sql2 = """
CREATE INDEX buildings_linestring_idx ON buildings USING gist(linestring);
"""

sql3 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(ST_Intersection(b1.linestring, b2.linestring)))
FROM
    buildings AS b1,
    buildings AS b2
WHERE
    b1.id > b2.id AND
    b1.linestring && b2.linestring AND
    ST_Area(ST_Intersection(b1.linestring, b2.linestring)) <> 0
;
"""

class Analyser_Osmosis_Building_Overlaps(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"0", "desc":{"fr":"Intersections de bâtiments", "en":"Building intersection"} }

    def analyser_osmosis(self):
        self.run(sql1)
        self.run(sql2)
        self.run(sql3, lambda res: {"class":1, "data":[self.way, self.way, self.positionAsText]} )
