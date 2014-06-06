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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class _Analyser_Merge_Street_Number(Analyser_Merge):

    def __init__(self, config, classs, city, logger, source, load, mapping):
        self.missing_official = {"item":"8080", "class": classs, "level": 3, "tag": ["addr"], "desc": T_(u"Missing address %s", city) }
        Analyser_Merge.__init__(self, config, logger, source, load, mapping)
        self.mapping.select = Select(
            types = ["nodes", "ways"],
            tags = {"addr:housenumber": None})
        self.mapping.extraJoin = "addr:housenumber"
        self.mapping.conflationDistance = 15


class Analyser_Merge_Street_Number_Toulouse(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 1, "Toulouse", logger,
            Source(
                url = "http://data.grandtoulouse.fr/les-donnees/-/opendata/card/12673-n-de-rue",
                name = u"GrandToulouse-N° de rue",
                file = "address_france_toulouse.csv.bz2",
                csv = CSV(separator = ";")),
            Load("X_WGS84", "Y_WGS84", srid = 4326, table = "street_number_toulouse",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                generate = Generate(
                    static = {
                        "source": "ToulouseMetropole",
                        "source:date": "2012-10-04"},
                mapping = {"addr:housenumber": "no"},
                text = lambda tags, fields: {"en": u"%s %s" % (fields["no"], fields["lib_off"])} )))


class Analyser_Merge_Street_Number_Nantes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 2, "Nantes", logger,
            Source(
                url = "http://data.nantes.fr/donnees/detail/adresses-postales-de-nantes-metropole/",
                name = u"Adresses postales de Nantes Métropole",
                file = "address_france_nantes.csv.bz2",
                encoding = "ISO-8859-15"),
            Load("LONG_WGS84", "LAT_WGS84", srid = 4326, table = "street_number_nantes"),
            Mapping(
                generate = Generate(
                    static = {"source": u"Nantes Métropole 01/2013"},
                    mapping = {"addr:housenumber": "NUMERO"},
                    text = lambda tags, fields: {"en": fields["ADRESSE"]} )))


class Analyser_Merge_Street_Number_Bordeaux(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 3, "Bordeaux", logger,
            Source(
                url = "http://data.lacub.fr/data.php?themes=8",
                name = u"Numéro de voirie de la CUB",
                # Convert shp L93 with QGis, save as CSV with layer "GEOMETRY=AS_XY", because official CSV doesn't have coords.
                file = "address_france_bordeaux.csv.bz2"),
            Load("X", "Y", srid = 2154, table = "street_number_bordeaux"),
            Mapping(
                generate = Generate(
                    static = {"source": u"Communauté Urbaine de Bordeaux 05/2013"},
                    mapping = {"addr:housenumber": "NUMERO"},
                    text = lambda tags, fields: {"en": fields["NUMERO"]} )))


class Analyser_Merge_Street_Number_Lyon(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 4, "Lyon", logger,
            Source(
                url = "http://smartdata.grandlyon.com/localisation/point-dadressage-sur-bftiment-voies-et-adresses/",
                name = u"Grand Lyon - Point d'adressage sur bâtiment (Voies et adresses)",
                # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
                file = "address_france_lyon.csv.bz2"),
            Load("X", "Y", srid = 4326, table = "street_number_lyon"),
            Mapping(
                generate = Generate(
                    static = {"source": u"Grand Lyon - 10/2011"},
                    mapping = {"addr:housenumber": "numero"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["numero"], fields["voie"])} )))


class Analyser_Merge_Street_Number_Montpellier(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 5, "Montpellier", logger,
            Source(
                url = "http://opendata.montpelliernumerique.fr/Point-adresse",
                name = u"Ville de Montpellier - Point adresse",
                # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
                file = "address_france_montpellier.csv.bz2"),
            Load("X", "Y", srid = 2154, table = "street_number_montpellier",
                where = lambda res: res["NUM_VOI"] != "0"),
            Mapping(
                generate = Generate(
                    static = {"source": u"Ville de Montpellier - 01/2013"},
                    mapping = {"addr:housenumber": "NUM_SUF"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["NUM_SUF"], fields["LIB_OFF"])} )))


class Analyser_Merge_Street_Number_Arles(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 6, "Arles", logger,
            Source(
                url = "http://opendata.regionpaca.fr/donnees/detail/base-de-donnees-adresses-de-laccm.html",
                name = u"Base de données Adresses de l'ACCM",
                # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
                file = "address_france_arles.csv.bz2"),
            Load("X", "Y", srid = 2154, table = "street_number_arles"),
            Mapping(
                generate = Generate(
                    static = {"source": u"Arles Crau Camargue Montagnette - 02/2013"},
                    mapping = {"addr:housenumber": lambda res: res["NUM_VOI"] + (res["SUF_VOI"] if res["SUF_VOI"] else "")},
                    text = lambda tags, fields: {"en": fields["ADRESSE"]} )))


class Analyser_Merge_Street_Number_Rennes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 7, "Rennes", logger,
            Source(
                url = "http://www.data.rennes-metropole.fr/les-donnees/catalogue/?tx_icsopendatastore_pi1[uid]=217",
                name = u"Référentiel voies et adresses de Rennes Métropole",
                file = "address_france_rennes.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";")),
            Load("X_WGS84", "Y_WGS84", srid = 4326, table = "street_number_rennes",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                generate = Generate(
                    static = {"source": u"Rennes Métropole - 05/2013"},
                    mapping = {"addr:housenumber": lambda res: res["NUMERO"] + (res["EXTENSION"] if res["EXTENSION"] else "") + ((" "+res["BATIMENT"]) if res["BATIMENT"] else "")},
                    text = lambda tags, fields: {"en": fields["ADR_CPLETE"]} )))
