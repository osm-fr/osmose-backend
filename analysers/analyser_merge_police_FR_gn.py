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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Police_FR_gn(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8190", "class": 1, "level": 3, "tag": ["merge"], "desc": T_(u"Police/\"Gendarmerie\" not integrated") }
        self.possible_merge   = {"item":"8191", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Police/\"Gendarmerie\", integration suggestion") }
        self.update_official  = {"item":"8192", "class": 4, "level": 3, "tag": ["merge"], "desc": T_(u"Police/\"Gendarmerie\" update") }

        Analyser_Merge.__init__(self, config, logger,
            "https://www.data.gouv.fr/fr/datasets/liste-des-unites-de-gendarmerie-accueillant-du-public-comprenant-leur-geolocalisation-et-leurs-horaires-douverture/",
            u"Liste des points d'accueil de la gendarmerie nationale",
            CSV(Source(attribution = u"data.gouv.fr:Ministère de l'Intérieur", millesime = "10/2018",
                    fileUrl = "https://www.data.gouv.fr/fr/datasets/r/d6a43ef2-d302-4456-90e9-ff2c47cac562"),
                separator = ";"),
            Load("geocodage_x_GPS", "geocodage_y_GPS",
                where = lambda row: u"Centre d'information et de recrutement" not in row["service"] and u"motorisé" not in row["service"] ),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "police"}),
                conflationDistance = 500,
                osmRef = "ref:FR:GendarmerieNationale",
                generate = Generate(
                    static1 = {
                        "amenity": "police",
                        "name": "Gendarmerie nationale",
                        "police:FR": "gendarmerie",
                        "operator:wikidata": "Q1422336",
                        "seasonal": lambda fields: "yes" if "Poste provisoire" in fields["service"] else None,
                        "operator": "Gendarmerie nationale"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:GendarmerieNationale": "identifiant_public_unite"},
                    mapping2 = {
                        "phone": "telephone",
                        "official_name": "service",
                    },
                text = lambda tags, fields: {"en": u"%s, %s" % (fields["service"], fields["adresse_geographique"])} )))
