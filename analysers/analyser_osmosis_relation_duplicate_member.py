#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose Project 2023                                        ##
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
  ST_AsText(relation_locate(id)),
  array_agg(duplicate_typeid ORDER BY duplicate_typeid), -- sequence doesn't matter as long as it's constant until relation changes
  array_agg(duplicate_string ORDER BY duplicate_string) -- keep same sequence as line above
FROM (
  SELECT
    id,
    member_type || member_id AS duplicate_typeid,
    member_type || member_id || ' (' || COUNT(*) || ')' AS duplicate_string
  FROM
    {0}relations AS relations
    JOIN relation_members ON
        relations.id = relation_id
  WHERE
    relations.tags != ''::hstore AND
    relations.tags?'type' AND
    relations.tags->'type' IN ('multipolygon', 'site', 'waterway', 'enforcement', 'public_transport', 'building')
  GROUP BY
    id,
    member_id,
    member_type,
    member_role
  HAVING
    COUNT(*) > 1
) AS t
GROUP BY
  id
"""

class Analyser_Osmosis_Relation_Duplicate_Member(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[3] = self.def_class(item = 1040, level = 1, tags = ['relation', 'fix:chair', 'geom'],
            title = T_('Duplicate relation member'),
            detail = T_(
'''The relation contains the same member (with the same role) more than once. This is not expected for this type of relations.'''),
            fix = T_(
'''Remove the duplicate members until only unique members remain.'''))

        self.callback10 = lambda res: {"class": 3, "data": [self.relation, self.positionAsText, self.array_id], "text": {"en": ', '.join(res[3]).lower()}}

    def analyser_osmosis_full(self):
        self.run(sql10.format(""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10.format("touched_"), self.callback10)



###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_relation_duplicate_member.osm",
                                         config.dir_tmp + "/tests/osmosis_relation_duplicate_member.test.xml", {})

    def test_classes(self):
        with Analyser_Osmosis_Relation_Duplicate_Member(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="3", elems=[("relation", "10001"), ("way", "1")])
        self.check_num_err(1)
