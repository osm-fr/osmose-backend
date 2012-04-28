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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    w1.id,
    w2.id,
    ST_ASText(ST_GeometryN(ST_Multi(ST_Intersection(w1.linestring, w2.linestring)), 1))
FROM
    (VALUES ('waterway'), ('natural'), ('landuse')) AS tt(t)
    JOIN ways AS w1 ON
        w1.tags?t AND
        (t != 'waterway' OR w1.tags->t = 'riverbank')
    JOIN ways AS w2 ON
        -- Same tags and value
        w2.tags?t AND
        w1.tags->t = w2.tags->t AND
        -- Avoid duplicate check
        w1.id < w2.id
WHERE
    -- Ways not linked
    NOT ST_Touches(w1.linestring, w2.linestring) AND
    -- Ways share inner space
    ST_Crosses(w1.linestring, w2.linestring) AND
    -- If ways are polygons they share more than one point
    (
        NOT (w1.is_polygon AND w2.is_polygon) OR
        ST_NumGeometries(ST_Intersection(w1.linestring, w2.linestring)) > 1
    )
;
"""

class Analyser_Osmosis_Surface_Overlaps(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1150", "level": 3, "tag": ["landuse", "geom"], "desc":{"fr":"Intersection entres surfaces", "en":"Surfaces intersection"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10, self.callback10)
