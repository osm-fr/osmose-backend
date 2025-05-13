#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights XioNoX 2025                                                ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, SHP, LoadGeomCentroid, Conflate, Select, Mapping


class analyser_merge_advertising_board_FR_Brest(Analyser_Merge_Point):
    def __init__(self, config, logger=None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item=8360, id=1, level=3, tags=['merge', 'public equipment', 'fix:survey', 'fix:picture'],
                                        title=T_('Advertising board in OpenData but not in OSM'))
        self.def_class_missing_osm(item=7361, id=2, level=3, tags=['merge'],
                                   title=T_('Advertising board in OSM but not in OpenData'))
        self.def_class_possible_merge(item=8361, id=3, level=3, tags=['merge'],
                                      title=T_('Advertising board in both OpenData and OSM, integration suggestion'))
        self.init(
            "https://www.data.gouv.fr/fr/datasets/panneaux-dexpression-libre/",
            "Position des panneaux d'expression libre sur le territoire de Brest métropole.",
            SHP(
                SourceDataGouv(
                    attribution="data.gouv.fr:Brest Métropole",
                    dataset="648095d82697b64f06b91860",
                    resource="286dfad1-406c-4970-a2a3-ea6eb855f960"),
                zip="ESP_MOB_PanneauxExpresLibre.shp"),
            LoadGeomCentroid(),
            Conflate(
                select=Select(
                    types=["nodes", "ways"],
                    tags={"advertising": "board"}),
                conflationDistance=10,
                mapping=Mapping(
                    static1={"advertising": "board",
                             "access": "yes"},
                    static2={"source": self.source,
                             "land_property": "public",
                             "animated": "no",
                             "man_made": "advertising",
                             "message": "opinions;non_profit;showbiz"},
                    mapping1={
                        "display_surface": lambda res: res.get("SURFACE")
                    })))
