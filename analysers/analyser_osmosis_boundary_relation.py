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

sql10 = """
SELECT
    relations.id,
    ST_AsText(relation_locate(relations.id)),

    relations.tags->'name' AS name,
    relations.tags->'ref:INSEE' AS ref_insee,
    relations.tags->'wikipedia' AS wikipedia,
    relations.tags->'population' AS population,

    coalesce(nodes.tags->'ref:INSEE', ways.tags->'ref:INSEE'),
    coalesce(nodes.tags->'wikipedia', ways.tags->'wikipedia'),
    coalesce(nodes.tags->'population', ways.tags->'population'),

    relation_members.member_role IS NULL,
    (relations.tags->'name') IS NULL,
    (relations.tags->'ref:INSEE') IS NULL,
    (relations.tags->'wikipedia') IS NULL,
    coalesce(nodes.tags->'population', ways.tags->'population') > relations.tags->'population'
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
    relations.tags->'admin_level' = '8' AND
    (
        relation_members.member_role IS NULL OR
        (relations.tags->'name') IS NULL OR
        (relations.tags->'ref:INSEE') IS NULL OR
        (relations.tags->'wikipedia') IS NULL OR
        coalesce(nodes.tags->'population', ways.tags->'population') > relations.tags->'population'
    )
"""

class Analyser_Osmosis_Boundary_Administrative(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs_change[1] = {"item":"7120", "level": 2, "tag": ["boundary"], "desc":{"fr":"Rôle admin_centre absent", "en":"Missing admin_centre role"} }
        self.classs_change[2] = {"item":"7120", "level": 1, "tag": ["boundary", "name"], "desc":{"fr":"Nom manquant", "en":"Missing name"} }
        self.classs_change[3] = {"item":"7120", "level": 2, "tag": ["boundary", "ref"], "desc":{"fr":"ref:INSEE manquant", "en":"Missing ref:INSEE"} }
        self.classs_change[4] = {"item":"7120", "level": 2, "tag": ["boundary", "wikipedia"], "desc":{"fr":"Tag wikipedia manquant", "en":"Missing wikipedia tag"} }
        self.classs_change[5] = {"item":"7120", "level": 3, "tag": ["boundary"], "desc":{"fr":"Tag population inconsistant entre la relation et le admin_centre", "en":"Bad population tag between relation and admin_centre"} }
        def cal_class(res):
            for i in range(9,13+1):
                if res[i]:
                    return i-9+1
        def cal_text(res):
            if res[13]:
                return {"fr": "Population du rôle admin_centre (%s) suppérieure à la polulation de la relation (%s)" % (res[8], res[5])}
        def cal_fix(res):
            if res[11] and res[6]:
                return {"ref:INSEE": res[6]}
            if res[12] and res[7]:
                return {"wikipedia": res[7]}
        self.callback10 = lambda res: {"class":cal_class(res), "data":[self.relation_full, self.positionAsText], "text":cal_text(res), "fix":cal_fix(res)}

    def analyser_osmosis_all(self):
        self.run(sql10.format("", ""), self.callback10)

    def analyser_osmosis_touched(self):
        self.run(sql10.format("touched_", ""), self.callback10)
        self.run(sql10.format("", "touched_"), self.callback10)
