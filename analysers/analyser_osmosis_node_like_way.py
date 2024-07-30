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

from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

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
SELECT DISTINCT ON (nodes.id)
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
            nodes.tags ?| ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building', 'man_made'] AND
            not (node.tags?'aeroway' AND node.tags->'aeroway' = 'parking_position') and
            NOT nodes.tags ?| ARRAY['proposed', 'construction']
    ORDER BY
      1 -- Just to force the query planner to does not merge sub and main request
    ) AS nodes
    JOIN {0}ways AS ways ON
        ways.id = nodes.way_id AND
        ways.tags != ''::hstore AND
        ways.tags ?| ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building', 'man_made'] AND
        NOT ways.tags ?| ARRAY['proposed', 'construction']
WHERE
    slice(ways.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building', 'man_made']) @>
    slice(nodes.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building', 'man_made']) OR
    slice(ways.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building', 'man_made']) <@
    slice(nodes.tags, ARRAY['aerialway', 'aeroway', 'amenity', 'highway', 'landuse', 'leisure', 'natural', 'railway', 'waterway', 'building', 'man_made'])
ORDER BY
    nodes.id
"""

class Analyser_Osmosis_Node_Like_Way(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 4090, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Way node tagged like way'),
            detail = T_(
'''Way node tagged like way. Probably due to a wrong selection when
editing, nodes in the way have the same tags that way.'''),
            fix = T_(
'''Check and remove tag from node.'''))
        self.callback10 = lambda res: {"class":1, "data":[None, self.way_full, self.node_full, self.positionAsText], "fix":[ [None, None, {"-": res[0]}] ]}

    def analyser_osmosis_full(self):
        self.run(sql10)
        self.run(sql20.format("", ""), self.callback10)

    def analyser_osmosis_diff(self):
        self.run(sql10)
        self.run(sql20.format("touched_", "not_touched_"), self.callback10)
        self.run(sql20.format("", "touched_"), self.callback10)
