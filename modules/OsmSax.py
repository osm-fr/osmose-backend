###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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
import gzip
from xml.sax import make_parser, handler
from xml.sax.saxutils import XMLGenerator, quoteattr
import dateutil.parser
from . import config
from .OsmState import OsmState
import subprocess
from io import StringIO
from .OsmReader import OsmReader, dummylog

###########################################################################

class dummyout:
    def __init__(self):
        self._n = 0
        self._w = 0
        self._r = 0
    def NodeCreate(self, data):
        self._n += 1
        return
    def WayCreate(self, data):
        self._w += 1
        return
    def RelationCreate(self, data):
        self._r += 1
        return
    def __del__(self):
        print(self._n, self._w, self._r)

###########################################################################

class OsmSaxNotXMLFile(Exception):
    pass

class OsmSaxReader(OsmReader, handler.ContentHandler):

    def log(self, txt):
        self._logger.log(txt)

    def __init__(self, filename, logger = dummylog(), state_file = None):
        self._filename = filename
        self._state_file = state_file
        self._logger   = logger
        self.since_timestamp = None

        # check if file begins with an xml tag
        f = self._GetFile()
        line = f.readline()
        if not line.startswith(b"<?xml"):
            raise OsmSaxNotXMLFile("File %s is not XML" % filename)

    def set_filter_since_timestamp(self, since_timestamp):
        self.since_timestamp = since_timestamp.isoformat()
        self.filtered_nodes_osmid = []
        self.filtered_wayss_osmid = []
        self.filtered_relationss_osmid = []

    def filtered_nodes(self):
        return self.filtered_nodes_osmid

    def filtered_ways(self):
        return self.filtered_wayss_osmid

    def filtered_relations(self):
        return self.filtered_relationss_osmid

    def timestamp(self):
        if self._state_file:
            osm_state = OsmState(self._state_file)
            return osm_state.timestamp()

        else:
            try:
                # Compute max timestamp from data
                res = subprocess.check_output('{} {} --out-statistics | grep "timestamp max"'.format(config.bin_osmconvert, self._filename), shell=True).decode('utf-8')
                s = res.split(' ')[2]
                return dateutil.parser.parse(s).replace(tzinfo=None)
            except:
                return

    def _GetFile(self):
        try:
            if self._filename.endswith(".bz2"):
                return bz2.BZ2File(self._filename)
            elif self._filename.endswith(".gz"):
                return gzip.open(self._filename)
            else:
                return open(self._filename, "rb")
        except AttributeError:
            return self._filename

    def CopyTo(self, output):
        self._debug_in_way      = False
        self._debug_in_relation = False
        self.log("starting nodes")
        self._output = output
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(self._GetFile())

    def startElement(self, name, attrs):
        attrs = attrs._attrs
        if name == "changeset":
            self._tags = {}
        elif name == "node":
            attrs["id"] = int(attrs["id"])
            attrs["lat"] = float(attrs["lat"])
            attrs["lon"] = float(attrs["lon"])
            if "version" in attrs:
                attrs["version"] = int(attrs["version"])
            if "user" in attrs:
                attrs["user"] = attrs["user"]
            self._data = attrs
            self._tags = {}
        elif name == "way":
            if not self._debug_in_way:
                self._debug_in_way = True
                self.log("starting ways")
            attrs["id"] = int(attrs["id"])
            if "version" in attrs:
                attrs["version"] = int(attrs["version"])
            if "user" in attrs:
                attrs["user"] = attrs["user"]
            self._data = attrs
            self._tags = {}
            self._nodes = []
        elif name == "relation":
            if not self._debug_in_relation:
                self._debug_in_relation = True
                self.log("starting relations")
            attrs["id"] = int(attrs["id"])
            if "version" in attrs:
                attrs["version"] = int(attrs["version"])
            if "user" in attrs:
                attrs["user"] = attrs["user"]
            self._data = attrs
            self._members = []
            self._tags = {}
        elif name == "nd":
            self._nodes.append(int(attrs["ref"]))
        elif name == "tag":
            self._tags[attrs["k"]] = attrs["v"]
        elif name == "member":
            attrs["type"] = attrs["type"]
            attrs["ref"] = int(attrs["ref"])
            attrs["role"] = attrs["role"]
            self._members.append(attrs)

    def endElement(self, name):
        if name == "node":
            self._data["tag"] = self._tags
            try:
                if self.since_timestamp is None or self._data['timestamp'] is None or self._data['timestamp'] > self.since_timestamp:
                    self._output.NodeCreate(self._data)
                else:
                    self.filtered_nodes_osmid.append(self._data['id'])
            except:
                print(self._data)
                raise
        elif name == "way":
            self._data["tag"] = self._tags
            self._data["nd"]  = self._nodes
            try:
                if self.since_timestamp is None or self._data['timestamp'] is None or self._data['timestamp'] > self.since_timestamp:
                    self._output.WayCreate(self._data)
                else:
                    self.filtered_nodes_osmid.append(self._data['id'])
            except:
                print(self._data)
                raise
        elif name == "relation":
            self._data["tag"]    = self._tags
            self._data["member"] = self._members
            try:
                if self.since_timestamp is None or self._data['timestamp'] is None or self._data['timestamp'] > self.since_timestamp:
                    self._output.RelationCreate(self._data)
                else:
                    self.filtered_nodes_osmid.append(self._data['id'])
            except:
                print(self._data)
                raise

###########################################################################

class OscSaxReader(OsmReader, handler.ContentHandler):

    def log(self, txt):
        self._logger.log(txt)

    def __init__(self, filename, logger = dummylog(), state_file = None):
        self._filename = filename
        self._logger   = logger

    def is_change(self):
        return True

    def _GetFile(self):
        try:
            if self._filename.endswith(".bz2"):
                return bz2.BZ2File(self._filename)
            elif self._filename.endswith(".gz"):
                return gzip.open(self._filename)
            else:
                return open(self._filename)
        except AttributeError:
            return self._filename

    def CopyTo(self, output):
        self._output = output
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(self._GetFile())

    def startElement(self, name, attrs):
        attrs = attrs._attrs
        if name == "create":
            self._action = name
        elif name == "modify":
            self._action = name
        elif name == "delete":
            self._action = name
        elif name == "node":
            attrs["id"] = int(attrs["id"])
            attrs["lat"] = float(attrs["lat"])
            attrs["lon"] = float(attrs["lon"])
            attrs["version"] = int(attrs["version"])
            self._data = attrs
            self._tags = {}
        elif name == "way":
            attrs["id"] = int(attrs["id"])
            attrs["version"] = int(attrs["version"])
            self._data = attrs
            self._tags = {}
            self._nodes = []
        elif name == "relation":
            attrs["id"] = int(attrs["id"])
            attrs["version"] = int(attrs["version"])
            self._data = attrs
            self._members = []
            self._tags = {}
        elif name == "nd":
            self._nodes.append(int(attrs["ref"]))
        elif name == "tag":
            self._tags[attrs["k"]] = attrs["v"]
        elif name == "member":
            attrs["ref"] = int(attrs["ref"])
            self._members.append(attrs)

    def endElement(self, name):
        if name == "node":
            self._data["tag"] = self._tags
            if self._action == "create":
                self._output.NodeCreate(self._data)
            elif self._action == "modify":
                self._output.NodeUpdate(self._data)
            elif self._action == "delete":
                self._output.NodeDelete(self._data)
        elif name == "way":
            self._data["tag"] = self._tags
            self._data["nd"]  = self._nodes
            if self._action == "create":
                self._output.WayCreate(self._data)
            elif self._action == "modify":
                self._output.WayUpdate(self._data)
            elif self._action == "delete":
                self._output.WayDelete(self._data)
        elif name == "relation":
            self._data["tag"]    = self._tags
            self._data["member"] = self._members
            if self._action == "create":
                self._output.RelationCreate(self._data)
            elif self._action == "modify":
                self._output.RelationUpdate(self._data)
            elif self._action == "delete":


                self._output.RelationDelete(self._data)
            return

###########################################################################

def _formatData(data):
    data = dict(data)
    if "tag" in data:
        data.pop("tag")
    if "nd" in data:
        data.pop("nd")
    if "member" in data:
        data.pop("member")
    if "visible" in data:
        data["visible"] = str(data["visible"]).lower()
    if "id" in data:
        data["id"] = str(data["id"])
    if "lat" in data:
        data["lat"] = str(data["lat"])
    if "lon" in data:
        data["lon"] = str(data["lon"])
    if "changeset" in data:
        data["changeset"] = str(data["changeset"])
    if "version" in data:
        data["version"] = str(data["version"])
    if "uid" in data:
        data["uid"] = str(data["uid"])
    return data

class OsmSaxWriter(XMLGenerator):

    def __init__(self, out, enc):
        if type(out) is str:
            XMLGenerator.__init__(self, open(out, "w"), enc)
        else:
            XMLGenerator.__init__(self, out, enc)

    def startElement(self, name, attrs):
        self._write('<' + name)
        for (name, value) in attrs.items():
            self._write(' %s=%s' % (name, quoteattr(value)))
        self._write('>\n')

    def endElement(self, name):
        self._write('</%s>\n' % name)

    def Element(self, name, attrs):
        self._write('<' + name)
        for (name, value) in attrs.items():
            self._write(' %s=%s' % (name, quoteattr(value)))
        self._write(' />\n')

    def NodeCreate(self, data):
        if not data:
            return
        if data["tag"]:
            self.startElement("node", _formatData(data))
            for (k, v) in data["tag"].items():
                self.Element("tag", {"k":k, "v":v})
            self.endElement("node")
        else:
            self.Element("node", _formatData(data))

    def WayCreate(self, data):
        if not data:
            return
        self.startElement("way", _formatData(data))
        for (k, v) in data["tag"].items():
            self.Element("tag", {"k":k, "v":v})
        for n in data["nd"]:
            self.Element("nd", {"ref":str(n)})
        self.endElement("way")

    def RelationCreate(self, data):
        if not data:
            return
        self.startElement("relation", _formatData(data))
        for (k, v) in data["tag"].items():
            self.Element("tag", {"k":k, "v":v})
        for m in data["member"]:
            m["ref"] = str(m["ref"])
            self.Element("member", m)
        self.endElement("relation")

def NodeToXml(data, full = False):
    o = StringIO()
    w = OsmSaxWriter(o, "UTF-8")
    if full:
        w.startDocument()
        w.startElement("osm", {})
    if data:
        w.NodeCreate(data)
    if full:
        w.endElement("osm")
    return o.getvalue()

def WayToXml(data, full = False):
    o = StringIO()
    w = OsmSaxWriter(o, "UTF-8")
    if full:
        w.startDocument()
        w.startElement("osm", {})
    if data:
        w.WayCreate(data)
    if full:
        w.endElement("osm")
    return o.getvalue()

def RelationToXml(data, full = False):
    o = StringIO()
    w = OsmSaxWriter(o, "UTF-8")
    if full:
        w.startDocument()
        w.startElement("osm", {})
    if data:
        w.RelationCreate(data)
    if full:
        w.endElement("osm")
    return o.getvalue()


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
    def test_bz2(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.bz2", state_file = "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 8076)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)
        self.assertEqual(i1.timestamp(), dateutil.parser.parse("2015-03-25T19:05:08Z").replace(tzinfo=None))

    def test_gz(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz", state_file = "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 8076)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)

    def test_gz_no_state_txt(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 8076)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)
        self.assertEqual(i1.timestamp(), dateutil.parser.parse("2014-01-15T19:05:08Z").replace(tzinfo=None))

    def test_file(self):
        f = gzip.open("tests/saint_barthelemy.osm.gz")
        i1 = OsmSaxReader(f, state_file = "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 8076)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)

    def test_subprocess(self):
        import io
        f = io.BytesIO(subprocess.check_output(["gunzip", "-c", "tests/saint_barthelemy.osm.gz"]))
        i1 = OsmSaxReader(f, state_file = "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 8076)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)


    def test_stream_io(self):
        import io
        f = gzip.open("tests/saint_barthelemy.osm.gz")
        io = io.BytesIO(f.read())
        i1 = OsmSaxReader(io, state_file = "tests/saint_barthelemy.state.txt")
        o1 = MockCountObjects()
        i1.CopyTo(o1)
        self.assertEqual(o1.num_nodes, 8076)
        self.assertEqual(o1.num_ways, 625)
        self.assertEqual(o1.num_rels, 16)
        io.close()
