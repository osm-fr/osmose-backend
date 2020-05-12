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

from .Analyser_Merge import Analyser_Merge, Select


class _Analyser_Merge_Street_Number(Analyser_Merge):

    def __init__(self, config, classs, city, logger, url, name, parser, load, mapping):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8080, id = classs, level = 3, tags = ['addr'],
            title = T_f('Missing address {0}', city),
            detail = T_(
'''Address in an OpenData set was not found. Only the position and
street numbers are checked.'''),
            fix = T_(
'''Add or move a number, check the field.'''),
            trap = T_(
'''Pay attention to the data freshness.'''))

        self.init( url, name, parser, load, mapping)
        self.mapping.select = Select(
            types = ["nodes", "ways"],
            tags = [{"addr:housenumber": None}])
        self.mapping.extraJoin = "addr:housenumber"
        self.mapping.conflationDistance = 100
