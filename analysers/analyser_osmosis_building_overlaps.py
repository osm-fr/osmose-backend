#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011-2015                                 ##
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

sql20 = """
CREATE TEMP TABLE bnodes AS
SELECT
    id,
    ST_PointN(ST_ExteriorRing(polygon_proj), generate_series(1, npoints)) AS point_proj
FROM
    buildings
WHERE
    polygon_proj IS NOT NULL AND
    NOT relation AND
    NOT layer AND
    wall
"""

sql21 = """
CREATE INDEX bnodes_point_proj ON bnodes USING GIST(point_proj);
"""

sql30 = """
CREATE TABLE intersection_{0}_{1} AS
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Transform(ST_Centroid(ST_Intersection(b1.polygon_proj, b2.polygon_proj)), 4326)),
    ST_Area(ST_Intersection(b1.polygon_proj, b2.polygon_proj)) AS intersectionArea,
    least(b1.area, b2.area) * 0.10 AS threshold,
    b1.polygon_proj
FROM
    {0}buildings AS b1
    JOIN {1}buildings AS b2 ON
        b1.id > b2.id AND
        b1.linestring && b2.linestring AND
        ST_IsValid(ST_Intersection(b1.polygon_proj, b2.polygon_proj)) AND
        ST_Area(ST_Intersection(b1.polygon_proj, b2.polygon_proj)) > 0
WHERE
    b1.wall AND
    b2.wall AND
    NOT b1.relation AND
    NOT b2.relation AND
    NOT b1.layer AND
    NOT b2.layer AND
    b1.polygon_proj IS NOT NULL AND
    b2.polygon_proj IS NOT NULL
"""

sql31 = """
SELECT
    *
FROM
    intersection_{0}_{1}
"""

sql40 = """
SELECT
    id,
    ST_AsText(ST_Transform(ST_Centroid(polygon_proj), 4326))
FROM
    {0}buildings
WHERE
    NOT relation AND
    NOT layer AND
    polygon_proj IS NOT NULL AND
    wall AND
    area < 0.5 * 0.5
"""

sql50 = """
SELECT
    DISTINCT ON (bnodes.id, bnodes.point_proj)
    buildings.id,
    bnodes.id,
    ST_AsText(ST_Transform(bnodes.point_proj, 4326))
FROM
    {0}buildings AS buildings
    JOIN {1}bnodes AS bnodes ON
        buildings.id > bnodes.id AND
        ST_DWithin(buildings.polygon_proj, bnodes.point_proj, 0.01) AND
        ST_Disjoint(buildings.polygon_proj, bnodes.point_proj)
WHERE
    NOT buildings.relation AND
    NOT buildings.layer AND
    buildings.polygon_proj IS NOT NULL AND
    buildings.wall
ORDER BY
    bnodes.id,
    bnodes.point_proj
"""

sql60 = """
SELECT
    ST_AsText(ST_Transform(ST_Centroid(geom), 4326)),
    ST_Area(geom)
FROM
    (
    SELECT
        (ST_Dump(ST_Union(ST_Buffer(polygon_proj, 200, 'quad_segs=2')))).geom AS geom
    FROM
        intersection_{0}_{1}
    WHERE
        intersectionArea > threshold
    ) AS buffer
WHERE
    ST_Area(geom) > 1000 * 1000
"""

sql70 = """
SELECT
   DISTINCT ON (b2.id)
   b2.id,
   ST_AsText(way_locate(b2.linestring))
FROM
   {0}buildings AS b1
   JOIN {1}buildings AS b2 ON
       b2.id != b1.id AND
       b1.tags->'building' = b2.tags->'building' AND
       b1.wall = b2.wall AND
       ST_Intersects(b1.polygon_proj, b2.polygon_proj) AND
       b2.npoints = 3
WHERE
   NOT b1.relation AND
   NOT b2.relation AND
   NOT b1.layer AND
   NOT b2.layer AND
   b1.polygon_proj IS NOT NULL AND
   b2.polygon_proj IS NOT NULL
"""

class Analyser_Osmosis_Building_Overlaps(Analyser_Osmosis):

    requires_tables_full = ['buildings']
    requires_tables_diff = ['buildings', 'touched_buildings', 'not_touched_buildings']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.FR = config.options and ("country" in config.options and config.options["country"] == "FR" or "test" in config.options)
        self.classs_change[1] = {"item":"0", "level": 3, "tag": ["building", "geom", "fix:chair"], "desc": T_(u"Building intersection") }
        self.classs_change[2] = {"item":"0", "level": 2, "tag": ["building", "geom", "fix:chair"], "desc": T_(u"Large building intersection") }
        self.classs_change[3] = {"item":"0", "level": 3, "tag": ["building", "geom", "fix:chair"], "desc": T_(u"Building too small") }
        self.classs_change[4] = {"item":"0", "level": 3, "tag": ["building", "geom", "fix:chair"], "desc": T_(u"Gap between buildings") }
        self.classs_change[5] = {"item":"0", "level": 1, "tag": ["building", "fix:chair"], "desc": T_(u"Large building intersection cluster") }
        if self.FR:
            self.classs_change[6] = {"item":"1", "level": 3, "tag": ["building", "geom", "fix:chair"], "desc": T_(u"Building in parts") }
        self.callback30 = lambda res: {"class":2 if res[3]>res[4] else 1, "data":[self.way, self.way, self.positionAsText]}
        self.callback40 = lambda res: {"class":3, "data":[self.way, self.positionAsText]}
        self.callback50 = lambda res: {"class":4, "data":[self.way, self.way, self.positionAsText]}
        self.callback60 = lambda res: {"class":5, "data":[self.positionAsText]}
        if self.FR:
            self.callback70 = lambda res: {"class":6, "data":[self.way, self.positionAsText]}

    def analyser_osmosis_full(self):
        self.run(sql20)
        self.run(sql21)
        self.run(sql30.format("", ""))
        self.run(sql31.format("", ""), self.callback30)
        self.run(sql40.format(""), self.callback40)
        self.run(sql50.format("", ""), self.callback50)
        self.run(sql60.format("", ""), self.callback60)
        if self.FR:
            self.run(sql70.format("", ""), self.callback70)

    def analyser_osmosis_diff(self):
        self.run(sql20)
        self.run(sql21)
        self.create_view_touched("bnodes", "W")
        self.run(sql30.format("touched_", ""))
        self.run(sql30.format("not_touched_", "touched_"))
        self.run(sql31.format("touched_", ""), self.callback30)
        self.run(sql31.format("not_touched_", "touched_"), self.callback30)
        self.run(sql40.format("touched_"), self.callback40)
        self.run(sql50.format("touched_", ""), self.callback50)
        self.run(sql50.format("not_touched_", "touched_"), self.callback50)
        #self.run(sql60.format("", ""), self.callback60) Can be done in diff mode without runing a full sql30
        if self.FR:
            self.run(sql70.format("touched_", ""), self.callback70)
            self.run(sql70.format("not_touched_", "touched_"), self.callback70)
