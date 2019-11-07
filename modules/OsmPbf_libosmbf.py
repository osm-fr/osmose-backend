#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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

import time
import dateutil.parser
import traceback
from . import config
from .osm_pbf_parser import osm_pbf_parser
from .OsmState import OsmState
import subprocess

###########################################################################

class dummylog:
    def log(self, text):
        return

###########################################################################

class OsmPbfReader(osm_pbf_parser.Visitor):

    def log(self, txt):
        self._logger.log(txt)

    def __init__(self, pbf_file, state_file, logger = dummylog()):
        osm_pbf_parser.Visitor.__init__(self)
        self._pbf_file = pbf_file
        self._state_file = state_file
        self._logger = logger
        self._got_error = False

    def timestamp(self):
        if self._state_file:
            osm_state = OsmState(self._state_file)
            return osm_state.timestamp()

        else:
            try:
                # Try to get timestamp from metadata
                res = subprocess.check_output([config.bin_osmconvert, self._pbf_file, '--out-timestamp']).decode('utf-8')
                d = dateutil.parser.parse(res).replace(tzinfo=None)
                if not d:
                    raise ValueError()
                return d
            except:
                pass

            try:
                # Compute max timestamp from data
                res = subprocess.check_output('{} {} --out-statistics | grep "timestamp max"'.format(config.bin_osmconvert, self._pbf_file), shell=True).decode('utf-8')
                s = res.split(' ')[2]
                return dateutil.parser.parse(s).replace(tzinfo=None)

            except:
                return


    def CopyTo(self, output):
        self._output = output
        osm_pbf_parser.read_osm_pbf(self._pbf_file, self)


    def node(self, osmid, lon, lat, tags):
        data = {
            'id': osmid,
            'lon': lon,
            'lat': lat,
            'tag': tags,
            #'version'
            #'timestamp'
            #'uid'
        }
        self._output.NodeCreate(data)

    def way(self, osmid, tags, refs):
        data = {
            'id': osmid,
            'tag': tags,
            'nd': refs,
            #'version'
            #'timestamp'
            #'uid'
        }
        self._output.WayCreate(data)

    def relation(self, osmid, tags, ref):
        data = {
            'id': osmid,
            'tag': tags,
            #'version'
            #'timestamp'
            #'uid'
            'member': ref,
        }
        self._output.RelationCreate(data)


###########################################################################
import unittest

class MockCountObjects:
    def __init__(self):
        self.num_nodes = 0
        self.num_ways = 0
        self.num_rels = 0

    def NodeCreate(self, data):
        self.num_nodes += 1

    def WayCreate(self, data):
        self.num_ways += 1

    def RelationCreate(self, data):
        self.num_rels += 1

class Test(unittest.TestCase):
    def test_copy_all(self):
        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 83)  # only nodes with tags are reported
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)
        self.assertEquals(i1.timestamp(), dateutil.parser.parse("2015-03-25T19:05:08Z").replace(tzinfo=None))

    def test_copy_all_no_state_txt(self):
        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", None)
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 83)  # only nodes with tags are reported
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)
        self.assertEquals(i1.timestamp(), dateutil.parser.parse("2014-01-15T19:05:08Z").replace(tzinfo=None))

    def test_copy_all_pbf_timestamp(self):
        i1 = OsmPbfReader("tests/gibraltar.osm.pbf", None)
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 850)  # only nodes with tags are reported
        self.assertEquals(o1.num_ways, 3833)
        self.assertEquals(o1.num_rels, 55)
        self.assertEquals(i1.timestamp(), dateutil.parser.parse("2017-09-03T23:40:03Z").replace(tzinfo=None))
