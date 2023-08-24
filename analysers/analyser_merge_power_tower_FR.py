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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Power_Tower_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8290, id = 1, level = 3, tags = ['merge', 'power', 'fix:imagery', 'fix:survey'],
            title = T_('Power support not integrated'))
        self.def_class_missing_osm(item = 7200, id = 2, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power support without tag "ref" or invalid'))
        self.def_class_possible_merge(item = 8291, id = 3, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power support, integration suggestion'))

        self.init(
            "https://opendata.reseaux-energies.fr/explore/dataset/pylones-rte/",
            "Pylones RTE",
            CSV(SourceOpenDataSoft(
                attribution="data.gouv.fr:RTE",
                url="https://opendata.reseaux-energies.fr/explore/dataset/pylones-rte")),
            Load_XY("Longitude pylône (DD)", "Latitude pylône (DD)",
                select={"Hauteur pylône (m)": lambda t: "{0} IS NOT NULL AND {0} NOT IN ('', '0')".format(t) }),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = [{"power": ["tower", "pole", "terminal", "portal", "insulator"], "operator":[False, "RTE"]}]),
#                osmRef = "ref:FR:RTE", # Commented initial. Only issues missing tower. Then when the missing tower number lower, uncomment to integrate ref into OSM.
                conflationDistance = 10,
                mapping = Mapping(
                    static1 = {
                        "operator": "RTE",
                        "operator:wikidata": "Q2178795"},
                    static2 = {"power": "tower", # Currently default value, we're not able to destinguish tower, pole, terminal, portal and insulator in opendata
                        "source": self.source},
                    mapping1 = {
                        "ref": "Numéro pylône"},
                    mapping2 = {
                        "height": lambda fields: fields["Hauteur pylône (m)"] if fields["Hauteur pylône (m)"] != "0" else None})))
