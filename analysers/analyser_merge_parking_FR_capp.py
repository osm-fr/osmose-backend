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


class Analyser_Merge_Parking_FR_capp(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 1, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CAPP parking not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=18",
                name = u"Parkings sur la CAPP",
                file = "parking_FR_capp.csv.bz2",
                encoding = "ISO-8859-15"),
            Load("X", "Y", table = "capp_parking",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "parking"}),
                conflationDistance = 200,
                generate = Generate(
                    static = {
                        "source": u"Communauté d'Agglomération Pau-Pyrénées - 01/2013",
                        "amenity": "parking"},
                    mapping = {
                        "name": "NOM",
                        "fee": lambda res: "yes" if res["Pay_grat"] == "Payant" else "no",
                        "capacity": lambda res: res["Places"] if res["Places"] != "0" else None,
                        "parking": lambda res: "surface" if res["Ouvrage"] == "Plein air" else "underground" if res["Ouvrage"] == "Souterrain" else None},
                    text = lambda tags, fields: {"en": u"Parking %s" % tags["name"]} )))


class Analyser_Merge_Parking_FR_capp_disabled(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 11, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CAPP parking disabled not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=21",
                name = u"Stationnements règlementaires sur la commune de Pau - Stationnement Handi",
                file = "parking_FR_capp_disabled.csv.bz2",
                encoding = "ISO-8859-15"),
            Load("X", "Y", table = "capp_parking_disabled",
                select = {"Types": "Stationnement Handi"},
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {
                        "amenity": "parking",
                        "capacity:disabled": None}),
                    conflationDistance = 100,
                generate = Generate(
                    static = {
                        "source": u"Communauté d'Agglomération Pau-Pyrénées - 01/2013",
                        "amenity": "parking"},
                    mapping = {"capacity:disabled": lambda res: res["nombre"] if res["nombre"] != "0" else "yes"} )))
