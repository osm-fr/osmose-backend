#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2011                                      ##
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

import re

class Analyser(object):

    def __init__(self, config, logger = None):
        self.config = config
        self.logger = logger

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    re_points = re.compile("[\(,][^\(,\)]*[\),]")

    def get_points(self, text):
        if not text:
            return []
        pts = []
        for r in self.re_points.findall(text):
            lon, lat = r[1:-1].split(" ")
            pts.append({"lat":lat, "lon":lon})
        return pts

    def analyser(self):
        pass

    def analyser_change(self):
        self.analyser()
