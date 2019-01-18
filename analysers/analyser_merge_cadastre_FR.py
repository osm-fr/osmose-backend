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


class _Analyser_Merge_Cadastre_Point_ID_calvaire_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"9992", "class": 1, "level": 3, "tag": ["missing_official"], "desc": T_(u"Misc not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/58e5924b88ee3802ca255566/",
            u"PCI Vecteur (Plan Cadastral Informatisé) - Point_id",
            CSV(Source(attribution = u"Ministère de l’Economie et des Finances", millesime = "10/2017", file = "cadastre_TPOINT_id_clean.csv.bz2")),
            Load("X", "Y",
                select = {"tex": "%calvaire%"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"historic": "wayside_cross"}),
                conflationDistance = 200,
                generate = Generate(
                    static1 = {"historic": "wayside_cross"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": u"%s, confidence: %s" % (fields["tex"], 1)} )))

class Analyser_Merge_Cadastre_Point_ID_borne_incendie_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"9982", "class": 2, "level": 3, "tag": ["missing_official"], "desc": T_(u"Misc not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/58e5924b88ee3802ca255566/",
            u"PCI Vecteur (Plan Cadastral Informatisé) - Point_id",
            CSV(Source(attribution = u"Ministère de l’Economie et des Finances", millesime = "10/2017", file = "cadastre_TPOINT_id_clean.csv.bz2")),
            Load("X", "Y",
                select = {"tex": "%borne incendie%"}),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "ire_hydrant"}),
                conflationDistance = 200,
                generate = Generate(
                    static1 = {"emergency": "fire_hydrant"},
                    static2 = {"source": self.source},
                text = lambda tags, fields: {"en": u"%s, confidence: %s" % (fields["tex"], 1)} )))
