#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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

sql00 = """
CREATE TEMP TABLE surface AS
SELECT
    id,
    is_polygon,
    linestring,
    tags->'waterway' AS waterway,
    tags->'natural' AS natural,
    tags->'landuse' AS landuse
FROM
    ways
WHERE
    tags != ''::hstore AND
    tags ?| ARRAY['waterway', 'natural', 'landuse'] AND
    (NOT tags?'waterway' OR tags->'waterway' = 'riverbank') AND
    ST_NPoints(linestring) > 1
"""

sql01 = """
CREATE INDEX idx_surface_linestring ON surface USING GIST(linestring)
"""

sql10 = """
SELECT
    w1.id,
    w2.id,
    ST_ASText(ST_GeometryN(ST_Multi(ST_Intersection(w1.linestring, w2.linestring)), 1)),
    {1}
FROM
    surface AS w1,
    surface AS w2
WHERE
    -- Same value
    w1."{0}" IS NOT NULL AND
    w2."{0}" IS NOT NULL AND
    w1."{0}" = w2."{0}" AND
    -- Avoid duplicate check
    w1.id < w2.id AND
    -- Ways not linked
    NOT ST_Touches(w1.linestring, w2.linestring) AND
    -- Ways share inner space
    ST_Crosses(w1.linestring, w2.linestring) AND
    -- If ways are polygons they share more than one point
    (
        NOT (w1.is_polygon AND w2.is_polygon) OR
        ST_NumGeometries(ST_Intersection(w1.linestring, w2.linestring)) > 1
    )
"""

class Analyser_Osmosis_Surface_Overlaps(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.tags = ( (1, "waterway"),
                      (2, "natural"),
                      (3, "landuse"),
                    )

        for t in self.tags:
            self.classs[t[0]] = {"item":"1150", "level": 3, "tag": ["landuse", "geom", "fix:imagery"], "desc": T_(u"Area intersection %s", t[1]) }
        self.callback10 = lambda res: {"class":res[3], "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql00)
        self.run(sql01)
        for t in self.tags:
            self.run(sql10.format(t[1], t[0]), self.callback10)
