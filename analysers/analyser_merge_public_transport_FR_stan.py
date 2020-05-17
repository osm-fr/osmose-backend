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

from .Analyser_Merge import Analyser_Merge, Source, GTFS, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Transport_FR_stan(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "STAN"
        self.def_class_missing_official(item = 8040, id = 91, level = 3, tags = ['merge', 'public transport'],
            title = T_f('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 93, level = 3, tags = ['merge', 'public transport'],
            title = T_f('{0} stop, integration suggestion', place))

        self.init(
            u"http://opendata.grandnancy.eu/jeux-de-donnees/detail-dune-fiche-de-donnees/?tx_icsoddatastore_pi1%5Buid%5D=108&tx_icsoddatastore_pi1%5BreturnID%5D=447",
            u"Réseau Stan: horaires et lignes",
            GTFS(Source(attribution = u"Métropole du Grand Nancy", millesime = "06/2017",
                    fileUrl = u"http://opendata.grandnancy.eu/?eID=ics_od_datastoredownload&file=333")),
            Load("stop_lon", "stop_lat"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop"}, {"public_transport": "stop_position"}]),
                conflationDistance = 2,
                osmRef = "ref:FR:STAN",
                generate = Generate(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "stop_position",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:STAN": "stop_code",
                        "wheelchair": lambda fields: self.wheelchair_boarding[fields.get("wheelchair_boarding")]},
                    mapping2 = {"name": "stop_name"},
                    text = lambda tags, fields: T_f(u"{0} stop of {1}", place, fields["stop_name"]) )))

    wheelchair_boarding = {
        None: None,
        "0": None,
        "1": "yes",
        "2": "no"
    }
