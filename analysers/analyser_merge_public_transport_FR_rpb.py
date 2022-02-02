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
import re

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, GTFS, Load, Conflate, Select, Mapping, Source


class Analyser_Merge_Public_Transport_FR_rpb(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "Palm Bus"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://trouver.datasud.fr/dataset/palmbus-cannes-fr",
            "Réseau de transport urbain PALMBUS de l'Agglomération Cannes Pays de Lérins",
            GTFS(Source(attribution = "Régie Palm Bus", millesime = "12/2021",
                        fileUrl = "https://trouver.datasud.fr/dataset/73b25d9d-c790-4228-85a4-d9b8774da3c7/resource/d791708c-9a64-4c56-ac3d-3cc44b727b8c/download/palmbus-cannes-fr.zip")),
            Load("stop_lon", "stop_lat",
                 select = {"location_type": '0'},
                 ),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop", "public_transport": "platform"}, {"highway":"platform"}]),
                osmRef = "ref:FR:RPB",
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:RPB": lambda res: res["stop_id"],
                        "name": lambda res: res['stop_name'],
                        "wheelchair": lambda res: 'yes' if res["wheelchair_boarding"] == '1' else 'no' if res["wheelchair_boarding"] == '0' else None,
                    },
                    text = lambda tags, fields: T_(f"{place} stop of {fields['stop_name']}")))
        )
