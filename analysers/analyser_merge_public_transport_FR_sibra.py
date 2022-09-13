#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Pierrick Pratter 2021                                      ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, GTFS, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Public_Transport_FR_sibra(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        place = "SIBRA"
        self.def_class_missing_official(item = 8040, id = 101, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 103, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/offre-de-transports-sibra-a-annecy-gtfs/",
            "Réseau urbain Sibra",
            GTFS(SourceDataGouv(
                attribution="SIBRA",
                dataset="5bd9843e634f413220f7f04a",
                resource="6a98d6c8-63b3-4abd-9fa7-8c6c1a0cad31")),
            Load_XY("stop_lon", "stop_lat"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop"}, {"public_transport": "stop_position"}]),
                conflationDistance = 10,
                osmRef = "ref:FR:SIBRA",
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "stop_position",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:SIBRA": "stop_id",},
                    mapping2 = {"name": "stop_name"},
                    text = lambda tags, fields: T_("{0} stop of {1}", place, fields["stop_name"]) )))
