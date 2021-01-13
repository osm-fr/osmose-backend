#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Phyks (Lucas Verney) 2018                                  ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping

STANDS_TYPES = {
    "Arceau autre": "stands",
    "Arceau St-Germain": "wide_stands",
    "Epingle vélo": "stands",
    "Sans": "floor",
}
tag_mapping = {
    "capacity": (
        lambda res: None if res["Nombre places calculées"] in (None, "0", "-1") else res["Nombre places calculées"]
    ),
    "bicycle_parking": (
        lambda res: STANDS_TYPES.get(res['Type mobilier'], None)
    )
}


class Analyser_Merge_Bicycle_Parking_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 21, level = 3, tags = ['merge', 'public equipment', 'bicycle'],
            title = T_('Paris bicycle parking not integrated'))

        self.init(
            u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/information/",
            u"Stationnement sur voie publique - emplacements vélos",
            CSV(SourceOpenDataSoft(
                attribution="Ville de Paris",
                base_url="https://opendata.paris.fr",
                dataset="stationnement-voie-publique-emplacements")),
            Load("geo_point_2d", "geo_point_2d",
                select = {
                    u"Régime prioritaire": u"2 ROUES",
                    u"Régime particulier": u"Vélos",
                },
                xFunction = lambda x: Load.float_comma(x.split(',')[1]),
                yFunction = lambda y: Load.float_comma(y.split(',')[0])
            ),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = tag_mapping )))


class Analyser_Merge_Motorcycle_Parking_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 31, level = 3, tags = ['merge', 'public equipment', 'motorcycle'],
            title = T_('Paris motorcycle parking not integrated'))

        self.init(
            u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/information/",
            u"Stationnement sur voie publique - emplacements motos",
            CSV(SourceOpenDataSoft(attribution = u"Ville de Paris",
                    base_url = "https://opendata.paris.fr",
                    dataset = "stationnement-voie-publique-emplacements")),
            Load("geo_point_2d", "geo_point_2d",
                select = {
                    u"Régime prioritaire": u"2 ROUES",
                    u"Régime particulier": u"Motos",
                },
                xFunction = lambda x: Load.float_comma(x.split(',')[1]),
                yFunction = lambda y: Load.float_comma(y.split(',')[0])
            ),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "motorcycle_parking"}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "motorcycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = tag_mapping )))


class Analyser_Merge_Bicycle_Motorcycle_Parking_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 41, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'motorcycle'],
            title = T_('Paris shared motorcycle/motorcycle parking not integrated'))

        self.init(
            u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/information/",
            u"Stationnement sur voie publique - emplacements deux roues",
            CSV(SourceOpenDataSoft(attribution = u"Ville de Paris",
                    base_url = "https://opendata.paris.fr",
                    dataset = "stationnement-voie-publique-emplacements")),
            Load("geo_point_2d", "geo_point_2d",
                select = {
                    u"Régime prioritaire": u"2 ROUES",
                    u"Régime particulier": u"Mixte",
                },
                xFunction = lambda x: Load.float_comma(x.split(',')[1]),
                yFunction = lambda y: Load.float_comma(y.split(',')[0])
            ),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": ["bicycle_parking",
                                        "motorcycle_parking"]}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "motorcycle_parking", "bicycle": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = tag_mapping )))
