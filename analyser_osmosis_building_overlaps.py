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

sql10 = """
CREATE TEMP TABLE {0}buildings AS
SELECT
    ways.id,
    ST_MakePolygon(ways.linestring) AS polygon
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

sql11 = """
CREATE INDEX {0}buildings_polygon_idx ON {0}buildings USING gist(polygon);
"""

sql30 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(ST_Intersection(b1.polygon, b2.polygon))),
    ST_Area(ST_Intersection(b1.polygon, b2.polygon)) AS intersectionArea,
    least(ST_Area(b1.polygon), ST_Area(b2.polygon))*0.10 AS threshold
FROM
    {0}buildings AS b1,
    {1}buildings AS b2
WHERE
    b1.id > b2.id AND
    b1.polygon && b2.polygon AND
    ST_Area(ST_Intersection(b1.polygon, b2.polygon)) <> 0
;
"""

sql40 = """
SELECT
    id,
    ST_AsText(ST_Centroid(polygon))
FROM
    {0}buildings
WHERE
    ST_Area(polygon) < 0.05e-10
;
"""

class Analyser_Osmosis_Building_Overlaps(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"0", "level": 3, "tag": ["building", "geom"], "desc":{"fr":"Intersections de bâtiments", "en":"Building intersection"} }
        self.classs[2] = {"item":"0", "level": 2, "tag": ["building", "geom"], "desc":{"fr":"Grosses intersections de bâtiments", "en":"Large building intersection"} }
        self.classs[3] = {"item":"0", "level": 3, "tag": ["building", "geom"], "desc":{"fr":"Bâtiments trop petit", "en":"Too small building"} }
        self.callback30 = lambda res: {"class":2 if res[3]>res[4] else 1, "data":[self.way, self.way, self.positionAsText]}
        self.callback40 = lambda res: {"class":3, "data":[self.way, self.positionAsText]}

    def analyser_osmosis(self):
        self.run(sql10.format(""))
        self.run(sql11.format(""))
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)
        self.run(sql50.format("", ""), self.callback50)

    def analyser_osmosis_touched(self):
        self.run(sql10.format(""))
        self.run(sql11.format(""))
        self.run(sql10.format("touched_"))
        self.run(sql11.format("touched_"))
        dup = set()
        self.run(sql30.format("touched_", ""), lambda res: dup.add(res[0]) or self.callback30(res))
        self.run(sql30.format("", "touched_"), lambda res: res[0] in dup or dup.add(res[0]) or self.callback30(res))
        self.run(sql30.format("touched_", "touched_"), lambda res: res[0] in dup or dup.add(res[0]) or self.callback30(res))
        self.run(sql40.format("touched_"), self.callback40)
