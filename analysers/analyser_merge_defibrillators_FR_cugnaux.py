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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, GeoJSON, Load_XY, Conflate, Select, Mapping


class Analyser_merge_defibrillators_FR_cugnaux(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 110, level = 3, tags = ['merge', "emergency", "fix:picture", "fix:survey"],
            title = T_('Defibrillator not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/defibrillateurs-9/",
            "Défibrillateurs",
            GeoJSON(SourceDataGouv(
                attribution="Mairie de Cugnaux",
                dataset="58d284c0c751df3538a279f1",
                resource="d6820eaf-f988-47c4-bc6f-634e0a4da013")),
            Load_XY("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source} )))
