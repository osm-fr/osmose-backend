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
CREATE TEMP TABLE base_count AS
SELECT
    base as t0,
    ways.tags->base AS t1,
    COUNT(*) AS nbase
FROM
    ways,
    (VALUES ('highway'), ('cycleway'), ('waterway'), ('railway'), ('power'), ('man_made'), ('leisure'), ('amenity'), ('shop'), ('craft'), ('emergency'), ('tourism'), ('historic'), ('landuse'), ('military'), ('natural'), ('route'), ('boundary'), ('sport')) as t(base)
WHERE
    ways.tags?base
GROUP BY
    t0,
    t1
HAVING
    COUNT(*) > 50
"""

sql11 = """
CREATE TEMP TABLE base_extra_count AS
SELECT
    base as t0,
    ways.tags->base AS t1,
    ways.tags->(ways.tags->base) AS t2,
    COUNT(*) AS nextra
FROM
    ways,
    (VALUES ('highway'), ('cycleway'), ('waterway'), ('railway'), ('power'), ('man_made'), ('leisure'), ('amenity'), ('shop'), ('craft'), ('emergency'), ('tourism'), ('historic'), ('landuse'), ('military'), ('natural'), ('route'), ('boundary'), ('sport')) as t(base)
WHERE
    ways.tags?base AND
    ways.tags?(ways.tags->base)
GROUP BY
    t0,
    t1,
    t2
HAVING
    COUNT(*) > 50
"""

sql12 = """
SELECT
    ways.id,
    ST_AsText(way_locate(linestring)),
    t0,
    t1
FROM
    ways,
    (
    SELECT
        t0,
        t1,
        t2
    FROM
        base_count
        NATURAL JOIN base_extra_count
    WHERE
        CAST(nextra AS REAL) / nbase > 0.2
    ) AS ref
WHERE
    NOT tags?t0 AND
    tags?t1 AND
    tags->t1 = t2;
"""

class Analyser_Osmosis_Missing_Parent_Tag(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"2050", "level": 1, "tag": ["tag"], "desc":{"fr": u"Tag parent manquant", "en": u"Missing parent tag"} }

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {
            "class":1,
            "data":[self.way_full, self.positionAsText],
            "fix":[{"+":{res[2]:res[3]}}] })
