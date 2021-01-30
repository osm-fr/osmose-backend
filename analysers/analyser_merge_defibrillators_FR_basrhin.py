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
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, GeoJSON, Load, Conflate, Select, Mapping


class Analyser_merge_defibrillators_FR_basrhin(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 20, level = 3, tags = ['merge'],
            title = T_('Defibrillator not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/donnee-thematique-localisation-des-defibrillateurs-automatiques-externes-dae-bas-rhin/",
            "DONNEE THEMATIQUE : Localisation des Défibrillateurs Automatiques Externes (DAE) - Bas-Rhin",
            GeoJSON(
                SourceDataGouv(
                    attribution="data.gouv.fr:Service Départemental d'Incendie et de Secours du Bas-Rhin",
                    dataset="59256d13c751df5259330037",
                    resource="b84312e9-b198-4f1d-b2ad-8e4df5b7cb5b")),
            Load("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["LOCALISATI"], fields["PRECISIONS"], fields["HORAIRES"]]))} )))
