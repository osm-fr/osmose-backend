#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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


class Analyser_Merge_Bicycle_Parking_FR_Bordeaux(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8150", "class": 1, "level": 3, "tag": ["merge", "public equipment", "cycle"], "desc": T_(u"Bordeaux bicycle parking not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"http://opendata.bordeaux.fr/content/mobiliers-urbains-stationnement-2roues",
            u"Mobiliers urbains : Stationnement vélo",
            CSV(Source(attribution = u"Ville de Bordeaux", millesime = "01/2016",
                    fileUrl = u"http://opendatabdx.cloudapp.net/DataBrowser/DownloadCsv?container=databordeaux&entitySet=sigstavelo&filter=NOFILTER"),
                separator = ";"),
            Load("X_LONG", "Y_LAT",
                select = {
                    "REALISATION": u"Réalisé",
                    "NATURE": [u"Arceau vélo", u"Rack", u"Potelet"]},
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
                    mapping1 = {"capacity": lambda res: None if res["NOMBRE"] in (None, "0") else res["NOMBRE"] if res["NATURE"] == "Rack" else str(int(res["NOMBRE"])*2)} )))
