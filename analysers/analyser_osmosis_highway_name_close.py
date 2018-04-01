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
from modules import languages

sql10_regex = """regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(%s,
'[-\\[\\]\\{\\}\\(\\)\"\\\\/]', '', 'g'),
'(1st|2nd|3rd|[04-9]th)( |$)', '_', 'g'),
'(1ra|2da|3ra|4ta|5ta|6ta|7ma|8va|9na|0ma|1er|2do|3ro|4to|5to|6to|7mo|8vo|9no|0mo)( |$)', '_', 'g'),
'[/.0-9\u0660-\u0669\u06F0-\u06F9]', ' ', 'g'),
'(^| )[a-zA-Z](?= |$)', '\\1', 'g'),
'(^| )[IVXLDCM]+(?= |$)', '\\1', 'g'),
' +', ' ', 'g')"""

# Use temp table to force query planner
sql10 = """
CREATE TEMP TABLE highways_name AS
SELECT
  id,
  linestring,
  tags->'name' AS name,
  {0} AS namep
FROM
  highways
WHERE
  tags != ''::hstore AND
  tags?'name' AND
  length({0}) >= 4
""".format(sql10_regex % ("tags->'name'",))

sql11 = """
CREATE INDEX idx_highways_name_linestring ON highways_name USING gist(linestring)
"""

sql12 = """
SELECT
  h1.id,
  h2.id,
  ST_AsText(way_locate(h1.linestring)),
  h1.name
FROM
  highways_name AS h1
  JOIN highways_name AS h2 ON
    h1.linestring && h2.linestring AND
    h1.id < h2.id AND
    h1.namep != h2.namep AND
    abs(length(h1.name) - length(h2.name)) <= 1 AND
    levenshtein(h1.namep, h2.namep) = 1
"""


class Analyser_Osmosis_Highway_Name_Close(Analyser_Osmosis):

    requires_tables_full = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

        # Check langues for country are writen with alphabets
        self.alphabet = 'language' in config.options and languages.languages_are_alphabets(config.options['language'])

        if self.alphabet:
            self.classs_change[1] = {"item":"5080", "level": 1, "tag": ["highway", "name"], "desc": T_(u"Close similar name") }

    def analyser_osmosis_full(self):
        if self.alphabet:
            self.run(sql10)
            self.run(sql11)
            self.run(sql12, lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText], "text": {"en": res[3]}})

# TODO diff mode
