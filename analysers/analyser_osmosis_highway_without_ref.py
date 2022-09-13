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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT DISTINCT
  ways.id,
  ST_AsText(way_locate(linestring))
FROM
  highways AS ways
  LEFT JOIN relation_members ON
    relation_members.member_type = 'W' AND
    relation_members.member_id = ways.id
  LEFT JOIN relations ON
    relations.id = relation_members.relation_id AND
    relations.tags ?| ARRAY['noref', 'ref', 'nat_ref', 'int_ref']
WHERE
  ways.highway = 'motorway' AND
  NOT ways.tags ?| ARRAY['noref', 'ref', 'nat_ref', 'int_ref'] AND
  relations.id IS NULL
"""


class Analyser_Osmosis_Highway_Without_Ref(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs[20804] = self.def_class(item = 2080, level = 2, tags = ['highway', 'ref', 'fix:chair'],
            title = T_('Motorway without ref, nat_ref, int_ref or noref tag'))

        self.callback10 = lambda res: {"class":20804, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql10, self.callback10)
