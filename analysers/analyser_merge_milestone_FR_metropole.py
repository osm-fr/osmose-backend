#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Didier Marchand 2020                                       ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, SHP, LoadGeomCentroid, Conflate, Select, Mapping

class Analyser_Merge_Milestone_FR_metropole(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)

        doc = dict(
            detail = T_(
'''The list of milestone comes from the CEREMA's database "RIU" in France.'''),
            trap = T_(
'''Those milestones can't be on `*_link` ways. The position of the marker may be a little different than what is visible on the road.
Sometimes, a small white line perpendicular to the road on the emergency stop strip or the left flared strip can be seen on satellite images or Mapillary's photos.'''))

        self.def_class_missing_official(item = 8430, id = 41, level = 3, tags = ['merge', 'highway', 'fix:picture', 'fix:survey'],
            title = T_('Milestone not integrated'), **doc)
        self.def_class_possible_merge(item = 8431, id = 43, level = 3, tags = ['merge', 'highway', 'fix:picture', 'fix:survey'],
            title = T_('Milestone integration suggestion'), **doc)
        self.def_class_update_official(item = 8432, id = 44, level = 3, tags = ['merge', 'highway', 'fix:picture', 'fix:survey'],
            title = T_('Milestone update'), **doc)

        self.init(
            "https://www.data.gouv.fr/fr/datasets/liaisons-du-reseau-routier-national/",
            "Liaisons du réseau routier national",
            SHP(SourceDataGouv(
                attribution="data.gouv.fr:Ministère de la Transition écologique",
                dataset="57a837e2c751df5b90bb5dd4",
                resource="92d86944-52e8-44c1-b4cc-b17ac82d70ed"),
                zip='BORNAGE_TOUT.shp'),
            LoadGeomCentroid(
                where = lambda row: (
                    self.is_milestone(row)
                )), # Check for valid Lambert98 coords
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = [{"highway": "milestone"}]),
                osmRef = "nat_ref",
                conflationDistance = 150,
                mapping = Mapping(
                    static1 = {"highway": "milestone"},
                    static2 = {"source:nat_ref": self.source},
                    mapping1 = {
                        "distance": 'pr',
                        "nat_ref": 'nom_plo'}
                )))

    def is_milestone(self,row):
        if [ele for ele in ('P', 'N1', 'N2', 'A9', 'N9', 'A8', 'N8') if ele in row['route']]:
            #P for temporary ; N1 for future up_class and N2 for down_class road ; A9, N9 for way_link or roundabout ; A8, N8 for service area
            return False
        else:
            # Filter only real milestone (not logical as DRD, FRG, CS etc...)
            return row['nom_plo'][2:4] == 'PR'
