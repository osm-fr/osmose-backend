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
    ways AS w1,
    ways AS w2
WHERE
    -- Same tags
    w1.tags?'{0}' AND
    w2.tags?'{0}' AND
    -- Same value
    w1.tags->'{0}' = w2.tags->'{0}' AND
    ('{0}' != 'waterway' OR w1.tags->'{0}' = 'riverbank') AND
    -- Avoid duplicate check
    w1.id < w2.id AND
    -- Valid
    ST_NPoints(w1.linestring) > 1 AND
    ST_NPoints(w2.linestring) > 1 AND
    -- Ways not linked
    NOT ST_Touches(w1.linestring, w2.linestring) AND
    -- Ways share inner space
    ST_Crosses(w1.linestring, w2.linestring)
"""

class Analyser_Osmosis_Surface_Overlaps(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1150", "level": 3, "tag": ["landuse", "geom", "fix:imagery"], "desc":{"fr": u"Intersection entres surfaces", "en": u"Surfaces intersection", "es": u"Intersección entre superficies"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        sql = []
        for t in ("waterway", "natural", "landuse"):
            sql.append(sql10.format(t))
        sql = "(\n" + ("\n)UNION(\n".join(sql)) + "\n)"
        self.run(sql, self.callback10)
