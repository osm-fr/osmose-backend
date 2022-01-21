#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Théo Peltier 2022                                          ##
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
from .Analyser_Merge import Analyser_Merge_Point, GTFS, Load_XY, Conflate, Select, Mapping, SourceDataGouv


class Analyser_Merge_Public_Transport_FR_zestbus(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        place = "Zest'Bus"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/horaires-reseau-zest/",
            "Horaires du réseau de transport urbain des communes de Menton et de la communauté d'agglomération de la Riviera française",
            GTFS(SourceDataGouv(attribution = "Keolis Menton Riviera", millesime = "08/2022",
                dataset = "5bb49085634f4115ddc9293b", resource = "72609821-2459-47fb-a63b-3dbbc0d96c92")),
            Load_XY("stop_lon", "stop_lat",
                 select = {"parent_station": {'like': 'ARCOM%'}}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop", "public_transport": "platform"},{"highway": "bus_stop", "public_transport": False}, {"highway":"platform"}]),
                osmRef = "ref:FR:ZEST",
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:ZEST": lambda res: res["stop_code"],
                        "name": lambda res: self.replace(res['stop_name'].title()),
                        "wheelchair": lambda res: 'yes' if res["wheelchair_boarding"] == '1' else 'no' if res["wheelchair_boarding"] == '0' else None,
                    },
                    text = lambda tags, fields: T_(f"{place} stop of {fields['stop_name']}")) ))

    def replace(self, string):
        for term, translation in self.replacement.items():
            string = string.replace(term, translation)
        return string

    replacement = {
        ' De ': ' de ',
        ' Des ': ' des ',
        ' Du ': ' du ',
        ' La ': ' la ',
        ' et ': ' et ',
        'Rd ': 'Route départementale '
    }
