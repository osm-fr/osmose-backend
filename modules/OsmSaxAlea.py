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

import OsmSax
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
    fd.seek(0, 2)
    b_max = fd.tell()
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
    fd.seek(0, 2)
    b_max = fd.tell()
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
    b_max = os.fstat(fd.fileno()).st_size
    while True:
        b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        fd.readline()
        while True:
            line = fd.readline().strip()
            if line.startswith("<node "):
                nid = int(ReGetId.findall(line)[0])
                if nid < nodeid:
                    b_min = b_cur
                    break
                if nid > nodeid:
                    b_max = b_cur                    
                    break
                fd.seek(b_cur)
                b_cur += len(fd.readline())
                while True:
                    line = fd.readline()
                    if line.strip().startswith("<node "):
                        return b_cur
                    b_cur += len(line)
            if line.startswith("<way "):
                b_max = b_cur
                break
            if line.startswith("<relation "):
                b_max = b_cur
                break
        if b_max - b_min <= 1:
            return None

def get_way_id_start(fd, wayid):
    b_min = 0
    b_max = os.fstat(fd.fileno()).st_size
    while True:
        b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        fd.readline()
        while True:
            line = fd.readline().strip()
            if line.startswith("<node "):
                b_min = b_cur
                break
            if line.startswith("<way "):
                wid = int(ReGetId.findall(line)[0])
                if wid < wayid:
                    b_min = b_cur
                    break
                if wid > wayid:
                    b_max = b_cur                    
                    break
                fd.seek(b_cur)
                b_cur += len(fd.readline())
                while True:
                    line = fd.readline()
                    if line.strip().startswith("<way "):
                        return b_cur
                    b_cur += len(line)
            if line.startswith("<relation "):
                b_max = b_cur
                break
            if line.startswith("</osm>"):
                b_max = b_cur
                break;
        if b_max - b_min <= 1:
            return None

def get_relation_id_start(fd, relationid):
    b_min = 0
    b_max = os.fstat(fd.fileno()).st_size
    while True:
        b_cur = (b_min+b_max)/2
        fd.seek(b_cur)
        fd.readline()
        while True:
            line = fd.readline().strip()
            if line.startswith("<node "):
                b_min = b_cur
                break
            if line.startswith("<way "):
                b_min = b_cur
                break
            if line.startswith("<relation "):
                rid = int(ReGetId.findall(line)[0])
                if rid < relationid:
                    b_min = b_cur
                    break
                if rid > relationid:
                    b_max = b_cur                    
                    break
                fd.seek(b_cur)
                b_cur += len(fd.readline())
                while True:
                    line = fd.readline()
                    if line.strip().startswith("<relation "):
                        return b_cur
                    b_cur += len(line)
        if b_max - b_min <= 1:
            return None
        
def get_file_last_line(fd):
    st = max(0, os.fstat(fd.fileno()).st_size - 512)
    fd.seek(st)
    while True:
        line = fd.readline()
        if line.strip().startswith("</osm>"):
            return st
        st += len(line)

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

    def WayGet(self, WayId):
        start = get_way_id_start(self._GetFile(), WayId)
        return self._Get(start)

    def RelationGet(self, RelationId):
        start = get_relation_id_start(self._GetFile(), RelationId)
        return self._Get(start)
