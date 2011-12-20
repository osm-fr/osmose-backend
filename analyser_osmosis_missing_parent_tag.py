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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    ways.id,
    ST_AsText(ST_Centroid(linestring)),
    t0,
    t1
FROM
    ways,
    (
    SELECT
        base as t0,
        ways.tags->base AS t1,
        ways.tags->(ways.tags->base) AS t2,
        COUNT(*) AS c
    FROM
        ways,
        (VALUES ('highway'), ('cycleway'), ('waterway'), ('railway'), ('power'), ('man_made'), ('leisure'), ('amenity'), ('shop'), ('craft'), ('emergency'), ('tourism'), ('historic'), ('landuse'), ('military'), ('natural'), ('route'), ('boundary'), ('sport')) as t(base)
    WHERE
        ways.tags->base NOT IN ('cycleway', 'wood') AND
        ways.tags?base AND
        ways.tags?(ways.tags->base)
    GROUP BY
        base,
        t1,
        t2
    HAVING
        COUNT(*) > 50
    ) AS ref
WHERE
    NOT tags?t0 AND
    tags?t1 AND
    tags->t1 = t2
;
"""

class Analyser_Osmosis_Missing_Parent_Tag(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"2050", "desc":{"fr":"Tag parent manquant", "en":"Missing parent tag"} }

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {
            "class":1,
            "data":[self.way_full, self.positionAsText],
            "text":{"fr":"Manque %s=%s" % (res[2],res[3]), "en":"Missing %s=%s" % (res[2],res[3])} })
