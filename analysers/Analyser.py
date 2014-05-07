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

import __builtin__
import re, hashlib
from modules import OsmoseTranslation

if not hasattr(__builtin__, "T_"):
    translate = OsmoseTranslation.OsmoseTranslation()
    __builtin__.T_ = translate.translate

class Analyser(object):

    def __init__(self, config, logger = None):
        self.config = config
        self.logger = logger
        if not hasattr(__builtin__, "T_"):
            self.translate = OsmoseTranslation.OsmoseTranslation()
            __builtin__.T_ = self.translate.translate

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

    def stablehash(self, s):
        """
        Compute a stable positive integer hash on 32bits
        @param s: a string
        """
        return int(abs(int(hashlib.md5(s).hexdigest(), 16)) % 2147483647)
