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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Restriction_FR_92_Maxweight(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8320, id = 3, level = 3, tags = ['merge', 'maxweight', 'fix:survey', 'fix:picture'],
            title = T_('maxweight Restriction not integrated'))

        self.init(
            "https://opendata.hauts-de-seine.fr/explore/dataset/gabarits-et-limitation-de-poids-des-ponts/",
            "Gabarits et limitation de poids des ponts",
            CSV(
                SourceOpenDataSoft(
                    attribution="Département des Hauts-de-Seine",
                    url="https://opendata.hauts-de-seine.fr/explore/dataset/gabarits-et-limitation-de-poids-des-ponts")),
            Load_XY("geo_point_2d", "geo_point_2d",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {"NATURE": "Poids"}),
            Conflate(
                select = Select(
                    types = ["ways"],
                    tags = {
                        "highway": None,
                        "bridge": None,
                        "maxweight": None}),
                conflationDistance = 300,
                mapping = Mapping(
                    static2 = {"source:maxweight": self.source},
                    mapping1 = {"maxweight": lambda fields: self.et(fields["ETIQUETTES"])},
                    text = lambda tags, fields: {"en": fields["NOM_RD"]})))

    def et(self, v):
        return v[:-1].replace(",", ".").strip("0")


class Analyser_Merge_Restriction_FR_92_Maxheight(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8320, id = 4, level = 3, tags = ['merge', 'maxheight'],
            title = T_('maxheight Restriction not integrated'))

        self.init(
            "https://opendata.hauts-de-seine.fr/explore/dataset/gabarits-et-limitation-de-poids-des-ponts/",
            "Gabarits et limitation de poids des ponts",
            CSV(SourceOpenDataSoft(
                attribution="Département des Hauts-de-Seine",
                url="https://opendata.hauts-de-seine.fr/explore/dataset/gabarits-et-limitation-de-poids-des-ponts")),
            Load_XY("geo_point_2d", "geo_point_2d",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {"NATURE": "Hauteur"}),
            Conflate(
                select = Select(
                    types = ["ways"],
                    tags = {
                        "highway": None,
                        "maxheight": None}),
                conflationDistance = 300,
                mapping = Mapping(
                    static2 = {"source:maxheight": self.source},
                    mapping1 = {"maxheight": lambda fields: self.et(fields["ETIQUETTES"])},
                    text = lambda tags, fields: {"en": fields["NOM_RD"]})))

    def et(self, v):
        return v[:-1].replace(",", ".").strip("0")
