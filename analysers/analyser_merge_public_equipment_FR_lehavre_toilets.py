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


class Analyser_Merge_Public_Equipment_FR_LeHavre_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8180", "class": 7, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Le Havre toilets not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "https://data.agglo-lehavre.fr/",
            u"Toilettes publiques",
            GeoJSON(Source(attribution = u"Ville du Havre", millesime = "12/2017",
                    fileUrl = "https://data.agglo-lehavre.fr/api/v1/file/data/159/SANITAIRE/json", zip = "OD.SANITAIRE.json"),
                extractor = lambda geojson: geojson),
            Load("geometry", "geometry",
                xFunction = lambda g: g and g['coordinates'] and g['coordinates'][0],
                yFunction = lambda g: g and g['coordinates'] and g['coordinates'][1],
                srid = 3950),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "toilets",
                        "access": "public"},
                    static2 = {"source": self.source})))
