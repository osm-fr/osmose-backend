#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2022                                      ##
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
from .Analyser_Merge import SourceOpenDataSoft, GDAL, Load, Select, Mapping
from .Analyser_Merge_Network import Analyser_Merge_Network, ConflateNetwork


class Analyser_Merge_Power_Line_FR(Analyser_Merge_Network):
    def __init__(self, config, logger = None):
        Analyser_Merge_Network.__init__(self, config, logger)
        self.def_class_missing_official(item = 8290, id = 10, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:imagery'],
            title = T_('Power line not integrated'))

        self.init(
            "https://odre.opendatasoft.com/explore/dataset/lignes-aeriennes-rte-nv/information",
            "Lignes aériennes RTE",
            GDAL(SourceOpenDataSoft(
                url="https://odre.opendatasoft.com/explore/dataset/lignes-aeriennes-rte-nv/information",
                attribution="RTE",
                format="geojson"),
                fields=["tension"]),
            Load('geom',
                select={"tension": lambda t: f'{t} != \'HORS TENSION\''}),
            ConflateNetwork(
                select = Select(
                    types = ["ways"],
                    tags = [{"power": "line"}, {"disused:power": "line"}]),
                conflationDistance = 30,
                mapping = Mapping(
                    static1 = {
                        "power": "line", 
                        "operator": "RTE",
                        "operator:wikidata": "Q2178795"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "voltage": lambda fields: str((int(float(fields["tension"].replace("kV", "")) * 1000))) if fields["tension"] not in ("HORS TENSION", "<45kV", "COURANT CONTINU") else None,
                    },
                    text = lambda tags, fields: {"en": ", ".join(filter(lambda res: res and res != "None", [fields["tension"]]))} )))
