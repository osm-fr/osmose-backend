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

from .Analyser_Merge import Analyser_Merge, Source, SHP, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Transport_FR_TBM(Analyser_Merge):
    def __init__(self, config, logger = None):
        place = "TBM"
        self.missing_official = {"item":"8040", "class": 51, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"%s stop not integrated", place) }
        self.possible_merge   = {"item":"8041", "class": 53, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"%s stop, integration suggestion", place) }
        Analyser_Merge.__init__(self, config, logger,
            u"http://data.bordeaux-metropole.fr/data.php?themes=10",
            u"Arrêt physique sur le réseau",
            SHP(Source(attribution = u"Bordeaux Métropole", millesime = "07/2016",
                fileUrl = u"http://data.bordeaux-metropole.fr/files.php?gid=39&format=2", zip = "TB_ARRET_P.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154,
                select = {"RESEAU": [None, "BUS"]}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes",
                        "network": "TBM"},
                    static2 = {"source": self.source},
                    mapping2 = {
                        "name": lambda res: res['NOMARRET'],
                        "shelter": lambda res: "yes" if res["MOBILIE1"] and "abribus" in res["MOBILIE1"].lower() else "no" if res["MOBILIE1"] and "poteau" in res["MOBILIE1"].lower() else None},
                    text = lambda tags, fields: T_(u"%s stop %s", place, fields["NOMARRET"]) )))
