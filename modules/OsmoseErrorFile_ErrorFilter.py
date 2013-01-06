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

from shapely.wkt import loads
from shapely.geometry import Point


class ErrorFilter:
    def apply(self, classs, subclass, geom):
        return True


class PolygonErrorFilter(ErrorFilter):

    def __init__(self, polygon_file):
        f = open(polygon_file)
        s = f.read()
        if s.startswith("SRID="):
            s = s.split(";", 1)[1]
        self.polygon = loads(s)
        f.close()

    def apply(self, classs, subclass, geom):
        if "position" not in geom:
            return False
        else:
            inside = False
            for position in geom["position"]:
                lat = float(position["lat"])
                lon = float(position["lon"])
                pt = Point((lon, lat))
                inside |= self.polygon.intersects(pt)
            return inside
