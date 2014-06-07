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


class Analyser_Merge_Tourism_FR_Gironde_Caravan(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8140", "class": 1, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde caravan site not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.datalocale.fr/drupal7/file/liste-aire-publique-camping-cdt33-1",
                name = u"Liste des aires publiques pour camping-cars de Gironde",
                file = "tourism_FR_gironde_caravan.csv.bz2"),
            Load("LONGITUDE", "LATITUDE", table = "gironde_caravan"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "caravan_site"}),
                conflationDistance = 500,
                generate = Generate(
                    static = {
                        "source": u"Observatoire du comité départemental du Tourisme de la Gironde - 09/2013",
                        "tourism": "caravan_site"},
                    mapping = {"name": "NOM"},
                    text = lambda tags, fields: {"en": u"Caravan site of %s" % fields["NOM"], "fr": u"Site camping-cars de %s" % fields["NOM"]} )))


class Analyser_Merge_Tourism_FR_Gironde_Camp(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8140", "class": 11, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde camp site not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.datalocale.fr/drupal7/file/liste-campings-classes-cdt33-1",
                name = u"Liste des campings classes et anciennement classes de Gironde",
                file = "tourism_FR_gironde_camp.csv.bz2"),
            Load("LONGITUDE", "LATITUDE", table = "gironde_camp"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "camp_site"}),
                conflationDistance = 300,
                generate = Generate(
                    static = {
                        "source": u"Observatoire du comité départemental du Tourisme de la Gironde - 09/2013",
                        "tourism": "camp_site"},
                    mapping = {
                        "name": "RAISON_SOCIALE",
                        "stars": lambda res: res["CATEGORIE"][0] if res["CATEGORIE"][0].isdigit() else None,
                        "website": "SITE_WEB"},
                    text = lambda tags, fields: {"en": u"Camp site of %s" % fields["RAISON_SOCIALE"], "fr": u"Camping de %s" % fields["RAISON_SOCIALE"]} )))
