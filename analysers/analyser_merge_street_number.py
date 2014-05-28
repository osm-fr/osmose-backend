#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

import re
from Analyser_Merge import Analyser_Merge


class _Analyser_Merge_Street_Number(Analyser_Merge):

    def __init__(self, config, classs, city, logger = None):
        self.missing_official = {"item":"8080", "class": classs, "level": 3, "tag": ["addr"], "desc": T_(u"Missing address %s", city) }
        Analyser_Merge.__init__(self, config, logger)
        self.osmTags = {
            "addr:housenumber": None,
        }
        self.extraJoin = "addr:housenumber"
        self.osmTypes = ["nodes", "ways"]
        self.conflationDistance = 15


class Analyser_Merge_Street_Number_Toulouse(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 1, "Toulouse", logger)
        self.officialURL = "http://data.grandtoulouse.fr/les-donnees/-/opendata/card/12673-n-de-rue"
        self.officialName = u"GrandToulouse-N° de rue"
        self.csv_file = "merge_data/address_france_toulouse.csv"
        self.csv_separator = ";"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.sourceTable = "street_number_toulouse"
        self.sourceX = "X_WGS84"
        self.sourceY = "Y_WGS84"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "ToulouseMetropole",
            "source:date": "2012-10-04",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "no",
        }
        self.text = lambda tags, fields: {"en": u"%s %s" % (fields["no"], fields["lib_off"])}


class Analyser_Merge_Street_Number_Nantes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 2, "Nantes", logger)
        self.officialURL = "http://data.nantes.fr/donnees/detail/adresses-postales-de-nantes-metropole/"
        self.officialName = u"Adresses postales de Nantes Métropole"
        self.csv_file = "merge_data/address_france_nantes.csv"
        self.csv_encoding = "ISO-8859-15"
        self.sourceTable = "street_number_nantes"
        self.sourceX = "LONG_WGS84"
        self.sourceY = "LAT_WGS84"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Nantes Métropole 01/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "NUMERO",
        }
        self.text = lambda tags, fields: {"en": fields["ADRESSE"]}


class Analyser_Merge_Street_Number_Bordeaux(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 3, "Bordeaux", logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=8"
        self.officialName = u"Numéro de voirie de la CUB"
        # Convert shp L93 with QGis, save as CSV with layer "GEOMETRY=AS_XY", because official CSV doesn't have coords.
        self.csv_file = "merge_data/address_france_bordeaux.csv"
#        self.csv_encoding = "ISO-8859-15"
        self.sourceTable = "street_number_bordeaux"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Communauté Urbaine de Bordeaux 05/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "NUMERO",
        }
        self.text = lambda tags, fields: {"en": fields["NUMERO"]}


class Analyser_Merge_Street_Number_Lyon(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 4, "Lyon", logger)
        self.officialURL = "http://smartdata.grandlyon.com/localisation/point-dadressage-sur-bftiment-voies-et-adresses/"
        self.officialName = u"Grand Lyon - Point d'adressage sur bâtiment (Voies et adresses)"
        # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
        self.csv_file = "merge_data/address_france_lyon.csv"
        self.sourceTable = "street_number_lyon"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Grand Lyon - 10/2011",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "numero",
        }
        self.text = lambda tags, fields: {"en": u"%s %s" % (fields["numero"], fields["voie"])}


class Analyser_Merge_Street_Number_Montpellier(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 5, "Montpellier", logger)
        self.officialURL = "http://opendata.montpelliernumerique.fr/Point-adresse"
        self.officialName = u"Ville de Montpellier - Point adresse"
        # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
        self.csv_file = "merge_data/address_france_montpellier.csv"
        self.sourceTable = "street_number_montpellier"
        self.sourceWhere = lambda res: res["NUM_VOI"] != "0"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Ville de Montpellier - 01/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "NUM_SUF",
        }
        self.text = lambda tags, fields: {"en": u"%s %s" % (fields["NUM_SUF"], fields["LIB_OFF"])}


class Analyser_Merge_Street_Number_Arles(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 6, "Arles", logger)
        self.officialURL = "http://opendata.regionpaca.fr/donnees/detail/base-de-donnees-adresses-de-laccm.html"
        self.officialName = u"Base de données Adresses de l'ACCM"
        # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
        self.csv_file = "merge_data/address_france_arles.csv"
        self.sourceTable = "street_number_arles"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": u"Arles Crau Camargue Montagnette - 02/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": lambda res: res["NUM_VOI"] + (res["SUF_VOI"] if res["SUF_VOI"] else ""),
        }
        self.text = lambda tags, fields: {"en": fields["ADRESSE"]}


class Analyser_Merge_Street_Number_Rennes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 7, "Rennes", logger)
        self.officialURL = "http://www.data.rennes-metropole.fr/les-donnees/catalogue/?tx_icsopendatastore_pi1[uid]=217"
        self.officialName = u"Référentiel voies et adresses de Rennes Métropole"
        self.csv_file = "merge_data/address_france_rennes.csv"
        self.csv_separator = ";"
        self.csv_encoding = "ISO-8859-15"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.sourceTable = "street_number_rennes"
        self.sourceX = "X_WGS84"
        self.sourceY = "Y_WGS84"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Rennes Métropole - 05/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": lambda res: res["NUMERO"] + (res["EXTENSION"] if res["EXTENSION"] else "") + ((" "+res["BATIMENT"]) if res["BATIMENT"] else ""),
        }
        self.text = lambda tags, fields: {"en": fields["ADR_CPLETE"]}
