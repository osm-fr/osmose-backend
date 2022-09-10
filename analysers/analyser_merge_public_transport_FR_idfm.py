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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, Source, SHP, LoadGeomCentroid, Conflate, Select, Mapping


class _Analyser_Merge_Public_Transport_FR_IdFM(Analyser_Merge_Point):
    def __init__(self, config, logger, clas, conflationDistance, select, osmTags, defaultTag, label):
        Analyser_Merge_Point.__init__(self, config, logger)
        place = "IdFM"
        self.def_class_missing_official(item = 8040, id = 1+10*clas, level = 3, tags = ['merge', 'railway', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} from {1} not integrated', label, place))
        self.def_class_possible_merge(item = 8041, id = 3+10*clas, level = 3, tags = ['merge', 'railway', 'public transport', 'fix:chair'],
            title = T_('{0} from {1}, integration suggestion', label, place))

        self.init(
            "https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-arret-tc-idf",
            "Référentiel des arrêts : fichiers SIG",
            SHP(Source(attribution = 'Île-de-France Mobilités', millesime = '03/2022',
                    fileUrl = 'https://eu.ftp.opendatasoft.com/stif/Reflex/REF_ZDE.zip',
                    zip = '*.shp')),
            LoadGeomCentroid(
                select = {"type_arret": select}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = osmTags),
                osmRef = "ref:FR:STIF",
                conflationDistance = conflationDistance,
                mapping = Mapping(
                    static1 = defaultTag,
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:STIF": lambda fields: fields["id_refa"] and int(fields["id_refa"] or None)},
                    mapping2 = {"name": "nom_lda"},
                    text = lambda tags, fields: T_("{0} stop of {1}", place, tags["name"]) )))


class Analyser_Merge_IdFM_Bus(_Analyser_Merge_Public_Transport_FR_IdFM):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_IdFM.__init__(self, config, logger, 3, 100, "Arrêt de bus", {"highway": "bus_stop"}, {"highway": "bus_stop", "public_transport": "platform", "bus": "yes"}, "Arrêt de bus")

class Analyser_Merge_IdFM_Metro(_Analyser_Merge_Public_Transport_FR_IdFM):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_IdFM.__init__(self, config, logger, 0, 200, "Station de métro", {"railway": "platform"}, {"railway": "platform"}, "Quai de métro")

#class Analyser_Merge_IdFM_Train(_Analyser_Merge_Public_Transport_FR_IdFM):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_Public_Transport_FR_IdFM.__init__(self, config, logger, 1, 500, "Station ferrée / Val", {"railway": "platform"}, {"railway": "platform"}, "Quai de RER ou Transilien")

class Analyser_Merge_IdFM_Tram(_Analyser_Merge_Public_Transport_FR_IdFM):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Public_Transport_FR_IdFM.__init__(self, config, logger, 2, 100, "Arrêt de tram", {"railway": "platform"}, {"public_transport": "platform", "tram": "yes"}, "Quai de tram")
