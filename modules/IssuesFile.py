#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2013                                      ##
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

import bz2
from .IssuesFile_PolygonFilter import PolygonFilter


class IssuesFile:

    def __init__(self, dst, version = None, polygon_id = None):
        self.dst = dst
        self.version = version
        self.filter = None
        if polygon_id:
            try:
                self.filter = PolygonFilter(polygon_id)
            except Exception as e:
                print(e)
                pass

    def begin(self):
        if isinstance(self.dst, str):
            if self.dst.endswith(".bz2"):
                self.output = bz2.open(self.dst, "wt")
            else:
                self.output = open(self.dst, "w")
        else:
            self.output = self.dst
        return self.output

    def end(self):
        if isinstance(self.dst, str):
            self.output.close()

    def analyser(self, timestamp, analyser_version, change=False):
        pass

    def analyser_end(self):
        pass

    def classs(self, id, item, level, tags, title, detail = None, fix = None, trap = None, example = None, source = None, resource = None):
        pass

    def error(self, classs, subclass, text, ids, types, fix, geom, allow_override=False):
        if self.filter and not self.filter.apply(classs, subclass, geom):
            return

    def delete(self, t, id):
        pass

    FixTable = {'~':'modify', '+':'create', '-':'delete'}

    def fixdiff(self, fixes):
        """
        Normalise fix in e
        Normal form is [[{'+':{'k1':'v1', 'k2', 'v2'}, '-':{'k3':'v3'}, '~':{'k4','v4'}}, {...}]]
        Array of alternative ways to fix -> Array of fix for objects part of error -> Dict for diff actions -> Dict for tags
        """
        if not isinstance(fixes, list):
            fixes = [[fixes]]
        elif not isinstance(fixes[0], list):
            # Default one level array is different way of fix
            fixes = list(map(lambda x: [x], fixes))
        return list(map(lambda fix:
            list(map(lambda f:
                None if f is None else (f if '~' in f or '-' in f or '+' in f else {'~': f}),
                fix)),
            fixes))

    def filterfix(self, ids, types, fixes, geom):
        ret_fixes = []
        for fix in fixes:
            i = 0
            for f in fix:
                if f is not None and i < len(types):
                    osm_obj = next((x for x in geom[types[i]] if x['id'] == ids[i]), None)
                    if osm_obj:
                        fix_tags = f['+'].keys() if '+' in f else []
                        if len(set(osm_obj['tag'].keys()).intersection(fix_tags)) > 0:
                            # Fix try to override existing tag in object, drop the fix
                            i = 0
                            break
                i += 1
            if i > 0:
                ret_fixes.append(fix)
        return ret_fixes

################################################################################
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.a = IssuesFile(None)

    def check(self, b, c):
        import pprint
        d = self.a.fixdiff(b)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d)
        self.assertEqual(c, d, "fixdiff Excepted %s to %s but get %s" % (b, c, d))

    def test(self):
        self.check([[None]], [[None]] )
        self.check({"t": "v"}, [[{"~": {"t": "v"}}]] )
        self.check({"~": {"t": "v"}}, [[{"~": {"t": "v"}}]] )
        self.check({"~": {"t": "v"}, "+": {"t": "v"}}, [[{"~": {"t": "v"}, "+": {"t": "v"}}]] )
        self.check([{"~": {"t": "v"}, "+": {"t": "v"}}], [[{"~": {"t": "v"}, "+": {"t": "v"}}]] )
        self.check([{"~": {"t": "v"}}, {"+": {"t": "v"}}], [[{"~": {"t": "v"}}], [{"+": {"t": "v"}}]] )
        self.check([[{"t": "v"}], [{"t": "v"}]], [[{"~": {"t": "v"}}], [{"~": {"t": "v"}}]] )
        self.check([[None, {"t": "v"}]], [[None, {"~": {"t": "v"}}]] )
