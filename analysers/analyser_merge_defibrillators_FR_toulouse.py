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

from .Analyser_Merge import Analyser_Merge, Source, SHP, Load, Mapping, Select, Generate


class Analyser_merge_defibrillators_FR_toulouse(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 40, level = 3, tags = ['merge'],
            title = T_('Defibrillator not integrated'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/localisation-des-defibrillateurs-toulouse/",
            u"Localisation des défibrillateurs - Toulouse",
            SHP(Source(attribution = u"data.gouv.fr:Toulouse métropole",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/15cbc8a3-411b-4690-894a-d84a7e6cac7b", zip = "defibrillateurs.shp")),
            Load(("ST_X(ST_Centroid(geom))",), ("ST_Y(ST_Centroid(geom))",)),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source} )))
