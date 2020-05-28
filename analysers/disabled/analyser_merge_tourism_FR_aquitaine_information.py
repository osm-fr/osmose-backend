#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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


class Analyser_Merge_Tourism_FR_Aquitaine_information(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8010, id = 21, level = 3, tags = ['merge', 'tourism'],
            title = T_('Aquitaine tourism information not integrated'))
        self.def_class_possible_merge(item = 8011, id = 23, level = 3, tags = ['merge', 'tourism'],
            title = T_('Aquitaine tourism information, integration suggestion'))

        self.init(
            u"http://catalogue.datalocale.fr/dataset/liste-points-infos-tourisme-aquitaine",
            u"Liste des points infos tourisme en Aquitaine ",
            JSON(Source(attribution = u"Réseau SIRTAQUI - Comité Régional de Tourisme d'Aquitaine - www.sirtaqui-aquitaine.com", millesime = "08/2018",
                    fileUrl = u"http://wcf.tourinsoft.com/Syndication/aquitaine/0c7230f7-94ec-473b-9dce-e4cf38fedb44/Objects?$format=json"),
                extractor = lambda json: json['d']),
            Load("LON", "LAT",
                xFunction = self.degree,
                yFunction = self.degree),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "information"}),
                conflationDistance = 1000,
                generate = Generate(
                    static1 = {
                        "tourism": "information",
                        "information": "office"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": "NOMOFFRE",
                        "ref:FR:CRTA": "SyndicObjectID",
                        "website": lambda fields: None if not fields["URL"] else fields["URL"] if fields["URL"].startswith('http') else 'http://' + fields["URL"]},
                    mapping2 = {"phone": "TEL"},
                    text = lambda tags, fields: {"en": u', '.join(filter(lambda x: x, [fields["NOMOFFRE"], fields["AD1"], fields["AD1SUITE"], fields["AD2"], fields["AD3"], fields["CP"], fields["COMMUNE"]]))} )))
