#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Didier Marchand 2020                                       ##
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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

class Analyser_Merge_plo_riu_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)

        if config.db_schema == 'france_guyane':
            thesrid = '2972'
        elif config.db_schema == 'france_saintpierreetmiquelon':
            thesrid = '4467'
        elif config.db_schema == 'france_mayotte':
            thesrid = '4471'
        else:
            thesrid = '2154'

        doc = dict(
            detail = T_(
'''The list of way_link comes from the CEREMA's database "RIU" in France.'''),
            trap = T_(
'''The position of the marker may be a little different than that visible on the road. The point does not start at the beginning of the white strip but when it becomes wider.'''))

        self.def_class_missing_official(item = 8430, id = 41, level = 3, tags = ['merge', 'highway'],
            title = T_('way link nat_ref not integrated'), **doc)
        self.def_class_possible_merge(item = 8431, id = 43, level = 3, tags = ['merge', 'highway'],
            title = T_('way link nat_ref integration suggestion'), **doc)
        self.def_class_update_official(item = 8432, id = 44, level = 3, tags = ['merge', 'highway'],
            title = T_('way link nat_ref update'), **doc)

        self.init(
            "https://www.data.gouv.fr/fr/datasets/bornage-du-reseau-routier-national/",
            "Bornage du réseau routier national",
            CSV(Source(attribution = "data.gouv.fr:Ministère de la Transition écologique et solidaire", millesime = "01/2019",
                    fileUrl = "https://www.data.gouv.fr/fr/datasets/r/fbc8b73b-a65c-486b-a710-ed22b9e4070c"),
                    separator = "\t"),
            Load("x", "y", thesrid,
                xFunction = self.float_comma,
                yFunction = self.float_comma,
                where = lambda row: self.is_natref(row)),
            Mapping(
                select = Select(
                    types = ["ways"],
                    tags = [{"highway": ["motorway_link", "primary_link", "secondary_link", "tertiary_link"]}, {"junction": "roundabout"}]),
                osmRef = "nat_ref",
                conflationDistance = 350,
                generate = Generate(
                    static2 = {"source:nat_ref": self.source},
                    mapping1 = {
                        "nat_ref": lambda row: row['route'] + '_' + row['pr']}
                    )))

    def is_natref(self,row):
        if 'A9' in row['route']:
            return True
        elif 'N9' in row['route']:
            return True
        else: return False
