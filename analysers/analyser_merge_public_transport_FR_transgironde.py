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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, GTFS, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Public_Transport_FR_TransGironde(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "TransGironde"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/horaires-theoriques-du-reseau-de-transport-cg-33-transgironde/",
            "Horaires théoriques du réseau de transport 'CG 33 -TRANSGIRONDE'",
            GTFS(SourceDataGouv(
                attribution="Conseil général de la Gironde",
                dataset="5ab11a52c751df688f5268c4",
                resource="06b4ab72-01b2-4561-9fbf-7e02ee0dd613",
                encoding="ISO-8859-15")),
            Load_XY("stop_lon", "stop_lat"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                osmRef = "ref:FR:TransGironde",
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:TransGironde": lambda res: res["stop_id"].split(':')[1],
                        "name": lambda res: self.replace(res['stop_name'].split(' - ')[1]) if len(res['stop_name'].split(' - ')) > 1 else None},
                    text = lambda tags, fields: T_("{0} stop of {1}", place, fields["stop_name"]) )))

    def replace(self, string):
        for s in self.replacement.keys():
            string = string.replace(s, self.replacement[s])
        return string

    replacement = {
        u'Coll.': u'Collège',
        u'Pl.': u'Place',
        u'Eglise': u'Église',
        u'Rte ': u'Route ',
        u'Bld ': u'Boulevard ',
        u'St ': u'Saint ',
        u'Av. ': u'Avenue ',
        u'Hôp.': u'Hôpital',
    }
