#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Osmose Project 2026                                        ##
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

# Only list tags that make a network of POIs, i.e. that are likely to be mapped in the same area and thus to be duplicated.
# Avoid objects that cluster themselves, e.g. bus stops, or restaurants.
#
# WITH
# tag_nodes AS (
#     SELECT 'n' AS type, id,
#     coalesce(tags->'amenity', tags->'leisure', tags->'shop') AS tag,
#     ST_Transform(geom, 2154) AS geom
#     FROM nodes
#     WHERE
#         (tags ? 'amenity' AND tags->'amenity' IN ('pharmacy', 'restaurant', 'bank', 'bar', 'post_office', 'fire_station', 'hospital', 'place_of_worship', 'fuel', 'toilets', 'post_box', 'drinking_water', 'atm', 'clinic', 'community_centre', 'doctors', 'charging_station', 'townhall', 'police', 'library', 'marketplace')) OR
#         (tags ? 'leisure' AND tags->'leisure' IN ('stadium')) OR
#         (tags ? 'shop' AND tags->'shop' IN ('convenience', 'supermarket', 'bakery', 'mall'))
# ),
# tag_ways AS (
#     SELECT 'w' AS type, id,
#     coalesce(tags->'amenity', tags->'leisure', tags->'shop') AS tag,
#     ST_Transform(ST_Centroid(linestring), 2154) AS geom
#     FROM ways
#     WHERE
#         (tags ? 'amenity' AND tags->'amenity' IN ('pharmacy', 'restaurant', 'bank', 'bar', 'post_office', 'fire_station', 'hospital', 'place_of_worship', 'fuel', 'toilets', 'post_box', 'drinking_water', 'atm', 'clinic', 'community_centre', 'doctors', 'charging_station', 'townhall', 'police', 'library', 'marketplace')) OR
#         (tags ? 'leisure' AND tags->'leisure' IN ('stadium')) OR
#         (tags ? 'shop' AND tags->'shop' IN ('convenience', 'supermarket', 'bakery', 'mall'))
# ),
# all_points AS (
#     SELECT type, id, tag, geom FROM tag_nodes
#     UNION ALL
#     SELECT type, id, tag, geom FROM tag_ways
# ),
# delaunay_edges AS (
#     SELECT
#         tag,
#         ST_Length(
#             (ST_Dump(ST_DelaunayTriangles(ST_Collect(geom), 0, 1))).geom
#         ) AS seg_length
#     FROM all_points
#     GROUP BY tag
# )
# SELECT
#     tag,
#     COUNT(*) AS nb_total,
#     COUNT(*) FILTER (WHERE seg_length < 2000) AS nb_2000,
#     COUNT(*) FILTER (WHERE seg_length < 1000) AS nb_1000,
#     COUNT(*) FILTER (WHERE seg_length < 200) AS nb_200,
#     COUNT(*) FILTER (WHERE seg_length < 100) AS nb_100,
#     ROUND(100.0 * COUNT(*) FILTER (WHERE seg_length < 2000) / COUNT(*), 1) AS pct_2000,
#     ROUND(100.0 * COUNT(*) FILTER (WHERE seg_length < 1000) / COUNT(*), 1) AS pct_1000,
#     ROUND(100.0 * COUNT(*) FILTER (WHERE seg_length < 200)  / COUNT(*), 1) AS pct_200,
#     ROUND(100.0 * COUNT(*) FILTER (WHERE seg_length < 100)  / COUNT(*), 1) AS pct_100
# FROM delaunay_edges
# GROUP BY tag
# ORDER BY pct_200 DESC;

#        tag        | nb_total | nb_2000 | nb_1000 | nb_200 | nb_100 | pct_2000 | pct_1000 | pct_200 | pct_100
# ------------------+----------+---------+---------+--------+--------+----------+----------+---------+---------
#  restaurant       |   291340 |  219734 |  194190 | 124521 |  84099 |     75.4 |     66.7 |    42.7 |    28.9
#  bank             |    61284 |   37326 |   31527 |  18300 |  10508 |     60.9 |     51.4 |    29.9 |    17.1
#  bar              |    64310 |   36686 |   31940 |  16960 |   9544 |     57.0 |     49.7 |    26.4 |    14.8
#  atm              |    29634 |   14612 |   11184 |   4963 |   2794 |     49.3 |     37.7 |    16.7 |     9.4
#  doctors          |    39203 |   20379 |   15906 |   6154 |   4051 |     52.0 |     40.6 |    15.7 |    10.3
#  convenience      |    68812 |   36505 |   29773 |  10822 |   4903 |     53.1 |     43.3 |    15.7 |     7.1
#  drinking_water   |    78819 |   38563 |   29822 |  10734 |   5330 |     48.9 |     37.8 |    13.6 |     6.8
#  charging_station |    61751 |   30344 |   21519 |   7327 |   5317 |     49.1 |     34.8 |    11.9 |     8.6
#  toilets          |   108466 |   51172 |   38777 |  12162 |   6297 |     47.2 |     35.8 |    11.2 |     5.8
#  bakery           |    90376 |   47048 |   35376 |   9704 |   3956 |     52.1 |     39.1 |    10.7 |     4.4
#  supermarket      |    51081 |   25277 |   16100 |   3239 |   1312 |     49.5 |     31.5 |     6.3 |     2.6
#  clinic           |     6250 |    1727 |    1070 |    363 |    234 |     27.6 |     17.1 |     5.8 |     3.7
#  pharmacy         |    60875 |   30933 |   22092 |   3422 |   1003 |     50.8 |     36.3 |     5.6 |     1.6
#  community_centre |    67609 |   19217 |   11919 |   3736 |   2290 |     28.4 |     17.6 |     5.5 |     3.4
#  hospital         |     7731 |    1751 |    1044 |    346 |    204 |     22.6 |     13.5 |     4.5 |     2.6
#  fast_food        |      402 |      44 |      33 |     17 |      9 |     10.9 |      8.2 |     4.2 |     2.2
#  mall             |     4546 |     963 |     587 |    190 |    110 |     21.2 |     12.9 |     4.2 |     2.4
#  post_box         |   158209 |   84874 |   61663 |   6298 |   1353 |     53.6 |     39.0 |     4.0 |     0.9
#  marketplace      |    12115 |    2658 |    1360 |    463 |    316 |     21.9 |     11.2 |     3.8 |     2.6
#  fuel             |    39384 |   10618 |    5000 |   1081 |    660 |     27.0 |     12.7 |     2.7 |     1.7
#  place_of_worship |   186527 |   54368 |   25349 |   4175 |   1754 |     29.1 |     13.6 |     2.2 |     0.9
#  library          |    26988 |    4359 |    2120 |    533 |    337 |     16.2 |      7.9 |     2.0 |     1.2
#  police           |    19083 |    2842 |    1484 |    291 |    195 |     14.9 |      7.8 |     1.5 |     1.0
#  stadium          |     2343 |     148 |      83 |     27 |      9 |      6.3 |      3.5 |     1.2 |     0.4
#  post_office      |    54403 |    7760 |    3084 |    572 |    332 |     14.3 |      5.7 |     1.1 |     0.6
#  cafe             |      586 |      36 |      23 |      5 |      3 |      6.1 |      3.9 |     0.9 |     0.5
#  fire_station     |    19197 |     478 |     166 |     91 |     80 |      2.5 |      0.9 |     0.5 |     0.4
#  townhall         |   112972 |   11998 |    1471 |    243 |    179 |     10.6 |      1.3 |     0.2 |     0.2
# (37 rows)

sql00 = """
CREATE TEMP TABLE pois AS
WITH
objects AS (
    SELECT
        'N' AS type,
        id,
        geom,
        tags
    FROM
        nodes
    UNION ALL
    SELECT
        'W' AS type,
        id,
        ST_PointOnSurface(CASE WHEN is_polygon THEN ST_MakePolygon(linestring) ELSE linestring END) AS geom,
        tags
    FROM
        ways
),
poi_raw AS (
    SELECT
        type,
        id,
        geom,
        tags->'level' AS level,
        'amenity'::text AS poi_key,
        tags->'amenity' AS poi_value
    FROM
        objects
    WHERE
        tags != ''::hstore AND
        tags?'amenity' AND
        NOT (tags->'amenity' = 'post_office' AND tags->'post_office' = 'post_partner')

    UNION ALL

    SELECT
        type,
        id,
        geom,
        tags->'level' AS level,
        'leisure'::text AS poi_key,
        tags->'leisure' AS poi_value
    FROM
        objects
    WHERE
        tags != ''::hstore AND
        tags?'leisure'

    UNION ALL

    SELECT
        type,
        id,
        geom,
        tags->'level' AS level,
        'shop'::text AS poi_key,
        tags->'shop' AS poi_value
    FROM
        objects
    WHERE
        tags != ''::hstore AND
        tags?'shop'
),
a AS (
    SELECT
        type,
        id,
        geom,
        ST_Transform(geom, {proj}) AS geom_proj,
        level,
        poi_key,
        poi_value,
        CASE poi_value
            WHEN 'pharmacy' THEN 1
            WHEN 'post_office' THEN 2
            WHEN 'fire_station' THEN 3
            WHEN 'hospital' THEN 4
            WHEN 'fuel' THEN 5
            WHEN 'clinic' THEN 6
            WHEN 'community_centre' THEN 7
            WHEN 'townhall' THEN 8
            WHEN 'police' THEN 9
            WHEN 'library' THEN 10
            WHEN 'marketplace' THEN 11
            WHEN 'stadium' THEN 12
            WHEN 'mall' THEN 13
            WHEN 'supermarket' THEN 14
        END AS class,
        CASE poi_value
            WHEN 'pharmacy' THEN 50
            WHEN 'post_office' THEN 200
            WHEN 'fire_station' THEN 200
            WHEN 'hospital' THEN 100
            WHEN 'fuel' THEN 25
            WHEN 'clinic' THEN 100
            WHEN 'community_centre' THEN 100
            WHEN 'townhall' THEN 200
            WHEN 'police' THEN 200
            WHEN 'library' THEN 200
            WHEN 'marketplace' THEN 200
            WHEN 'stadium' THEN 200
            WHEN 'mall' THEN 100
            WHEN 'supermarket' THEN 25
        END AS distance_m
    FROM
        poi_raw
)
SELECT
    *
FROM
    a
WHERE
    class IS NOT NULL
"""

sql01 = """
CREATE INDEX pois_idx_geom_proj ON pois USING gist(geom_proj)
"""

sql10 = """
SELECT DISTINCT ON (n1.type, n1.id)
    n1.type || n1.id AS src_id,
    n2.type || n2.id AS dst_id,
    ST_AsText(n1.geom),
    n1.poi_key,
    n1.poi_value,
    n1.level,
    ST_Distance(n1.geom_proj, n2.geom_proj) AS dist_m
FROM
    pois AS n1
    JOIN pois AS n2 ON
        (n2.type, n2.id) < (n1.type, n1.id) AND
        n2.poi_key = n1.poi_key AND
        n2.poi_value = n1.poi_value AND
        n1.level IS NOT DISTINCT FROM n2.level AND
        ST_DWithin(n1.geom_proj, n2.geom_proj, n1.distance_m)
ORDER BY
    n1.type,
    n1.id,
    ST_Distance(n1.geom_proj, n2.geom_proj)
"""


class Analyser_Osmosis_Duplicated_Poi(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[6] = self.def_class(item = 1230, level = 2, tags = ['geom', 'fix:chair', 'poi'],
            title = T_('Duplicated POI within a short distance'),
            detail = T_('Two POI with the same type are mapped very close to each other. This often indicates a duplicate object.'),
            fix = T_('Keep one object and merge tags of the other one into it.'))

        self.callback10 = lambda res: {
            "class": 6,
            "data": [self.any_full, self.any_full, self.positionAsText],
            "text": {"en": f"{res[3]}={res[4]}{' level=' + res[5] if res[5] else ''} (distance={res[6]:.1f}m)"}
        }

    def analyser_osmosis_common(self):
        self.run(sql00.format(proj=self.config.options.get("proj")))
        self.run(sql01)
        self.run(sql10, self.callback10)


###########################################################################

from .Analyser_Osmosis import TestAnalyserOsmosis


class Test(TestAnalyserOsmosis):
    @classmethod
    def setup_class(cls):
        from modules import config
        TestAnalyserOsmosis.setup_class()
        cls.analyser_conf = cls.load_osm("tests/osmosis_duplicated_poi.osm",
                                         config.dir_tmp + "/tests/osmosis_duplicated_poi.test.xml",
                                         {"proj": 23032})

    def test_classes(self):
        with Analyser_Osmosis_Duplicated_Poi(self.analyser_conf, self.logger) as a:
            a.analyser()

        self.root_err = self.load_errors()
        self.check_err(cl="6", elems=[("node", "1"), ("node", "2")])
        self.check_err(cl="6", elems=[("node", "5"), ("node", "6")])
        self.check_err(cl="6", elems=[("node", "20"), ("way", "20")])
        self.check_num_err(3)
