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


class Analyser_merge_defibrillators_FR_gers(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = self.def_class(item = 8370, id = 90, level = 3, tags = ['merge'],
            title = T_('Defibrillator not integrated'))

        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/inventaire-des-defibrillateurs-automatises-externes-dae-dans-le-gers/#",
            u"Inventaire des Défibrillateurs Automatisés Externes (DAE) dans le Gers",
            GeoJSON(Source(attribution = u"Région Occitanie / Pyrénées Méditerranée",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/cc36c26e-e782-47bf-8fd6-a03aa459e8d0")),
            Load("geom_x", "geom_y"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["etablissement"], fields["horaire"], fields["detail"]]))} )))
