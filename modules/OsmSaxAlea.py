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

from . import OsmSax
import re, os

###########################################################################
## find functions

ReGetId = re.compile(" id=[\"']([0-9]+)[\"'][ />]")

def get_node_start(fd):
    fd.seek(0)
    st = 0
    while True:
        line = fd.readline()
        if line.strip().startswith("<node"):
            return st
        st += len(line)

def get_way_start(fd):
    b_min = 0
    b_max = get_file_last_line(fd)
    while True:
        b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        fd.readline()
        while True:
            line = fd.readline().strip()
            if (line == "</node>") or (line.startswith("<node") and line.endswith("/>")):
                b_min = b_cur
                break
            if line == "</way>":
                b_max = b_cur
                break
            if line == "</relation>":
                b_max = b_cur
                break
            if line == "</osm>":
                b_max = b_cur
                break
        if b_max - b_min <= 1:
            break
    fd.seek(b_max)
    b_max += len(fd.readline())
    return b_max

def get_relation_start(fd):
    b_min = 0
    b_max = get_file_last_line(fd)
    while True:
        b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        fd.readline()
        while True:
            line = fd.readline().strip()
            if (line == "</node>") or (line.startswith("<node") and line.endswith("/>")):
                b_min = b_cur
                break
            if line == "</way>":
                b_min = b_cur
                break
            if line == "</relation>":
                b_max = b_cur
                break
            if line == "</osm>":
                b_max = b_cur
                break
        if b_max - b_min <= 1:
            break
    fd.seek(b_max)
    b_max += len(fd.readline())
    return b_max

def get_node_id_start(fd, nodeid):
    b_min = 0
    b_max = get_file_last_line(fd)
    seq_read = False
    prev_seq_read = False
    while True:
        if seq_read == True:
            b_cur = b_min
            prev_seq_read = True
        else:
            b_cur = (b_min+b_max)/2
        fd.seek(b_cur)

        while True:
            line = fd.readline().strip()
            line_len = len(line)
            if line.startswith("<node "):
                nid = int(ReGetId.findall(line)[0])
                if nid < nodeid:
                    if b_cur >= b_max:
                        b_max *= 2
                    b_min = b_cur + line_len
                    break
                if nid > nodeid:
                    if b_max <= b_cur:
			# switch to sequential read if b_cur is in the middle
			# of the wanted element
                        seq_read = True
                    b_max = b_cur
                    break
                fd.seek(b_cur)
                while True:
                    line = fd.readline()
                    if line.strip().startswith("<node "):
                        return b_cur
                    b_cur += len(line)
            if (line.startswith("<way ") or line.startswith("<relation ") or
                     line.startswith("</osm>") or line_len == 0):
                if b_max <= b_cur:
                    # switch to sequential read if b_cur is in the middle
                    # of the wanted element
                    seq_read = True
                b_max = b_cur
                break
            b_cur += line_len
        if b_max - b_min <= 1 or (prev_seq_read and b_cur == b_max):
            return None

def get_way_id_start(fd, wayid):
    b_min = 0
    b_max = get_file_last_line(fd)
    seq_read = False
    prev_seq_read = False
    while True:
        if seq_read == True:
            b_cur = b_min
            prev_seq_read = True
        else:
            b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        while True:
            line = fd.readline().strip()
            line_len = len(line)
            if line.startswith("<node "):
                if b_cur >= b_max:
                    b_max *= 2
                b_min = b_cur + line_len
                break
            if line.startswith("<way "):
                wid = int(ReGetId.findall(line)[0])
                if wid < wayid:
                    if b_cur >= b_max:
                        b_max *= 2
                    b_min = b_cur + line_len
                    break
                if wid > wayid:
                    if b_max <= b_cur:
			# switch to sequential read if b_cur is in the middle
			# of the wanted element
                        seq_read = True
                    b_max = b_cur
                    break
                fd.seek(b_cur)
                while True:
                    line = fd.readline()
                    if line.strip().startswith("<way "):
                        return b_cur
                    b_cur += len(line)
            if line.startswith("<relation ") or line.startswith("</osm>") or line_len == 0:
                if b_max <= b_cur:
                    # switch to sequential read if b_cur is in the middle
                    # of the wanted element
                    seq_read = True
                b_max = b_cur
                break
            b_cur += line_len
        if b_max - b_min <= 1 or (prev_seq_read and b_cur == b_max):
            return None

def get_relation_id_start(fd, relationid):
    b_min = 0
    b_max = get_file_last_line(fd)
    seq_read = False
    prev_seq_read = False
    while True:
        if seq_read == True:
            b_cur = b_min
            prev_seq_read = True
        else:
            b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        while True:
            line = fd.readline().strip()
            line_len = len(line)
            if line.startswith("<node ") or line.startswith("<way "):
                if b_cur >= b_max:
                    b_max *= 2
                b_min = b_cur + line_len
                break
            if line.startswith("<relation "):
                rid = int(ReGetId.findall(line)[0])
                if rid < relationid:
                    if b_cur >= b_max:
                        b_max *= 2
                    b_min = b_cur + line_len
                    break
                if rid > relationid:
                    if b_max <= b_cur:
			# switch to sequential read if b_cur is in the middle
			# of the wanted element
                        seq_read = True
                    b_max = b_cur
                    break
                fd.seek(b_cur)
                while True:
                    line = fd.readline()
                    if line.strip().startswith("<relation "):
                        return b_cur
                    b_cur += len(line)
            if line.startswith("</osm>") or line_len == 0:
                if b_max <= b_cur:
                    # switch to sequential read if b_cur is in the middle
                    # of the wanted element
                    seq_read = True
                b_max = b_cur
                break;
            b_cur += line_len
        if b_max - b_min <= 1 or (prev_seq_read and b_cur == b_max):
            return None

def get_file_last_line(fd):
    return max(0, os.fstat(fd.fileno()).st_size)

###########################################################################

class OsmSaxReader(OsmSax.OsmSaxReader):

    def _Copy(self, output, get_start, get_end):
        self._debug_in_way      = True
        self._debug_in_relation = True
        self._output = output
        parser = OsmSax.make_parser()
        parser.setContentHandler(self)
        f = self._GetFile()
        start = get_start(f)
        end   = get_end(f)
        count = end - start
        bs    = 1024
        f.seek(start)
        parser.feed("<?xml version='1.0' encoding='UTF-8'?>")
        parser.feed("<osm>")
        for i in range(count/bs):
            parser.feed(f.read(bs))
        parser.feed(f.read(count-bs*int(count/bs)))
        parser.feed("</osm>")
                                        
    def CopyNodeTo(self, output):
        return self._Copy(output, get_node_start, get_way_start)
        
    def CopyWayTo(self, output):
        return self._Copy(output, get_way_start, get_relation_start)
    
    def CopyRelationTo(self, output):
        return self._Copy(output, get_relation_start, get_file_last_line)

    def _Get(self, start):        
        
        if start == None:
            return None
        
        class _output:
            data = None
            def NodeCreate(self, data):
                self.data = data
            def WayCreate(self, data):
                self.data = data
            def RelationCreate(self, data):
                self.data = data
        self._debug_in_way      = True
        self._debug_in_relation = True
        self._output = _output()
        parser = OsmSax.make_parser()
        parser.setContentHandler(self)
        parser.feed("<?xml version='1.0' encoding='UTF-8'?>")        

        f = self._GetFile()
        f.seek(start)
        while not self._output.data:
            parser.feed(f.readline())
        return self._output.data
        
    def NodeGet(self, NodeId):
        start = get_node_id_start(self._GetFile(), NodeId)
        return self._Get(start)

    def WayGet(self, WayId, dump_sub_elements=False):
        start = get_way_id_start(self._GetFile(), WayId)
        return self._Get(start)

    def RelationGet(self, RelationId, dump_sub_elements=False):
        start = get_relation_id_start(self._GetFile(), RelationId)
        return self._Get(start)

    def UserGet(self, UserId):
        return None

###########################################################################
import unittest

class Test(unittest.TestCase):
    def check(self, func, id, exists=True):
        res = func(id)
        if exists:
            assert res
            self.assertEquals(res["id"], id)
            assert res["changeset"]
            assert res["timestamp"]
            assert res["uid"]
            assert res["user"]
            self.assertEquals(type(res["tag"]), type(dict()))
        else:
            assert not res

    def test_node(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz")
        self.check(i1.NodeGet, 266053077)
        self.check(i1.NodeGet, 2619283351)
        self.check(i1.NodeGet, 2619283352)
        self.check(i1.NodeGet, 1, False)
        self.check(i1.NodeGet, 266053076, False)
        self.check(i1.NodeGet, 2619283353, False)

    def test_way(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz")
        self.check(i1.WayGet, 24473155)
        self.check(i1.WayGet, 53599877, False)
        self.check(i1.WayGet, 255316725)
        self.check(i1.WayGet, 1, False)
        self.check(i1.WayGet, 24473154, False)
        self.check(i1.WayGet, 255316726, False)

    def test_relation(self):
        i1 = OsmSaxReader("tests/saint_barthelemy.osm.gz")
        self.check(i1.RelationGet, 47796)
        self.check(i1.RelationGet, 2707693)
        self.check(i1.RelationGet, 1, False)
        self.check(i1.RelationGet, 47795, False)
        self.check(i1.RelationGet, 2707694, False)
