#! /usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
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

###########################################################################
## OSM IMPORT                                                            ##
###########################################################################
# 1. mkdir /data/osmbin
# 2. ./OsmBin.py --init /data/osmbin
# 3. wget -O - -o /dev/null http://planet.openstreetmap.org/planet-latest.osm.bz2 \
#    | bunzip2
#    | ./OsmBin.py --import /data/osmbin -

###########################################################################
## OSC UPDATE                                                            ##
###########################################################################
# for i in /data/updates
# do
#   bzcat /data/updates/$i | ./OsmBin.py --update /data/osmbin -
# done

###########################################################################
## PYTHON                                                                ##
###########################################################################
# import OsmBin
# bin = OsmBin("/data/osmbin", "r")
# print bin.NodeGet(12)
# print bin.WayGet(12)
# print bin.RelationGet(12)
# print bin.RelationFullRecur(12)

import sys, os, lockfile

class MissingDataError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "MissingDataError(%s)"%str(self.value)

class RelationLoopError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "RelationLoopError(%s)"%str(self.value)

###########################################################################
## Common functions

_CstMax2 = 2**16-1
_CstMax4 = 2**32-1

def _Str5ToInt(txt):
    if len(txt) != 5:
        return None
    # 0 to 1.099.511.627.776
    i0 = ord(txt[0])
    i1 = ord(txt[1])
    i2 = ord(txt[2])
    i3 = ord(txt[3])
    i4 = ord(txt[4])
    return 4294967296*i0+16777216*i1+65536*i2+256*i3+i4

def _IntToStr5(num):
    i0   = num/4294967296
    num -= 4294967296*i0    
    i1   = num/16777216
    num -= 16777216*i1
    i2   = num/65536
    num -= 65536*i2
    i3   = num/256
    i4   = num - 256*i3
    return chr(i0)+chr(i1)+chr(i2)+chr(i3)+chr(i4)

def _Str4ToInt(txt):
    # 0 to 4.294.967.295
    i0 = ord(txt[0])
    i1 = ord(txt[1])
    i2 = ord(txt[2])
    i3 = ord(txt[3])
    return 16777216*i0+65536*i1+256*i2+i3

def _IntToStr4(num):
    i0   = num/16777216
    num -= 16777216*i0
    i1   = num/65536
    num -= 65536*i1
    i2   = num/256
    i3   = num - 256*i2
    return chr(i0)+chr(i1)+chr(i2)+chr(i3)

def _Str2ToInt(txt):
    # 0 to 65535
    i0 = ord(txt[0])
    i1 = ord(txt[1])
    return 256*i0+i1

def _IntToStr2(num):
    i0   = num/256
    i1   = num - 256*i0
    return chr(i0)+chr(i1)

def _Str1ToInt(txt):
    # 0 to 255
    return ord(txt[0])

def _IntToStr1(i0):
    return chr(i0)

def _Str4ToCoord(num):
    return float(_Str4ToInt(num)-1800000000)/10000000

def _CoordToStr4(coord):
    return _IntToStr4(int((coord*10000000)+1800000000))

###########################################################################
## InitFolder

def InitFolder(folder):

    nb_node_max = 2**4
    nb_way_max  = 2**4
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    # create node.crd
    print "Creating node.crd"
    groupe = 2**10
    k = _IntToStr4(0) * 2 * groupe
    f = open(os.path.join(folder, "node.crd"), "wb")
    for i in range(nb_node_max/groupe):
        f.write(k)
    f.close()
    del k

    # create way.idx
    print "Creating way.idx"
    groupe = 1000
    k = _IntToStr5(0) * groupe
    f = open(os.path.join(folder, "way.idx"), "wb")
    for i in range(nb_way_max/groupe):
        f.write(k)
    f.close()
    del k
        
    # reset way.data
    print "Creating way.data"
    open(os.path.join(folder, "way.data"), "wb").write("--") # for no data at location 0
    
    # reset way.free
    print "Creating way.free"
    open(os.path.join(folder, "way.free"), "wb")

###########################################################################
## OsmBinWriter

class OsmBin:

    def __init__(self, folder, mode = "r"):
        self._mode           = mode
        self._folder         = folder
        self._reldir         = os.path.join(folder, "relation")
        self._fNode_crd      = open(os.path.join(folder, "node.crd"), {"w":"rb+", "r":"r"}[mode])
        self._fWay_idx       = open(os.path.join(folder, "way.idx") , {"w":"rb+", "r":"r"}[mode])
        self._fWay_data      = open(os.path.join(folder, "way.data"), {"w":"rb+", "r":"r"}[mode])
        self._fWay_data_size = os.stat(os.path.join(folder, "way.data")).st_size
        if self._mode=="w":
            lock_file = os.path.join(folder, "lock")
            self._lock = lockfile.FileLock(lock_file)
            self._lock.acquire(timeout=0)
            self._ReadFree()

        self.node_id_size = 5
        
    def __del__(self):
        try:
            self._fNode_crd.close()
            self._fWay_idx.close()
            self._fWay_data.close()
        except AttributeError:
            pass
        if self._mode=="w":
            self._WriteFree()
            self._lock.release()
        
    def _ReadFree(self):
        self._free = {}
        for nbn in range(2001):
            self._free[nbn] = []            
        f = open(os.path.join(self._folder, "way.free"))
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip().split(';')
            self._free[int(line[1])].append(int(line[0]))

    def _WriteFree(self):
        try:
            free = self._free
        except AttributeError:
            return
        f = open(os.path.join(self._folder, "way.free"), 'w')
        for nbn in self._free:
            for ptr in self._free[nbn]:
                f.write("%d;%d\n"%(ptr, nbn))
        f.close()
        
    def begin(self):
        pass

    def end(self):
        pass

    #######################################################################
    ## node functions
        
    def NodeGet(self, NodeId):
        data = {}
        data["id"] = NodeId
        self._fNode_crd.seek(8*data[u"id"])
        read = self._fNode_crd.read(8)
        if len(read) != 8:
            return None
        data["lat"] = _Str4ToCoord(read[:4])
        data["lon"] = _Str4ToCoord(read[4:])
        data["tag"] = {}
        return data
        
    def NodeCreate(self, data):
        LatStr4 = _CoordToStr4(data[u"lat"])
        LonStr4 = _CoordToStr4(data[u"lon"])
        self._fNode_crd.seek(8*data[u"id"])
        self._fNode_crd.write(LatStr4+LonStr4)
        
    NodeUpdate = NodeCreate

    def NodeDelete(self, data):
        LatStr4 = _IntToStr4(0)
        LonStr4 = _IntToStr4(0)
        self._fNode_crd.seek(8*data[u"id"])
        self._fNode_crd.write(LatStr4+LonStr4)

    #######################################################################
    ## way functions
    
    def WayGet(self, WayId):
        self._fWay_idx.seek(5*WayId)
        AdrWay = _Str5ToInt(self._fWay_idx.read(5))
        if not AdrWay:
            return None
        self._fWay_data.seek(AdrWay)
        nbn  = _Str2ToInt(self._fWay_data.read(2))
        data = self._fWay_data.read(self.node_id_size*nbn)
        nds = []
        for i in range(nbn):
            nds.append(_Str5ToInt(data[self.node_id_size*i:self.node_id_size*(i+1)]))
        return {"id": WayId, "nd": nds, "tag":{}}
    
    def WayCreate(self, data):
        self.WayDelete(data)
        # Search space big enough to store node list
        nbn = len(data["nd"])
        if self._free[nbn]:
            AdrWay = self._free[nbn].pop()
        else:
            AdrWay = self._fWay_data_size
            self._fWay_data_size += 2 + self.node_id_size*nbn
        # File way.idx
        self._fWay_idx.seek(5*data[u"id"])
        self._fWay_idx.write(_IntToStr5(AdrWay))
        # File way.dat
        self._fWay_data.seek(AdrWay)
        c = _IntToStr2(len(data[u"nd"]))
        for NodeId in data[u"nd"]:
            c += _IntToStr5(NodeId)
        self._fWay_data.write(c)

    WayUpdate = WayCreate
    
    def WayDelete(self, data):
        # Seek to position in file containing address to node list
        self._fWay_idx.seek(5*data[u"id"])
        AdrWay = _Str5ToInt(self._fWay_idx.read(5))
        if not AdrWay:
            return
        # Free space
        self._fWay_data.seek(AdrWay)
        nbn = _Str2ToInt(self._fWay_data.read(2))
        try:
            self._free[nbn].append(AdrWay)
        except KeyError:
            print "Cannot access free[%d] for way id=%d, idx=%d" % (nbn, data[u"id"], AdrWay)
            raise
        # Save deletion
        self._fWay_idx.seek(5*data[u"id"])
        self._fWay_idx.write(_IntToStr5(0))
        
    #######################################################################
    ## relation functions

    def RelationGet(self, RelationId):
        RelationId = "%09d"%RelationId
        RelFolder  = self._reldir + "/" + RelationId[0:3] + "/" + RelationId[3:6] + "/"
        RelFile    = RelationId[6:9]
        if os.path.exists(RelFolder + RelFile):
            return eval(open(RelFolder + RelFile).read())
        else:
            return None
    
    def RelationCreate(self, data):
        RelationId = "%09d"%data["id"]
        RelFolder  = self._reldir + "/" + RelationId[0:3] + "/" + RelationId[3:6] + "/"
        RelFile    = RelationId[6:9]
        if not os.path.exists(RelFolder):
            os.makedirs(RelFolder)
        open(RelFolder + RelFile, "w").write(repr(data))
    
    RelationUpdate = RelationCreate
    
    def RelationDelete(self, data):
        RelationId = "%09d"%data["id"]
        RelFolder  = self._reldir + "/" + RelationId[0:3] + "/" + RelationId[3:6] + "/"
        RelFile    = RelationId[6:9]
        try:
            os.remove(RelFolder + RelFile)
        except:
            pass

    def RelationFullRecur(self, RelationId, WayNodes = True, RaiseOnLoop = True, RemoveSubarea = False, RecurControl = []):
        rel = self.RelationGet(RelationId)
        dta = [{"type": "relation", "data": rel}]
        for m in rel["member"]:
            if m["type"] == "node":
                dta.append({"type": "node", "data": self.NodeGet(m["ref"])})
            elif m["type"] == "way":
                way = self.WayGet(m["ref"])
                if not way:
                    raise MissingDataError("missing way %d"%m["ref"])
                dta.append({"type": "way", "data": way})
                if WayNodes:
                    for n in way["nd"]:
                        dta.append({"type": "node", "data": self.NodeGet(n)})
            elif m["type"] == "relation":
                if m["ref"] == RelationId:
                    if not RaiseOnLoop:
                        continue
                    raise RelationLoopError('self member '+str(RelationId))
                if m["ref"] in RecurControl:
                    if not RaiseOnLoop:
                        continue
                    raise RelationLoopError('member loop '+str(RecurControl+[RelationId, m["ref"]]))
                if RemoveSubarea and m["role"] in [u"subarea", u"region"]:
                    continue
                dta += self.RelationFullRecur(m["ref"], WayNodes = WayNodes, RaiseOnLoop = RaiseOnLoop, RecurControl = RecurControl+[RelationId])
        return dta

    #######################################################################
    ## user functions

    def UserGet(self, UserId):
        return None

    #######################################################################

    def CopyWayTo(self, output):
        self._fWay_idx.seek(0,2)
        way_idx_size = self._fWay_idx.tell()
        for i in xrange(way_idx_size / 5):
            way = self.WayGet(i)
            if way:
                output.WayCreate(way)
    
    def CopyRelationTo(self, output):
        for i in os.listdir(self._reldir):
            for j in os.listdir(self._reldir+"/"+i):
                for k in os.listdir(self._reldir+"/"+i+"/"+j):
                    output.RelationCreate(eval(open(self._reldir+"/"+i+"/"+j+"/"+k).read()))
        
###########################################################################

if __name__=="__main__":
    import sys
    
    if sys.argv[1]=="--init":
        InitFolder(sys.argv[2])

    if sys.argv[1]=="--import":
        if sys.argv[3] == "-":
            import OsmSax
            i = OsmSax.OsmSaxReader(sys.stdin)
        elif sys.argv[3].endswith(".pbf"):
            import OsmPbf
            i = OsmPbf.OsmPbfReader(sys.argv[3])
        else:
            import OsmSax
            i = OsmSax.OsmSaxReader(sys.argv[3])
        o = OsmBin(sys.argv[2], "w")
        i.CopyTo(o)

    if sys.argv[1]=="--update":
        import OsmSax
        if sys.argv[3] == "-":
            i = OsmSax.OscSaxReader(sys.stdin)
        else:
            i = OsmSax.OscSaxReader(sys.argv[3])
        o = OsmBin(sys.argv[2], "w")
        i.CopyTo(o)
        
    if sys.argv[1]=="--read":
        i = OsmBin(sys.argv[2])
        if sys.argv[3]=="node":
            print i.NodeGet(int(sys.argv[4]))
        if sys.argv[3]=="way":
            print i.WayGet(int(sys.argv[4]))
        if sys.argv[3]=="relation":
            print i.RelationGet(int(sys.argv[4]))
        if sys.argv[3]=="relation_full":
            import pprint
            pprint.pprint(i.RelationFullRecur(int(sys.argv[4])))
            
    if sys.argv[1]=="--pyro":
        import Pyro.core
        import Pyro.naming
        class OsmBin2(Pyro.core.ObjBase, OsmBin):
            def __init__(self, folder):
                Pyro.core.ObjBase.__init__(self)
                OsmBin.__init__(self, folder)
        daemon=Pyro.core.Daemon()
        #ns=Pyro.naming.NameServerLocator().getNS()
        #daemon.useNameServer(ns)
        uri=daemon.connect(OsmBin2("/data/work/osmbin/data/"), "OsmBin")
        daemon.requestLoop()
