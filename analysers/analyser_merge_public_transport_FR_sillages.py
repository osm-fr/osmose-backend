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
from .Analyser_Merge import Analyser_Merge_Point, GTFS, Load_XY, Conflate, Select, Mapping, Source


class Analyser_Merge_Public_Transport_FR_sillages(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        place = "Sillages"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://trouver.datasud.fr/dataset/lignes-regulieres-de-transports-en-pays-de-grasse",
            "Données descriptives de l’offre de transport urbain (lignes, arrêts, horaires théoriques, etc) de la Communauté d’agglomération du Pays de Grasse, au format GTFS.",
            GTFS(Source(attribution = "Communauté d'Agglomération du Pays de Grasse", millesime = "10/2021",
                fileUrl = "https://trouver.datasud.fr/dataset/9b1a687b-d3eb-478a-91da-a63e6b263487/resource/3e2a1506-5bd2-48e6-a93b-00b0a7c29d1c/download/202209215_gtfs_sillages_urbain.zip")),
            Load_XY("stop_lon", "stop_lat",
                 select = {"location_type": '0'}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop", "public_transport": "platform"},{"highway": "bus_stop", "public_transport": False}, {"highway":"platform"}]),
                osmRef = "ref:FR:SILLAGES",
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:SILLAGES": lambda res: res["stop_code"],
                        "name": lambda res: self.replace(res['stop_name'].title()),
                        "addr:city": lambda res: res["city_name"].title(),
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
