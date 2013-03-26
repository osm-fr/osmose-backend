#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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
    relation_members.member_role IS NULL AS admin_centre,
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
    relations.tags->'admin_level' = '8'
"""

sql10 = """
SELECT
    id,
    ST_AsText(relation_locate(id))
FROM
    admin
WHERE
    NOT admin_centre
"""

sql20 = """
SELECT
    id,
    ST_AsText(relation_locate(id))
FROM
    admin
WHERE
    NOT rtags?'name'
"""

sql30 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    coalesce(ntags->'ref:INSEE', wtags->'ref:INSEE')
FROM
    admin
WHERE
    NOT rtags?'ref:INSEE'
"""

sql40 = """
SELECT
    id,
    ST_AsText(relation_locate(id)),
    coalesce(ntags->'wikipedia', wtags->'wikipedia')
FROM
    admin
WHERE
    NOT rtags?'wikipedia'
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
    coalesce(ntags->'population', wtags->'population') > rtags->'population'
"""

class Analyser_Osmosis_Boundary_Administrative(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.FR = config.options and "country" in config.options and config.options["country"] == "FR"
        self.classs_change[1] = {"item":"7120", "level": 2, "tag": ["boundary"], "desc":{"fr":"Rôle admin_centre absent", "en":"Missing admin_centre role"} }
        self.classs_change[2] = {"item":"7120", "level": 1, "tag": ["boundary", "name"], "desc":{"fr":"Nom manquant", "en":"Missing name"} }
        if self.FR:
            self.classs_change[3] = {"item":"7120", "level": 2, "tag": ["boundary", "ref"], "desc":{"fr":"ref:INSEE manquant", "en":"Missing ref:INSEE"} }
        self.classs_change[4] = {"item":"7120", "level": 2, "tag": ["boundary", "wikipedia"], "desc":{"fr":"Tag wikipedia manquant", "en":"Missing wikipedia tag"} }
        self.classs_change[5] = {"item":"7120", "level": 3, "tag": ["boundary"], "desc":{"fr":"Tag population inconsistant entre la relation et le admin_centre", "en":"Bad population tag between relation and admin_centre"} }
        self.callback10 = lambda res: {"class":1, "data":[self.relation_full, self.positionAsText]}
        self.callback20 = lambda res: {"class":2, "data":[self.relation_full, self.positionAsText]}
        self.callback30 = lambda res: {"class":3, "data":[self.relation_full, self.positionAsText], "fix":{"ref:INSEE": res[2]} if res[2] else None}
        self.callback40 = lambda res: {"class":4, "data":[self.relation_full, self.positionAsText], "fix":{"wikipedia": res[2]} if res[2] else None}
        self.callback50 = lambda res: {"class":5, "data":[self.relation_full, self.positionAsText], "text":{"fr": "Population du rôle admin_centre (%s) suppérieure à la polulation de la relation (%s)" % (res[2], res[3])}}

    def analyser_osmosis_all(self):
        self.run(sql00.format("", ""))
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
        if self.FR:
            self.run(sql30, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50, self.callback50)

    def analyser_osmosis_touched(self):
        self.run(sql00.format("touched_", ""))
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
        if self.FR:
            self.run(sql30, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50, self.callback50)

        self.run(sql00.format("", "touched_"))
        self.run(sql10, self.callback10)
        self.run(sql20, self.callback20)
        if self.FR:
            self.run(sql30, self.callback30)
        self.run(sql40, self.callback40)
        self.run(sql50, self.callback50)
