#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2017                                          ##
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

from .Analyser_Merge import Analyser_Merge, Source, JSON, Load, Mapping, Select, Generate
import json


class Analyser_Merge_Public_Equipment_FR_Nantes_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8180", "class": 5, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"%s toilets not integrated", "Nantes") }
        Analyser_Merge.__init__(self, config, logger,
            u"http://data.nantes.fr/donnees/detail/toilettes-publiques-de-nantes-metropole/",
            u"Toilettes publiques",
            JSON(Source(attribution = u"Nantes Métropole", millesime = "11/2016",
                    fileUrl = u"http://data.nantes.fr/api/publication/24440040400129_NM_NM_00170/Toilettes_publiques_nm_STBL/content/?format=json"),
                extractor = lambda json: json['data']),
            Load("_l", "_l",
                xFunction = lambda c: c and json.loads(c)[1],
                yFunction = lambda c: c and json.loads(c)[0]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "toilets",
                        "access": "public"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": lambda res: res['geo.name'] if res['geo.name'] else None,
                        "ref": lambda res: res['ID'] if res['ID'] else None,
                        "wheelchair": lambda res: "yes" if res['Acces_PMR'] == u'oui' else "no" if res['Acces_PMR'] == u'non' else None } )))
