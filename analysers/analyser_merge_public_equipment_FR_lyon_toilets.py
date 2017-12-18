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

from Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Equipment_FR_Lyon_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8180", "class": 3, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Lyon toilets not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "https://data.grandlyon.com/equipements/toilettes-publiques-sur-le-territoire-du-grand-lyon/",
            u"Toilettes publiques",
            GeoJSON(Source(attribution = u"Métropole de Lyon", millesime = "12/2017",
                    fileUrl = "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&outputformat=GEOJSON&request=GetFeature&typename=gin_nettoiement.gintoilettepublique&SRSNAME=urn:ogc:def:crs:EPSG::4326"),
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
                        "operator": lambda res: res['properties']['gestionnaire'] if res['properties'] and res['properties']['gestionnaire'] else None,
                        "ref": lambda res: res['properties']['identifiant'] if res['properties'] and res['properties']['identifiant'] else None } )))
