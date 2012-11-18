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

    FixTable = {'~':'modify', '+':'create', '-':'delete'}

    def fixdiff(self, fixes):
        """
        Normalise fix in e
        Normal form is [[{'+':{'k1':'v1', 'k2', 'v2'}, '-':{'k3':'v3'}, '~':{'k4','v4'}}, {...}]]
        Array of diff way to fix -> Array of fix for object part of error -> Dict for diff actions -> Dict for tags
        """
        if not isinstance(fixes, list):
            fixes = [[fixes]]
        elif not isinstance(fixes[0], list):
            # Default one level array is different way of fix
            fixes = map(lambda x: [x], fixes)
        return map(lambda fix:
            map(lambda f:
                None if f == None else (f if f.has_key('~') or f.has_key('-') or f.has_key('+') else {'~': f}),
                fix),
            fixes)


if __name__ == "__main__":
    import pprint
    a = Analyser(None)
    def check(b, c):
        d = a.fixdiff(b)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d)
        if d != c:
            raise Exception("fixdiff Excepted %s to %s but get %s" % (b, c, d) )
    check([[None]], [[None]] )
    check({"t": "v"}, [[{"~": {"t": "v"}}]] )
    check({"~": {"t": "v"}}, [[{"~": {"t": "v"}}]] )
    check({"~": {"t": "v"}, "+": {"t": "v"}}, [[{"~": {"t": "v"}, "+": {"t": "v"}}]] )
    check([{"~": {"t": "v"}, "+": {"t": "v"}}], [[{"~": {"t": "v"}, "+": {"t": "v"}}]] )
    check([{"~": {"t": "v"}}, {"+": {"t": "v"}}], [[{"~": {"t": "v"}}], [{"+": {"t": "v"}}]] )
    check([[{"t": "v"}], [{"t": "v"}]], [[{"~": {"t": "v"}}], [{"~": {"t": "v"}}]] )
    check([[None, {"t": "v"}]], [[None, {"~": {"t": "v"}}]] )
