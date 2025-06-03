#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016, Noémie Lehuby 2021                  ##
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
  relation_members.member_role AS mrole,
  relation_members.sequence_id AS morder,
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
  relation_members.member_role AS mrole,
  relation_members.sequence_id AS morder,
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
SELECT
    relations.id,
    ST_AsText(relation_locate(relations.id))
FROM
    relations
    LEFT JOIN relation_members ON
        relation_members.member_id = relations.id AND
        relation_members.member_type = 'R'
    LEFT JOIN relations AS parent ON
        parent.id = relation_members.relation_id AND
        parent.tags->'type' = 'route_master'
WHERE
    relations.tags->'type' = 'route' AND
    (NOT relations.tags?'public_transport:version' OR relations.tags->'public_transport:version' != '1') AND
    relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
    relation_locate(relations.id) IS NOT NULL
GROUP BY
    relations.id
HAVING
    bool_and(parent.id IS NULL)
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
    highways.highway NOT IN ('footway', 'path', 'pedestrian', 'platform', 'steps')
GROUP BY
    nodes.id,
    nodes.geom
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
    node_id IS NULL;
"""

sql80 = """
SELECT
    relations.id,
    'N' || nodes.id,
    ST_AsText(nodes.geom) AS geom
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
    highways.highway NOT IN ('footway', 'path', 'pedestrian', 'platform', 'steps')
GROUP BY
    relations.id,
    nodes.id,
    nodes.geom
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
    node_id IS NULL
GROUP BY
    stop_platform.id,
    stop_platform.member_type,
    stop_platform.mid,
    stop_platform.geom
"""

sqlA0 = """
CREATE TEMP TABLE n_bs AS
SELECT
    geom
FROM
    nodes
WHERE
    tags != ''::hstore AND
    (
        (tags?'public_transport' AND tags->'public_transport' = 'platform') OR
        (tags?'highway' AND tags->'highway' = 'bus_stop')
    )
"""

sqlA1 = """
CREATE INDEX n_bs_idx_geom ON n_bs USING gist(geom)
"""

sqlA2 = """
CREATE TEMP TABLE w_bs AS
SELECT
    linestring
FROM
    ways
WHERE
    tags != ''::hstore AND
    (
        (tags?'public_transport' AND tags->'public_transport' = 'platform') OR
        (tags?'highway' AND tags->'highway' = 'bus_stop')
    )
"""

sqlA3 = """
CREATE INDEX w_bs_idx_geom ON w_bs USING gist(linestring)
"""

sqlA4 = """
SELECT
    sp.id,
    ST_AsText(sp.geom) AS geom
FROM
    nodes AS sp
    LEFT JOIN n_bs ON
        ST_Intersects(ST_Transform(ST_Buffer(ST_Transform(sp.geom, {0}), 100), 4326), n_bs.geom)
    LEFT JOIN w_bs ON
        ST_Intersects(ST_Transform(ST_Buffer(ST_Transform(sp.geom, {0}), 100), 4326), w_bs.linestring)
WHERE
    sp.tags != ''::hstore AND
    sp.tags?'public_transport' AND
    sp.tags->'public_transport' = 'stop_position' AND
    sp.tags?'bus' AND
    sp.tags->'bus' = 'yes' AND
    n_bs.geom IS NULL AND
    w_bs.linestring IS NULL
"""

sql100 = """
CREATE OR REPLACE FUNCTION generate_linestring_geom(route_id bigint) RETURNS geometry(MultiLineString, 4326) LANGUAGE PLPGSQL AS $$
DECLARE
   f record;
   full_way geometry(LineString, 4326);
   last_roundabout geometry(LineString, 4326);
BEGIN
    FOR f IN
        SELECT
            ways.id,
            ways.linestring AS geom
        FROM
            relations
            JOIN relation_members ON
                relation_members.relation_id = relations.id AND
                relation_members.member_type = 'W' AND
                relation_members.member_role NOT IN ('stop', 'stop_exit_only', 'stop_entry_only', 'platform', 'platform_exit_only', 'platform_entry_only')
            JOIN ways ON
                ways.id = relation_members.member_id AND
                ST_NPoints(linestring) >= 2
        WHERE
            relations.tags->'type' = 'route' AND
            relations.tags->'route' IN ('train', 'subway', 'monorail', 'tram', 'bus', 'trolleybus', 'aerialway', 'ferry', 'coach', 'funicular', 'share_taxi', 'light_rail', 'school_bus') AND
            (NOT relations.tags?(relations.tags->'route') OR relations.tags->(relations.tags->'route') != 'on_demand') AND
            relations.id = route_id
        ORDER BY
            relation_members.sequence_id
    LOOP
        CASE
            WHEN full_way IS NULL THEN
                full_way := f.geom;
            WHEN ST_EndPoint(f.geom) = ST_StartPoint(f.geom) THEN
                last_roundabout := f.geom;
            WHEN last_roundabout IS NOT NULL THEN
                CASE
                    WHEN ST_Intersects(last_roundabout,ST_StartPoint(f.geom)) THEN
                        CASE
                            WHEN ST_LineLocatePoint(last_roundabout, ST_EndPoint(full_way)) > ST_LineLocatePoint(last_roundabout, ST_StartPoint(f.geom)) THEN
                                full_way:= ST_MakeLine(full_way,ST_LineSubstring(last_roundabout, ST_LineLocatePoint(last_roundabout, ST_EndPoint(full_way)), 1));
                                full_way:= ST_MakeLine(full_way,ST_LineSubstring(last_roundabout, 0, ST_LineLocatePoint(last_roundabout, ST_StartPoint(f.geom))));
                            ELSE
                                full_way:= ST_MakeLine(full_way,ST_LineSubstring(last_roundabout, ST_LineLocatePoint(last_roundabout, ST_EndPoint(full_way)), ST_LineLocatePoint(last_roundabout, ST_StartPoint(f.geom))));
                        END CASE;
                        full_way:= ST_MakeLine(full_way,f.geom);
                    WHEN ST_Intersects(last_roundabout,ST_EndPoint(f.geom)) THEN
                        CASE
                            WHEN ST_LineLocatePoint(last_roundabout, ST_EndPoint(full_way)) > ST_LineLocatePoint(last_roundabout, ST_EndPoint(f.geom)) THEN
                                full_way:= ST_MakeLine(full_way,ST_LineSubstring(last_roundabout, ST_LineLocatePoint(last_roundabout, ST_EndPoint(full_way)), 1));
                                full_way:= ST_MakeLine(full_way,ST_LineSubstring(last_roundabout, 0, ST_LineLocatePoint(last_roundabout, ST_EndPoint(f.geom))));
                            ELSE
                                full_way:= ST_MakeLine(full_way,ST_LineSubstring(last_roundabout, ST_LineLocatePoint(last_roundabout, ST_EndPoint(full_way)), ST_LineLocatePoint(last_roundabout, ST_EndPoint(f.geom))));
                        END CASE;
                        full_way:= ST_MakeLine(full_way,ST_Reverse(f.geom));
                    ELSE
                        RETURN NULL;
                END CASE;
                last_roundabout = NULL;
            WHEN ST_EndPoint(full_way) = ST_StartPoint(f.geom) THEN
                full_way:= ST_MakeLine(full_way,f.geom);
            WHEN ST_EndPoint(full_way) = ST_EndPoint(f.geom) THEN
                full_way:= ST_MakeLine(full_way,ST_Reverse(f.geom));
            WHEN ST_StartPoint(full_way) = ST_EndPoint(f.geom) THEN
                full_way:= ST_MakeLine(ST_Reverse(full_way),ST_Reverse(f.geom));
            WHEN ST_StartPoint(full_way) = ST_StartPoint(f.geom) THEN
                full_way:= ST_MakeLine(ST_Reverse(full_way),f.geom);
            ELSE
                RETURN NULL;
        END CASE;
    END LOOP;
    RETURN full_way;
END;
$$;
"""

sql101 = """
CREATE TEMP TABLE route_linestring AS
SELECT
    id,
    relations.tags->'route' AS public_transport_mode,
    ST_Transform(generate_linestring_geom(id), {0}) AS geom
FROM
    relations
WHERE
    relations.tags->'type' = 'route' AND
    relations.tags->'route' IN (
        'train',
        'subway',
        'monorail',
        'tram',
        'bus',
        'trolleybus',
        'aerialway',
        'ferry',
        'coach',
        'funicular',
        'share_taxi',
        'light_rail',
        'school_bus'
    ) AND
    (
        NOT relations.tags?(relations.tags->'route')
        OR relations.tags->(relations.tags->'route') != 'on_demand'
    ) AND
    generate_linestring_geom(id) IS NOT NULL
"""

sql101b = """
CREATE INDEX route_linestring_idx ON route_linestring USING gist(geom)
"""

sql102 = """
CREATE TEMP TABLE platform_that_can_project AS (
SELECT
    route_linestring.id AS route_id,
    stop_platform.member_type || stop_platform.mid AS stop_id,
    stop_platform.geom AS stop,
    ROW_NUMBER () OVER (PARTITION BY route_linestring.id ORDER BY stop_platform.morder) AS stop_order,
    ROW_NUMBER () OVER (PARTITION BY route_linestring.id ORDER BY ST_LineLocatePoint(ST_OffsetCurve(route_linestring.geom, -10), stop_platform.geom) DESC) AS projected_stop_order,
    CASE
        WHEN LEAD(stop_platform.morder, 1) OVER (PARTITION BY route_linestring.id ORDER BY stop_platform.morder) IS NULL THEN 1
        ELSE 0
    END AS is_last_platform
FROM
    stop_platform
    JOIN route_linestring ON
        route_linestring.id = stop_platform.id
    WHERE
        stop_platform.mrole IN ('platform', 'platform_exit_only', 'platform_entry_only') AND
        stop_platform.member_type='N' AND
        GeometryType(ST_OffsetCurve(route_linestring.geom, -10)) = 'LINESTRING' AND
        ST_LineLocatePoint(route_linestring.geom, ST_ClosestPoint(route_linestring.geom, stop_platform.geom)) NOT IN (0, 1)
)
"""

sql102b = """
CREATE INDEX platform_that_can_project_idx ON platform_that_can_project USING gist(stop)
"""

sql103 = """
SELECT DISTINCT ON (route_id)
    platform_that_can_project.route_id,
    ST_AsText(ST_Transform(platform_that_can_project.stop,4326)) AS geom
FROM
    platform_that_can_project
WHERE
    stop_order != projected_stop_order
"""

sql110 = """
SELECT
  platform_that_can_project.route_id,
  platform_that_can_project.stop_id,
  ST_AsText(ST_Transform(platform_that_can_project.stop, 4326))
FROM
    platform_that_can_project
    JOIN route_linestring ON
        route_linestring.id = platform_that_can_project.route_id AND
        ST_DWithin(route_linestring.geom, platform_that_can_project.stop, 50) AND
        NOT ST_Intersects(ST_Buffer(route_linestring.geom, 50, 'side={}'), platform_that_can_project.stop) AND
        route_linestring.public_transport_mode IN ('bus', 'trolleybus', 'coach', 'share_taxi', 'school_bus')
WHERE
    platform_that_can_project.is_last_platform != 1 AND
    platform_that_can_project.stop_order != 1
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
        self.classs[10] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('Stop position without platform nor bus stop'),
            fix = T_('A bus `public_transport=stop_position` without close `public_transport=platform` nor `highway=bus_stop`.'))
        self.classs[11] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The stops may not be in the right order'))
        self.classs[12] = self.def_class(item = 1260, level = 3, tags = ['public_transport'],
            title = T_('The platform is not on the right side of the road'))

        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.positionAsText]}
        self.callback50 = lambda res: {"class":5,
             "text": T_("{0} are different", ", ".join(filter(lambda r: r, [res[3] and "network", res[4] and "operator", res[5] and "ref", res[6] and "colour"]))),
             "data": [self.relation_full, self.relation_full, self.positionAsText] }
        self.callback60 = lambda res: {"class":6, "data":[self.node_full, self.positionAsText]}
        self.callback70 = lambda res: {"class":7, "data":[self.node_full, self.positionAsText]}
        self.callback80 = lambda res: {"class":8, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callback90 = lambda res: {"class":9, "data":[self.relation_full, self.any_full, self.positionAsText]}
        self.callbackA0 = lambda res: {"class":10, "data":[self.node_full, self.positionAsText]}
        self.callback100 = lambda res: {"class":11, "data":[self.relation_full, self.positionAsText]}
        self.callback110 = lambda res: {"class":12, "data":[self.relation_full, self.any_full, self.positionAsText]}

        if self.config.options.get("driving_side") == "left":
            self.buffer_driving_side = "left"
        else:
            self.buffer_driving_side = "right"

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
        self.run(sqlA0)
        self.run(sqlA1)
        self.run(sqlA2)
        self.run(sqlA3)
        self.run(sqlA4.format(self.config.options.get("proj")), self.callbackA0)
        self.run(sql100)
        self.run(sql101.format(self.config.options.get("proj")))
        self.run(sql101b)
        self.run(sql102)
        self.run(sql102b)
        self.run(sql103, self.callback100)
        postgis_version = self.config.osmosis_manager.postgis_version()
        if postgis_version >= [2, 5]:
            self.run(sql110.format(self.buffer_driving_side), self.callback110)
