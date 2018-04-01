#-*- coding: utf-8 -*-

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

import bz2, gzip
from xml.sax import make_parser, handler
from xml.sax.saxutils import XMLGenerator, quoteattr
import dateutil.parser
from . import config
from .OsmState import OsmState

try:
    # For Python 3.0 and later
    import subprocess
    getstatusoutput = subprocess.getstatusoutput
except:
    # Fall back to Python 2
    import commands
    getstatusoutput = commands.getstatusoutput

try:
    # For Python 3.0 and later
    from io import StringIO
except ImportError:
    # Fall back to Python 2
    from cStringIO import StringIO

###########################################################################

class dummylog:
    def log(self, text):
        return

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

class OsmSaxReader(handler.ContentHandler):

    def log(self, txt):
        self._logger.log(txt)
    
    def __init__(self, filename, state_file = None, logger = dummylog()):
        self._filename = filename
        self._state_file = state_file
        self._logger   = logger

        # check if file begins with an xml tag
        f = self._GetFile()
        line = f.readline()
        if not line.startswith("<?xml"):
            raise OsmSaxNotXMLFile("File %s is not XML" % filename)

    def timestamp(self):
        if self._state_file:
            osm_state = OsmState(self._state_file)
            return osm_state.timestamp()

        else:
            try:
                # Compute max timestamp from data
                res = getstatusoutput("%s %s --out-statistics | grep 'timestamp max'" % (config.bin_osmconvert, self._filename))
                if not res[0]:
                    s = res[1].split(' ')[2]
                    return dateutil.parser.parse(s).replace(tzinfo=None)
            except:
                return

    def _GetFile(self):
        if isinstance(self._filename, basestring):
            if self._filename.endswith(".bz2"):
                return bz2.BZ2File(self._filename)
            elif self._filename.endswith(".gz"):
                return gzip.open(self._filename)
            else:
                return open(self._filename)
        else:
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
        if name == u"changeset":
            self._tags = {}
        elif name == u"node":
            attrs[u"id"] = int(attrs[u"id"])
            attrs[u"lat"] = float(attrs[u"lat"])
            attrs[u"lon"] = float(attrs[u"lon"])
            if u"version" in attrs:
                attrs[u"version"] = int(attrs[u"version"])
            if u"user" in attrs:
                attrs[u"user"] = unicode(attrs[u"user"])
            self._data = attrs
            self._tags = {}
        elif name == u"way":
            if not self._debug_in_way:
                self._debug_in_way = True
                self.log("starting ways")
            attrs["id"] = int(attrs["id"])
            if u"version" in attrs:
                attrs[u"version"] = int(attrs[u"version"])
            if u"user" in attrs:
                attrs[u"user"] = unicode(attrs[u"user"])
            self._data = attrs
            self._tags = {}
            self._nodes = []
        elif name == u"relation":
            if not self._debug_in_relation:
                self._debug_in_relation = True
                self.log("starting relations")
            attrs["id"] = int(attrs["id"])
            if u"version" in attrs:
                attrs[u"version"] = int(attrs[u"version"])
            if u"user" in attrs:
                attrs[u"user"] = unicode(attrs[u"user"])
            self._data = attrs
            self._members = []
            self._tags = {}
        elif name == u"nd":
            self._nodes.append(int(attrs["ref"]))
        elif name == u"tag":
            self._tags[attrs["k"]] = attrs["v"]
        elif name == u"member":
            attrs["type"] = attrs["type"]
            attrs["ref"] = int(attrs["ref"])
            attrs["role"] = attrs["role"]
            self._members.append(attrs)

    def endElement(self, name):
        if name == u"node":
            self._data[u"tag"] = self._tags
            try:
                self._output.NodeCreate(self._data)
            except:
                print(self._data)
                raise
        elif name == u"way":
            self._data[u"tag"] = self._tags
            self._data[u"nd"]  = self._nodes
            try:
                self._output.WayCreate(self._data)
            except:
                print(self._data)
                raise
        elif name == u"relation":
            self._data[u"tag"]    = self._tags
            self._data[u"member"] = self._members
            try:
                self._output.RelationCreate(self._data)
            except:
                print(self._data)
                raise

###########################################################################

class OscSaxReader(handler.ContentHandler):

    def log(self, txt):
        self._logger.log(txt)

    def __init__(self, filename, logger = dummylog()):
        self._filename = filename
        self._logger   = logger
 
    def _GetFile(self):
        if type(self._filename) == file:
            return self._filename
        elif self._filename.endswith(".bz2"):
            return bz2.BZ2File(self._filename)
        elif self._filename.endswith(".gz"):
            return gzip.open(self._filename)
        else:
            return open(self._filename)
        
    def CopyTo(self, output):
        self._output = output
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(self._GetFile())
        
    def startElement(self, name, attrs):
        attrs = attrs._attrs
        if name == u"create":
            self._action = name
        elif name == u"modify":
            self._action = name
        elif name == u"delete":
            self._action = name
        elif name == u"node":
            attrs[u"id"] = int(attrs[u"id"])
            attrs[u"lat"] = float(attrs[u"lat"])
            attrs[u"lon"] = float(attrs[u"lon"])
            attrs[u"version"] = int(attrs[u"version"])
            self._data = attrs
            self._tags = {}
        elif name == u"way":
            attrs["id"] = int(attrs["id"])
            attrs[u"version"] = int(attrs[u"version"])
            self._data = attrs
            self._tags = {}
            self._nodes = []
        elif name == u"relation":
            attrs["id"] = int(attrs["id"])
            attrs[u"version"] = int(attrs[u"version"])
            self._data = attrs
            self._members = []
            self._tags = {}
        elif name == u"nd":
            self._nodes.append(int(attrs["ref"]))
        elif name == u"tag":
            self._tags[attrs["k"]] = attrs["v"]
        elif name == u"member":
            attrs["ref"] = int(attrs["ref"])
            self._members.append(attrs)

    def endElement(self, name):
        if name == u"node":
            self._data[u"tag"] = self._tags
            if self._action == u"create":
                self._output.NodeCreate(self._data)
            elif self._action == u"modify":
                self._output.NodeUpdate(self._data)
            elif self._action == u"delete":
                self._output.NodeDelete(self._data)             
        elif name == u"way":
            self._data[u"tag"] = self._tags
            self._data[u"nd"]  = self._nodes
            if self._action == u"create":
                self._output.WayCreate(self._data)
            elif self._action == u"modify":
                self._output.WayUpdate(self._data)
            elif self._action == u"delete":
                self._output.WayDelete(self._data)  
        elif name == u"relation":
            self._data[u"tag"]    = self._tags
            self._data[u"member"] = self._members
            if self._action == u"create":
                self._output.RelationCreate(self._data)
            elif self._action == u"modify":
                self._output.RelationUpdate(self._data)
            elif self._action == u"delete":
                self._output.RelationDelete(self._data)  
            return

###########################################################################

def _formatData(data):
    data = dict(data)
    if u"tag" in data:
        data.pop(u"tag")
    if u"nd" in data:
        data.pop(u"nd")
    if u"member" in data:
        data.pop(u"member")
    if u"visible" in data:
        data[u"visible"] = str(data[u"visible"]).lower()
    if u"id" in data:
        data[u"id"] = str(data[u"id"])
    if u"lat" in data:
        data[u"lat"] = str(data[u"lat"])
    if u"lon" in data:
        data[u"lon"] = str(data[u"lon"])
    if u"changeset" in data:
        data[u"changeset"] = str(data[u"changeset"])
    if u"version" in data:
        data[u"version"] = str(data[u"version"])
    if u"uid" in data:
        data[u"uid"] = str(data[u"uid"])
    return data

class OsmSaxWriter(XMLGenerator):

    def __init__(self, out, enc):
        if type(out) == str:
            XMLGenerator.__init__(self, open(out, "w"), enc)
        else:
            XMLGenerator.__init__(self, out, enc)
    
    def startElement(self, name, attrs):
        self._write(u'<' + name)
        for (name, value) in attrs.items():
            self._write(u' %s=%s' % (name, quoteattr(value)))
        self._write(u'>\n')
        
    def endElement(self, name):
        self._write(u'</%s>\n' % name)
    
    def Element(self, name, attrs):
        self._write(u'<' + name)
        for (name, value) in attrs.items():
            self._write(u' %s=%s' % (name, quoteattr(value)))
        self._write(u' />\n')

    def NodeCreate(self, data):
        if not data:
            return
        if data[u"tag"]:
            self.startElement("node", _formatData(data))
            for (k, v) in data[u"tag"].items():
                self.Element("tag", {"k":k, "v":v})
            self.endElement("node")
        else:
            self.Element("node", _formatData(data))
    
    def WayCreate(self, data):
        if not data:
            return
        self.startElement("way", _formatData(data))
        for (k, v) in data[u"tag"].items():
            self.Element("tag", {"k":k, "v":v})
        for n in data[u"nd"]:
            self.Element("nd", {"ref":str(n)})
        self.endElement("way")
    
    def RelationCreate(self, data):
        if not data:
            return
        self.startElement("relation", _formatData(data))
        for (k, v) in data[u"tag"].items():
            self.Element("tag", {"k":k, "v":v})
        for m in data[u"member"]:
            m[u"ref"] = str(m[u"ref"])
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

class TestCountObjects:
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
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.bz2", "tests/saint_barthelemy.state.txt")
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 8076)
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)
        self.assertEquals(i1.timestamp(), dateutil.parser.parse("2015-03-25T19:05:08Z").replace(tzinfo=None))

    def test_gz(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz", "tests/saint_barthelemy.state.txt")
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 8076)
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)

    def test_gz_no_state_txt(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz", None)
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 8076)
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)
        self.assertEquals(i1.timestamp(), dateutil.parser.parse("2014-01-15T19:05:08Z").replace(tzinfo=None))

    def test_file(self):
        f = gzip.open("tests/saint_barthelemy.osm.gz")
        i1 = OsmSaxReader(f, "tests/saint_barthelemy.state.txt")
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 8076)
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)

    def test_popen(self):
        import popen2
        f = popen2.popen2("gunzip -c tests/saint_barthelemy.osm.gz")[0]
        i1 = OsmSaxReader(f, "tests/saint_barthelemy.state.txt")
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 8076)
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)


    def test_stream_io(self):
        import io
        f = gzip.open("tests/saint_barthelemy.osm.gz")
        io = io.BytesIO(f.read())
        i1 = OsmSaxReader(io, "tests/saint_barthelemy.state.txt")
        o1 = TestCountObjects()
        i1.CopyTo(o1)
        self.assertEquals(o1.num_nodes, 8076)
        self.assertEquals(o1.num_ways, 625)
        self.assertEquals(o1.num_rels, 16)
        io.close()
