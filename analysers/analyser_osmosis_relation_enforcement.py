#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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

sql00 = """
SELECT
  nodes.id,
  ST_AsText(nodes.geom)
FROM
  nodes
  LEFT JOIN highways ON
    nodes.geom && highways.linestring AND
    nodes.id = ANY (highways.nodes) AND
    NOT highways.is_construction
  LEFT JOIN relation_members ON
    relation_members.member_type = 'N' AND
    relation_members.member_id = nodes.id
  LEFT JOIN relations ON
    relations.id = relation_members.relation_id AND
    relations.tags?'type' AND
    relations.tags->'type' = 'enforcement'
WHERE
  nodes.tags?'highway' AND
  nodes.tags->'highway' = 'speed_camera' AND
  relations.id IS NULL AND
  highways.id IS NULL
"""

class Analyser_Osmosis_Relation_Enforcement(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1280", "level": 3, "tag": ["highway", "fix:chair"], "desc": T_(u"Speed camera should be on the highway or in an enforcement relation") }

    def analyser_osmosis_common(self):
        self.run(sql00, lambda res: {"class":1, "data":[self.node_full, self.positionAsText]})
