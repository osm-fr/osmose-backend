#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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


class Analyser_Merge_Power_Tower_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8290, id = 1, level = 3, tags = ['merge', 'power'],
            title = T_('Power support not integrated'))
        self.def_class_missing_osm(item = 7200, id = 2, level = 3, tags = ['merge', 'power'],
            title = T_('Power support without tag "ref" or invalid'))
        self.def_class_possible_merge(item = 8291, id = 3, level = 3, tags = ['merge', 'power'],
            title = T_('Power support, integration suggestion'))

        self.init(
            u"https://opendata.reseaux-energies.fr/explore/dataset/pylones-rte",
            u"Pylones RTE",
            CSV(Source(attribution = u"data.gouv.fr:RTE", millesime = "12/2018",
                    fileUrl = u"https://opendata.reseaux-energies.fr/explore/dataset/pylones-rte/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = u";"),
            Load(u"Longitude pylône (DD)", u"Latitude pylône (DD)"),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = [{"power": "tower", "operator": "RTE"}, {"power": "pole", "operator": "RTE"}, {"power": "terminal", "operator": "RTE"}, {"power": "portal", "operator": "RTE"}, {"power": "insulator", "operator": "RTE"},
                      {"power": "tower", "operator": False}, {"power": "pole", "operator": False}, {"power": "terminal", "operator": False}, {"power": "portal", "operator": False}, {"power": "insulator", "operator": False}]),
#                osmRef = "ref:FR:RTE", # Commented initial. Only issues missing tower. Then when the missing tower number lower, uncomment to integrate ref into OSM.
                conflationDistance = 10,
                generate = Generate(
                    static1 = {
                        "power": "tower",
                        "operator": "RTE"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref": u"Numéro pylône"},
                    mapping2 = {
                        "height": lambda fields: fields[u"Hauteur pylône (m)"] if fields[u"Hauteur pylône (m)"] != "0" else None})))
