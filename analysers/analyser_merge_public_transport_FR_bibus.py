#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Arzhel Younsi 2024                                         ##
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


class Analyser_Merge_Public_Transport_FR_bibus(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        place = "Bibus"
        self.def_class_missing_official(item = 8040, id = 151, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 153, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/horaires-theoriques-et-temps-reel-des-bus-et-tramways-circulant-sur-le-territoire-de-brest-metropole/",
            "Horaires théoriques et temps-réel des bus et tramways circulant sur le territoire de Brest métropole",
            GTFS(SourceDataGouv(attribution = "Brest Métropole",
                    dataset = "55ffbe0888ee387348ccb97d", resource = "583d1419-058b-481b-b378-449cab744c82")),
            Load_XY("stop_lon", "stop_lat", select = {"location_type": '0'}),
            Conflate(
                mapping = Mapping(
                    static1 = {"public_transport": "platform"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:Bibus": "stop_id",
                        "wheelchair": lambda fields: self.wheelchair_boarding[fields.get("wheelchair_boarding")]},
                    mapping2 = {"name": "stop_name"},
                    text = lambda tags, fields: T_("{0} stop {1}", place, fields["stop_name"])),
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop", "public_transport": "platform"},
                            {"tram": "yes", "public_transport": "platform"},
                            {"aerialway": "station", "public_transport": "platform"}
                            ]),
                conflationDistance = 10,
                osmRef = "ref:Bibus"))

    wheelchair_boarding = {
        None: None,
        "0": None,
        "1": "yes",
        "2": "no"
    }
