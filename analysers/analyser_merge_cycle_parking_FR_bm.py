#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Éric Gillet 2021                                           ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, SHP, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_Bicycle_Parking_FR_Bordeaux_Metropole(Analyser_Merge):
    def __init__(self, config, logger=None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(
            item=8150, id=50, level=3, tags=['merge', 'public equipment', 'bicycle'],
            title=T_('Bordeaux Metropole bicycle parking not integrated'))
        self.init(
            "https://opendata.bordeaux-metropole.fr/explore/dataset/st_arceau_p",
            "Mobiliers urbains : Stationnement deux-roues",
            SHP(SourceOpenDataSoft(
                attribution="Bordeaux Métropole",
                url="https://opendata.bordeaux-metropole.fr/explore/dataset/st_arceau_p",
                format="shp",
                zip='st_arceau_p.shp'
            )),
            LoadGeomCentroid(
                select={
                    "typologie": [None, "ARCEAU_VELO_CARGO"],
                }
            ),
            Conflate(
                select=Select(
                    types=["nodes", "ways"],
                    tags={"amenity": "bicycle_parking"}),
                conflationDistance=20,
                mapping=Mapping(
                    static1={"amenity": "bicycle_parking"},
                    static2={"source": self.source},
                    mapping1={
                        "capacity": lambda res: None if res["nombre"] in (None, "0") else str(int(res["nombre"])*2),
                        "cargo_bike": lambda res: "yes" if res["typologie"] == "ARCEAU_VELO_CARGO" else None,
                    }
                )
            )
        )


class Analyser_Merge_Motorcycle_Parking_FR_Bordeaux_Metropole(Analyser_Merge):
    def __init__(self, config, logger=None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(
            item=8150, id=60, level=3, tags=['merge', 'public equipment', 'motorcycle'],
            title=T_('Bordeaux Metropole motorcycle parking not integrated'))
        self.init(
            "https://opendata.bordeaux-metropole.fr/explore/dataset/st_arceau_p",
            "Mobiliers urbains : Stationnement deux-roues",
            SHP(SourceOpenDataSoft(
                attribution="Bordeaux Métropole",
                url="https://opendata.bordeaux-metropole.fr/explore/dataset/st_arceau_p",
                format="shp",
                zip='st_arceau_p.shp'
            )),
            LoadGeomCentroid(
                select={
                    "typologie": "ARCEAU_MOTO",
                }
            ),
            Conflate(
                select=Select(
                    types=["nodes", "ways"],
                    tags={"amenity": "motorcycle_parking"}),
                conflationDistance=20,
                mapping=Mapping(
                    static1={"amenity": "motorcycle_parking"},
                    static2={"source": self.source},
                    mapping1={
                        "capacity": lambda res: None if res["nombre"] in (None, "0") else str(int(res["nombre"])*2),
                    }
                )
            )
        )
