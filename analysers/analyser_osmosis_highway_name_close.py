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
from modules import languages

sql10_regex = "regexp_replace(regexp_replace(regexp_replace(regexp_replace({0}, '[/.0-9\u0660-\u0669\u06F0-\u06F9]', '', 'g'), '(^| )[a-zA-Z](?= |$)', '\\1', 'g'), '(^| )[IVXLDCM]+(?= |$)', '\\1', 'g'), ' +', ' ')"

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
    length({0}) >= 2 AND
    levenshtein({0}, {1}) = 1
WHERE
  h1.tags != ''::hstore AND
  h1.tags?'name' AND
  h2.tags != ''::hstore AND
  h2.tags?'name'
""".format(sql10_regex.format("h1.tags->'name'"), sql10_regex.format("h2.tags->'name'"))


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
            self.run(sql10, lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText], "text": {"en": res[3]}})
