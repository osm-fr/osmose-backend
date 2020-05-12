#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select


class _Analyser_Merge_TMC_Point_FR(Analyser_Merge):
    def __init__(self, config, logger, level, title, osmTags, osmTypes, c, tcd, stcd, threshold):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 7110, id = tcd*100+stcd, level = level, tags = ['merge', 'highway'],
            title = title,
            detail = T_(
'''TMC data refers to a not found element of the road network. '''),
            trap = T_(
'''TMC data may be wrong or poorly located.'''))

        self.init(
            u"http://diffusion-numerique.info-routiere.gouv.fr/tables-alert-c-a4.html",
            "Alert-C-point",
            CSV(Source(fileUrl = u"http://diffusion-numerique.info-routiere.gouv.fr/IMG/zip/cd_alert_c_v12.1.zip", zip = "Data/Mff/POINTS.DAT"),
                separator = u";"),
            Load("XCOORD", "YCOORD",
                xFunction = lambda x: float(x)/100000,
                yFunction = lambda y: float(y)/100000,
                where = lambda res: res["CLASS"] == c and res["TCD"] == str(tcd) and res["STCD"] == str(stcd)),
            Mapping(
                select = Select(
                    types = osmTypes,
                    tags = osmTags),
                conflationDistance = threshold))


class Analyser_Merge_TMC_Point_Bridge_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            2,
            T_(u"Bridge missing (TMC)"),
            {"highway": ["motorway", "motorway_link", "primary", "primary_link", "secondary", "secondary_link", "tertiary", "tertiary_link"], "bridge": None},
            ["ways"],
            "P", 3, 1,
            500)

class Analyser_Merge_TMC_Point_Rest_Area_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            1,
            T_(u"Rest area missing"),
            {"highway": "rest_area"},
            ["nodes", "ways"],
            "P", 3, 4,
            300)

class Analyser_Merge_TMC_Point_Roundabout_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            2,
            T_(u"Roundabout missing (TMC)"),
            {"highway": ["motorway", "motorway_link", "primary", "primary_link", "secondary", "secondary_link", "tertiary", "tertiary_link"], "junction": "roundabout"},
            ["ways"],
            "P", 1, 8,
            150)

class Analyser_Merge_TMC_Point_Services_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            2,
            T_(u"Services area missing (TMC)"),
            {"highway": "services"},
            ["nodes", "ways"],
            "P", 3, 3,
            300)

class Analyser_Merge_TMC_Point_Toll_Booth_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            1,
            T_(u"Toll missing (TMC)"),
            {"barrier": "toll_booth"},
            ["nodes", "ways"],
            "P", 3, 16,
            500)

class Analyser_Merge_TMC_Point_Traffic_Signals_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            2,
            T_(u"Traffic signals missing (TMC)"),
            {"highway": "traffic_signals"},
            ["nodes"],
            "P", 1, 10,
            100)

class Analyser_Merge_TMC_Point_Tunnel_Fr(_Analyser_Merge_TMC_Point_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_FR.__init__(self, config, logger,
            1,
            T_(u"Tunnel missing (TMC)"),
            {"highway": ["motorway", "motorway_link", "primary", "primary_link", "secondary", "secondary_link", "tertiary", "tertiary_link"], "tunnel": None},
            ["ways"],
            "P", 3, 5,
            500)
