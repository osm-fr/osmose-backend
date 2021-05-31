#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jérôme Amagat <jerome.amagat gmail.com> 2016               ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Public_Transport_FR_Star(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "STAR"
        self.def_class_missing_official(item = 8040, id = 81, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 83, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 84, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://data.rennesmetropole.fr/explore/dataset/topologie-des-points-darret-de-bus-du-reseau-star",
            "Topologie des points d'arrêt de bus du réseau STAR",
            CSV(SourceOpenDataSoft(
                attribution="Keolis Rennes",
                url="https://data.rennesmetropole.fr/explore/dataset/topologie-des-points-darret-de-bus-du-reseau-star")),
            Load("Coordonnées", "Coordonnées",
                xFunction = lambda x: x.split(",")[1].strip(),
                yFunction = lambda y: y.split(",")[0].strip()),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                osmRef = "ref:FR:STAR",
                conflationDistance = 10,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:STAR": "Code",
                        "name": "Nom",
                        "wheelchair": lambda res: "yes" if res["Accessible aux PMR"] == "true" else "no" if res["Accessible aux PMR"] == "false" else None,
                        "shelter": lambda res: "yes" if res["Mobilier"] and "Abri" in res["Mobilier"] else "no" if res["Mobilier"] == "Poteau" else None},
                    text = lambda tags, fields: T_("{0} stop of {1}", place, fields["Nom"]) )))
