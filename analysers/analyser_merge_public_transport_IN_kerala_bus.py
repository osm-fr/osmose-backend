#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2021                                         ##
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
from .Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load, Conflate, Mapping, Select


class Analyser_Merge_Public_Transport_IN_Kerala_Bus_Stops(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8040, id = 61, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', 'Kerala'))

        self.init(
            u"https://opensdi.kerala.gov.in/",
            u"Kerala Bus Stops",
            GeoJSON(Source(attribution = u"Kerala State Electronics Development Corporation Limited", millesime = "09/2021",
                    fileUrl = u"https://opensdi.kerala.gov.in/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typename=geonode%3AKerala_Bus_Stops&outputFormat=json&srs=EPSG%3A32643&srsName=EPSG%3A4326"),
                extractor = lambda geojson: geojson),
            Load("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"highway": "bus_stop"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": lambda res: res["Name"].title()
                    }
                )
            )
        )
