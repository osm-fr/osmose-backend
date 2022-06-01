#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, SHP, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_Parking_FR_bm(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 31, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:survey'],
            title = T_('{0} parking not integrated', 'BM'))
        self.def_class_possible_merge(item = 8131, id = 33, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:chair'],
            title = T_('{0} parking integration suggestion', 'BM'))
        self.def_class_update_official(item = 8132, id = 34, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:chair'],
            title = T_('{0} parking update', 'BM'))

        self.init(
            'https://opendata.bordeaux-metropole.fr/explore/dataset/st_park_p',
            'Parking hors voirie',
            SHP(SourceOpenDataSoft(
                attribution="Bordeaux Métropole",
                url="https://opendata.bordeaux-metropole.fr/explore/dataset/st_park_p",
                format="shp",
                zip='st_park_p.shp')),
            LoadGeomCentroid(),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "parking"}),
                osmRef = "ref:FR:CUB",
                conflationDistance = 300,
                mapping = Mapping(
                    static1 = {"amenity": "parking"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:CUB": "ident",
                        "start_date": "an_serv",
                        "parking": lambda res: {"SURFACE": "surface", "ENTERRE": "underground"}.get(res["type"]),
                        "levels": "nb_niv",
                        "capacity": "np_total",
                        "capacity:disabled": "np_pmr",
                        "name": "nom",
                        "operator": "exploit"},
                    text = lambda tags, fields: {"en": "Parking {0}".format(fields["nom"])} )))


class Analyser_Merge_Parking_FR_bm_disabled(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 21, level = 3, tags = ['merge', 'parking'],
            title = T_('{0} parking for disabled not integrated', 'BM'))

        self.init(
            'https://opendata.bordeaux-metropole.fr/explore/dataset/grs_gigc_p',
            'Place de stationnement PMR',
            SHP(SourceOpenDataSoft(
                attribution="Bordeaux Métropole",
                url="https://opendata.bordeaux-metropole.fr/explore/dataset/grs_gigc_p",
                format="shp",
                zip="grs_gigc_p.shp")),
            LoadGeomCentroid(),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {
                        "amenity": "parking",
                        "capacity:disabled": None}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "parking",
                        "capacity:disabled": "yes"},
                    static2 = {"source": self.source} )))
