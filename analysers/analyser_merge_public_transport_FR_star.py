#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jérôme Amagat <jerome.amagat gmail.com> 2016               ##
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


class Analyser_Merge_Public_Transport_FR_Star(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8040", "class": 81, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"Star stop not integrated") }
        self.possible_merge   = {"item":"8041", "class": 83, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"Star stop, integration suggestion") }
        self.update_official  = {"item":"8042", "class": 84, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"Star stop update") }
        Analyser_Merge.__init__(self, config, logger,
            "https://data.rennesmetropole.fr/explore/dataset/topologie-des-points-darret-de-bus-du-reseau-star",
            u"Topologie des points d'arrêt de bus du réseau STAR",
            CSV(Source(attribution = u"Keolis Rennes", millesime = "09/2016",
                    fileUrl = "https://data.rennesmetropole.fr/explore/dataset/topologie-des-points-darret-de-bus-du-reseau-star/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = ";"),
            Load("Coordonnées", "Coordonnées",
                xFunction = lambda x: x.split(",")[1].strip(),
                yFunction = lambda y: y.split(",")[0].strip()),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                osmRef = "ref:FR:Star",
                conflationDistance = 10,
                generate = Generate(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "stop_position",
                        "bus": "yes",
                        "network": "Star"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:Star": "Code",
                        "name": "Nom",
                        "wheelchair": lambda res: "yes" if res["Accessible aux PMR"] == "true" else "no" if res["Accessible aux PMR"] == "false" else None,
                        "shelter": lambda res: "yes" if res["Mobilier"] and "Abris" in res["Mobilier"] else "no" if res["Mobilier"] == "Poteau" else None},
                    text = lambda tags, fields: {"en": u"Star stop of %s" % fields["Nom"], "fr": u"Arrêt Star de %s" % fields["Nom"]} )))
