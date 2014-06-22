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
from modules import OsmoseErrorFile
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
        self.open_error_file()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_error_file()
        pass

    def open_error_file(self):
        self.error_file = OsmoseErrorFile.ErrorFile(self.config)
        self.error_file.begin()

    def close_error_file(self):
        self.error_file.end()

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
        return int(abs(int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)) % 2147483647)

###########################################################################
import unittest

class TestAnalyser(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        import __builtin__
        import sys
        sys.path.append(".")
        import modules.OsmoseLog
        if not hasattr(cls, "logger"):
            cls.logger = modules.OsmoseLog.logger(sys.stdout, True)

    @classmethod
    def teardown_class(cls):
        pass


    def load_errors(self):
        import xml.etree.ElementTree as ET
        tree = ET.parse(self.xml_res_file)
        return tree.getroot()

    def check_err(self, cl=None, lat=None, lon=None, elems=None):
        for e in self.root_err.find("analyser").findall('error'):
            if cl is not None and e.attrib["class"] != cl:
               continue
            if lat is not None and e.find("location").attrib["lat"] != lat:
               continue
            if lon is not None and e.find("location").attrib["lon"] != lon:
               continue
            if elems is not None:
               xml_elems = []
               for t in ("node", "way", "relation"):
                   for err_elem in e.findall(t):
                       xml_elems.append((t, err_elem.attrib["id"]))
               if set(elems) != set(xml_elems):
                   continue
            return True

        assert False, "Error not found"

    def check_num_err(self, num=None, min=None):
        xml_num = len(self.root_err.find("analyser").findall('error'))
        if num is not None:
            self.assertEquals(xml_num, num, "Found %d errors instead of %d" % (xml_num, num))
        if min is not None:
            self.assertGreaterEqual(xml_num, min, "Found %d errors instead of > %d" % (xml_num, min))


###########################################################################

class Test(unittest.TestCase):
    def test_stablehash(self):
        a = Analyser(None)
        h1 = a.stablehash( "toto")
        h2 = a.stablehash(u"toto")
        h3 = a.stablehash(u"é")
        self.assertEquals(h1, h2)
        self.assertNotEquals(h1, h3)
