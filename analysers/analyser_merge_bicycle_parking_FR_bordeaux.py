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
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 1, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('Bordeaux bicycle parking not integrated'))

        self.init(
            u"http://opendata.bordeaux.fr/content/mobiliers-urbains-stationnement-2roues",
            u"Mobiliers urbains : Stationnement deux-roues",
            CSV(Source(attribution = u"Ville de Bordeaux", millesime = "01/2019",
                    fileUrl = u"http://opendatabdx.cloudapp.net/DataBrowser/DownloadCsv?container=databordeaux&entitySet=sigstavelo&filter=NOFILTER")),
            Load("x_long", "y_lat",
                select = {
                    "realisation": u"Réalisé",
                    "nature": [u"Arceau vélo", u"Rack", u"Potelet"]}),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = {"capacity": lambda res: None if res["nombre"] in (None, "0") else res["nombre"] if res["nombre"] == "Rack" else str(int(res["nombre"])*2)} )))
