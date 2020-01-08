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

sql10 = """
SELECT
  (array_agg(tid))[1:10],
  ST_AsText(any_locate((array_agg(type))[1], (array_agg(id))[1])),
  w
FROM ((
  SELECT
    tags->'wikipedia' AS w,
    'N' || id AS tid,
    'N' AS type,
    id
  FROM
    nodes
  WHERE
    tags != ''::hstore AND
    tags?'wikipedia' AND
    NOT tags->'wikipedia' LIKE '%#%' AND
    NOT tags?| ARRAY['highway', 'railway', 'waterway', 'power', 'place', 'shop', 'network', 'operator']
) UNION ALL (
  SELECT
    tags->'wikipedia' AS w,
    'W' || id AS tid,
    'W' AS type,
    id
  FROM
    ways
  WHERE
    tags != ''::hstore AND
    tags?'wikipedia' AND
    NOT tags->'wikipedia' LIKE '%#%' AND
    NOT tags?| ARRAY['highway', 'railway', 'waterway', 'power', 'place', 'shop', 'network', 'operator']
) UNION ALL (
  SELECT
    tags->'wikipedia' AS w,
    'R' || id AS tid,
    'R' AS type,
    id
  FROM
    relations
  WHERE
    tags != ''::hstore AND
    tags?'wikipedia' AND
    NOT tags->'wikipedia' LIKE '%#%' AND
    NOT tags->'type' IN ('route', 'boundary') AND
    NOT tags?| ARRAY['highway', 'railway', 'waterway', 'power', 'place', 'shop', 'network', 'operator']
)) AS t
GROUP BY
  w
HAVING
  count(*) > 1
"""

class Analyser_Osmosis_Wikipedia(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 4130, level = 3, tags = ['fix:chair'],
            title = T_('Duplicate wikipedia tag'))

    def analyser_osmosis_common(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.array_full, self.positionAsText], "text": {"en": res[2]}})
