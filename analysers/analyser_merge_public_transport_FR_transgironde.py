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

from Analyser_Merge import Analyser_Merge, Source, GTFS, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Transport_FR_TransGironde(Analyser_Merge):
    def __init__(self, config, logger = None):
        place = "TransGironde"
        self.missing_official = {"item":"8040", "class": 41, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"%s stop not integrated", place) }
        self.possible_merge   = {"item":"8041", "class": 43, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"%s stop, integration suggestion", place) }
        self.update_official  = {"item":"8042", "class": 44, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"%s stop update", place) }
        Analyser_Merge.__init__(self, config, logger,
            "http://catalogue.datalocale.fr/dataset/liste-lignereguliere-transgironde",
            u"Horaires des lignes régulières du réseau transgironde",
            GTFS(Source(attribution = u"Conseil général de la Gironde", millesime = "12/2016",
                    fileUrl = "https://datacat.datalocale.fr/file/1479301/raw/download", encoding = "ISO-8859-15")),
            Load("stop_lon", "stop_lat"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                osmRef = "ref:FR:TransGironde",
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes",
                        "network": "TransGironde"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:TransGironde": lambda res: res["stop_id"].split(':')[1],
                        "name": lambda res: res['stop_name'].split(' - ')[1] if len(res['stop_name'].split(' - ')) > 1 else None},
                    text = lambda tags, fields: T_(u"%s stop of %s", place, fields["stop_name"]) )))

    def replace(self, string):
        for s in self.replacement.keys():
            string = string.replace(s, self.replacement[s])
        return string

    replacement = {
        u'Coll.': u'Collège',
        u'Pl.': u'Place',
        u'Eglise': u'Église',
        u'Rte ': u'Route ',
        u'Bld ': u'Boulevard',
        u'St ': u'Staint ',
        u'Av. ': u'Avenue',
        u'Hôp.': u'Hôpital',
    }
