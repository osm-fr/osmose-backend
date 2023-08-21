#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyright Osmose Contributors 2023                                    ##
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
    id,
    ST_AsText(way_locate(linestring)),
    ST_Length(linestring_proj)
FROM
    {0}highways
WHERE
    (
        (tags?'footway' AND tags->'footway' = 'crossing') OR
        (tags?'cycleway' AND tags->'cycleway' = 'crossing') OR
        (tags?'path' AND tags->'path' = 'crossing')
    ) AND
    ST_Length(linestring_proj) > 200

UNION ALL
SELECT
    id,
    ST_AsText(way_locate(linestring)),
    ST_Length(linestring_proj)
FROM
    {0}highways
WHERE
    tags?'ford' AND tags->'ford' in ('yes', 'stepping_stones') AND
    -- Some fords are pretty long, e.g. way 1077661529: 301m. Hence add quite a margin
    ST_Length(linestring_proj) > 1000
"""

class Analyser_Osmosis_Highway_Long_Crossing(Analyser_Osmosis):

    requires_tables_full = ['highways']
    requires_tables_diff = ['touched_highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        if not "proj" in self.config.options:
            return
        self.classs_change[10] = self.def_class(item = 2090, level = 2, tags = ['tag', 'highway', 'fix:survey'],
            title = T_('Long crossing'),
            detail = T_(
'''The crossing way is much longer than usual.'''),
            fix = T_(
'''Split the way at the point were it no longer crosses a highway or waterway.
Remove crossing-related tags (such as `*=crossing`, `ford=*`) from the fragment that isn't a crossing.'''))

        self.callback10 = lambda res: {
            "class": 10, "data": [self.way_full, self.positionAsText],
            "text": T_("Highway or waterway crossing of {0}m", round(res[2]))
        }

    def analyser_osmosis_full(self):
        self.run(sql10.format(""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_"), self.callback10)
