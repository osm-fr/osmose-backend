#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2020                                          ##
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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate
from modules import reaccentue

class Analyser_merge_defibrillators_FR_aedmap(Analyser_Merge):
    def cleanName(self, name):
        return reaccentue.reaccentue(name) if name.upper() == name else name

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 130, level = 3, tags = ["merge"],
            title = T_("Defibrillator not integrated"))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/defibrillateurs-publics/",
            u"Défibrillateurs publics",
            CSV(Source(attribution = u"AEDMAP France",
                    fileUrl = u"https://files.pavie.info/depot/remote/aedmap_merge.csv")),
            Load("Longitude", "Latitude",
                 xFunction = self.float_comma,
                 yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": lambda res: self.cleanName(res["Nom"]) if res["Nom"] else None
                    },
                    text = lambda tags, fields: {"en": " ".join(filter(lambda x: x, [
                        fields["Nom"],
                        fields["Adresse"],
                        fields["Adresse 2"],
                        fields["Code postal"],
                        fields["Ville"],
                    ]))} )))
