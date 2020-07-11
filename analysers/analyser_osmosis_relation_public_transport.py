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

from .Analyser_Osmosis import Analyser_Osmosis

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
  relations.id,
  relations.tags
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
  relation_locate(t.id) IS NOT NULL AND
  string != count(*)
"""

sql20 = """
CREATE TEMP TABLE stop_platform AS
(
SELECT DISTINCT ON (relations.id, ways.id)
  relations.id,
  relation_members.member_type,
  ways.id AS mid,
  relation_members.member_role as mrole,
  ST_Transform(ways.linestring, {0}) AS geom
FROM
  relations
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
ORDER BY
  relations.id,
  ways.id
) UNION ALL (
SELECT DISTINCT ON (relations.id, nodes.id)
  relations.id,
  relation_members.member_type,
  nodes.id AS mid,
  relation_members.member_role as mrole,
  ST_Transform(nodes.geom, {0}) AS geom
FROM
  relations
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
ORDER BY
  relations.id,
  nodes.id
)
"""

sql20b = """
CREATE INDEX indx_stop_platform_geom ON stop_platform USING gist(geom)
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
    ST_DWithin(route_geom.geom, stop_platform.geom, 1000) AND
    ST_Distance(route_geom.geom, stop_platform.geom) BETWEEN 50 AND 1000
"""

sql30 = """
SELECT DISTINCT ON(relations.id, relation_members.member_type || relation_members.member_id)
  relations.id,
  relation_members.member_type || relation_members.member_id,
  ST_AsText(coalesce(
    any_locate(relation_members.member_type, relation_members.member_id),
    relation_locate(relations.id)
  ))
FROM
  relations
  JOIN relation_members ON
    relation_members.relation_id = relations.id
  LEFT JOIN relations AS m ON
    relation_members.member_type = 'R' AND
    m.id = relation_members.member_id AND
    m.tags->'type' != 'route'
WHERE
  relations.tags->'type' = 'route_master' AND
  (
    (relation_members.member_type != 'R' AND any_locate(relation_members.member_type, relation_members.member_id) IS NOT NULL) OR
    (m.id IS NOT NULL AND relation_locate(relations.id) IS NOT NULL)
  )
"""

sql40 = """
SELECT DISTINCT ON(relations.id)
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
    (relation_members.member_id IS NULL OR parent.tags->'type' != 'route_master') AND
    relation_locate(relations.id) IS NOT NULL
"""

sql50 = """
SELECT DISTINCT ON (parent.id, relation_members.member_id)
    parent.id,
    relation_members.member_id,
    ST_AsText(relation_locate(relations.id)),
    parent.tags->'network' != (relations.tags->'network'),
    parent.tags->'operator' != (relations.tags->'operator'),
    parent.tags->'ref' != (relations.tags->'ref'),
    parent.tags->'colour' != (relations.tags->'colour')
FROM
    relations
    LEFT JOIN relation_members ON
        relation_members.member_id = relations.id AND
        relation_members.member_type = 'R'
    LEFT JOIN relations AS parent ON
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

sql60 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom) AS geom
FROM
    nodes
    JOIN way_nodes ON
        nodes.id = way_nodes.node_id
    JOIN highways ON
    way_nodes.way_id = highways.id
WHERE
    nodes.tags != ''::hstore AND
    nodes.tags?'highway' AND nodes.tags->'highway' = 'bus_stop' AND
    nodes.tags->'public_transport' != 'stop_position' AND
    highways.highway NOT IN ('footway', 'platform')
"""

sql70 = """
SELECT
    nodes.id,
    ST_AsText(nodes.geom) AS geom
FROM
    nodes
    LEFT JOIN way_nodes ON
        nodes.id = way_nodes.node_id
WHERE nodes.tags != ''::hstore AND
    nodes.tags?'public_transport' AND
    nodes.tags->'public_transport' = 'stop_position' AND
    node_id is null;
"""

sql80 = """
SELECT
    relations.id,
    'N' || nodes.id,
    ST_AsText(nodes.geom) AS geom,
    way_nodes.way_id
FROM
    way_nodes
    JOIN relation_members ON
        relation_members.member_type = 'N' AND
        relation_members.member_id = node_id AND
        relation_members.member_role NOT IN ('stop', 'stop_exit_only', 'stop_entry_only')
    JOIN relations ON
        relation_members.relation_id = relations.id
    JOIN highways ON
        way_nodes.way_id = highways.id
    JOIN nodes ON
        nodes.id = way_nodes.node_id
WHERE
  relations.tags->'type' = 'route' AND
  relations.tags->'route' IN ('bus', 'trolleybus', 'coach', 'share_taxi', 'school_bus', 'walking_bus') AND
  highways.highway NOT IN ('footway', 'platform')
"""

sql90 = """
SELECT
    stop_platform.id,
    stop_platform.member_type || stop_platform.mid,
    ST_AsText(stop_platform.geom) AS geom
FROM
  stop_platform
  JOIN relations ON
      stop_platform.id = relations.id
  LEFT JOIN way_nodes ON
      mid = node_id
WHERE
    mrole IN ('stop', 'stop_exit_only', 'stop_entry_only') AND
    relations.tags->'public_transport:version' = '2' AND
    node_id IS NULL;
"""

class Analyser_Osmosis_Relation_Public_Transport(Analyser_Osmosis):
    requires_tables_common = ['highways']

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The track of this route contains gaps'))
        self.classs[2] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The stop or platform is too far from the track of this route'))
        self.classs[3] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('Non route relation member in route_master relation'))
        self.classs[4] = self.def_class(item = 1260, level = 2, tags = ['public_transport'],
            title = T_('Public transport relation route not in route_master relation'))
        self.classs[5] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('network, operator, ref, colour tag should be the same on route and route_master relations'))
        self.classs[6] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The bus stop is part of a way, it should have public_transport=stop_position tag'))
        self.classs[7] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The stop_position is not part of a way'))
        self.classs[8] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The platform is part of a way, it should have the role stop'))
        self.classs[9] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The stop is not part of a way'),
            fix = T_('Change the role in the relation to platform or add the stop to the way and turn it to a public_transport=stop_position'))

        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":5,
             "text": T_("%s are different", ", ".join(filter(lambda r: r, [res[3] and "network", res[4] and "operator", res[5] and "ref", res[6] and "colour"]))),
             "data": [self.relation_full, self.relation_full, self.positionAsText] }
        self.callback60 = lambda res: {"class":6, "data":[self.node_full, self.positionAsText]}
        self.callback70 = lambda res: {"class":7, "data":[self.node_full, self.positionAsText]}
        self.callback80 = lambda res: {"class":8, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback90 = lambda res: {"class":9, "data":[self.relation_full, self.any_full, self.positionAsText]}


    def analyser_osmosis_common(self):
        self.run(sql00)
        self.run(sql01)
        self.run(sql10, self.callback10)
        self.run(sql20.format(self.config.options.get("proj")))
        self.run(sql20b)
        self.run(sql21.format(self.config.options.get("proj")))
        self.run(sql22, self.callback20)
        self.run(sql30, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50, self.callback50)
        self.run(sql60, self.callback60)
        self.run(sql70, self.callback70)
        self.run(sql80, self.callback80)
        self.run(sql90, self.callback90)
