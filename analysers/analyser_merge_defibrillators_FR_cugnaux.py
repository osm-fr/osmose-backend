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


class Analyser_merge_defibrillators_FR_cugnaux(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8370", "class": 90, "level": 3, "tag": ["merge"], "desc": T_(u"Defibrillator not integrated") }

        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/defibrillateurs-9/",
            u"Défibrillateurs",
            GeoJSON(Source(attribution = u"Mairie de Cugnaux",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/d6820eaf-f988-47c4-bc6f-634e0a4da013"),
                    ),
            Load("geom_x", "geom_y"),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {
                        "emergency": "defibrillator",
                    },
                    static2 = {"source": self.source},)))
