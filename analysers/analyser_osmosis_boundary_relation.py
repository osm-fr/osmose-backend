#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013-2015                                 ##
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
CREATE TEMP TABLE {0}_{1}_admin AS
SELECT
    relations.id,
    (relation_members.member_role IS NOT NULL) AS has_admin_centre,
    relations.tags AS rtags,
    nodes.tags AS ntags,
    ways.tags AS wtags
FROM
    {0}relations AS relations
    LEFT JOIN relation_members ON
        relations.id = relation_members.relation_id AND
        relation_members.member_role = 'admin_centre'
    LEFT JOIN {1}nodes AS nodes ON
        relation_members.member_type = 'N' AND
        relation_members.member_id = nodes.id
    LEFT JOIN {1}ways AS ways ON
        relation_members.member_type = 'W' AND
        relation_members.member_id = ways.id
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'boundary' AND
    relations.tags?'boundary' AND
    relations.tags->'boundary' = 'administrative' AND
    relations.tags?'admin_level' AND
    relations.tags->'admin_level' = '{2}'
"""

sql10 = """
SELECT
    id,
    ST_AsText(relation_locate(id))
FROM
    {0}_{1}_admin
WHERE
    NOT has_admin_centre
"""

sql20 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    {2}
FROM
    {0}_{1}_admin
WHERE
    {3}
"""

sql50 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    coalesce(ntags->'population', wtags->'population'),
    rtags->'population' AS population
FROM
    {0}_{1}_admin
WHERE
    rtags?'population' AND
    regexp_replace(coalesce(ntags->'population', wtags->'population'), '([0-9]{{0,9}}).*', '0\\1')::int >
    regexp_replace(rtags->'population', '([0-9]{{0,9}}).*', '0\\1')::int
"""

sql60 = """
SELECT
    relations.id,
    ST_AsText(relation_locate(relations.id)),
    coalesce(relations.tags->'name', relation_members.member_role),
    relations.tags->'admin_level',
    relation_members.member_role,
    relation_members.member_type
FROM
    {0}relations AS relations
    JOIN relation_members ON
        relation_members.relation_id = relations.id AND
        relation_members.member_role NOT IN ('', 'admin_centre', 'label', 'inner', 'outer', 'subarea', 'land_area')
WHERE
    relations.tags?'type' AND
    relations.tags->'type' = 'boundary' AND
    relations.tags?'boundary' AND
    relations.tags->'boundary' = 'administrative'
"""

class Analyser_Osmosis_Boundary_Relation(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.admin_level = self.config.options and self.config.options.get("boundary_detail_level", 8) or 8
        self.municipality_ref = self.config.options and self.config.options.get("municipality_ref")
        if self.municipality_ref and not isinstance(self.municipality_ref, list):
            self.municipality_ref = [self.municipality_ref]

        self.classs_change[1] = {"item":"7120", "level": 2, "tag": ["boundary", "fix:chair"], "desc": T_f(u"Missing admin_centre role") }
        self.classs_change[2] = {"item":"7120", "level": 1, "tag": ["boundary", "name", "fix:chair"], "desc": T_f(u"Missing name") }
        if self.municipality_ref:
            self.classs_change[3] = {"item":"7120", "level": 2, "tag": ["boundary", "ref", "fix:chair"], "desc": T_f(u"Missing municipality ref tag") }
        self.classs_change[4] = {"item":"7120", "level": 2, "tag": ["boundary", "wikipedia", "fix:chair"], "desc": T_f(u"Missing wikipedia tag") }
        self.classs_change[5] = {"item":"7120", "level": 3, "tag": ["boundary", "fix:chair"], "desc": T_(u"Different population tag between relation and admin_centre") }
        self.classs_change[6] = {"item":"7120", "level": 2, "tag": ["boundary", "fix:chair"], "desc": T_(u"Invalid role") }
        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.positionAsText], "fix":{"name": res[2]} if res[2] else None}
        if self.municipality_ref:
            self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.positionAsText], "text":T_f(u"Missing municipality ref tag {0}", ", ".join(self.municipality_ref)),
                "fix":{self.municipality_ref: res[2]} if res[2] else None}
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.positionAsText], "fix":{"wikipedia": res[2]} if res[2] else None}
        self.callback50 = lambda res: {"class":5, "data":[self.relation_full, self.positionAsText],
            "text": T_f(u"Population on admin_centre role ({0}) greater than population on the relation ({1})", res[2], res[3]) }
        self.callback60 = lambda res: {"class":6, "data":[self.relation_full, self.positionAsText], "text":{"en": res[2]}}

    def municipality_col(self, tags):
        if isinstance(tags, list):
            return "NULL::text"
        else:
            return "coalesce(ntags->'name', wtags->'name')"

    def municipality_not(self, tags):
        if isinstance(tags, list):
            return " AND ".join(map(lambda t: "NOT rtags?'{0}'".format(t), tags))
        else:
            return "NOT rtags?'{0}'".format(tags)

    def analyser_osmosis_full(self):
        self.run(sql00.format("", "", self.admin_level))
        self.run(sql10.format("", ""), self.callback10)
        self.run(sql20.format("", "", self.municipality_col("name"), self.municipality_not("name")), self.callback20)
        if self.municipality_ref:
            self.run(sql20.format("", "", self.municipality_col(self.municipality_ref), self.municipality_not(self.municipality_ref)), self.callback30)
        self.run(sql20.format("", "", self.municipality_col("wikipedia"), self.municipality_not("wikipedia")), self.callback40)
        self.run(sql50.format("", ""), self.callback50)
        self.run(sql60.format(""), self.callback60)

    def analyser_osmosis_diff(self):
        self.run(sql00.format("touched_", "", self.admin_level))
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql20.format("touched_", "", self.municipality_col("name"), self.municipality_not("name")), self.callback20)
        if self.municipality_ref:
            self.run(sql20.format("touched_", "", self.municipality_col(self.municipality_ref), self.municipality_not(self.municipality_ref)), self.callback30)
        self.run(sql20.format("touched_", "", self.municipality_col("wikipedia"), self.municipality_not("wikipedia")), self.callback40)
        self.run(sql50.format("touched_", ""), self.callback50)

        self.run(sql00.format("not_touched_", "touched_", self.admin_level))
        self.run(sql10.format("not_touched_", "touched_"), self.callback10)
        self.run(sql20.format("not_touched_", "touched_", self.municipality_col("name"), self.municipality_not("name")), self.callback20)
        if self.municipality_ref:
            self.run(sql20.format("not_touched_", "touched_", self.municipality_col(self.municipality_ref), self.municipality_not(self.municipality_ref)), self.callback30)
        self.run(sql20.format("not_touched_", "touched_", self.municipality_col("wikipedia"), self.municipality_not("wikipedia")), self.callback40)
        self.run(sql50.format("not_touched_", "touched_"), self.callback50)

        self.run(sql60.format("touched_"), self.callback60)
