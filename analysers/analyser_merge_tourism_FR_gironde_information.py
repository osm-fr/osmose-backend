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


class Analyser_Merge_Tourism_FR_Gironde_information(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8010", "class": 21, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde tourism information not integrated") }
        self.possible_merge   = {"item":"8011", "class": 23, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde tourism information, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            "http://www.datalocale.fr/drupal7/dataset/liste-office-tourisme-cdt33",
            u"Liste des Offices de Tourisme et Syndicats d'initiative de Gironde",
            CSV(Source(file = "tourism_FR_gironde_information.csv.bz2")),
            Load("LONGITUDE", "LATITUDE", table = "gironde_tourism_information"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "information"}),
                conflationDistance = 1000,
                generate = Generate(
                    static = {
                        "source": u"Observatoire du comité départemental du Tourisme de la Gironde - 09/2013",
                        "tourism": "information",
                        "information": "office"},
                    mapping = {
                        "name": "RAISON_SOCIALE",
                        "phone": "TELEPHONE",
                        "siteweb": "SITE_WEB"},
                    text = lambda tags, fields: {"en": ", ".join(filter(lambda e: e, [fields["RAISON_SOCIALE"], fields["ADRESSE"], fields["ADRESSE_SUITE"], fields["COMMUNE"]]))} )))
