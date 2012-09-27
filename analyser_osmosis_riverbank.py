#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
SELECT
    rb.id,
    ST_AsText(way_locate(rb.linestring))
FROM
    {0}ways AS rb
    LEFT JOIN (
        SELECT
            id,
            linestring
        FROM
            {1}ways
        WHERE
            tags?'waterway' AND
            tags->'waterway' IN ('river', 'canal', 'stream')
        ) AS ww ON
        ST_Intersects(ST_MakePolygon(rb.linestring), ww.linestring)
WHERE
    rb.tags?'waterway' AND
    rb.tags->'waterway' = 'riverbank' AND
    rb.is_polygon AND
    ww.id IS NULL
"""


class Analyser_Osmosis_Riverbank(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1220", "level": 3, "tag": ["waterway"], "desc":{"fr":"Riverbank sans river", "en":"Riverbank without river"} }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_change(self):
        self.run(sql10.format("_touched", ""), self.callback10)
        self.run(sql10.format("", "_touched"), self.callback10)
