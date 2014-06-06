#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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


class Analyser_Merge_Recycling_FR_capp_clothes(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8120", "class": 21, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"CAPP clothes recycling not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=7",
                name = u"Point d'apport volontaire du textile : Relais 64 sur la CAPP",
                file = "recycling_FR_capp_clothes.csv.bz2",
                encoding = "ISO-8859-15"),
            Load("X", "Y", table = "capp_recycling_clothes",
                xFunction = self.float_comma,
                yFunction = self.float_comma,
                select = {"USAGE_": "En service"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                conflationDistance = 100,
                generate = Generate(
                    static = {
                        "source": u"Communauté d'Agglomération Pau-Pyrénées - 01/2013",
                        "amenity": "recycling",
                        "recycling:clothes": "yes",
                        "recycling_type": "container"} )))
