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

from .Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load, Mapping, Select, Generate


class Analyser_merge_defibrillators_FR_lorient(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 100, level = 3, tags = ['merge'],
            title = T_('Defibrillator not integrated'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/localisation-des-defibrillateurs-municipaux-dae-ville-de-lorient/",
            u"Localisation des défibrillateurs municipaux (DAE) - Ville de Lorient",
            GeoJSON(Source(attribution = u"Ville de Lorient",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/01f2a133-4929-4001-906c-412f682d0d59")),
            Load("geom_x", "geom_y"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["emplacement"]]))} )))
