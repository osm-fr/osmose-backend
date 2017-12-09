#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2010                       ##
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

sql10 = u"""
SELECT
    ST_AsText(ST_Centroid(geom))
FROM (
    SELECT
        (ST_Dump(ST_Polygonize(linestring))).geom AS geom
    FROM (
        SELECT
            linestring
        FROM
            ways
            JOIN relation_members ON
                ways.id = relation_members.member_id AND
                relation_members.member_type = 'W'
            JOIN relations ON
                relations.id = relation_members.relation_id AND
                relations.tags?'admin_level' AND
                relations.tags->'admin_level' = '{0}'
        WHERE
            NOT ways.is_polygon AND -- avoid islands and isolated polygons
            ST_NPoints(linestring) > 1
        GROUP BY
            ways.id,
            ways.linestring
    ) AS foo
) AS bar
WHERE
  ST_NPoints(geom) < 100 -- Experimental value
"""

class Analyser_Osmosis_Boundary_Hole(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.admin_level = self.config.options and self.config.options.get("boundary_detail_level", 8) or 8
        self.classs[1] = {"item":"6060", "level": 2, "tag": ["boundary", "geom", "fix:chair"], "desc": T_(u"Hole between administrative boundaries of admin_level {0}", self.admin_level) }

    def analyser_osmosis_common(self):
        self.run(sql10.format(self.admin_level), lambda res: {"class":1, "subclass":self.stablehash(res[0]), "data":[self.positionAsText]} )
