#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, SHP, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_Public_Transport_FR_TBM(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "TBM"
        self.def_class_missing_official(item = 8040, id = 51, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 53, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))

        self.init(
            'https://opendata.bordeaux-metropole.fr/explore/dataset/tb_arret_p',
            'Arrêt physique sur le réseau',
            SHP(SourceOpenDataSoft(
                attribution='Bordeaux Métropole',
                url='https://opendata.bordeaux-metropole.fr/explore/dataset/tb_arret_p',
                format="shp",
                zip="tb_arret_p.shp")),
            LoadGeomCentroid(
                select = {"reseau": [None, "BUS"]}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes",
                        "network": "TBM"},
                    static2 = {"source": self.source},
                    mapping2 = {
                        "name": lambda res: res['nomarret'],
                        "shelter": lambda res: "yes" if res["mobilie1"] and "abribus" in res["mobilie1"].lower() else "no" if res["mobilie1"] and "poteau" in res["mobilie1"].lower() else None},
                    text = lambda tags, fields: T_("{0} stop {1}", place, fields["nomarret"]) )))
