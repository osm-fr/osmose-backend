#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2021                                      ##
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
from .Analyser_Merge import Analyser_Merge, Source, GPKG, LoadGeomCentroid, Mapping, Select, Generate


class Analyser_Merge_Highway_Ref_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 7170, id = 200, level = 3, tags = ['merge', 'highway', 'ref'],
            title = T_('Highway ref not integrated'))

        self.init(
            "https://ign.fr",
            "IGN-Point de repère",
            GPKG(Source(attribution = "IGN", millesime = "01/2021",
                    file = "point_de_repere.gpkg")),
            LoadGeomCentroid(
                where = lambda res: res["route"][0] in ('A', 'D', 'N'),
                map = lambda res: {"_x": float(res["_x"]), "_y": float(res["_y"]), 'route': res['route'].replace('A', 'A ').replace('D', 'D ').replace('N', 'N ').replace('P', 'P ') }),
            Mapping(
                select = Select(
                    types = ["ways"],
                    tags = [
                        {"highway": ["motorway", "trunk", "primary", "secondary", "terciary"]}, ]),
                osmRef = "ref",
                conflationDistance = 100,
                generate = Generate(
                    mapping1 = {
                        "ref": "route"}, )))
