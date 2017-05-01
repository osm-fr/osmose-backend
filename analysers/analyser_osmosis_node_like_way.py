#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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
CREATE OR REPLACE FUNCTION intersection(anyarray, anyarray) RETURNS anyarray as $$
SELECT ARRAY(
    SELECT $1[i]
    FROM generate_series( array_lower($1, 1), array_upper($1, 1) ) i
    WHERE ARRAY[$1[i]] && $2
);
$$ language sql
   IMMUTABLE
   RETURNS NULL ON NULL INPUT;
"""

sql20 = """
SELECT
    intersection(akeys(ways.tags), akeys(nodes.tags)),
    ways.id,
    nodes.id,
    ST_AsText(nodes.geom)
FROM
    (
    SELECT
        nodes.id,
        way_nodes.way_id,
        nodes.tags,
        nodes.geom
    FROM
        way_nodes
        JOIN {1}nodes AS nodes ON
            nodes.id = way_nodes.node_id AND
            nodes.tags != ''::hstore AND
            nodes.tags ?| ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building'] AND
            NOT nodes.tags ?| ARRAY['proposed', 'construction']
    ORDER BY
      1 -- Just to force the query planner to does not merge sub and main request
    ) AS nodes
    JOIN {0}ways AS ways ON
        ways.id = nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags ?| ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building'] AND
        NOT ways.tags ?| ARRAY['proposed', 'construction']
WHERE
    slice(ways.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building']) @>
    slice(nodes.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building']) OR
    slice(ways.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building']) <@
    slice(nodes.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building'])
"""

class Analyser_Osmosis_Node_Like_Way(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"4090", "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Way node tagged like way") }
        self.callback10 = lambda res: {"class":1, "data":[None, self.way_full, self.node_full, self.positionAsText], "fix":[ [None, None, {"-": res[0]}] ]}

    def analyser_osmosis_full(self):
        self.run(sql10)
        self.run(sql20.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10)
        self.run(sql20.format("touched_", "not_touched_"), self.callback10)
        self.run(sql20.format("", "touched_"), self.callback10)
