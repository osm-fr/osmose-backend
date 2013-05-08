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

    def __init__(self, config, classs, logger = None):
        self.missing_official = {"item":"8080", "class": classs, "level": 3, "tag": ["addr"], "desc":{"fr": u"Adresse manquante"} }
        Analyser_Merge.__init__(self, config, logger)
        self.osmTags = {
            "addr:housenumber": None,
        }
        self.extraJoin = "addr:housenumber"
        self.osmTypes = ["nodes", "ways"]
        self.conflationDistance = 15


class Analyser_Merge_Street_Number_Toulouse(_Analyser_Merge_Street_Number):

    create_table = """
        no VARCHAR(255),
        numero VARCHAR(255),
        lib_off VARCHAR(255),
        mot_directeur VARCHAR(255),
        sti VARCHAR(255),
        nrivoli VARCHAR(255),
        rivoli VARCHAR(255),
        X_CC43 NUMERIC(11, 3),
        Y_CC43 NUMERIC(11, 3),
        X_WGS84 NUMERIC(11, 8),
        Y_WGS84 NUMERIC(11, 8)
    """

    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 1, logger)
        self.officialURL = "http://data.grandtoulouse.fr/les-donnees/-/opendata/card/12673-n-de-rue"
        self.officialName = "GrandToulouse-N° de rue"
        self.csv_file = "merge_data/adress_france_toulouse.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS '' CSV HEADER"
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
        self.text = lambda tags, fields: {"fr": u"%s %s" % (fields["no"], fields["lib_off"])}


class Analyser_Merge_Street_Number_Nantes(_Analyser_Merge_Street_Number):

    create_table = """
        adresse VARCHAR(255),
        nomcom VARCHAR(255),
        mot_directeur VARCHAR(255),
        numero VARCHAR(255),
        rivoli VARCHAR(255),
        code_postal VARCHAR(255),
        LONG_WGS84 NUMERIC(16, 14),
        LAT_WGS84 NUMERIC(16, 14)
    """

    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 2, logger)
        self.officialURL = "http://data.nantes.fr/donnees/detail/adresses-postales-de-nantes-metropole/"
        self.officialName = "Adresses postales de Nantes Métropole"
        self.csv_file = "merge_data/adress_france_nantes.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        self.sourceTable = "street_number_nantes"
        self.sourceX = "LONG_WGS84"
        self.sourceY = "LAT_WGS84"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Nantes Métropole 01/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "numero",
        }
        self.text = lambda tags, fields: {"fr": u"%s" % (fields["adresse"])}


class Analyser_Merge_Street_Number_Bordeaux(_Analyser_Merge_Street_Number):

    create_table = """
        x NUMERIC(10, 2),
        y NUMERIC(10, 2),
        gid VARCHAR(255),
        datexist VARCHAR(255),
        ident VARCHAR(255),
        numero VARCHAR(255),
        numero_x VARCHAR(255),
        numero_y VARCHAR(255),
        numero_o VARCHAR(255),
        rs_fv_voie VARCHAR(255),
        geom_o VARCHAR(255)
    """

    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 3, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=8"
        self.officialName = "Numéro de voirie de la CUB"
        # Convert shp L93 with QGis, save as CSV with layer "GEOMETRY=AS_XY", because official CSV doesn't have coords.
        self.csv_file = "merge_data/adress_france_bordeaux.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
#        self.csv_encoding = "ISO-8859-15"
        self.sourceTable = "street_number_bordeaux"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": "Communauté Urbaine de Bordeaux 05/2013",
        }
        self.defaultTagMapping = {
            "addr:housenumber": "numero",
        }
        self.text = lambda tags, fields: {"fr": u"%s" % (fields["numero"])}
