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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping
import re

class Analyser_Merge_Museum_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8010, id = 31, level = 3, tags = ['merge', 'tourism', 'fix:survey', 'fix:picture'],
            title = T_('Museum not integrated'))
        self.def_class_possible_merge(item = 8011, id = 33, level = 3, tags = ['merge', 'tourism', 'fix:survey', 'fix:picture', 'fix:chair'],
            title = T_('Museum, integration suggestion'))

        re_phone = re.compile("^0[0-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2}$")

        self.init(
            "https://www.data.gouv.fr/fr/datasets/musees-de-france-base-museofile/",
            "Musées de France : base Muséofile",
            CSV(
                SourceDataGouv(
                    attribution="Ministère de la Culture - Muséofile",
                    encoding="utf-8-sig",
                    dataset="5d12ee8206e3e762c0c89a4c",
                    resource="5ccd6238-4fb0-4b2c-b14a-581909489320"),
                separator=';'),
            Load_XY("coordonnees", "coordonnees",
                 where = lambda row: row["coordonnees"],
                 xFunction = lambda x: x and x.split(',')[1],
                 yFunction = lambda y: y and y.split(',')[0]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"tourism": "museum"}),
                conflationDistance = 300,
                osmRef = "ref:FR:museofile",
                mapping = Mapping(
                    static1 = {"tourism": "museum"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:museofile": "identifiant"},
                    mapping2 = {
                        "website": lambda res: None if not res["url"] else res["url"] if res["url"].startswith('http') else 'http://' + res["url"],
                        "phone": lambda res: "+33 " + res["telephone"][1:] if res["telephone"] and re_phone.match(res["telephone"]) else None,
                        "name": lambda res: res["nom_officiel"][0].upper() + res["nom_officiel"][1:] if res["nom_officiel"] else res["nom_officiel"][0].upper() + res["nom_officiel"][1:] if res["nom_officiel"] else None},
                    text = lambda tags, fields: {"en": ' '.join(filter(lambda x: x, [fields["adrl1_m"], fields["cp_m"], fields["ville_m"]]))} )))
