#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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

from .Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load, Mapping, Select, Generate


class Analyser_Merge_Bicycle_Rental_FR_IDF(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8160, id = 11, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_f('{0} bicycle rental not integrated', 'IDF'))
        self.def_class_possible_merge(item = 8161, id = 13, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_f('{0} bicycle rental integration suggestion', 'IDF'))
        self.def_class_update_official(item = 8162, id = 14, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_f('{0} bicycle update', 'IDF'))

        self.init(
            u"https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/",
            u"Vélib' - Disponibilité temps réel",
            GeoJSON(Source(attribution = u"Autolib Velib Métropole", millesime = "04/2020",
                fileUrl = u"https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/download/?format=geojson&timezone=Europe/Berlin")),
            Load("geom_x", "geom_y"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_rental"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "bicycle_rental",
                        "network": u"Vélib’",
                        "operator": "Smovengo"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": "name",
                        "capacity": lambda res: res["capacity"] if res["capacity"] != "0" else None} )))
