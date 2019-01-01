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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

STANDS_TYPES = {
    "Arceau autre": "stands",
    "Arceau St-Germain": "wide_stands",
    "Epingle vélo": "stands",
    "Sans": "floor",
}
tag_mapping = {
    "capacity": (
        lambda res: None if res["PLACAL"] in (None, "0") else res["PLACAL"]
    ),
    "bicycle_parking": (
        lambda res: STANDS_TYPES.get(res['TYPEMOB'], None)
    )
}


class Analyser_Merge_Bicycle_Parking_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8150", "class": 21, "level": 3, "tag":
                                 ["merge", "public equipment", "cycle"],
                                 "desc": T_(u"Paris bicycle parking not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/information/",
            u"Stationnement sur voie publique - emplacements vélos",
            CSV(Source(attribution = u"Ville de Paris", millesime = "02/2018",
                    fileUrl = u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = ";"),
            Load("geo_point_2d", "geo_point_2d",
                select = {
                    u"Régime prioritaire": u"2 ROUES",
                    u"Régime particulier": u"Vélos",
                },
                xFunction = lambda x: self.float_comma(x.split(',')[1]),
                yFunction = lambda y: self.float_comma(y.split(',')[0])
            ),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 20,
                generate = Generate(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = tag_mapping )))


class Analyser_Merge_Motorcycle_Parking_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8150", "class": 31, "level": 3, "tag":
                                 ["merge", "public equipment", "motorcycle"],
                                 "desc": T_(u"Paris motorcycle parking not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/information/",
            u"Stationnement sur voie publique - emplacements motos",
            CSV(Source(attribution = u"Ville de Paris", millesime = "02/2018",
                    fileUrl = u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = ";"),
            Load("geo_point_2d", "geo_point_2d",
                select = {
                    u"Régime prioritaire": u"2 ROUES",
                    u"Régime particulier": u"Motos",
                },
                xFunction = lambda x: self.float_comma(x.split(',')[1]),
                yFunction = lambda y: self.float_comma(y.split(',')[0])
            ),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "motorcycle_parking"}),
                conflationDistance = 20,
                generate = Generate(
                    static1 = {"amenity": "motorcycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "capacity": lambda res: None if res["PLACAL"] in (None, "0") else res["PLACAL"],
                    })))


class Analyser_Merge_Bicycle_Motorcycle_Parking_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8150", "class": 41, "level": 3, "tag":
                                 ["merge", "public equipment", "bicycle", "motorcycle"],
                                 "desc": T_(u"Paris shared motorcycle/motorcycle parking not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/information/",
            u"Stationnement sur voie publique - emplacements deux roues",
            CSV(Source(attribution = u"Ville de Paris", millesime = "02/2018",
                    fileUrl = u"https://opendata.paris.fr/explore/dataset/stationnement-voie-publique-emplacements/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = ";"),
            Load("geo_point_2d", "geo_point_2d",
                select = {
                    u"Régime prioritaire": u"2 ROUES",
                    u"Régime particulier": u"Mixte",
                },
                xFunction = lambda x: self.float_comma(x.split(',')[1]),
                yFunction = lambda y: self.float_comma(y.split(',')[0])
            ),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": ["bicycle_parking",
                                        "motorcycle_parking"]}),
                conflationDistance = 20,
                generate = Generate(
                    static1 = {"amenity": "motorcycle_parking", "bicycle": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = tag_mapping )))
