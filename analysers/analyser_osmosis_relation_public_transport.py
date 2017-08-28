#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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

sql00 = """
CREATE TEMP TABLE route AS
SELECT
  relations.id,
  relations.tags->'route' AS type,
  (ST_Dump(ST_LineMerge(ST_Collect(ways.linestring)))).geom AS geom
FROM
  relations
  JOIN relation_members ON
    relation_members.member_type = 'W' AND
    relation_members.relation_id = relations.id AND
    relation_members.member_role NOT IN ('stop', 'stop_exit_only', 'stop_entry_only', 'platform', 'platform_exit_only', 'platform_entry_only')
  JOIN ways ON
    ways.id = relation_members.member_id
WHERE
  relations.tags->'type' = 'route' AND
  relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
  (NOT relations.tags?(relations.tags->'route') OR relations.tags->(relations.tags->'route') != 'on_demand') AND
  ST_NPoints(linestring) >= 2
GROUP BY
  relations.id
"""

sql01 = """
CREATE INDEX route_geom_idx ON route USING gist(geom)
"""

sql10 = """
SELECT
  t.id,
  ST_AsText(relation_locate(t.id))
FROM (
  SELECT
    id,
    count(*) AS string
  FROM (
    WITH RECURSIVE t(id, list, geom) AS (
      SELECT
        *
      FROM (
        SELECT DISTINCT ON (id)
          id,
          ARRAY[ctid] AS list,
          geom
        FROM
          route
        ORDER BY
          id,
          ctid
      ) AS a
      UNION ALL
      SELECT
        *
      FROM (
        SELECT DISTINCT ON (t.id)
          t.id,
          t.list || route.ctid,
          ST_Union(t.geom, route.geom) AS geom
        FROM
          t
          JOIN route ON
            route.id = t.id AND
            NOT route.ctid = ANY (t.list) AND
            ST_Intersects(t.geom, route.geom)
        ORDER BY
          t.id
      ) AS e
    )
    SELECT
      distinct unnest(list),
      id
    FROM
      t
  ) AS t
  GROUP BY
    id
) AS t
  JOIN route ON
    route.id = t.id
GROUP BY
  t.id,
  t.string
HAVING
  string != count(*)
"""

sql20 = """
CREATE TEMP TABLE stop_platform AS
(
SELECT
  relations.id,
  relation_members.member_type,
  ways.id AS mid,
  ST_Transform(ways.linestring, {0}) AS geom
FROM
  relations
  JOIN route ON
    route.id = relations.id
  JOIN relation_members ON
    relation_members.member_type = 'W' AND
    relation_members.relation_id = relations.id AND
    relation_members.member_role IN ('stop', 'stop_exit_only', 'stop_entry_only', 'platform', 'platform_exit_only', 'platform_entry_only')
  JOIN ways ON
    ways.id = relation_members.member_id
WHERE
  relations.tags->'type' = 'route' AND
  relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
  (NOT relations.tags?(relations.tags->'route') OR relations.tags->(relations.tags->'route') != 'on_demand')
) UNION (
SELECT
  relations.id,
  relation_members.member_type,
  nodes.id AS mid,
  ST_Transform(nodes.geom, {0}) AS geom
FROM
  relations
  JOIN route ON
    route.id = relations.id
  JOIN relation_members ON
    relation_members.member_type = 'N' AND
    relation_members.relation_id = relations.id AND
    relation_members.member_role IN ('stop', 'stop_exit_only', 'stop_entry_only', 'platform', 'platform_exit_only', 'platform_entry_only')
  JOIN nodes ON
    nodes.id = relation_members.member_id
WHERE
  relations.tags->'type' = 'route' AND
  relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
 (NOT relations.tags?(relations.tags->'route') OR relations.tags->(relations.tags->'route') != 'on_demand')
)
"""

sql21 = """
CREATE TEMP TABLE route_geom AS
SELECT
  id,
  type,
  ST_Transform(ST_Collect(geom), {0}) AS geom
FROM
  route
GROUP BY
  id,
  type
"""

sql22 = """
SELECT
  stop_platform.id,
  stop_platform.member_type || stop_platform.mid,
  ST_AsText(any_locate(stop_platform.member_type, stop_platform.mid))
FROM
  stop_platform
  JOIN route_geom ON
    route_geom.id = stop_platform.id AND
    ST_Distance(route_geom.geom, stop_platform.geom) > 20
"""

sql30 = """
SELECT
  relations.id,
  relation_members.member_type || relation_members.member_id,
  ST_AsText(any_locate(relation_members.member_type, relation_members.member_id))
FROM
  {0}relations AS relations
  JOIN relation_members ON
    relation_members.relation_id = relations.id
  LEFT JOIN {1}relations AS m ON
    relation_members.member_type = 'R' AND
    m.id = relation_members.member_id AND
    m.tags->'type' != 'route'
WHERE
  relations.tags->'type' = 'route_master' AND
  (
    relation_members.member_type != 'R' OR
    m.id IS NOT NULL
  )
"""

sql40 = """
SELECT
    relations.id,
    ST_AsText(relation_locate(relations.id))
FROM
    relations
    LEFT JOIN relation_members ON
        relation_members.member_id = relations.id AND
        relation_members.member_type = 'R'
    LEFT JOIN relations AS parent ON
        parent.id = relation_members.relation_id
WHERE
    relations.tags->'type' = 'route' AND
    relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
    (relation_members.member_id IS NULL OR parent.tags->'type' != 'route_master')
"""

sql50 = """
SELECT
    parent.id,
    relation_members.member_type || relation_members.member_id,
    ST_AsText(relation_locate(relations.id)),
    CASE
        WHEN parent.tags->'network' != (relations.tags->'network') THEN 0
        WHEN parent.tags->'operator' != (relations.tags->'operator') THEN 1
        WHEN parent.tags->'ref' != (relations.tags->'ref') THEN 2
        WHEN parent.tags->'colour' != (relations.tags->'colour') THEN 3
    END
FROM
    {0}relations AS relations
    LEFT JOIN relation_members ON
        relation_members.member_id = relations.id AND
        relation_members.member_type = 'R'
    LEFT JOIN {1}relations AS parent ON
        parent.id = relation_members.relation_id
WHERE
    relations.tags->'type' = 'route' AND
    parent.tags->'type' = 'route_master' AND
    relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
    (
        parent.tags->'network' != (relations.tags->'network') OR
        parent.tags->'operator' != (relations.tags->'operator') OR
        parent.tags->'ref' != (relations.tags->'ref') OR
        parent.tags->'colour' != (relations.tags->'colour')
    )
"""

class Analyser_Osmosis_Relation_Public_Transport(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"The track of this route contains gaps") }
        self.classs[2] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"The stop or platform is too far from the track of this route") }
        self.classs_change[3] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"Non route relation member in route_master relation") }
        self.classs[4] = {"item": "1260", "level": 2, "tag": ["public_transport"], "desc": T_(u"Public transport relation route not in route_master relation") }
        self.classs_change[50] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"network tag should be the same on route and route_master relations") }
        self.classs_change[51] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"operator tag should be the same on route and route_master relations") }
        self.classs_change[52] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"ref tag should be the same on route and route_master relations") }
        self.classs_change[53] = {"item": "1260", "level": 3, "tag": ["public_transport"], "desc": T_(u"colour tag should be the same on route and route_master relations") }
        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":50 + res[3], "data":[self.relation_full, self.any_full, self.positionAsText]}

    def analyser_osmosis_common(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql10, self.callback10)
        self.run(sql20.format(self.config.options.get("proj")))
        self.run(sql21.format(self.config.options.get("proj")))
        self.run(sql22, self.callback20)

    def analyser_osmosis_full(self):
        self.run(sql30.format("", ""), self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50.format("", ""), self.callback50)

    def analyser_osmosis_diff(self):
        self.run(sql30.format("touched_", ""), self.callback10)
        self.run(sql30.format("not_touched_", "touched_"), self.callback10)
        self.run(sql50.format("touched_", ""), self.callback50)
        self.run(sql50.format("", "touched_"), self.callback50)
