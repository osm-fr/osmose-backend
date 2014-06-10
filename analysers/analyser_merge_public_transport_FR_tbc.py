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

from Analyser_Merge import Analyser_Merge, Source, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Transport_FR_TBC(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8040", "class": 51, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TBC stop not integrated") }
        self.possible_merge   = {"item":"8041", "class": 53, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TBC stop, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://data.lacub.fr/data.php?themes=10",
                name = u"Arrêt physique sur le réseau",
                file = "public_transport_FR_tbc.csv.bz2",
                encoding = "ISO-8859-15"),
            Load("X", "Y", srid = 2154, table = "tbc",
                select = {"RESEAU": [None, "BUS"]}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                conflationDistance = 100,
                generate = Generate(
                    static = {
                        "source": u"Communauté Urbaine de Bordeaux - 03/2014",
                        "highway": "bus_stop",
                        "public_transport": "stop_position",
                        "bus": "yes",
                        "network": "TBC"},
                    mapping = {
                        "name": lambda res: res['NOMARRET'],
                        "shelter": lambda res: "yes" if res["MOBILIE1"] and "abribus" in res["MOBILIE1"].lower() else "no" if res["MOBILIE1"] and "poteau" in res["MOBILIE1"].lower() else None},
                    text = lambda tags, fields: {"en": u"TBC stop %s" % fields["NOMARRET"], "fr": u"Arrêt TBC %s" % fields["NOMARRET"]} )))
