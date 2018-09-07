#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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

from . import analyser_merge_wikipedia as w


class Analyser_Merge_Wikipedia_FR_Airport(w._Analyser_Merge_Wikipedia_Airport):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Airport.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_City(w._Analyser_Merge_Wikipedia_City):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_City.__init__(self, config, "FR", "fr", logger)
        self.sourceWhere = lambda res: not res["titel"].startswith("Canton ") and not res["titel"].startswith("Circonscription ") and not res["titel"].startswith("Arrondissement ")

class Analyser_Merge_Wikipedia_FR_Edu(w._Analyser_Merge_Wikipedia_Edu):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Edu.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Forest(w._Analyser_Merge_Wikipedia_Forest):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Forest.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Glacier(w._Analyser_Merge_Wikipedia_Glacier):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Glacier.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Isle(w._Analyser_Merge_Wikipedia_Isle):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Isle.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Mountain(w._Analyser_Merge_Wikipedia_Mountain):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Mountain.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Pass(w._Analyser_Merge_Wikipedia_Pass):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Pass.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_RailwayStation(w._Analyser_Merge_Wikipedia_RailwayStation):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_RailwayStation.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Waterbody(w._Analyser_Merge_Wikipedia_Waterbody):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_Waterbody.__init__(self, config, "FR", "fr", logger)

class Analyser_Merge_Wikipedia_FR_Chateau(w._Analyser_Merge_Wikipedia_fr_Chateau):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_fr_Chateau.__init__(self, config, "FR", logger)

class Analyser_Merge_Wikipedia_FR_Eglise(w._Analyser_Merge_Wikipedia_fr_Eglise):
    def __init__(self, config, logger = None):
        w._Analyser_Merge_Wikipedia_fr_Eglise.__init__(self, config, "FR", logger)
