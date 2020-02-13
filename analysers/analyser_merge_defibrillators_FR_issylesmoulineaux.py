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


class Analyser_merge_defibrillators_FR_issylesmoulineaux(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item = 8370, id = 10, level = 3, tags = ['merge'],
            title = T_('Defibrillator not integrated'))

        self.init(
            u"https://data.issy.com/explore/dataset/defibrillateurs-issy-les-moulineaux/information",
            u"Défibrillateurs à la Ville d'Issy-les-Moulineaux",
            CSV(Source(attribution = u"data.gouv.fr:Ville d'Issy-les-Moulineaux",
                    fileUrl = u"https://data.issy.com/explore/dataset/defibrillateurs-issy-les-moulineaux/download/?format=csv&timezone=Europe/Berlin"),
                separator = u";"),
            Load("coordonnees_geographiques", "coordonnees_geographiques",
                xFunction = lambda x: x.split(",")[1].strip(),
                yFunction = lambda y: y.split(",")[0].strip()),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["titre"], fields["localisation"], fields["acces"], fields["horaires"]]))} )))
