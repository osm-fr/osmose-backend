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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourcePublicLu, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Emergency_Points_LU(Analyser_Merge):
    def __init__(self, config, logger=None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item=8440, id=1, level=3, tags=['merge', 'emergency', 'fix:survey'],
                                               title=T_('Emergency point not integrated'))
        self.possible_merge = self.def_class(item=8441, id=3, level=3, tags=['merge', 'emergency', 'fix:survey', 'fix:chair'],
                                               title=T_('Emergency point integration suggestion'))
        self.init(
            "https://data.public.lu/fr/datasets/linstallation-des-points-de-secours-rettungspunkte",
            "Points de secours",
            CSV(SourcePublicLu(attribution="Corps grand-ducal d'incendie et de secours",
                       dataset="5eec6f76d2bfb251e132f1ba",
                       resource="b8d9d38a-7894-49fb-ab88-94072fe2c722",
                       encoding="iso-8859-1"),
                separator=";"),
            Load("GEOGRAPHISCHE LÄNGE", "GEOGRAPHISCHE BREITE"),
            Conflate(
                select=Select(
                    types=["nodes"],
                    tags={"highway": "emergency_access_point"}),
                osmRef = "ref",
                conflationDistance=50,
                mapping=Mapping(
                    static1={
                        "highway": "emergency_access_point"
                    },
                    static2={
                        "source": self.source,
                    },
                    mapping1={
                        "ref": "NAME",
                        "name": "ZUSATZ"
                    }
                )))
