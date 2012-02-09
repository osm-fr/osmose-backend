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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
DROP TABLE survery_building CASCADE;
CREATE TEMP TABLE survery_building AS
SELECT DISTINCT
    MIN(nodes.id) AS id,
    nodes.geom
FROM
    nodes
    JOIN (VALUES
        ('bâtiment'),
        ('blockhaus'),
        ('château'),
        ('chapelle'),
        ('cheminée'),
        ('clocher'),
        ('croix'),
        ('église'),
        ('mairie'),
        ('maison'),
        ('phare'),
        ('réservoir'),
        ('silo'),
        ('tour')
    ) AS k(kw) ON
        nodes.tags ? 'man_made' AND
        nodes.tags->'man_made' = 'survey_point' AND
        nodes.tags ? 'description' AND
        position(k.kw in lower(nodes.tags->'description')) > 0 AND
        position('point constat dtruit' in lower(nodes.tags->'description')) = 0 AND
        SUBSTRING(nodes.tags->'description' from '#"%#" -%' for '#') IS NOT NULL
GROUP BY
    nodes.geom
;
"""

sql11 = """
CREATE INDEX survery_building_idx ON survery_building USING gist(geom);
"""

sql12 = """
DROP VIEW vicinity CASCADE;
CREATE VIEW vicinity AS
SELECT
    survery_building.id AS s_id,
    ways.id AS b_id
FROM
    survery_building
    JOIN {0}ways AS ways ON
        survery_building.geom && ways.linestring AND
        ways.tags ? 'building' AND
        ways.is_polygon AND
        ST_Within(survery_building.geom, ST_MakePolygon(ways.linestring))
;
"""

sql13 = """
SELECT
    id
FROM
    survery_building
    LEFT JOIN vicinity ON
        vicinity.s_id = survery_building.id
WHERE
    vicinity.s_id IS NULL
;

"""

class Analyser_Osmosis_Geodesie(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"7010", "desc":{"fr":"Repère géodésique sans bâtiment", "en":"Geodesic mark without building"} }
        self.callback10 = lambda res: {"class":1,
            "data":[self.node_full, self.positionAsText],
            "text":{"en":res[2]} }

    def analyser_osmosis_all(self):
        self.run(sql10.format(""), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12.format("touched_"))
        self.run(sql13, self.callback10)
