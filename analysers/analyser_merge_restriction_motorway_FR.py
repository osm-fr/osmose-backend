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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Restriction_Motorway_FR_Maxweight(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8320, id = 1, level = 3, tags = ['merge', 'maxweight'],
            title = T_('maxweight Restriction not integrated'))

        self.init(
            u"http://professionnels.ign.fr/route500",
            u"ROUTE 500®",
            CSV(Source(attribution = u"IGN", millesime = "06/2017",
                    file = "restriction_motorway_FR.csv.bz2")),
            Load("X", "Y",
                where = lambda row: row["REST_POIDS"] != "0"),
            Mapping(
                select = Select(
                    types = ["ways"],
                    tags = {
                        "highway": ["motorway", "trunk", "primary", "secondary"],
                        "bridge": None,
                        "maxweight": None}),
                conflationDistance = 200,
                generate = Generate(
                    static2 = {"source:maxweight": self.source},
                    mapping1 = {
                        "maxweight": "REST_POIDS"})))


class Analyser_Merge_Restriction_Motorway_FR_Maxheight(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8320, id = 2, level = 3, tags = ['merge', 'maxheight'],
            title = T_('maxheight Restriction not integrated'))

        self.init(
            u"http://professionnels.ign.fr/route500",
            u"ROUTE 500®",
            CSV(Source(attribution = u"IGN", millesime = "06/2017",
                    file = "restriction_motorway_FR.csv.bz2")),
            Load("X", "Y",
                where = lambda row: row["REST_HAUT"] != "0"),
            Mapping(
                select = Select(
                    types = ["ways"],
                    tags = {
                        "highway": ["motorway", "trunk", "primary", "secondary"],
                        "maxheight": None}),
                conflationDistance = 200,
                generate = Generate(
                    static2 = {"source:maxheight": self.source},
                    mapping1 = {
                        "maxheight": "REST_HAUT"})))
