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


class Analyser_merge_defibrillators_FR_montfort(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 70, level = 3, tags = ['merge', "emergency", "fix:picture", "fix:survey"],
            title = T_('Defibrillator not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/defibrillateurs-montfort-communaute-1/",
            "Défibrillateurs Montfort Communauté",
            CSV(SourceDataGouv(
                attribution="Défibrillateurs Montfort Communauté",
                dataset="5baca9798b4c411829c4659a",
                resource="ad484c5d-0566-4bd4-9bb4-1ca418031968")),
            Load_XY("X","Y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["LOC"], fields["ACCES"], fields["DETAIL"], fields["ADRESSE"]]))} )))
