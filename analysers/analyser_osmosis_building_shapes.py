#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Vincent Pottier <@.> 2010                                  ##
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
SELECT
    type_id,
    ST_AsText(polygon_locate(poly))
FROM
    {0}buildings
WHERE
    wall AND
    npoints > 15 AND
    area / ST_Area(ST_MinimumBoundingCircle(poly_proj)) > 0.95 AND
    ST_MaxDistance(poly_proj, poly_proj) > 5 AND
    tags - ARRAY['created_by', 'source', 'name', 'building', 'man_made', 'note:qadastre'] = ''::hstore AND
    tags->'building' NOT IN ('hut', 'ger', 'yurt', 'slurry_tank') AND
    tags->'man_made' NOT IN ('water_tower', 'reservoir_covered', 'wastewater_plant', 'storage_tank', 'windmill', 'dovecote', 'silo', 'gasometer', 'lighthouse', 'bioreactor')
"""

sql20 = """
SELECT
    type_id,
    ST_AsText(polygon_locate(poly))
FROM
    {0}buildings
WHERE
    wall AND
    ST_MaxDistance(poly_proj, poly_proj) > 300 AND
    tags - ARRAY['created_by', 'source', 'name', 'building', 'note:qadastre'] = ''::hstore AND
    tags->'building' NOT IN ('warehouse', 'industrial', 'greenhouse', 'manufacture', 'hospital', 'university')
"""

class Analyser_Osmosis_Building_Shapes(Analyser_Osmosis):

    requires_tables_full = ['buildings']
    requires_tables_diff = ['touched_buildings']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if "proj" in self.config.options:
            detail = T_(
'''The shape of the building is characteristic and as such would be
tagged.''')
            self.classs_change[1] = self.def_class(item = 7011, level = 3, tags = ['building', 'fix:imagery'],
                title = T_('Special building (round)'),
                detail = detail)
            self.classs_change[2] = self.def_class(item = 7011, level = 3, tags = ['building', 'fix:imagery'],
                title = T_('Special building (large)'),
                detail = detail)

            self.callback10 = lambda res: {"class":1, "data":[self.any_full, self.positionAsText], "fix":[
                {"+":{"man_made":"water_tower"}},
                {"+":{"man_made":"reservoir_covered"}},
                {"+":{"man_made":"wastewater_plant"}},
                {"+":{"man_made":"storage_tank"}},
                {"+":{"man_made":"windmill"}},
                {"+":{"man_made":"dovecote"}},
                {"+":{"man_made":"silo"}},
                {"+":{"building":"hut"}},
                {"+":{"building":"ger"}},
            ]}
            self.callback20 = lambda res: {"class":2, "data":[self.any_full, self.positionAsText], "fix":[
                {"+":{"man_made":"works"}},
                {"+":{"shop":"mall"}},
                {"+":{"shop":"supermarket"}},
                {"~":{"building":"warehouse"}},
                {"~":{"building":"industrial"}},
                {"~":{"building":"greenhouse"}},
            ]}

    def analyser_osmosis_full(self):
        if "proj" in self.config.options:
            self.run(sql10.format(''), self.callback10)
            self.run(sql20.format(''), self.callback20)

    def analyser_osmosis_diff(self):
        if "proj" in self.config.options:
            self.run(sql10.format('touched_'), self.callback10)
            self.run(sql20.format('touched_'), self.callback20)
