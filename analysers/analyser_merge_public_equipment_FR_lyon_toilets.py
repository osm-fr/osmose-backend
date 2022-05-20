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
import json


class Analyser_Merge_Public_Equipment_FR_Lyon_Toilets(Analyser_Merge):
    def ohToStr(self, oh):
        if not oh:
            return None
        else:
            theJson = json.loads(oh.replace("'", '"'))
            return "Opens: " + " | ".join(map(lambda s: s['opens'] + " to " + s['closes'] + " (" + ", ".join(map(lambda x: x[18:], s['dayOfWeek'])) + ")", theJson))

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 33, level = 3, tags = ['merge', 'public equipment', 'fix:survey', 'fix:picture'],
            title = T_('{0} toilets not integrated', 'Grand Lyon'))
        self.def_class_possible_merge(item = 8181, id = 34, level = 3, tags = ['merge', 'public equipment', 'fix:chair'],
            title = T_('{0} toilets, integration suggestion', 'Grand Lyon'))
        self.def_class_update_official(item = 8182, id = 35, level = 3, tags = ['merge', 'public equipment', 'fix:chair'],
            title = T_('{0} toilets update', 'Grand Lyon'))

        self.init(
            u"https://data.grandlyon.com/jeux-de-donnees/toilettes-publiques-metropole-lyon-v2-0-0",
            u"Toilettes publiques",
            GeoJSON(Source(attribution = u"Grand Lyon", millesime = "02/2020",
                    fileUrl = u"https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=adr_voie_lieu.toilettepublique_latest&outputFormat=application/json;%20subtype=geojson&SRSNAME=EPSG:4326&startIndex=0"),
                extractor = lambda geojson: geojson),
            Load_XY("geom_x", "geom_y",
                 where = lambda res: res['provenance'] != 'Open Street Map'),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 50,
                mapping = Mapping(
                    text = lambda tags, fields: {"en": " - ".join(filter(lambda x: x, [
                        fields['adresse'],
                        fields['infoloc'],
                        self.ohToStr(fields['openinghoursspecification'])
                    ]))},
                    static1 = {
                        "amenity": "toilets"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "wheelchair": lambda res: 'yes' if res and res['acceshandi'] == 'true' else None,
                        "fee": lambda res: 'yes' if res and res['payant'] == 'true' else None,
                        "male": lambda res: 'yes' if res and res['hommes'] == 'true' else None,
                        "female": lambda res: 'yes' if res and res['femmes'] == 'true' else None,
                        "unisex": lambda res: 'yes' if res and res['unisexe'] == 'true' else None,
                        "child": lambda res: 'yes' if res and res['enfants'] == 'true' else None,
                        "website": lambda res: res['web'] if res and res['web'] else None } )))
