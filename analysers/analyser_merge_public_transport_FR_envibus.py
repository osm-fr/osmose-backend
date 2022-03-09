#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Théo Peltier 2022                                          ##
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
from .Analyser_Merge import Analyser_Merge, GTFS, Load, Conflate, Select, Mapping, Source


class Analyser_Merge_Public_Transport_FR_envibus(Analyser_Merge):

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "Envibus"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://trouver.datasud.fr/dataset/arrets-horaires-et-parcours-theoriques-du-reseau-envibus-gtfs",
            "Liste des arrêts, des horaires et des parcours théoriques des bus du réseau des transports publics ENVIBUS",
            GTFS(Source(attribution = "Communauté d'Agglomération Sophia Antipolis", millesime = "01/2022",
                        fileUrl = "https://trouver.datasud.fr/dataset/2fd535c3-8472-40b6-b93e-46325f4bda42/resource/19da0f1e-193a-43d9-93a8-5c53620895fe/download/gtfs.zip")),
            Load("stop_lon", "stop_lat",
                 #select = {"location_type": '0', "stop_code": True},
                 ),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"highway": "bus_stop", "public_transport": "platform"},{"highway": "bus_stop", "public_transport": False}, {"highway":"platform"}]),
                osmRef = "ref:FR:ENVIBUS",
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:ENVIBUS": lambda res: res["stop_code"],
                        # If stop_code is defined, the platform belongs to the Lignes d'Azur network,
                        # else it belongs generally to the ZOU (Région Sud) network, which some old
                        # Lignes d'Azur / TAM lines have been transferred to (lines 100 and 200 for example)
                        # If stop_name contains an upper case name, it's the station city name
                        "name": lambda res: self.replace(res['stop_name'].title()),
                    },
                    text = lambda tags, fields: T_(f"{place} stop of {fields['stop_name']}")))
        )


    def replace(self, string):
        for term in self.replacement.items():
            string = string.replace(term, self.replacement[term])
        return string

    replacement = {
        'Av.': 'Avenue',
        'Coll.': 'Collège',
        'Ch.': 'Chemin',
        'Pl.': 'Place',
        'Eglise': 'Église',
        'Rte ': 'Route ',
        'Rp ': 'Rond-Point ',
        'Bld ': 'Boulevard ',
        'St ': 'Saint-',
        'Av. ': 'Avenue ',
        'Hôp.': 'Hôpital',
        ' De ': ' de ',
        ' Du ': ' du ',
        ' La ': ' la ',
        'Rd ': 'Route départementale '
    }
