#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2020                                 ##
##            Didier Marchand 2020                                       ##
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

from collections import OrderedDict
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

class Analyser_Merge_Milestone_FR_metropole(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)

        doc = dict(
            detail = T_(
'''The list of milestone comes from the CEREMA's database "RIU" in France.'''),
            trap = T_(
'''The position of the marker may be a little different than that visible on the road. Sometimes, a small white line perpendicular to the road on the emergency stop strip or the left flared strip can be seen on satellite images or Mapillary's photo.'''))

        self.def_class_missing_official(item = 8130, id = 41, level = 3, tags = ['merge', 'highway'],
            title = T_('Milestone not integrated'), **doc)
        self.def_class_possible_merge(item = 8131, id = 43, level = 3, tags = ['merge', 'highway'],
            title = T_('Milestone integration suggestion'), **doc)
        self.def_class_update_official(item = 8132, id = 44, level = 3, tags = ['merge', 'highway'],
            title = T_('Milestone update'), **doc)

        self.init(
            "https://www.data.gouv.fr/fr/datasets/bornage-du-reseau-routier-national/",
            "Bornage du réseau routier national",
            CSV(Source("data.gouv.fr:Ministère de la Transition écologique et solidaire", millesime = "01/2019",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/fbc8b73b-a65c-486b-a710-ed22b9e4070c",
                    separator = "\t"),
                    
            Load("x", "y",srid = 2154,
                xFunction = self.float_comma, 
                yFunction = self.float_comma,
                where = lambda row: self.is_natref(row)),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = [{"highway": "milestone"}]),
                osmRef = "nat_ref",
                extraJoin = "ref",
                conflationDistance = 150,
                generate = Generate(
                    static1 = {"highway": "milestone"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "distance": 'pr',
                        "nat_ref": lambda row: self.transform_to_natref(row),
                        "ref": lambda row: self.transform_route(row['route']) }
                    )))
    
    def is_natref(self,row):
        if len(row['depPr']) == 3:
            return False
        elif row['route'][0:1] == 'P':
            #P for temporary,
            return False
        elif row['route'][0:2] in ('N1', 'N2'):
            #N1 for future up_class and N2 for down_class road,
            return False
        elif row['route'][2:4] in ('A9', 'N9'):
            #In metropole, it's not milestone but way_link or roundabout
            return False
        else :
            return True

    def transform_to_natref(self,row):
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
            
    def transform_route(self, route):
        #remove multiple 0 and add space
        if   route[0:4] in ('A000', 'N000') : return route[0:1] + " " + route[4:]
        elif route[0:3] in ('A00', 'N00')   : return route[0:1] + " " + route[3:]
        elif route[0:2] in ('A0', 'N0')     : return route[0:1] + " " + route[2:]
        else : return route[0:1] + " " + route[1:]
