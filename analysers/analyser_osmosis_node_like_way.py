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
CREATE OR REPLACE FUNCTION intersection(anyarray, anyarray) RETURNS anyarray as $$
SELECT ARRAY(
    SELECT $1[i]
    FROM generate_series( array_lower($1, 1), array_upper($1, 1) ) i
    WHERE ARRAY[$1[i]] && $2
);
$$ language sql;
"""

sql20 = """
SELECT DISTINCT
    intersection(akeys(ways.tags), akeys(nodes.tags)),
    ways.id,
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    (VALUES
        ('aerialway'),
        ('aeroway'),
        ('amenity'),
        ('highway'),
        ('landuse'),
        ('leisure'),
        ('natural'),
        ('railway'),
        ('waterway'),
        ('building')
    ) AS tt(t)
    JOIN {0}ways AS ways ON
        ways.tags?t
    JOIN way_nodes ON
        way_nodes.way_id = ways.id
    JOIN {1}nodes AS nodes ON
        nodes.tags?t AND
        nodes.id = way_nodes.node_id
WHERE
    ways.tags->t = nodes.tags->t
;
"""

class Analyser_Osmosis_Node_Like_Way(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"4090", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Way node tagged like way") }
        self.callback20 = lambda res: {"class":1, "data":[None, self.way_full, self.node_full, self.positionAsText], "fix":[ [None, None, {"-": res[0]}] ]}

    def analyser_osmosis_all(self):
        self.run(sql10)
        self.run(sql20.format("", ""), self.callback20)

    def analyser_osmosis_touched(self):
        self.run(sql10)
        dup = set()
        self.run(sql20.format("touched_", ""), lambda res: dup.add(res[2]) or self.callback10(res))
        self.run(sql20.format("", "touched_"), lambda res: res[2] in dup or dup.add(res[2]) or self.callback10(res))
