#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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
CREATE TEMP TABLE park_highway AS
SELECT
  id,
  linestring,
  tags->'access' AS access
FROM
  highways
WHERE
  highway NOT IN ('footway', 'cycleway', 'steps', 'platform') AND
  NOT is_construction
"""

sql11 = """
CREATE INDEX park_highway_linestring_idx ON park_highway USING gist(linestring)
"""

sql12 = """
CREATE TEMP TABLE parkings AS
SELECT
  *
FROM (
  SELECT
    'W' || id AS type_id,
    tags,
    ST_MakePolygon(ways.linestring) AS poly
  FROM
    ways
  WHERE
    is_polygon AND
    tags != ''::hstore
  UNION ALL
    SELECT
      'R' || id AS type_id,
      tags,
      poly
    FROM
      multipolygons
    WHERE
      is_valid
) AS t
WHERE
  tags?'amenity' AND
  tags->'amenity' = 'parking' AND
  (NOT tags?'parking' OR tags->'parking' NOT IN ('street_side', 'lane'))
"""

sql13 = """
SELECT
  pr.type_id,
  ST_AsText(ST_PointOnSurface(pr.poly)),
  pr.tags->'park_ride' != 'no',
  ST_Perimeter(ST_Transform(pr.poly, {proj})) / ST_Area(ST_Transform(pr.poly, {proj}))
FROM
  parkings AS pr
  LEFT JOIN park_highway AS highway ON
    ST_Intersects(pr.poly, highway.linestring)
WHERE
  highway.id IS NULL
"""


sql20 = """
SELECT
  parking.type_id,
  array_agg('W' || parking_way.id),
  ST_AsText(ST_PointOnSurface(parking.poly)),
  array_agg(parking_way.access),
  parking.tags->'access'
FROM
  parkings AS parking
  JOIN park_highway AS parking_way ON
    ST_Intersects(parking.poly, parking_way.linestring) AND
    NOT ST_Contains(parking.poly, parking_way.linestring)
WHERE
  NOT parking.tags?'access' OR
  (
    parking.tags->'access' NOT IN ('private', 'permit', 'delivery', 'customers', 'no') AND
    parking.tags->'access' NOT LIKE '%;%'
  )
GROUP BY
  parking.type_id,
  parking.tags,
  parking.poly
HAVING
  array_agg(parking_way.access) <@ array['private', 'permit', 'delivery', 'customers']
"""

class Analyser_Osmosis_Parking_highway(Analyser_Osmosis):

    requires_tables_common = ['highways', 'multipolygons']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 3161, level = 1, tags = ['highway', 'fix:chair'],
            title = T_('Missing access way to parking'),
            detail = T_('There should be a `highway` feature leading to this parking facility to allow for correct routing.'))
        self.classs[2] = self.def_class(item = 3161, level = 3, tags = ['highway', 'fix:chair'],
            title = T_('Missing access way to parking'),
            detail = T_(
'''There should be a `highway` feature leading to this parking facility
to allow for correct routing. Add a road or check if `parking=*` is
correct. If it is a street side parking (`parking=street_side`) or lane,
then add appropriate tags.

See [parking](https://wiki.openstreetmap.org/wiki/Key:parking) tag on the wiki.'''))
        self.classs[3] = self.def_class(item = 3161, level = 3, tags = ['highway'],
            title = T_('Inconsistent access of parking'),
            detail = T_('''The `access` tag of the parking does not match the `access` tag of the ways inside the parking.
As a result, this public parking space can only be reached via limited-access roads.'''),
            fix = T_('Check which access restrictions are correct and apply them accordingly to the highways and the parking.'),
            trap = T_('A parking may be partially publicly accessible and partially private.'))

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12)
        self.run(sql13.format(proj=self.config.options["proj"]), lambda res: {
            "class": 1 if res[2] else 2,
            "data": [self.any_full, self.positionAsText],
            # Street side parkings typically have a perimeter/area ratio > 0.1
            "fix": {"+": {"parking": "street_side"}} if res[3] > 0.1 else None,
        })
        self.run(sql20, lambda res: {
            "class": 3,
            "data": [self.any_full, self.array_full, self.positionAsText],
            "text": T_("highway: `access={0}` - parking: `access={1}`", '/'.join(set(res[3])), res[4] if res[4] else '')
        })



###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis

class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_parking_highway.osm",
                                         config.dir_tmp + "/tests/osmosis_parking_highway.test.xml",
                                         {"proj": 2154}) # Random proj to satisfy highway table generation

    def test_classes(self):
        with Analyser_Osmosis_Parking_highway(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="1", elems=[("way", "101")])
        self.check_err(cl="2", elems=[("way", "100")], fixes=[{"+": {"parking": "street_side"}}])
        self.check_err(cl="2", elems=[("way", "124")], fixes=[])
        self.check_err(cl="2", elems=[("way", "125")], fixes=[])
        self.check_err(cl="3", elems=[("way", "103"), ("way", "102")])
        self.check_err(cl="3", elems=[("way", "118"), ("way", "119"), ("way", "120")])
        self.check_num_err(6)
