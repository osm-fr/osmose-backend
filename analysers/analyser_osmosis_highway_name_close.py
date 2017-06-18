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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
  h1.id,
  h2.id,
  ST_AsText(way_locate(h1.linestring)),
  h1.tags->'name'
FROM
  highways AS h1
  JOIN highways AS h2 ON
    h1.linestring && h2.linestring AND
    h1.id < h2.id AND
    h1.tags->'name' != (h2.tags->'name') AND
    abs(length(h1.tags->'name') - length(h2.tags->'name')) <= 1 AND
    length(regexp_replace(h1.tags->'name', '[.0-9]', '', 'g')) >= 2 AND
    levenshtein(regexp_replace(h1.tags->'name', '[.0-9]', '', 'g'), regexp_replace(h2.tags->'name', '[.0-9]', '', 'g')) = 1
WHERE
  h1.tags != ''::hstore AND
  h1.tags?'name' AND
  h2.tags != ''::hstore AND
  h2.tags?'name'
"""


class Analyser_Osmosis_Highway_Name_Close(Analyser_Osmosis):

    requires_tables_full = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"5080", "level": 1, "tag": ["highway", "name"], "desc": T_(u"Close similar name") }

    def analyser_osmosis_full(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText], "text": {"en": res[3]}})
