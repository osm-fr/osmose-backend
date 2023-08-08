#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Tristram Gräbener 2023                                     ##
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

# This analyser is similar to Analyser_Osmosis_Way_Approximate
# However, this one measures angles and not radiuses
# It most likely indicates a node that was accidentaly dragged
# While Analyser_Osmosis_Way_Approximate indicates that the way was drawn
# with too few nodes

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
WITH
    points AS (
        SELECT
            id,
            tags->'{tag}' AS type,
            (ST_DumpPoints(linestring)).geom AS geom4326,
            (ST_DumpPoints(ST_Transform(linestring, {srid}))).geom AS geom,
            (ST_DumpPoints(ST_Transform(linestring, {srid}))).path[1] AS index
        FROM
            {table_prefix}ways as ways
        WHERE
            tags != ''::hstore AND
            tags?'{tag}' AND tags->'{tag}' IN ('{tag_values}') AND
            ST_NPoints(linestring) >= 3
    ),
    angles AS (
        SELECT
            id, index, type,
            lead(geom4326) OVER (PARTITION BY id ORDER BY index) AS geom4326,
            lead(geom) OVER (PARTITION BY id ORDER BY index) AS geom,
            degrees(
                ST_Angle(geom,
                     lead(geom, 1) OVER (PARTITION BY id ORDER BY index),
                     lead(geom, 2) OVER (PARTITION BY id ORDER BY index)
                )
            ) angle,
            ST_Distance(
                geom,
                lead(geom, 1) OVER (PARTITION BY id ORDER BY index)
            ) AS length_1,
            ST_Distance(
                lead(geom, 1) OVER (PARTITION BY id ORDER BY index),
                lead(geom, 2) OVER (PARTITION BY id ORDER BY index)
            ) AS length_2
        FROM
            points
    )

    SELECT
        id,
        ST_AsText(geom4326),
        angle,
        type,
        index
    FROM
        angles
    WHERE
        (angle < 150 OR angle > 210)
        AND length_1 < 100
        AND length_2 < 100
"""

class Analyser_Osmosis_Way_Suspicious_Angle(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

        self.classs_change[11] = self.def_class(item = 1190, level = 2, tags = ['geom', 'railway', 'fix:imagery'],
            title = T_('Suspicious angle in way'),
            detail = T_(
'''Sharp angles on a railway are suspicious. Maybe a node was accidentally dragged?'''),
            fix = T_(
'''After checking orthophotos, add nodes or move existing nodes.'''),
            trap = T_(
''' On service ways, train stations and train workshops this could be a false positive.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/9/9d/Osmose-eg-error-1190.png)

`railway=rail` crudely drawn.'''))

        self.tags = ("rail", "light_rail")
        self.callback10 = lambda res: {"class":11, "subclass":res[4], "data":[self.way_full, self.positionAsText], "text": T_("railway={0} with suspicious angle {1}°", res[3], int(res[2]))}

    def analyser_osmosis_full(self):
        self.run(sql10.format(table_prefix="", tag="railway", tag_values="', '".join(self.tags), srid=self.config.options.get("proj")), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format(table_prefix="touched_", tag="railway", tag_values="', '".join(self.tags), srid=self.config.options.get("proj")), self.callback10)
