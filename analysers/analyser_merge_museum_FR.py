#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jérôme Amagat 2019                                         ##
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
import re

class Analyser_Merge_Museum_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8010, id = 31, level = 3, tags = ['merge'],
            title = T_('Museum not integrated'))
        self.def_class_possible_merge(item = 8011, id = 33, level = 3, tags = ['merge'],
            title = T_('Museum, integration suggestion'))

        re_phone = re.compile(u"^0[0-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2}$")

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/musees-de-france-base-museofile/",
            u"Musées de France : base Muséofile",
            CSV(Source(attribution = u"Ministère de la Culture - Muséofile", millesime = "09/2019",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/5ccd6238-4fb0-4b2c-b14a-581909489320"),
                separator = u';'),
            Load("geolocalisation", "geolocalisation",
                 where = lambda row: row["geolocalisation"],
                 xFunction = lambda x: x and x.split(',')[1],
                 yFunction = lambda y: y and y.split(',')[0]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"tourism": "museum"}),
                conflationDistance = 300,
                osmRef = u"ref:FR:museofile",
                generate = Generate(
                    static1 = {"tourism": "museum"},
                    static2 = {"source": self.source},
                    mapping1 = {u"ref:FR:museofile": "Identifiant"},
                    mapping2 = {
                        "website": lambda res: None if not res["URL"] else res["URL"] if res["URL"].startswith('http') else 'http://' + res["URL"],
                        "phone": lambda res: u"+33 " + res[u"Téléphone"][1:] if res[u"Téléphone"] and re_phone.match(res[u"Téléphone"]) else None,
                        "name": lambda res: res["Nom usage"][0].upper() + res["Nom usage"][1:] if res["Nom usage"] else res["Nom officiel"][0].upper() + res["Nom officiel"][1:] if res["Nom officiel"] else None,
                        "official_name": lambda res: res["Nom officiel"][0].upper() + res["Nom officiel"][1:] if res["Nom usage"] and res["Nom officiel"].lower() != res["Nom usage"].lower() else None},
                    text = lambda tags, fields: {"en": ' '.join(filter(lambda x: x, [fields["Adresse"], fields["Code Postal"], fields["Ville"]]))} )))
