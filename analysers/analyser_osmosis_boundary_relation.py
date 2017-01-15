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

from Analyser_Osmosis import Analyser_Osmosis

sql00 = """
DROP TABLE IF EXISTS admin;
CREATE TEMP TABLE admin AS
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
    admin
WHERE
    NOT has_admin_centre
"""

sql20 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    coalesce(ntags->'{0}', wtags->'{0}')
FROM
    admin
WHERE
    NOT rtags?'{0}'
"""

sql50 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    coalesce(ntags->'population', wtags->'population'),
    rtags->'population' AS population
FROM
    admin
WHERE
    rtags?'population' AND
    regexp_replace(coalesce(ntags->'population', wtags->'population'), '([0-9]{0,9}).*', '0\\1')::int >
    regexp_replace(rtags->'population', '([0-9]{0,9}).*', '0\\1')::int
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
        self.classs_change[1] = {"item":"7120", "level": 2, "tag": ["boundary", "fix:chair"], "desc": T_(u"Missing admin_centre role") }
        self.classs_change[2] = {"item":"7120", "level": 1, "tag": ["boundary", "name", "fix:chair"], "desc": T_(u"Missing name") }
        if self.municipality_ref:
            self.classs_change[3] = {"item":"7120", "level": 2, "tag": ["boundary", "ref", "fix:chair"], "desc": T_(u"Missing municipality ref %s", self.municipality_ref) }
        self.classs_change[4] = {"item":"7120", "level": 2, "tag": ["boundary", "wikipedia", "fix:chair"], "desc": T_(u"Missing wikipedia tag") }
        self.classs_change[5] = {"item":"7120", "level": 3, "tag": ["boundary", "fix:chair"], "desc": T_(u"Different population tag between relation and admin_centre") }
        self.classs_change[6] = {"item":"7120", "level": 2, "tag": ["boundary", "fix:chair"], "desc": T_(u"Invalid role") }
        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.positionAsText], "fix":{"name": res[2]} if res[2] else None}
        if self.municipality_ref:
            self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.positionAsText], "fix":{self.municipality_ref: res[2]} if res[2] else None}
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.positionAsText], "fix":{"wikipedia": res[2]} if res[2] else None}
        self.callback50 = lambda res: {"class":5, "data":[self.relation_full, self.positionAsText],
            "text": T_(u"Population on admin_centre role (%s) greater than population on the relation (%s)", res[2], res[3]) }
        self.callback60 = lambda res: {"class":6, "data":[self.relation_full, self.positionAsText], "text":{"en": res[2]}}

    def analyser_osmosis_full(self):
        self.run(sql00.format("", "", self.admin_level))
        self.run(sql10, self.callback10)
        self.run(sql20.format("name"), self.callback20)
        if self.municipality_ref:
            self.run(sql20.format(self.municipality_ref), self.callback30)
        self.run(sql20.format("wikipedia"), self.callback40)
        self.run(sql50, self.callback50)
        self.run(sql60.format(""), self.callback60)

    def analyser_osmosis_diff(self):
        self.run(sql00.format("touched_", "", self.admin_level))
        self.run(sql10, self.callback10)
        self.run(sql20.format("name"), self.callback20)
        if self.municipality_ref:
            self.run(sql20.format(self.municipality_ref), self.callback30)
        self.run(sql20.format("wikipedia"), self.callback40)
        self.run(sql50, self.callback50)

        self.run(sql00.format("", "touched_", self.admin_level))
        self.run(sql10, self.callback10)
        self.run(sql20.format("name"), self.callback20)
        if self.municipality_ref:
            self.run(sql20.format(self.municipality_ref), self.callback30)
        self.run(sql20.format("wikipedia"), self.callback40)
        self.run(sql50, self.callback50)

        self.run(sql60.format("touched_"), self.callback60)
