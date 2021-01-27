#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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
from .Analyser_Merge import Analyser_Merge, Source, GTFS, Load, Conflate, Select, Mapping


class Analyser_Merge_Public_Transport_FR_sibra(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "SIBRA"
        self.def_class_missing_official(item = 8040, id = 91, level = 3, tags = ['merge', 'public transport'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 93, level = 3, tags = ['merge', 'public transport'],
            title = T_('{0} stop, integration suggestion', place))

        self.init(
            u"https://transport.data.gouv.fr/datasets/offre-de-transports-sibra-a-annecy-gtfs",
            u"Réseau urbain Sibra",
            GTFS(Source(attribution = u"SIBRA", millesime = "08/2020",
                    fileUrl = u"https://static.data.gouv.fr/resources/offre-de-transports-sibra-a-annecy-gtfs/20200821-090711/gtfs-sibra-jybus-202009.zip")),
            Load("stop_lon", "stop_lat"),
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
