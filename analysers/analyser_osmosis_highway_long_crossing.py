#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyright Osmose Contributors 2023                                   ##
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
    ST_AsText(way_locate(linestring))
FROM
    {0}ways
WHERE
    tags != ''::hstore AND
    (
        (tags?'footway' AND tags->'footway' = 'crossing') OR
        (tags?'cycleway' AND tags->'cycleway' = 'crossing')
    ) AND
    ST_Length(linestring::geography) > 200
"""

class Analyser_Osmosis_Highway_Long_Crossing(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 7800, level = 2, tags = ['tag', 'highway', 'fix:survey'],
            title = T_('Long Crossing'),
            detail = T_(
'''The crossing way is much longer than expected'''))

        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText] }

    def analyser_osmosis_full(self):
        self.run(sql10.format(""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_"), self.callback10)
