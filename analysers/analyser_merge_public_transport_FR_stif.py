#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class _Analyser_Merge_Public_Transport_FR_Stif(Analyser_Merge):
    def __init__(self, config, logger, clas, conflationDistance, select, osmTags, defaultTag):
        Analyser_Merge.__init__(self, config, logger)
        place = "STIF"
        self.def_class_missing_official(item = 8040, id = 1+10*clas, level = 3, tags = ['merge', 'railway', 'public transport'],
            title = T_f('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 3+10*clas, level = 3, tags = ['merge', 'railway', 'public transport'],
            title = T_f('{0} stop, integration suggestion', place))

        self.init(
            u"https://opendata.stif.info/explore/dataset/referentiel-arret-tc-idf/information/",
            u"Référentiel des arrêts de transport en commun en Ile-de-France",
            CSV(Source(attribution = 'STIF', millesime = '02/2020',
                    fileUrl = 'https://eu.ftp.opendatasoft.com/stif/Reflex/REFLEX.csv'),
                separator = '|'),
            Load("ZDEr_X_Y", "ZDEr_X_Y", srid = 2154,
                select = {"ZDEr_LIBELLE_TYPE_ARRET": select},
                xFunction = lambda x: x.split(",")[0],
                yFunction = lambda y: y.split(",")[1]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = osmTags),
                osmRef = "ref:FR:STIF",
                conflationDistance = conflationDistance,
                generate = Generate(
                    static1 = defaultTag,
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:STIF": "ZDEr_ID_REF_A"},
                    mapping2 = {"name": "ZDEr_NOM"},
                    text = lambda tags, fields: T_f(u"{0} stop of {1}", place, tags["name"]) )))


#class Analyser_Merge_Stif_Bus(_Analyser_Merge_Public_Transport_FR_Stif):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_Public_Transport_FR_Stif.__init__(self, config, logger, 3, 100, u"Arrêt de bus", {"highway": "bus_stop"}, {"highway": "bus_stop", "public_transport": "platform", "bus": "yes"})

class Analyser_Merge_Stif_Metro(_Analyser_Merge_Public_Transport_FR_Stif):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_Stif.__init__(self, config, logger, 0, 200, u"Station de métro", {"railway": "station"}, {"railway": "station"})

class Analyser_Merge_Stif_Train(_Analyser_Merge_Public_Transport_FR_Stif):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_Stif.__init__(self, config, logger, 1, 500, u"Gare ferrée", {"railway": "station"}, {"railway": "station"})

class Analyser_Merge_Stif_Tram(_Analyser_Merge_Public_Transport_FR_Stif):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_Stif.__init__(self, config, logger, 2, 100, u"Arrêt de tram", {"railway": "tram_stop"}, {"railway": "tram_stop", "public_transport": "platform", "tram": "yes"})
