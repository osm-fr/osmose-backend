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
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 5, level = 3, tags = ['merge', 'public equipment'],
            title = T_f('{0} toilets not integrated', 'Nantes Métropole'))

        self.init(
            u"https://data.nantesmetropole.fr/explore/dataset/244400404_toilettes-publiques-nantes-metropole",
            u"Toilettes publiques de Nantes Métropole",
            JSON(Source(attribution = u"Nantes Métropole", millesime = "11/2016",
                    fileUrl = u"https://data.nantesmetropole.fr/explore/dataset/244400404_toilettes-publiques-nantes-metropole/download/?format=json&timezone=Europe/Berlin"),
                extractor = lambda json: map(lambda j: j['fields'], json)),
            Load("location", "location",
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
                        "name": 'nom',
                        "ref": 'id',
                        "wheelchair": lambda res: "yes" if res['acces_pmr'] == u'oui' else "no" if res['acces_pmr'] == u'non' else None } )))
