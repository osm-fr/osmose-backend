#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights David Morais Ferreira 2020                                 ##
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


class Analyser_Merge_Emergency_Points_LU(Analyser_Merge):
    def __init__(self, config, logger=None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item=9110, id=3, level=3, tags=['merge'],
                                               title=T_('Emergency point not integrated'))
        self.possible_merge = self.def_class(item=9111, id=3, level=3, tags=['merge'],
                                               title=T_('Emergency point integration suggestion'))
        self.init(
            "https://data.public.lu/fr/datasets/linstallation-des-points-de-secours-rettungspunkte",
            "Points de secours",
            CSV(Source(attribution="Corps grand-ducal d'incendie et de secours",
                       fileUrl="https://data.public.lu/fr/datasets/r/b8d9d38a-7894-49fb-ab88-94072fe2c722",
                       encoding="iso-8859-1"),
                separator=";"),
            Load("GEOGRAPHISCHE LÄNGE", "GEOGRAPHISCHE BREITE"),
            Mapping(
                select=Select(
                    types=["nodes"],
                    tags={"highway": "emergency_access_point"}),
                conflationDistance=50,
                generate=Generate(
                    static1={
                        "highway": "emergency_access_point"
                    },
                    mapping1={
                        "ref": "NAME",
                        "name": "ZUSATZ"
                    }
                )))
