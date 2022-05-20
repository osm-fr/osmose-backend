#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Nicolas Bétheuil 2019                                      ##
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
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_merge_defibrillators_FR_saintmalo(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 80, level = 3, tags = ['merge', "emergency", "fix:picture", "fix:survey"],
            title = T_('Defibrillator not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/defibrillateurs-1/",
            "Ville de Saint-Malo",
            CSV(
                SourceDataGouv(
                    attribution="Ville de Saint-Malo",
                    dataset="54295e4188ee380326a5915d",
                    resource="75e18892-529f-4037-b38f-a9e4d9c39a91",
                    encoding="iso-8859-14"),
                separator=";"),
            Load_XY("XCOORD", "YCOORD", srid = 2154),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source} )))
