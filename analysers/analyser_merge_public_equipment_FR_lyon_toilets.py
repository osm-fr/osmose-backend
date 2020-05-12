#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2017                                          ##
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


class Analyser_Merge_Public_Equipment_FR_Lyon_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 3, level = 3, tags = ['merge', 'public equipment'],
            title = T_f('{0} toilets not integrated', 'Lyon'))

        self.init(
            u"https://data.grandlyon.com/equipements/toilettes-publiques-sur-le-territoire-du-grand-lyon/",
            u"Toilettes publiques",
            GeoJSON(Source(attribution = u"Métropole de Lyon", millesime = "12/2017",
                    fileUrl = u"https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&outputformat=GEOJSON&request=GetFeature&typename=gin_nettoiement.gintoilettepublique&SRSNAME=urn:ogc:def:crs:EPSG::4326"),
                extractor = lambda geojson: geojson),
            Load("geom_x", "geom_y"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "toilets",
                        "access": "public"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "operator": lambda res: res['gestionnaire'] if res and res['gestionnaire'] else None,
                        "ref": lambda res: res['identifiant'] if res and res['identifiant'] else None } )))
