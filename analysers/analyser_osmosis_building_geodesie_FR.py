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

sql10 = u"""
CREATE TEMP TABLE survery_building AS
SELECT DISTINCT ON (nodes.geom)
    nodes.id,
    nodes.geom,
    ST_Transform(nodes.geom, {0}) AS geom_transform,
    SUBSTRING(nodes.tags->'description' from '#"%#" -%' for '#') AS desc
FROM
    nodes
    JOIN (VALUES
        ('basilique'),
        ('bâtiment'),
        ('blockhaus'),
        ('cathédrale'),
        ('château'),
        ('chapelle'),
        ('cheminée'),
        ('clocher'),
        ('église'),
        ('mairie'),
        ('maison'),
        ('moulin'),
        ('phare'),
        ('réservoir'),
        ('silo'),
        ('tour')
    ) AS k(kw) ON
        position(k.kw in lower(nodes.tags->'description')) > 0
    JOIN (VALUES
        ('marche')
    ) AS z(kw) ON
        position(z.kw in lower(nodes.tags->'description')) <= 0
WHERE
    nodes.tags != ''::hstore AND
    nodes.tags?'man_made' AND
    nodes.tags->'man_made' = 'survey_point' AND
    nodes.tags?'description' AND
    position('point constaté détruit' in lower(nodes.tags->'description')) = 0 AND
    SUBSTRING(nodes.tags->'description' from '#"%#" -%' for '#') IS NOT NULL
"""

sql11 = """
CREATE INDEX survery_building_idx ON survery_building USING gist(geom)
"""

sql12 = """
DROP VIEW IF EXISTS vicinity CASCADE;
CREATE VIEW vicinity AS
SELECT
    survery_building.id AS s_id,
    ways.id AS b_id
FROM
    survery_building
    JOIN buildings AS ways ON
        survery_building.geom && ways.linestring AND
        ST_DWithIn(survery_building.geom_transform, polygon_proj, 0.5)
"""

sql13 = """
SELECT
    id,
    ST_AsText(geom),
    survery_building.desc
FROM
    survery_building
    LEFT JOIN vicinity ON
        vicinity.s_id = survery_building.id
WHERE
    vicinity.s_id IS NULL
"""

class Analyser_Osmosis_Building_Geodesie_FR(Analyser_Osmosis):

    requires_tables_full = ['buildings']
    requires_tables_diff = ['touched_buildings']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 7010, level = 3, tags = ['building', 'fix:chair'],
            title = T_('Geodesic mark without building'),
            detail = T_(
'''A survey point has a name which indicates it is located on a
building (bell tower, water tower, tower), but the node is not inside a
building polygon (`building=*`).'''),
            fix = T_(
'''If the building footprint is present but is misplaced because of a
shift in the source data (cadastre, orthophotographs), replace the
layout of the building to correct this issue. Otherwise, the building must
be drawn.'''),
            trap = T_(
'''Do not move the geodetic point, because it is a reference point (see the
[import of these geodetic
markers](https://wiki.openstreetmap.org/wiki/France/Rep%C3%A8res_G%C3%A9od%C3%A9siques)).
It could be that all the surrounding buildings are shifted.'''))

        self.callback10 = lambda res: {"class":1,
            "data":[self.node_full, self.positionAsText],
            "text":{"en":res[2]} }

    def analyser_osmosis_common(self):
        self.run(sql10.format(self.config.options.get("proj")))
        self.run(sql11)
        self.run(sql12)
        self.run(sql13, self.callback10)
