#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
from modules.Stablehash import stablehash64
from .Analyser_Osmosis import Analyser_Osmosis
from modules.downloader import urlread
import json

sql10 = """
CREATE TEMP TABLE rtag_{type} AS
SELECT
    key,
    SUM(count) AS count
FROM
    (
    SELECT
        key,
        count
    FROM
        (
        SELECT
            split_part((each(tags)).key, ':', 1) AS key,
            COUNT(*) AS count
        FROM
            {type}
        WHERE
            tags != ''::hstore
        GROUP BY
            key
        ) AS keys
    WHERE
        length(key) > {keylen} AND
        key NOT IN (
            -- Regional keys (imports and such)
            'dcgis', -- vs dc-gis (Columbia, USA)
            'fdot', -- vs foot (Florida, USA)
            'kern', -- vs kerb (California, USA)
            'linz', -- vs line (New Zealand)
            'traces', -- vs tracks (Hungary)
            -- Documented keys without their own key:* wiki page. Between () where it's documented
            'levels', -- vs level (listed as deprecated on building:levels)
            -- Undocumented keys, not found in Wiki
            'clock', -- vs lock
            'hall', -- vs wall
            'mail', -- vs email (#702)
            'plane', -- vs place, plant, lane
            'rock', -- vs lock, dock, rack (from: MapComplete)
            'sale', -- vs salt, male (from: JOSM)
            'services', -- vs service (from: JOSM)
            'start', -- vs stairs, stars
            'weight', -- vs height
            'well' -- vs wall
        ) AND
        NOT key LIKE 'AND_%' AND -- Dutch AND import tags
        NOT key LIKE 'expected_%n_route_relations' AND -- Node networks, not all tags have wiki pages
        NOT key SIMILAR TO '%[1-9]' -- ignore name_1, addr2, etc
    ) AS keys
GROUP BY
    key
"""

sql20 = """
CREATE TEMP TABLE fix_{type} AS
SELECT DISTINCT ON (t1.key)
    t1.key as low_key,
    t2.key as hight_key
FROM
    rtag_{type} AS t1,
    rtag_{type} AS t2
WHERE
    t1.count < t2.count / 20 AND
    t1.key NOT IN ({wikikeys}) AND
    abs(length(t1.key) - length(t2.key)) <= 1 AND
    levenshtein(t1.key, t2.key) <= 1
ORDER BY
    t1.key,
    t2.count DESC
"""

sql30 = """
SELECT
    id,
    key,
    value,
    low_key,
    hight_key,
    ST_AsText({as_text})
FROM
    (
    SELECT
        id,
        (each(tags)).key AS key,
        (each(tags)).value AS value,
        {geo}
    FROM
        {table}
    GROUP BY
        id,
        key,
        value,
        {geo}
    ) AS keys,
    fix_{type} As fix
WHERE
    keys.key = fix.low_key OR
    (POSITION(':' IN keys.key) > 0 AND SUBSTRING(keys.key FROM 1 FOR LENGTH(fix.low_key)+1) = fix.low_key || ':')
"""

class Analyser_Osmosis_Tag_Typo(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 3150, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Typo in tag'),
            detail = T_(
'''The tag is misspelled. Detection is based on statistics.'''),
            trap = T_(
'''Check that the correction does not change the intent of the tag.'''),
            resource = "https://taginfo.openstreetmap.org/")

        self.minKeyLength = 3
        self.keysWithWiki = "'" + "','".join(self.get_keys_wiki_taginfo()) + "'"


    def get_keys_wiki_taginfo(self):
        # See https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_keys_wiki_pages
        # TagInfo has a JSON file with all keys with wiki pages
        taginfo_url = "https://taginfo.openstreetmap.org/api/4/keys/wiki_pages"
        json_str = urlread(taginfo_url, 30)
        json_entrylist = json.loads(json_str)['data']
        keyset = set(map(lambda x: x['key'].split(':', 1)[0], json_entrylist)) # Get all (unique) keys, discard :suffixes
        return list(filter(lambda x: len(x) > self.minKeyLength, keyset)) # Ignore small keys / wildcards


    def analyser_osmosis_common(self):
        self.run(sql10.format(type="nodes", keylen=self.minKeyLength))
        self.run(sql20.format(type="nodes", wikikeys=self.keysWithWiki))
        self.run(sql30.format(type="nodes", as_text="geom", table="nodes", geo="geom"), lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.node_full, None, None, None, None, self.positionAsText],
            "text": T_("`{0}` is more common than `{1}`, is `{1}` a typo?", res[1].replace(res[3], res[4], 1), res[1]),
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10.format(type="ways", keylen=self.minKeyLength))
        self.run(sql20.format(type="ways", wikikeys=self.keysWithWiki))
        self.run(sql30.format(type="ways", as_text="way_locate(linestring)", table="ways", geo="linestring"), lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.way_full, None, None, None, None, self.positionAsText],
            "text": T_("`{0}` is more common than `{1}`, is `{1}` a typo?", res[1].replace(res[3], res[4], 1), res[1]),
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })

        self.run(sql10.format(type="relations", keylen=self.minKeyLength))
        self.run(sql20.format(type="relations", wikikeys=self.keysWithWiki))
        self.run(sql30.format(type="relations", as_text="relation_locate(id)", table="relations", geo="user"), lambda res: {
            "class":1,
            "subclass": stablehash64(res[1]),
            "data":[self.relation_full, None, None, None, None, self.positionAsText],
            "text": T_("`{0}` is more common than `{1}`, is `{1}` a typo?", res[1].replace(res[3], res[4], 1), res[1]),
            "fix":{"-": [res[1]], "+": {res[1].replace(res[3], res[4], 1): res[2] }} })
