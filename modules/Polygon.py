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
from shapely.geometry import MultiPolygon
from modules import downloader


class Polygon:

    def __init__(self, polygon_id, cache_delay=60):
        polygon_url = u"http://polygons.openstreetmap.fr/"
        url = polygon_url + "index.py?id="+str(polygon_id)
        s = downloader.urlread(url, cache_delay)
        url = polygon_url + "get_wkt.py?params=0&id="+str(polygon_id)
        s = downloader.urlread(url, cache_delay)
        if s.startswith("SRID="):
            s = s.split(";", 1)[1]
        self.polygon = loads(s)

    def bboxes(self):
        bbox = self.polygon.bounds
        if not(bbox[0] < -179 and bbox[2] > 179):
            return [bbox]
        else: # Cross the 180°
            negative = []
            positive = []
            for polygon in self.polygon:
                sub_bbox = polygon.bounds
                if sub_bbox[0] < 0:
                    negative.append(polygon)
                else:
                    positive.append(polygon)
            return [
                MultiPolygon(negative).bounds,
                MultiPolygon(positive).bounds,
            ]


###########################################################################
import unittest

class Test(unittest.TestCase):

    def test(self):
        # France
        p = Polygon(1403916)
        b = p.bboxes()
        self.assertNotEquals(b, None)
        self.assertEquals(len(b), 1)

        # Alaska
        p = Polygon(1116270)
        b = p.bboxes()
        self.assertNotEquals(b, None)
        self.assertEquals(len(b), 2)
