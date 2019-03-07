#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jocelyn Jaubert 2019                                       ##
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

from . import OsmPbf_imposm
OsmPbfReader = OsmPbf_imposm.OsmPbfReader
TestCountObjects = OsmPbf_imposm.TestCountObjects

###########################################################################
import unittest

class Test(unittest.TestCase):
    def test_copy_all(self):
        # basic test to verify connection to submodules
        import dateutil

        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", "tests/saint_barthelemy.state.txt")
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 83)  # only nodes with tags are reported
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)
        self.assertEquals(i1.timestamp(), dateutil.parser.parse("2015-03-25T19:05:08Z").replace(tzinfo=None))
