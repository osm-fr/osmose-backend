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


class Analyser_Merge_Recycling_FR_capp_glass(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = '8120', id = 11, level = 3, tags = ['merge', 'recycling', 'fix:survey', 'fix:picture'],
            title = T_('CAPP glass recycling not integrated'))

        self.init(
            u"http://opendata.agglo-pau.fr/index.php/fiche?idQ=8",
            u"Point d'apport volontaire du verre : Bornes à verres sur la CAPP",
            # Dod_Bav_CC43.csv is in WGS84
            CSV(Source(attribution = u"Communauté d'Agglomération Pau-Pyrénées", millesime = "01/2013",
                    fileUrl = u"http://opendata.agglo-pau.fr/sc/call.php?f=1&idf=8", zip = "Dod_Bav_CC43.csv")),
            Load("X", "Y",
                xFunction = Load.float_comma,
                yFunction = Load.float_comma,
                select = {"USAGE_": "En service"}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "recycling",
                        "recycling:glass_bottles": "yes",
                        "recycling_type": "container"},
                    static2 = {"source": self.source} )))
