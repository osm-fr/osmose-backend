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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_merge_defibrillators_FR_issylesmoulineaux(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 10, level = 3, tags = ['merge', "emergency", "fix:picture", "fix:survey"],
            title = T_('Defibrillator not integrated'))

        self.init(
            "https://data.issy.com/explore/dataset/defibrillateurs-issy-les-moulineaux/information",
            "Défibrillateurs à la Ville d'Issy-les-Moulineaux",
            CSV(
                SourceOpenDataSoft(
                    attribution="data.gouv.fr:Ville d'Issy-les-Moulineaux",
                    url="https://data.issy.com/explore/dataset/defibrillateurs-issy-les-moulineaux")),
            Load_XY("Coordonnées géographiques", "Coordonnées géographiques",
                xFunction = lambda x: x.split(",")[1].strip(),
                yFunction = lambda y: y.split(",")[0].strip()),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["Titre"], fields["Localisation"], fields["Accès"], fields["Horaires"]]))} )))
