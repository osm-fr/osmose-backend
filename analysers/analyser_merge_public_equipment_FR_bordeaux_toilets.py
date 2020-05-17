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


class Analyser_Merge_Public_Equipment_FR_Bordeaux_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 1, level = 3, tags = ['merge', 'public equipment'],
            title = T_f('{0} toilets not integrated', 'Bordeaux'))

        self.init(
            u"http://opendata.bordeaux.fr/content/toilettes-publiques",
            u"Toilettes publiques",
            CSV(Source(attribution = u"Ville de Bordeaux", millesime = "01/2019",
                    fileUrl = u"http://opendatabdx.cloudapp.net/DataBrowser/DownloadCsv?container=databordeaux&entitySet=sigsanitaire&filter=NOFILTER")),
            Load("x_long", "y_lat"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "toilets",
                        "fee": "no",
                        "access": "public"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "toilets:wheelchair": lambda res: "yes" if res["options"] == u"Handicapé" else None,
                        "toilets:position": lambda res: "urinal" if res["typologie"] == u"Urinoir" else None} )))
