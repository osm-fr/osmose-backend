#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose Project 2022                                        ##
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
WITH RECURSIVE rcte AS (
  -- initial 'seed' relation
  SELECT DISTINCT ON (relation_id)
    relation_id AS start_id,
    member_id,
    1 as nloops,
    CONCAT('r', relation_id) AS path
  FROM
    relation_members
  WHERE
    member_type = 'R' AND
    relation_locate(relation_id) IS NOT NULL -- can't display relations without way/node members

  UNION ALL

  -- loop children until no 'relation'-type members or relation back to start
  SELECT
    rcte.start_id,
    child.member_id,
    nloops + 1 AS nloops,
    CONCAT(rcte.path, ' > r', child.relation_id) AS path
  FROM
    rcte
    JOIN relation_members AS child ON
      child.relation_id = rcte.member_id
    WHERE
      child.member_type = 'R' AND
      child.relation_id != rcte.start_id AND
      nloops < {maxloops} -- avoid getting stuck in strange constructions
)
SELECT DISTINCT ON (start_id)
  start_id,
  ST_AsText(relation_locate(start_id)),
  path
FROM
  rcte
WHERE
  start_id = member_id AND
  nloops < {maxloops}
ORDER BY
  start_id,
  LENGTH(path) -- to get the shortest path selected by the DISTINCT ON call
"""

class Analyser_Osmosis_Relation_Cyclic(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[2] = self.def_class(item = 1160, level = 2, tags = ['relation', 'fix:chair'],
            title = T_('Cyclic relation'),
            detail = T_(
'''A relation whose members (eventually) refer back to itself is rarely correct.'''))

    def analyser_osmosis_common(self):
        self.run(sql10.format(maxloops=10), lambda res: {
            "class": 2,
            "data": [self.relation, self.positionAsText],
            "text": {"en": res[2] + " > r" + str(res[0])}
        })



###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_relation_cyclic.osm",
                                         config.dir_tmp + "/tests/osmosis_relation_cyclic.test.xml", {})

    def test_classes(self):
        with Analyser_Osmosis_Relation_Cyclic(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="2", elems=[("relation", "10005")])
        self.check_err(cl="2", elems=[("relation", "10006")])
        self.check_err(cl="2", elems=[("relation", "10007")])
        self.check_err(cl="2", elems=[("relation", "10008")])
        self.check_err(cl="2", elems=[("relation", "10009")])
        self.check_err(cl="2", elems=[("relation", "10010")])
        self.check_err(cl="2", elems=[("relation", "10011")])
        self.check_err(cl="2", elems=[("relation", "10012")])
        self.check_num_err(8)
