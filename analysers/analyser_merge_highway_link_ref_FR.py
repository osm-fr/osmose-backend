#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Didier Marchand, Frederic Rodrigo 2024                     ##
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
from .Analyser_Merge import SHP, SourceDataGouv, Load, Select, Mapping
from .Analyser_Merge_Network import Analyser_Merge_Network, ConflateNetwork

class Analyser_Merge_Highway_Link_Ref_FR(Analyser_Merge_Network):
    def __init__(self, config, logger = None):
        Analyser_Merge_Network.__init__(self, config, logger)
        doc = dict(
            detail = T_('''The list of road comes from the database "RIU" in France.'''),
            trap = T_('''Those nat_ref can only be on `*_link` ways or roundabouts.'''))

        self.def_class_possible_merge(item = 8432, id = 47, level = 3, tags = ['merge', 'highway'],
            title = T_('*_link French métropole nat_ref integration suggestion'), **doc)
        self.def_class_update_official(item = 8432, id = 48, level = 3, tags = ['merge', 'highway'],
            title = T_('*_link French métropole nat_ref update'), **doc)
        self.init(
            "https://www.data.gouv.fr/fr/datasets/liaisons-du-reseau-routier-national/",
            "Liaisons du réseau routier national",
            SHP(SourceDataGouv(
                attribution="data.gouv.fr:Ministère de la Transition écologique",
                dataset="57a837e2c751df5b90bb5dd4",
                resource='90a65602-3ca4-41d7-bf7c-23d435c916e1'),
                zip='VSMAP_TOUT.shp'),
            Load('geom',
                table_name = 'ref_link_fr_' + config.options['country'].replace("-", "_"),
                where = lambda row: (self.is_riu_link(row))),
            ConflateNetwork(
                select = Select(
                    types = ["ways"],
                    tags = [{"highway": ["motorway_link","trunk_link","primary_link","roundabout"]}]),
                osmRef = "nat_ref",
                conflationDistance = 15,
                minLength = 50,
                mapping = Mapping(
                    static2 = {"source:nat_ref": self.source},
                    mapping1 = {
                        "operator": 'gestionnai',
                        "nat_ref": lambda row: (self.linkplo_isidor(row))}
                )))

        def is_riu_link(self,row):
            # Filter only DB, FB
            return row['nom_plo_in'][0:2] == 'DB'
        def linkplo_isidor(self,row):
            #plo format isidor
            return row['lib_rte'] + '_' + row['nom_plo'][2:]  + 'D'
