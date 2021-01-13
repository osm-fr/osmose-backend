#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2018                                         ##
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
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Police_FR_pn(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8190, id = 10, level = 3, tags = ['merge'],
            title = T_('Police not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/liste-des-services-de-police-accueillant-du-public-avec-geolocalisation/",
            "Liste des points d'accueil de la police nationale",
            CSV(
                SourceDataGouv(
                    attribution="data.gouv.fr:Ministère de l'Intérieur",
                    dataset="53ba5222a3a729219b7beade",
                    resource="2cb2f356-42b2-4195-a35c-d4e4d986c62b"),
                separator = ";"),
            Load("geocodage_x_GPS", "geocodage_y_GPS"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "police"}),
                conflationDistance = 500,
                mapping = Mapping(
                    static1 = {
                        "amenity": "police",
                        "name": "Police nationale",
                        "police:FR": "police",
                        "operator:wikidata": "Q121484",
                        "operator": "Police nationale"},
                    static2 = {"source": self.source},
                    mapping2 = {
                        "phone": "telephone",
                        "official_name": "service",
                    },
                text = lambda tags, fields: {"en": "{0}, {1}".format(fields["service"], fields["adresse_geographique"])} )))
