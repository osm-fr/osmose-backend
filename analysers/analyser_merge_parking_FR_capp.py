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

from Analyser_Merge import Analyser_Merge
import re


class Analyser_Merge_Parking_FR_capp(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 1, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CAPP parking not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=18"
        self.officialName = u"Parkings sur la CAPP"
        self.csv_file = "parking_FR_capp.csv.bz2"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "amenity": "parking",
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "capp_parking"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Communauté d'Agglomération Pau-Pyrénées - 01/2013",
            "amenity": "parking",
        }
        self.defaultTagMapping = {
            "name": "NOM",
            "fee": lambda res: "yes" if res["Pay_grat"] == "Payant" else "no",
            "capacity": lambda res: res["Places"] if res["Places"] != "0" else None,
            "parking": lambda res: "surface" if res["Ouvrage"] == "Plein air" else "underground" if res["Ouvrage"] == "Souterrain" else None,
        }
        self.conflationDistance = 200
        self.text = lambda tags, fields: {"en": u"Parking %s" % tags["name"]}


class Analyser_Merge_Parking_FR_capp_disabled(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 11, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CAPP parking disabled not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=21"
        self.officialName = u"Stationnements règlementaires sur la commune de Pau - Stationnement Handi"
        self.csv_file = "parking_FR_capp_disabled.csv.bz2"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("(\"-?[0-9]+),([0-9]+\")")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.csv_select = {
            "Types": "Stationnement Handi"
        }
        self.osmTags = {
            "amenity": "parking",
            "capacity:disabled": None,
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "capp_parking_disabled"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Communauté d'Agglomération Pau-Pyrénées - 01/2013",
            "amenity": "parking",
        }
        self.defaultTagMapping = {
            "capacity:disabled": lambda res: res["nombre"] if res["nombre"] != "0" else "yes",
        }
        self.conflationDistance = 100
