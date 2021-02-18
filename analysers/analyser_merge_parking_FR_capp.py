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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Parking_FR_capp(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 1, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:survey'],
            title = T_('{0} parking not integrated', 'CAPP'))

        self.init(
            u"http://opendata.agglo-pau.fr/index.php/fiche?idQ=18",
            u"Parkings sur la CAPP",
            CSV(Source(attribution = u"Communauté d'Agglomération Pau-Pyrénées", millesime = "01/2013",
                    fileUrl = u"http://opendata.agglo-pau.fr/sc/call.php?f=1&idf=18", zip = "Parking_WGS84.csv", encoding = "ISO-8859-15")),
            Load("X", "Y",
                xFunction = Load.float_comma,
                yFunction = Load.float_comma),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "parking"}),
                conflationDistance = 200,
                mapping = Mapping(
                    static1 = {
                        "amenity": "parking"},
                    static2 = {
                        "source": self.source},
                    mapping1 = {
                        "name": "NOM",
                        "fee": lambda res: "yes" if res["Pay_grat"] == "Payant" else "no",
                        "capacity": lambda res: res["Places"] if res["Places"] != "0" else None,
                        "parking": lambda res: "surface" if res["Ouvrage"] == "Plein air" else "underground" if res["Ouvrage"] == "Souterrain" else None},
                    text = lambda tags, fields: {"en": "Parking {0}".format(tags["name"])} )))


class Analyser_Merge_Parking_FR_capp_disabled(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 11, level = 3, tags = ['merge', 'parking'],
            title = T_('{0} parking for disabled not integrated', 'CAPP'))

        self.init(
            u"http://opendata.agglo-pau.fr/index.php/fiche?idQ=21",
            u"Stationnements règlementaires sur la commune de Pau - Stationnement Handi",
            CSV(Source(attribution = u"Communauté d'Agglomération Pau-Pyrénées", millesime = "01/2013",
                    fileUrl = u"http://opendata.agglo-pau.fr/sc/call.php?f=1&idf=21", zip = "Sta_Regl_Wgs84.csv", encoding = "ISO-8859-15")),
            Load("X", "Y",
                select = {"Types": "Stationnement Handi"},
                xFunction = Load.float_comma,
                yFunction = Load.float_comma),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {
                        "amenity": "parking",
                        "capacity:disabled": None}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {"amenity": "parking"},
                    static2 = {"source": self.source},
                    mapping1 = {"capacity:disabled": lambda res: res["nombre"] if res["nombre"] != "0" else "yes"} )))
