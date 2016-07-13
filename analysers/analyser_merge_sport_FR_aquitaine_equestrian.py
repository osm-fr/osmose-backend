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

from Analyser_Merge import Analyser_Merge, Source, JSON, Load, Mapping, Select, Generate


class Analyser_Merge_Sport_FR_Aquitaine_Equestrian(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8170", "class": 1, "level": 3, "tag": ["merge", "sport"], "desc": T_(u"Gironde equestrian spot not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "http://catalogue.datalocale.fr/dataset/liste-des-activites-de-pratique-equestre-en-aquitaine",
            u"Liste des activités de pratique équestre en aquitaine",
            JSON(Source(fileUrl = "http://wcf.tourinsoft.com/Syndication/aquitaine/3db03dc1-a2aa-415f-b219-53f70d387b53/Objects?$format=json"),
                extractor = lambda json: json['d']),
            Load("LON", "LAT",
                xFunction = self.degree,
                yFunction = self.degree),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"sport": "equestrian"}),
                conflationDistance = 1000,
                generate = Generate(
                    static = {
                        "source": u"Réseau SIRTAQUI - Comité Régional de Tourisme d'Aquitaine - www.sirtaqui-aquitaine.com - 06/2016",
                        "sport": "equestrian"},
                    mapping = {
                        "name": "NOMOFFRE",
                        "ref:FR:CRTA": "SyndicObjectID",
                        "website": lambda fields: None if not fields["URL"] else fields["URL"] if fields["URL"].startswith('http') else 'http://' + fields["URL"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x != "None", [fields["NOMOFFRE"], fields["AD1"], fields["AD1SUITE"], fields["AD2"], fields["AD3"], fields["CP"], fields["COMMUNE"]]))} )))
