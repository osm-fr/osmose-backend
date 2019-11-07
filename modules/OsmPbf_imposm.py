#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jocelyn Jaubert 2012                                       ##
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

import sys
import time
import dateutil.parser
import traceback
from . import config
from .OsmState import OsmState
import subprocess

###########################################################################

class dummylog:
    def log(self, text):
        return

###########################################################################

class OsmPbfReader:

    def log(self, txt):
        self._logger.log(txt)

    def __init__(self, pbf_file, state_file, logger = dummylog()):
        import imposm.parser.simple
        self.OSMParser = imposm.parser.simple.OSMParser

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
        self.parser = self.OSMParser(concurrency=2,
                                nodes_callback=self.NodeParse,
                                ways_callback=self.WayParse,
                                relations_callback=self.RelationParse)
        self.parser.parse(self._pbf_file)
        del self.parser
        if self._got_error:
            raise Exception()

    def CopyWayTo(self, output):
        self._output = output
        self.parser = self.OSMParser(concurrency=2,
                                nodes_callback=None,
                                ways_callback=self.WayParse,
                                relations_callback=None)
        self.parser.parse(self._pbf_file)
        del self.parser
        if self._got_error:
            raise Exception()

    def CopyRelationTo(self, output):
        self._output = output
        self.parser = self.OSMParser(concurrency=2,
                                nodes_callback=None,
                                ways_callback=None,
                                relations_callback=self.RelationParse)
        self.parser.parse(self._pbf_file)
        del self.parser
        if self._got_error:
            raise Exception()

    def NodeParse(self, nodes):
        if self._got_error:
            return
        for node in nodes:
            data = {}
            data["id"] = node[0]
            data["tag"] = node[1]
            data["lon"] = node[2][0]
            data["lat"] = node[2][1]
            if len(node) > 3:
                data["version"] = node[3]
                data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(node[4]))
                data["uid"] = node[5]
            try:
                self._output.NodeCreate(data)
            except:
                print(node, data)
                print(traceback.format_exc())
                self._got_error = True

    def WayParse(self, ways):
        if self._got_error:
            return
        for way in ways:
            data = {}
            data["id"] = way[0]
            data["tag"] = way[1]
            data["nd"] = way[2]
            if len(way) > 3:
                data["version"] = way[3]
                data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(way[4]))
                data["uid"] = way[5]
            try:
                self._output.WayCreate(data)
            except:
                print(way, data)
                print(traceback.format_exc())
                self._got_error = True

    def RelationParse(self, relations):
        if self._got_error:
            return
        for relation in relations:
            data = {}
            data["id"] = relation[0]
            data["tag"] = relation[1]
            if len(relation) > 3:
                data["version"] = relation[3]
                data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(relation[4]))
                data["uid"] = relation[5]
            data["member"] = []
            for (ref, type, role) in relation[2]:
                attrs = { "ref": int(ref),
                          "role": role,
                          "type": type,
                        }

                data["member"].append(attrs)

            try:
                self._output.RelationCreate(data)
            except:
                print(data)
                print(traceback.format_exc())
                self._got_error = True


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

@unittest.skipIf(sys.version_info > (3, ), "imposm is not supported in python3")
class Test(unittest.TestCase):
    def test_copy_all(self):
        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 83)  # only nodes with tags are reported
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)
        self.assertEqual(i1.timestamp(), dateutil.parser.parse("2015-03-25T19:05:08Z").replace(tzinfo=None))

    def test_copy_all_no_state_txt(self):
        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", None)
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 83)  # only nodes with tags are reported
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)
        self.assertEqual(i1.timestamp(), dateutil.parser.parse("2014-01-15T19:05:08Z").replace(tzinfo=None))

    def test_copy_all_pbf_timestamp(self):
        i1 = OsmPbfReader("tests/gibraltar.osm.pbf", None)
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 850)  # only nodes with tags are reported
        self.assertEqual(o1.num_ways, 3833)
        self.assertEqual(o1.num_rels, 55)
        self.assertEqual(i1.timestamp(), dateutil.parser.parse("2017-09-03T23:40:03Z").replace(tzinfo=None))

    def test_copy_way(self):
        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyWayTo(o1)
        self.assertEqual(o1.num_nodes, 0)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 0)

    def test_copy_relation(self):
        i1 = OsmPbfReader("tests/saint_barthelemy.osm.pbf", "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyRelationTo(o1)
        self.assertEqual(o1.num_nodes, 0)
        self.assertEqual(o1.num_ways, 0)
        self.assertEqual(o1.num_rels, 16)
