#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Vincent Bergeot 2017                                       ##
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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Recycling_FR_sitcom(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"2042", "class": 31, "level": 3, "tag": ["missing_official", "recycling"], "desc": T_(u"SITCOM recycling not integrated") }
        self.possible_merge   = {"item":"2044", "class": 33, "level": 3, "tag": ["possible_merge", "recycling"], "desc": T_(u"SITCOM recycling, integration suggestion") }
        self.update_official  = {"item":"2045", "class": 34, "level": 3, "tag": ["update_official", "recycling"], "desc": T_(u"SITCOM recycling update") }
        Analyser_Merge.__init__(self, config, logger,
            u"http://www.sitcom40.fr/",
            u"Emplacements d'apport volontaire",
            CSV(Source(attribution = u"Sitcom Côte Sud Landes", millesime = "07/2017",
                    file = "recycling_FR_sitcom.csv.bz2")),
            Load("Y", "X", # lat/lon inverted
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling", "recycling_type": "container"}),
                osmRef = "ref:FR:SITCOM",
                conflationDistance = 200,
                generate = Generate(
                    static1 = {
                        "amenity": "recycling",
                        "recycling_type": "container"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:SITCOM": "Cle"},
                    text = lambda tags, fields: {"en": fields["Nom du point"]} )))
