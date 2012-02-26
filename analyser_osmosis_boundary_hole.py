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
    ST_AsText(st_centroid(geom))
FROM (
    SELECT
        (ST_Dump(ST_Polygonize(linestring))).geom AS geom
    FROM (
        SELECT
            linestring
        FROM
            ways
                JOIN relation_members ON ways.id = relation_members.member_id AND relation_members.member_type = 'W'
                JOIN relations ON relations.id = relation_members.relation_id AND relations.tags ? 'admin_level' AND relations.tags -> 'admin_level' = '%d'
        WHERE
            NOT ways.is_polygon -- retire les polygones (îles et communes isolés)
        GROUP BY
            ways.id,
            ways.linestring
        HAVING
            COUNT(ways.id) = 1
    ) AS foo
) AS bar
WHERE
  ST_NPoints(geom) < 100 -- Valeur exp. determiné sur l'Aquitaine pour ne pas avoir de faux positifs
;
"""

class Analyser_Osmosis_Boundary_Hole(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"6060", "desc":{"fr":"Trou entre les limites administratives", "en":"Hole between administrative boundarie"} }

    def analyser_osmosis(self):
        if self.config.options:
            admin_level = self.config.options["admin_level"]
        else:
            admin_level = 8
        sql = sql10 % (admin_level)

        self.run(sql, lambda res: {"class":1, "subclass":abs(int(hash(res[0]))), "data":[self.positionAsText]} )
