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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Bicycle_Parking_FR_CAPP(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 11, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('CAPP bicycle parking not integrated'))

        self.init(
            u"http://opendata.agglo-pau.fr/index.php/fiche?idQ=20",
            u"Supports vélos sur la CAPP",
            CSV(Source(attribution = u"Communauté d'Agglomération Pau-Pyrénées", millesime = "01/2013",
                    fileUrl = u"http://opendata.agglo-pau.fr/sc/call.php?f=1&idf=20", zip = "Sta_Velo_Agglo_WGS84.csv")),
            Load("X", "Y",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = {"capacity": lambda res: str(int(res["NOMBRE"])*2)} )))
