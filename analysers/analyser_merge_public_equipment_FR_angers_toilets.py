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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Equipment_FR_Angers_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 8, level = 3, tags = ['merge', 'public equipment'],
            title = T_f('{0} toilets not integrated', 'Angers'))

        self.init(
            u"https://data.angers.fr/explore/dataset/sanitaires-publics-angers/",
            u"Toilettes publiques",
            CSV(Source(attribution = u"Angers Loire Métropole", millesime = "01/2017",
                    fileUrl = u"https://data.angers.fr/explore/dataset/sanitaires-publics-angers/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = u";"),
            Load("Geo Point", "Geo Point",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "toilets",
                        "access": "public"},
                    static2 = {"source": self.source})))
