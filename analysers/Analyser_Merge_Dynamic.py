#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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

from .Analyser import Analyser
from .Analyser_Merge import Analyser_Merge, Source, Load, Mapping


class Analyser_Merge_Dynamic(Analyser):

    def classFactory(self, classs, subclass_name, *args):
        def __init__(self, config, error_file, logger = None):
            classs.__init__(self, config, error_file, logger, *args)

        generatedClass = type("{0}_{1}".format(classs.__name__, subclass_name), (classs,), {"__init__": __init__})
        self.analysers.append(generatedClass)

    def __init__(self, config, logger = None):
        Analyser.__init__(self, config, logger)
        self.analysers = []

    def analyser(self):
        for obj in self.analysers:
            with obj(self.config, self.error_file,  self.logger) as analyser_obj:
#                if not options.change or not xml_change:
                    analyser_obj.analyser()
#                else:
#                    analyser_obj.analyser_change()

    def timestamp(self):
        with self.analysers[0](self.config, self.error_file,  self.logger) as analyser_obj:
            return analyser_obj.timestamp()


class SubAnalyser_Merge_Dynamic(Analyser_Merge):

    def __init__(self, config, error_file, logger):
        Analyser_Merge.__init__(self, config, logger)
        self.error_file = error_file

    def init(self, url, name, source = Source(), load = Load(), mapping = Mapping()):
        if not load.table_name: # Rename all table of sub analysers the same
            load.table_name = self.__class__.__name__.lower()[18:]
            load.table_name = '_'.join(load.table_name.split('_')[:-1])
        Analyser_Merge.init(self, url, name, source, load, mapping)

    def open_error_file(self):
        pass

    def close_error_file(self):
        pass
