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
        self.missing_official = self.def_class(item = 8160, id = 11, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('IDF bicycle rental not integrated'))
        self.possible_merge   = self.def_class(item = 8161, id = 13, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('IDF bicycle rental integration suggestion'))
        self.update_official  = self.def_class(item = 8162, id = 14, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('IDF bicycle update'))

        Analyser_Merge.__init__(self, config, logger,
            u"https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/",
            u"Vélib' - Disponibilité temps réel",
            GeoJSON(Source(attribution = u"Autolib Velib Métropole", millesime = "04/2019",
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
                        "name": "station_name",
                        "capacity": lambda res: res["nbedock"] if res["nbedock"] != "0" else None} )))
