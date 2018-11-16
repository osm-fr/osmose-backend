#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2013-2018                                 ##
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
from modules import downloader


class Polygon:

    def __init__(self, polygon_id, cache_delay=60):
        polygon_url = "http://polygons.openstreetmap.fr/"
        url = polygon_url + "index.py?id="+str(polygon_id)
        s = downloader.urlread(url, cache_delay)
        url = polygon_url + "get_wkt.py?params=0&id="+str(polygon_id)
        s = downloader.urlread(url, cache_delay)
        if s.startswith("SRID="):
            s = s.split(";", 1)[1]
        self.polygon = loads(s)

    def bbox(self):
        return self.polygon.bounds


###########################################################################
import unittest

class Test(unittest.TestCase):

    def test(self):
        # France
        p = Polygon(1403916)
        assert(p.bbox() != None)
