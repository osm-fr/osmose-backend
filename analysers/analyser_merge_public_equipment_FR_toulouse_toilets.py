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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Public_Equipment_FR_Toulouse_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 4, level = 3, tags = ['merge', 'public equipment'],
            title = T_('{0} toilets not integrated', 'Toulouse'))

        self.init(
            "https://data.toulouse-metropole.fr/explore/dataset/sanisettes/",
            "Toilettes publiques",
            CSV(SourceOpenDataSoft(
                attribution="Toulouse Métropole",
                url="https://data.toulouse-metropole.fr/explore/dataset/sanisettes")),
            Load("Geo Point", "Geo Point",
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
                        "wheelchair": lambda res: "yes" if res["accessibilité"] == "Accessible aux personnes à mobilité réduite" else "no" if res["accessibilité"] == "Non accessible aux personnes à mobilité réduite" else None} )))
