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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_defibrillators_FR_paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 30, level = 3, tags = ['merge'],
            title = T_('Defibrillator not integrated'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/batiments-publics-equipes-de-defibrillateurs-a-paris/",
            u"Défibrillateurs à Paris",
            CSV(Source(attribution = u"data.gouv.fr:Mairie de Paris", millesime = "23/04/2018",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/d2b94d3d-977d-4dcb-ab8c-77e2568de736"),
                separator = u";"),
            Load("longitude", "latitude"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["Type"], fields["Nom"], fields["Addresse"]]))} )))
