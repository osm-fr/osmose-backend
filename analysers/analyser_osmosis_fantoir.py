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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    array_agg(ids) AS ids,
    ST_AsText(array_locate(array_agg(ids))) AS geom,
    fantoir,
    names
FROM
    (
    SELECT
        fantoir,
        regexp_split_to_table(ids, ',') AS ids,
        names
    FROM
        (
        SELECT
            fantoir,
            array_agg(name) AS names,
            string_agg(ids, ',') AS ids
        FROM
            (
            SELECT
                fantoir,
                name,
                string_agg(type||id, ',') AS ids
            FROM
                ((
                SELECT
                    'N'::char(1) AS type,
                    id,
                    tags->'ref:FR:FANTOIR' AS fantoir,
                    tags->'addr:street' AS name
                FROM
                    nodes
                WHERE
                    tags != ''::hstore AND
                    tags?'ref:FR:FANTOIR' AND
                    tags?'addr:street'
                ) UNION ALL (
                SELECT
                    'W'::char(1) AS type,
                    id,
                    tags->'ref:FR:FANTOIR' AS fantoir,
                    COALESCE(tags->'addr:street', tags->'name') AS name
                FROM
                    ways
                WHERE
                    tags != ''::hstore AND
                    tags?'ref:FR:FANTOIR' AND
                    COALESCE(tags->'addr:street', tags->'name') IS NOT NULL
                ) UNION ALL (
                SELECT
                    'R'::char(1) AS type,
                    id,
                    tags->'ref:FR:FANTOIR' AS fantoir,
                    tags->'name' AS name
                FROM
                    relations
                WHERE
                    tags?'ref:FR:FANTOIR' AND
                    tags?'name'
                )) AS y
            WHERE
                length(fantoir) >= 10
            GROUP BY
                fantoir,
                name
            ) AS t
        GROUP BY
            fantoir
        HAVING
            count(*) > 1
        ) AS r
    ) AS m
GROUP BY
    fantoir,
    names
"""

class Analyser_Osmosis_Fantoir(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[11] = {"item":"2060", "level": 3, "tag": ["addr", "fix:chair"], "desc": T_f(u"Multiple name for the same ref FANTOIR") }

    def analyser_osmosis_common(self):
        self.run(sql10, lambda res: {"class":11, "data":[self.array_full, self.positionAsText],
            "text": T_f(u"Multiple name for the same ref FANTOIR {0}: {1}", res[2], ', '.join(res[3]))} )
