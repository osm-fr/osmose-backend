#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2019                                         ##
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

class Analyser_Merge_Parking_FR_IDF_park_ride(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 751, level = 3, tags = ['merge', 'parking'],
            title = T_('P+R parking in Île-de-France not integrated'))

        self.init(
            u"https://opendata.stif.info/explore/dataset/parcs-relais-idf/information/",
            u"Parcs Relais en Île-de-France",
            CSV(Source(attribution = u"Île-de-France Mobilités", millesime = "04/2019",
                    fileUrl = u"https://opendata.stif.info/explore/dataset/parcs-relais-idf/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                    separator = u";"),
            Load("Geo Point", "Geo Point",
                xFunction = lambda x: x.split(",")[1],
                yFunction = lambda y: y.split(",")[0]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {
                        "amenity": "parking",
                        "park_ride": None}),
                conflationDistance = 300,
                generate = Generate(
                    static1 = {"amenity": "parking", "park_ride": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {"capacity": lambda res: int(float(res["NB_PL_PR"])) if res["NB_PL_PR"] != "0" else None} )))
