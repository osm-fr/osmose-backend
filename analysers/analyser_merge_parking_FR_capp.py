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

    create_table = """
        places VARCHAR(254),
        pay_grat VARCHAR(254),
        commune VARCHAR(254),
        ouvrage VARCHAR(254),
        nom VARCHAR(254),
        x VARCHAR(254),
        y VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 1, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CAPP parking not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=18"
        self.officialName = "Parkings sur la CAPP"
        self.csv_file = "merge_data/parking_FR_capp.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "amenity": "parking",
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "capp_parking"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Communauté d'Aglomération Pau-Pyrénées - 01/2013",
            "amenity": "parking",
        }
        self.defaultTagMapping = {
            "name": "nom",
            "fee": lambda res: "yes" if res["pay_grat"] == "Payant" else "no",
            "capacity": lambda res: res["place"] if res["place"] != "0" else None,
            "parking": lambda res: "surface" if res["ouvrage"] == "Plein air" else "underground" if res["ouvrage"] == "Souterrain" else None,
        }
        self.conflationDistance = 200
        self.text = lambda tags, fields: {"en": u"Parking %s" % tags["name"]}


class Analyser_Merge_Parking_FR_capp_disabled(Analyser_Merge):

    create_table = """
        commune VARCHAR(254),
        nom_voie VARCHAR(254),
        nombre VARCHAR(254),
        ouvrage VARCHAR(254),
        types VARCHAR(254),
        x VARCHAR(254),
        y VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 11, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CAPP parking disabled not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://opendata.agglo-pau.fr/index.php/fiche?idQ=21"
        self.officialName = "Stationnements règlementaires sur la commune de Pau - Stationnement Handi"
        self.csv_file = "merge_data/parking_FR_capp_disabled.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("(\"-?[0-9]+),([0-9]+\")")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.csv_select = {
            "types": "Stationnement Handi"
        }
        self.osmTags = {
            "amenity": "parking",
            "capacity:disabled": None,
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "capp_parking_disabled"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Communauté d'Aglomération Pau-Pyrénées - 01/2013",
            "amenity": "parking",
        }
        self.defaultTagMapping = {
            "capacity:disabled": lambda res: res["nombre"] if res["nombre"] != "0" else "yes",
        }
        self.conflationDistance = 100
