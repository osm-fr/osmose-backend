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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

class Analyser_Merge_Milestone_FR_metropole(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)

        doc = dict(
            detail = T_(
'''The list of milestone comes from the CEREMA's database "RIU" in France.'''),
            trap = T_(
'''Those milestones can't be on way * _link. The position of the marker may be a little different than what is visible on the road. Sometimes, a small white line perpendicular to the road on the emergency stop strip or the left flared strip can be seen on satellite images or Mapillary's photos.'''))

        self.def_class_missing_official(item = 8430, id = 41, level = 3, tags = ['merge', 'highway'],
            title = T_('Milestone not integrated'), **doc)
        self.def_class_possible_merge(item = 8431, id = 43, level = 3, tags = ['merge', 'highway'],
            title = T_('Milestone integration suggestion'), **doc)
        self.def_class_update_official(item = 8432, id = 44, level = 3, tags = ['merge', 'highway'],
            title = T_('Milestone update'), **doc)

        self.init(
            "https://www.data.gouv.fr/fr/datasets/bornage-du-reseau-routier-national/",
            "Bornage du réseau routier national",
            CSV(Source(attribution = "data.gouv.fr:Ministère de la Transition écologique et solidaire", millesime = "01/2020",
                    fileUrl = "https://www.data.gouv.fr/fr/datasets/r/7de08adc-74ae-4e62-8967-6f559ff6cbed")),
            Load("x", "y", srid = 2154,
                xFunction = self.float_comma,
                yFunction = self.float_comma,
                where = lambda row: self.is_milestone(row)),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = [{"highway": "milestone"}]),
                osmRef = "nat_ref",
                conflationDistance = 150,
                generate = Generate(
                    static1 = {"highway": "milestone"},
                    static2 = {"source:nat_ref": self.source},
                    mapping1 = {
                        "distance": 'pr',
                        "nat_ref": lambda row: self.transform_to_plo(row) }
                    )))

    def is_milestone(self,row):
        if len(row['depPr']) == 3:
            return False
        elif [ele for ele in ('P', 'N1', 'N2', 'A9', 'N9') if ele in row['route']]:
            #P for temporary ; N1 for future up_class and N2 for down_class road ; A9,N9 in metropole, is not milestone but way_link or roundabout
            return False
        else:
            return True

    def transform_to_plo(self, row):
        # use plo format, description available at http://dtrf.setra.fr/pdf/pj/Dtrf/0005/Dtrf-0005792/DT5792.pdf
        #dept must be on 2 caracter
        dept = row['depPr']
        if len(dept) == 1:
            dept = '0' + dept

        #C or '', not 'N'
        concede = 'C' if row['concessionPr'] == 'C' else ''

        #I is for ignore, sens is D,G or U for droite (sens croissant), gauche (sens décroissant), unique.
        sens = row['cote']
        if sens == 'I':
            sens = 'U'

        return dept + 'PR' + row['pr'] + sens + concede
