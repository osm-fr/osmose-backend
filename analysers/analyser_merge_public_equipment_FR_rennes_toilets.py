#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2017                                          ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Public_Equipment_FR_Rennes_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id =2, level = 3, tags = ['merge', 'public equipment', 'fix:survey', 'fix:picture'],
            title = T_('{0} toilets not integrated', 'Rennes'))

        self.init(
            "https://data.rennesmetropole.fr/explore/dataset/toilettes_publiques_vdr/",
            "Toilettes publiques",
            CSV(SourceOpenDataSoft(
                attribution="Ville de Rennes",
                url="https://data.rennesmetropole.fr/explore/dataset/toilettes_publiques_vdr/")),
            Load_XY("Geo Point", "Geo Point",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "toilets",
                        "access": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "wheelchair": lambda res: "yes" if res["pmr"] == "OUI" else "no" if res["pmr"] == "NON" else None} )))
