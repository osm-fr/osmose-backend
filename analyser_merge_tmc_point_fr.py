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

from Analyser_Merge import Analyser_Merge


class _Analyser_Merge_TMC_Point_Fr(Analyser_Merge):
    def __init__(self, config, logger, level, desc, osmTags, osmTypes, c, tcd, stcd):
        self.missing_official = {"item":"7110", "class": tcd*10+stcd, "level": level, "tag": ["merge", "highway"], "desc":desc}
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://diffusion-numerique.info-routiere.gouv.fr/tables-alert-c-a4.html"
        self.officialName = "Alert-C-point"
        self.osmTags = osmTags
        self.osmTypes = osmTypes
        self.sourceTable = "tmc_point_fr"
        self.sourceX = "xcoord"
        self.sourceXfunction = lambda x: x/100000
        self.sourceY = "ycoord"
        self.sourceYfunction = lambda y: y/100000
        self.sourceSRID = "4326"
        self.sourceWhere = lambda res: res["class"] == c and res["tcd"] == str(tcd) and res["stcd"] == str(stcd)
        self.conflationDistance = 100


class Analyser_Merge_TMC_Point_Bridge_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            2,
            {"fr":u"Pont manquant (TMC)"},
            {"highway": None, "bridge": None},
            ["ways"],
            "P", 3, 1)

class Analyser_Merge_TMC_Point_Rest_Area_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            1,
            {"fr":u"Aire de repos manquante (TMC)"},
            {"highway": "rest_area"},
            ["nodes", "ways"],
            "P", 3, 4)

class Analyser_Merge_TMC_Point_Roundabout_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            2,
            {"fr":u"Rond-point manquant (TMC)"},
            {"highway": None, "junction": "roundabout"},
            ["ways"],
            "P", 1, 8)

class Analyser_Merge_TMC_Point_Services_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            2,
            {"fr":u"Aire de services manquante (TMC)"},
            {"highway": "services"},
            ["nodes", "ways"],
            "P", 3, 3)

class Analyser_Merge_TMC_Point_Toll_Booth_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            1,
            {"fr":u"Péage manquant (TMC)"},
            {"barrier": "toll_booth"},
            ["nodes", "ways"],
            "P", 3, 16)


class Analyser_Merge_TMC_Point_Traffic_Signals_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            2,
            {"fr":u"Feu de signalisation manquant (TMC)"},
            {"highway": "traffic_signals"},
            ["nodes"],
            "P", 1, 10)


class Analyser_Merge_TMC_Point_Tunnel_Fr(_Analyser_Merge_TMC_Point_Fr):
    def __init__(self, config, logger = None):
        _Analyser_Merge_TMC_Point_Fr.__init__(self, config, logger,
            1,
            {"fr":u"Tunnel manquant (TMC)"},
            {"highway": None, "tunnel": None},
            ["ways"],
            "P", 3, 1)
