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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Car_Rental_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8160", "class": 1, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Paris Autolib' car rental not integrated") }
        self.missing_osm      = {"item":"7140", "class": 2, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Paris Autolib' car rental without ref:FR:Paris:DSP") }
        self.possible_merge   = {"item":"8161", "class": 3, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"Paris Autolib' car rental integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://opendata.paris.fr/explore/dataset/stations_et_espaces_autolib_de_la_metropole_parisienne",
                name = u"Stations et espaces AutoLib de la métropole parisienne",
                fileUrl = "http://opendata.paris.fr/explore/dataset/stations_et_espaces_autolib_de_la_metropole_parisienne/download/?format=csv&use_labels_for_header=true",
                csv = CSV(separator = ";")),
            Load("XY", "XY", table = "car_rental_FR_paris",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Mapping(
                select = Select(
                    types = ["ways",  "nodes"],
                    tags = {"amenity": "car_rental", "network": "Autolib'"}),
                osmRef = "ref:FR:Paris:DSP",
                conflationDistance = 200,
                generate = Generate(
                    static = {
                        "source": u"Mairie de Paris - 03/2016",
                        "amenity": "car_rental",
                        "network": "Autolib'",
                        "operator": "Autolib'",
                    },
                    mapping = {
                        "name": "ID Autolib",
                        "ref:FR:Paris:DSP": "ID DSP",
                        "capacity": lambda res: int(float(res["prises Autolib"]))} )))
