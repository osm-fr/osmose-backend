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

from .Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Equipment_FR_Montpellier_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 6, level = 3, tags = ['merge', 'public equipment'],
            title = T_f('{0} toilets not integrated', 'Montpellier'))

        self.init(
            u"http://data.montpellier3m.fr/dataset/toilettes-publiques-de-montpellier",
            u"Toilettes publiques",
            GeoJSON(Source(attribution = u"Montpellier Mediterranée Métropole", millesime = "05/2019",
                    fileUrl = u"http://data.montpellier3m.fr/sites/default/files/ressources/MMM_MTP_WC_Publics.json")),
            Load("geom_x", "geom_y",
                select = {u'enservice': u'En Service'}),
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
                        "name": lambda res: res['nom'] if res['nom'] else None,
                        "operator": lambda res: res['gestion'] if res['gestion'] else None,
                        "wheelchair": lambda res: "yes" if res['pmr'] == u'PMR' else "no" if res['pmr'] == u'non PMR' else None } )))
