#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2022                                      ##
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

from collections import defaultdict

from .Analyser_Merge import Analyser_Merge


sql10 = """
CREATE TEMP TABLE osm_item_buffer AS
SELECT
    id,
    tags,
    ST_Buffer(geom, {buffer}, 'quad_segs=1') AS geom_buffer
FROM
    osm_item
"""

sql11 = """
CREATE INDEX osm_item_buffer_geom_buffer ON osm_item_buffer USING gist(geom_buffer)
"""

sql20 = """
CREATE TEMP TABLE diff AS
SELECT
    opendata.tags,
    opendata.fields,
    coalesce(
        ST_Difference(
            opendata.geom,
            ST_MemUnion(osm_item_buffer.geom_buffer)
        ),
        opendata.geom
    ) AS geom
FROM
    {0} AS opendata
    LEFT JOIN osm_item_buffer ON
        ST_Intersects(osm_item_buffer.geom_buffer, opendata.geom)
GROUP BY
    opendata.tags,
    opendata.geom,
    opendata.fields
"""

sql21 = """
CREATE TEMP TABLE diff2 AS
SELECT
    *
FROM (
    SELECT
        tags,
        fields,
        (ST_Dump(geom)).geom AS geom
    FROM
        diff
) AS t
WHERE
    NOT ST_isEmpty(geom) AND
    ST_Length(geom) > 30
"""

sql30 = """
SELECT
    0, -- new node
    ST_AsText(ST_Transform(ST_LineInterpolatePoint(ST_Segmentize(geom, 100), 0.5), 4326)),
    tags,
    fields
FROM
    diff2
"""

class Analyser_Merge_Network(Analyser_Merge):

    def analyser_osmosis_common(self):
        table = super().analyser_osmosis_common()
        if not table:
            return

        self.run(sql10.format(buffer = self.conflate.conflationDistance))
        self.run(sql11)
        self.run(sql20.format(table))
        self.run(sql21)
        self.run(sql30, lambda res: {
            "class": self.missing_official['id'],
            "data": [self.node_new, self.positionAsText],
            "text": self.conflate.mapping.text(defaultdict(lambda: None, res[2]), defaultdict(lambda: None, res[3])),
            "fix": self.passTags(res[2]) if res[2] != {} else None,
        })
