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

from Analyser_Merge import Analyser_Merge, Source, CSV, SHP, Load, Mapping, Select, Generate


class _Analyser_Merge_Street_Number(Analyser_Merge):

    def __init__(self, config, classs, city, logger, url, name, parser, load, mapping):
        self.missing_official = {"item":"8080", "class": classs, "level": 3, "tag": ["addr"], "desc": T_(u"Missing address %s", city) }
        Analyser_Merge.__init__(self, config, logger, url, name, parser, load, mapping)
        self.mapping.select = Select(
            types = ["nodes", "ways"],
            tags = [{"addr:housenumber": None}])
        self.mapping.conflationDistance = 100
        self.mapping.extraJoin = "addr:housenumber"
        if config.options and ("country" in config.options and config.options["country"] == "FR"):
            # Normalize France's addr:housenumber format
            self.mapping.extraJoinNormalize = lambda expr: "replace(replace(replace(replace(upper(%s), 'BIS', 'B'), 'TER','T'), 'QUATER','Q'), ' ', '')" % (expr,)


class Analyser_Merge_Street_Number_Toulouse(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 1, "Toulouse", logger,
            "http://data.grandtoulouse.fr/les-donnees/-/opendata/card/12673-n-de-rue",
            u"GrandToulouse-N° de rue",
            CSV(Source(attribution = "ToulouseMetropole", millesime = "2012-10-04",
                    file = "address_france_toulouse.csv.bz2"),
                separator = ";"),
            Load("X_WGS84", "Y_WGS84",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                generate = Generate(
                    static2 = {
                        "source": lambda a: a.parser.source.attribution,
                        "source:date": lambda a: a.parser.source.millesime},
                    mapping1 = {"addr:housenumber": "no"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["no"], fields["lib_off"])} )))


class Analyser_Merge_Street_Number_Nantes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 2, "Nantes", logger,
            "http://data.nantes.fr/donnees/detail/adresses-postales-de-nantes-metropole/",
            u"Adresses postales de Nantes Métropole",
            CSV(Source(attribution = u"Nantes Métropole %s", millesime = "03/2016",
                    fileUrl = "http://data.nantes.fr/fileadmin/data/datastore/nm/urbanisme/24440040400129_NM_NM_00001/ADRESSES_NM_csv.zip", zip= "ADRESSES_NM.csv", encoding = "ISO-8859-15")),
            Load("LONG_WGS84", "LAT_WGS84"),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "NUMERO"},
                    text = lambda tags, fields: {"en": fields["ADRESSE"]} )))


class Analyser_Merge_Street_Number_Bordeaux(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 3, "Bordeaux", logger,
            "http://data.bordeaux-metropole.fr/data.php?themes=8",
            u"Numéro de voirie de Bordeaux Métropole",
            SHP(Source(attribution = u"Bordeaux Métropole", millesime = "08/2016",
                    fileUrl = "http://data.bordeaux-metropole.fr/files.php?gid=20&format=2", zip = "FV_NUMVO_P.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "NUMERO"},
                    text = lambda tags, fields: {"en": fields["NUMERO"]} )))


class Analyser_Merge_Street_Number_Lyon(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 4, "Lyon", logger,
            "http://smartdata.grandlyon.com/localisation/point-dadressage-sur-bftiment-voies-et-adresses/",
            u"Grand Lyon - Point d'adressage sur bâtiment (Voies et adresses)",
            SHP(Source(attribution = u"Grand Lyon", millesime = "06/2016",
                    fileUrl = "http://data.grandlyon.com/smartdata/wp-content/plugins/wp-smartdata/proxy.php?format=Shape-zip&name=adr_voie_lieu.adradresse&projection=urn:ogc:def:crs:EPSG::4326&commune=&href=https%3A%2F%2Fdownload.data.grandlyon.com%2Fwfs%2Fgrandlyon%3FSERVICE%3DWFS%26VERSION%3D2.0.0%26outputformat%3DSHAPEZIP%26request%3DGetFeature%26SRSNAME%3DEPSG%3A3946%26typename%3Dadr_voie_lieu.adradresse",
                zip = "adr_voie_lieu.adradresse.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",)),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "numero"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["numero"], fields["voie"])} )))


class Analyser_Merge_Street_Number_Montpellier(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 5, "Montpellier", logger,
            "http://opendata.montpelliernumerique.fr/Point-adresse",
            u"Ville de Montpellier - Point adresse",
            # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
            CSV(Source(attribution = u"Ville de Montpellier", millesime = "05/2016",
                    file = "address_france_montpellier.csv.bz2")),
            Load("X", "Y", srid = 2154,
                where = lambda res: res["NUM_VOI"] != "0"),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "NUM_SUF"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["NUM_SUF"], fields["LIB_OFF"])} )))


class Analyser_Merge_Street_Number_Arles(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 6, "Arles", logger,
            "http://opendata.regionpaca.fr/donnees/detail/base-de-donnees-adresses-postales-de-laccm.html",
            u"Base de données Adresses postales de l'ACCM",
            SHP(Source(attribution = u"Arles Crau Camargue Montagnette", millesime = "02/2013",
                    fileUrl = "http://opendata.regionpaca.fr/donnees.html?type=109&no_cache=1&tx_ausyopendata_pi1%5Bdataset%5D=283&tx_ausyopendata_pi1%5Bdatafile%5D=278&tx_ausyopendata_pi1%5Baction%5D=download&tx_ausyopendata_pi1%5Bcontroller%5D=Dataset&cHash=5d538731e8fa4c9f44d1a103dc452ab1", zip = "ADRESSE_ACCM.shp")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": lambda res: str(res["num_voi"]) + (res["suf_voi"] if res["suf_voi"] else "")},
                    text = lambda tags, fields: {"en": fields["adresse"]} )))


class Analyser_Merge_Street_Number_Rennes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 7, "Rennes", logger,
            "http://www.data.rennes-metropole.fr/les-donnees/catalogue/?tx_icsopendatastore_pi1[uid]=217",
            u"Référentiel voies et adresses de Rennes Métropole",
            CSV(Source(attribution = u"Rennes Métropole", millesime = "05/2013",
                    fileUrl = "http://www.data.rennes-metropole.fr/fileadmin/user_upload/data/data_sig/referentiels/voies_adresses/voies_adresses_csv.zip", zip = "voies_adresses_csv/donnees/rva_adresses.csv"),
                separator = ";"),
            Load("X_WGS84", "Y_WGS84",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": lambda res: res["NUMERO"] + (res["EXTENSION"] if res["EXTENSION"] else "") + ((" "+res["BATIMENT"]) if res["BATIMENT"] else "")},
                    text = lambda tags, fields: {"en": fields["ADR_CPLETE"]} )))
