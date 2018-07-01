#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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
  ways.id,
  relations.id,
  ST_AsText(way_locate(linestring))
FROM
  {0}relations AS relations
  JOIN relation_members ON
    relation_members.relation_id = relations.id AND
    relation_members.member_type = 'W'
  JOIN {1}ways AS ways ON
    ways.tags != ''::hstore AND
    ways.id = relation_members.member_id AND
    (
      NOT ways.tags?'route' OR
      ways.tags->'route' != 'ferry'
    ) AND
    (
      NOT ways.tags?'highway' OR
      ways.tags->'{3}' IN ({4}) OR
      (
        ways.tags->'highway' IN ({5}) AND
        (
           NOT ways.tags?'{3}' OR
           ways.tags->'{3}' NOT IN ({6})
        )
      )
    )
WHERE
  relations.tags != ''::hstore AND
  relations.tags?'type' AND
  relations.tags->'type' = 'route' AND
  relations.tags?'route' AND
  relations.tags->'route' = '{2}'
"""

class Analyser_Osmosis_Relation_Route_Access(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.map = {
            'bicycle': {
                'class': 1,
                'acces_tag': 'bicycle',
                'no_acces': "'no', 'false', 'private', 'discouraged'",
                'highway_overide': "'footway', 'pedestrian', 'trunk', 'motorway', 'trunk_link', 'motorway_link'",
                'highway_overide_access': "'yes', 'permissive', 'true', 'designated', 'shoulder', 'dismount'"},
            'foot': {
                'class': 2,
                'acces_tag': 'foot',
                'no_acces': "'no', 'false', 'private', 'discouraged'",
                'highway_overide': "'trunk', 'motorway', 'trunk_link', 'motorway_link'", # 'cycleway' default for foot depends on country
                'highway_overide_access': "'yes', 'permissive', 'true', 'designated'"},
            'hiking': { # Same as foot
                'class': 3,
                'acces_tag': 'foot',
                'no_acces': "'no', 'false', 'private', 'discouraged'",
                'highway_overide': "'trunk', 'motorway', 'trunk_link', 'motorway_link'", # 'cycleway' default for foot depends on country
                'highway_overide_access': "'yes', 'permissive', 'true', 'designated'"},
        }
        for route_type, access in self.map.items():
            self.classs_change[access['class']] = {'item':'3240', 'level': 2, 'tag': ['relation', 'routing'], 'desc': T_(u'Way access mismatch relation route=%s', route_type) }

    def callback10(self, clazz):
        return lambda res: {'class':clazz, 'data':[self.way_full, self.relation_full, self.positionAsText] }

    def analyser_osmosis_full(self):
        for route_type, access in self.map.items():
            self.run(sql10.format('', '', route_type, access['acces_tag'], access['no_acces'], access['highway_overide'], access['highway_overide_access']), self.callback10(access['class']))

    def analyser_osmosis_diff(self):
        for route_type, access in self.map.items():
            self.run(sql10.format('', 'touched_', route_type, access['acces_tag'], access['no_acces'], access['highway_overide'], access['highway_overide_access']), self.callback10(access['class']))
            self.run(sql10.format('touched_', 'not_touched_', route_type, access['acces_tag'], access['no_acces'], access['highway_overide'], access['highway_overide_access']), self.callback10(access['class']))
