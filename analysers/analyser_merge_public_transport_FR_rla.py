#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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


class Analyser_Merge_Public_Transport_FR_rla(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "Lignes d'Azur"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "http://opendata.nicecotedazur.org/data/dataset/export-quotidien-au-format-gtfs-du-reseau-de-transport-lignes-d-azur/resource/aacb4eea-d008-4b13-b17a-848b8ced7e03",
            "Export quotidien au format GTFS du réseau de transport Lignes d'Azur",
            GTFS(Source(attribution = "Régie Ligne d'Azur", millesime = "01/2022",
                        fileUrl = "http://opendata.nicecotedazur.org/data/storage/f/gtfs1642637701/GTFSExport.zip")),
            Load("stop_lon", "stop_lat",
                 select = {"location_type": '0', "stop_code": True},
                 ),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop"}, {"public_transport": "platform"}, {"highway":"platform"}]),
                osmRef = "ref:FR:RLA",
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:RLA": lambda res: res["stop_code"],
                        # If stop_code is defined, the platform belongs to the Lignes d'Azur network,
                        # else it belongs generally to the ZOU (Région Sud) network, which some old
                        # Lignes d'Azur / TAM lines have been transferred to (lines 100 and 200 for example)
                        "name": lambda res: res['stop_name'],
                    },
                    text = lambda tags, fields: T_(f"{place} stop of {fields['stop_name']}")))
        )
