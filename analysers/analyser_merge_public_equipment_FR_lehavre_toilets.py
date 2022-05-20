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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Public_Equipment_FR_LeHavre_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 7, level = 3, tags = ['merge', 'public equipment', 'fix:survey', 'fix:picture'],
            title = T_('{0} toilets not integrated', 'Le Havre'))

        self.init(
            'https://data.lehavreseinemetropole.fr',
            'Sanitaires publics',
            GeoJSON(Source(attribution = 'Ville du Havre', millesime = '04/2022',
                    fileUrl ='https://data.lehavreseinemetropole.fr/api/v1/file/data/159/SANITAIRE/json', zip = 'OD.SANITAIRE.json'),
                extractor = lambda geojson: geojson),
            Load_XY("geom_x", "geom_y",
                srid = 3950),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "toilets",
                        "access": "yes"},
                    static2 = {"source": self.source})))
