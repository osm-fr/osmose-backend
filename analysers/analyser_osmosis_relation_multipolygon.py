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

from modules.Stablehash import stablehash
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

sql11= """
CREATE INDEX rel_poly_linestring_idx ON rel_poly USING gist(linestring)
"""

sql12 = """
SELECT
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
SELECT
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
        (ways.tags?'natural' AND ways.tags->'natural' in ('wood', 'scrub', 'heath', 'moor', 'grassland', 'fell', 'bare_rock', 'scree', 'shingle', 'sand', 'mud', 'water', 'wetland', 'glacier', 'bay', 'beach', 'hot_spring', 'rock', 'stone', 'sinkhole')) OR
        (ways.tags?'waterway' AND ways.tags->'waterway' in ('boatyard', 'dock', 'riverbank', 'fuel')) OR
        (ways.tags?'leisure' AND ways.tags->'leisure' in ('adult_gaming_centre', 'amusement_arcade', 'beach_resort', 'bandstand', 'bird_hide', 'common', 'dance', 'dog_park', 'firepit', 'fishing', 'fitness_centre', 'garden', 'golf_course', 'hackerspace', 'horse_riding', 'ice_rink', 'marina', 'miniature_golf', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'sports_centre', 'stadium', 'summer_camp', 'swimming_area', 'swimming_pool', 'water_park', 'wildlife_hide', 'user', 'defined')) OR
        (ways.tags?'amenity' AND ways.tags->'amenity' in ('bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant', 'college', 'kindergarten', 'library', 'public_bookcase', 'school', 'music_school', 'driving_school', 'language_school', 'university', 'bicycle_repair_station', 'bicycle_rental', 'boat_sharing', 'bus_station', 'car_rental', 'car_sharing', 'car_wash', 'ferry_terminal', 'fuel', 'motorcycle_parking', 'parking', 'parking_space', 'taxi', 'bank', 'baby_hatch', 'clinic', 'dentist', 'doctors', 'hospital', 'nursing_home', 'pharmacy', 'social_facility', 'veterinary', 'blood_donation', 'arts_centre', 'brothel', 'casino', 'cinema', 'community_centre', 'fountain', 'gambling', 'nightclub', 'planetarium', 'social_centre', 'studio', 'swingerclub', 'theatre', 'animal_boarding', 'animal_shelter', 'courthouse', 'coworking_space', 'crematorium', 'crypt', 'dive_centre', 'dojo', 'embassy', 'fire_station', 'firepit', 'game_feeding', 'grave_yard', 'gym', 'hunting_stand', 'internet_cafe', 'kneipp_water_cure', 'marketplace', 'place_of_worship', 'police', 'post_office', 'prison', 'public_building', 'ranger_station', 'recycling', 'rescue_station', 'sauna', 'shelter', 'shower', 'toilets', 'townhall', 'waste_transfer_station')) OR
        ways.tags?'building'
    ) AND
    ways.linestring IS NOT NULL AND
    NOT ways.is_polygon AND
    relation_members.member_id IS NULL
"""

class Analyser_Osmosis_Relation_Multipolygon(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"1170", "level": 3, "tag": ["relation", "geom", "fix:chair"], "desc": T_(u"Double inner polygon") }
        self.classs_change[2] = {"item":"1170", "level": 2, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"Inconsistant multipolygon nature with members nature") }
        self.classs_change[3] = {"item":"1170", "level": 2, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"Inconsistant multipolygon member nature") }
        self.classs_change[4] = {"item":"1170", "level": 1, "tag": ["relation", "geom", "fix:chair"], "desc": T_(u"Should be polygon, part of multipolygon or not having area tag") }
        self.callback10 = lambda res: {"class":1, "data":[self.way_full, self.way_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "subclass":stablehash(res[11]), "data":[self.relation_full, self.way_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "%s=(%s,%s)"%k, filter(lambda k: k[1], (("landuse",res[3],res[4]), ("natural",res[5],res[6]), ("waterway",res[7],res[8]), ("building",res[9],res[10])))))}
        }
        self.callback30 = lambda res: {"class":3, "subclass":1, "data":[self.relation_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "%s=(%s)"%k, filter(lambda k: k[1], (("landuse",res[2]), ("natural",res[3]), ("waterway",res[4]), ("building",res[5])))))}
        }
        self.callback40 = lambda res: {"class":4, "subclass":stablehash(res[9]), "data":[self.way_full, self.positionAsText],
            "text": {"en": u", ".join(map(lambda k: "%s=%s"%k, filter(lambda k: k[1], (("area",res[2]), ("landuse",res[3]), ("natural",res[4]), ("waterway",res[5]), ("leisure",res[6]), ("amenity",res[7]), ("building",res[8])))))}
        }

    def analyser_osmosis_full(self):
        self.run(sql10)
        self.run(sql11)
        self.run(sql12.format("", "", ""), self.callback10)
        self.run(sql20.format("", ""), self.callback20)
        self.run(sql30.format("", ""), self.callback30)
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
        self.run(sql30.format("touched_", ""), self.callback30)
        self.run(sql30.format("not_touched_", "touched_"), self.callback30)
        self.run(sql40.format("touched_"), self.callback40)
