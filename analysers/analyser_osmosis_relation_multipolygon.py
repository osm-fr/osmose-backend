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

from modules.Stablehash import stablehash64
from modules.OsmoseTranslation import T_
from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE rel_poly AS
SELECT
    id,
    linestring,
    nodes
FROM
    ways
WHERE
    is_polygon AND
    tags != ''::hstore AND
    tags ?| ARRAY['landuse', 'aeroway', 'natural', 'water']
"""

sql11 = """
CREATE INDEX rel_poly_linestring_idx ON rel_poly USING gist(linestring)
"""

sql12 = """
SELECT DISTINCT
    relations.id,
    w1.id,
    w2.id,
    ST_AsText(ST_Centroid(ST_Envelope(w1.linestring)))
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role = 'inner'
    JOIN {1}ways AS w1 ON
        w1.id = relation_members.member_id AND
        w1.is_polygon AND
        w1.tags = ''::hstore
    JOIN {2}rel_poly AS w2 ON
        w1.id != w2.id AND
        w1.linestring && w2.linestring AND
        w1.nodes @> w2.nodes AND w1.nodes <@ w2.nodes -- check that both ways contain the same nodes
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon'
"""

sql20 = """
SELECT DISTINCT
    relations.id,
    ways.id,
    ST_AsText(way_locate(ways.linestring)),
    relations.tags->'landuse' rl,
    ways.tags->'landuse' wl,
    relations.tags->'natural' rn,
    ways.tags->'natural' wn,
    relations.tags->'waterway' rw,
    ways.tags->'waterway' ww,
    relations.tags->'building' rb,
    ways.tags->'building' wb,
    COALESCE(relations.tags->'landuse', relations.tags->'natural', relations.tags->'waterway', relations.tags->'building')
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_type = 'W' AND
        relation_members.member_role IN ('', 'outer')
    JOIN {1}ways AS ways ON
        ways.id = relation_members.member_id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'multipolygon' AND
    ways.tags != ''::hstore AND
    (
        (
            relations.tags?'landuse' AND
            ways.tags?'landuse' AND
            ways.tags->'landuse' != (relations.tags->'landuse')
        ) OR (
            relations.tags?'natural' AND
            relations.tags->'natural' IN ('bay', 'beach', 'fell', 'grassland', 'glacier', 'heath', 'mud', 'sand', 'scree', 'scrub', 'sinkhole', 'water', 'wetland', 'wood') AND
            ways.tags?'natural' AND
            ways.tags->'natural' IN ('bay', 'beach', 'fell', 'grassland', 'glacier', 'heath', 'mud', 'sand', 'scree', 'scrub', 'sinkhole', 'water', 'wetland', 'wood') AND
            ways.tags->'natural' != (relations.tags->'natural')
        ) OR (
            relations.tags?'waterway' AND
            relations.tags->'waterway' IN ('boatyard', 'dock', 'riverbank') AND
            ways.tags?'waterway' AND
            ways.tags->'waterway' IN ('boatyard', 'dock', 'riverbank') AND
            ways.tags->'waterway' != (relations.tags->'waterway')
        ) OR (
            relations.tags?'building' AND
            ways.tags?'building' AND
            ways.tags->'building' != (relations.tags->'building')
        )
    )
"""

sql30 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    string_agg(landuse, ',') AS landuse,
    string_agg("natural", ',') AS "natural",
    string_agg(waterway, ',') AS waterway,
    string_agg(building, ',') AS building
FROM
(
    SELECT
        relations.id,
        ways.tags->'landuse' AS landuse,
        ways.tags->'natural' AS "natural",
        ways.tags->'waterway' AS waterway,
        ways.tags->'building' AS building
    FROM
        relations
        JOIN relation_members ON
            relation_members.relation_id = relations.id AND
            relation_members.member_type = 'W' AND
            relation_members.member_role IN ('', 'outer')
        JOIN ways ON
            ways.id = relation_members.member_id
    WHERE
        relations.tags?'type' AND
        relations.tags->'type' = 'multipolygon' AND
        NOT relations.tags ?| ARRAY['landuse', 'natural', 'waterway', 'building'] AND
        ways.tags != ''::hstore AND
        ways.tags ?| ARRAY['landuse', 'natural', 'waterway', 'building']
    GROUP BY
        relations.id,
        ways.tags->'landuse',
        ways.tags->'natural',
        ways.tags->'waterway',
        ways.tags->'building'
) AS t
GROUP BY
    id
HAVING
    COUNT(*) > 1
"""

sql40 = """
SELECT
    ways.id,
    ST_AsText(way_locate(ways.linestring)),
    ways.tags->'area',
    ways.tags->'landuse',
    ways.tags->'natural',
    ways.tags->'waterway',
    ways.tags->'leisure',
    ways.tags->'amenity',
    ways.tags->'building',
    COALESCE(ways.tags->'area', ways.tags->'landuse', ways.tags->'natural', ways.tags->'waterway', ways.tags->'leisure', ways.tags->'amenity', ways.tags->'building')
FROM
    {0}ways AS ways
    LEFT JOIN relation_members ON
        relation_members.member_id = ways.id AND
        relation_members.member_type = 'W'
WHERE
    ways.tags != ''::hstore AND
    (
        (ways.tags?'area' AND ways.tags->'area' in ('yes', 'true')) OR
        ways.tags?'landuse' OR
        (ways.tags?'natural' AND ways.tags->'natural' in ('bare_rock', 'bay', 'beach', 'fell', 'glacier', 'grassland', 'heath', 'hot_spring', 'moor', 'mud', 'rock', 'sand', 'scree', 'scrub', 'shingle', 'sinkhole', 'stone', 'water', 'wetland', 'wood')) OR
        (ways.tags?'waterway' AND ways.tags->'waterway' in ('boatyard', 'dock', 'fuel', 'riverbank')) OR
        (ways.tags?'leisure' AND ways.tags->'leisure' in ('adult_gaming_centre', 'amusement_arcade', 'bandstand', 'beach_resort', 'bird_hide', 'common', 'dance', 'dog_park', 'firepit', 'fishing', 'fitness_centre', 'garden', 'golf_course', 'hackerspace', 'horse_riding', 'ice_rink', 'marina', 'miniature_golf', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'sports_centre', 'stadium', 'summer_camp', 'swimming_area', 'swimming_pool', 'water_park', 'wildlife_hide')) OR
        (ways.tags?'amenity' AND ways.tags->'amenity' in ('animal_boarding', 'animal_shelter', 'arts_centre', 'baby_hatch', 'bank', 'bar', 'bicycle_rental', 'bicycle_repair_station', 'biergarten', 'blood_donation', 'boat_sharing', 'brothel', 'bus_station', 'cafe', 'car_rental', 'car_sharing', 'car_wash', 'casino', 'cinema', 'clinic', 'college', 'community_centre', 'courthouse', 'coworking_space', 'crematorium', 'crypt', 'dentist', 'dive_centre', 'doctors', 'dojo', 'driving_school', 'embassy', 'fast_food', 'ferry_terminal', 'fire_station', 'firepit', 'food_court', 'fountain', 'fuel', 'gambling', 'game_feeding', 'grave_yard', 'gym', 'hospital', 'hunting_stand', 'ice_cream', 'internet_cafe', 'kindergarten', 'kneipp_water_cure', 'language_school', 'library', 'marketplace', 'motorcycle_parking', 'music_school', 'nightclub', 'nursing_home', 'parking', 'parking_space', 'pharmacy', 'place_of_worship', 'planetarium', 'police', 'post_office', 'prison', 'pub', 'public_bookcase', 'public_building', 'ranger_station', 'recycling', 'rescue_station', 'restaurant', 'sauna', 'school', 'shelter', 'shower', 'social_centre', 'social_facility', 'studio', 'swingerclub', 'taxi', 'theatre', 'toilets', 'townhall', 'university', 'veterinary', 'waste_transfer_station')) OR
        ways.tags?'building'
    ) AND
    ways.linestring IS NOT NULL AND
    NOT ways.is_polygon AND
    relation_members.member_id IS NULL AND
    -- Avoid confusing warnings for invalid polygons. Any closed way with >3 nodes that doesn't match
    -- is_polygon (with any of the tags above) must be an invalid polygon (which is checked elsewhere)
    -- Note: use array_length instead of ST_NPoints as the former includes nodes outside of the extract
    (NOT ST_IsClosed(ways.linestring) OR array_length(ways.nodes,1) = 3)
"""

class Analyser_Osmosis_Relation_Multipolygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = self.def_class(item = 1170, level = 3, tags = ['relation', 'fix:chair', 'geom'],
            title = T_('Double inner polygon'),
            detail = T_(
'''The geometry of the inner of the multipolygon is duplicated. One in
relation without tag and another with tags not part of the relation.'''),
            fix = T_(
'''Remove the ring without tag. Add in the relation the one with the tags
as `inner` role.'''))
        self.classs_change[2] = self.def_class(item = 1170, level = 2, tags = ['relation', 'fix:chair', 'multipolygon'],
            title = T_('Inconsistent multipolygon nature with members nature'),
            detail = T_(
'''Multipolygon defines a nature that is different from that specified in
the outers roles.'''))
        self.classs[3] = self.def_class(item = 1170, level = 2, tags = ['relation', 'fix:chair', 'multipolygon'],
            title = T_('Inconsistent multipolygon member nature'),
            detail = T_(
'''Multipolygon does not define nature, several found on the outer role
members.'''))
        self.classs_change[4] = self.def_class(item = 1170, level = 1, tags = ['relation', 'fix:chair', 'geom'],
            title = T_('Should be polygon, part of multipolygon or not having area tag'),
            detail = T_(
'''The nature of the way indicates that it is a surface, the way would be
a polygon or a part of a multipolygon as outer role.'''),
            fix = T_(
'''Close the way to make a polygon or add to a multipolygon.'''))

        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "subclass":stablehash64(res[11]), "data":[self.relation_full, self.way_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "{0}=({1},{2})".format(*k), filter(lambda k: k[1], (("landuse",res[3],res[4]), ("natural",res[5],res[6]), ("waterway",res[7],res[8]), ("building",res[9],res[10])))))}
        }
        self.callback30 = lambda res: {"class":3, "subclass":1, "data":[self.relation_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "{0}=({1})".format(*k), filter(lambda k: k[1], (("landuse",res[2]), ("natural",res[3]), ("waterway",res[4]), ("building",res[5])))))}
        }
        self.callback40 = lambda res: {"class":4, "subclass":stablehash64(res[9]), "data":[self.way_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "{0}={1}".format(*k), filter(lambda k: k[1], (("area",res[2]), ("landuse",res[3]), ("natural",res[4]), ("waterway",res[5]), ("leisure",res[6]), ("amenity",res[7]), ("building",res[8])))))}
        }

    def analyser_osmosis_common(self):
        self.run(sql30, self.callback30)

    def analyser_osmosis_full(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12.format("", "", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql40.format(""), self.callback40)

    def analyser_osmosis_diff(self):
        self.run(sql10)
        self.run(sql11)
        self.create_view_touched("rel_poly", "W")
        self.run(sql12.format("touched_", "", ""), self.callback10)
        self.run(sql12.format("not_touched_", "touched_", ""), self.callback10)
        self.run(sql12.format("not_touched_", "not_touched_", "touched_"), self.callback10)
        self.run(sql20.format("touched_", ""), self.callback20)
        self.run(sql20.format("not_touched_", "touched_"), self.callback20)
        self.run(sql40.format("touched_"), self.callback40)
