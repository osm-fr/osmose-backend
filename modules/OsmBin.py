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

from modules.lockfile import lockfile
import sys, os

# Python 3 has renamed xrange() to range()
if sys.version_info[0] == 2:
    range = xrange

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
    print("Creating node.crd")
    groupe = 2**10
    k = _IntToStr4(0) * 2 * groupe
    f = open(os.path.join(folder, "node.crd"), "wb")
    for i in range(nb_node_max/groupe):
        f.write(k)
    f.close()
    del k

    # create way.idx
    print("Creating way.idx")
    groupe = 1000
    k = _IntToStr5(0) * groupe
    f = open(os.path.join(folder, "way.idx"), "wb")
    for i in range(nb_way_max/groupe):
        f.write(k)
    f.close()
    del k
        
    # reset way.data
    print("Creating way.data")
    open(os.path.join(folder, "way.data"), "wb").write("--") # for no data at location 0
    
    # reset way.free
    print("Creating way.free")
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
            self._lock = lockfile(lock_file)
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
            del self._lock
        
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
            self._free
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
    
    def WayGet(self, WayId, dump_sub_elements=False):
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
            print("Cannot access free[%d] for way id=%d, idx=%d" % (nbn, data[u"id"], AdrWay))
            raise
        # Save deletion
        self._fWay_idx.seek(5*data[u"id"])
        self._fWay_idx.write(_IntToStr5(0))
        
    #######################################################################
    ## relation functions

    def RelationGet(self, RelationId, dump_sub_elements=False):
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
        for i in range(way_idx_size / 5):
            way = self.WayGet(i)
            if way:
                output.WayCreate(way)
    
    def CopyRelationTo(self, output):
        for i in os.listdir(self._reldir):
            for j in os.listdir(self._reldir+"/"+i):
                for k in os.listdir(self._reldir+"/"+i+"/"+j):
                    output.RelationCreate(eval(open(self._reldir+"/"+i+"/"+j+"/"+k).read()))

    def Import(self, f):
        if f == "-":
            import OsmSax
            i = OsmSax.OsmSaxReader(sys.stdin)
        elif f.endswith(".pbf"):
            import OsmPbf
            i = OsmPbf.OsmPbfReader(f, None)
        else:
            import OsmSax
            i = OsmSax.OsmSaxReader(f, None)
        i.CopyTo(self)

    def Update(self, f):
        import OsmSax
        if f == "-":
            i = OsmSax.OscSaxReader(sys.stdin)
        else:
            i = OsmSax.OscSaxReader(f)
        i.CopyTo(self)


###########################################################################

if __name__=="__main__":
    if sys.argv[1]=="--init":
        InitFolder(sys.argv[2])

    if sys.argv[1]=="--import":
        o = OsmBin(sys.argv[2], "w")
        o.Import(sys.argv[3])

    if sys.argv[1]=="--update":
        o = OsmBin(sys.argv[2], "w")
        o.Update(sys.argv[3])
        
    if sys.argv[1]=="--read":
        i = OsmBin(sys.argv[2])
        if sys.argv[3]=="node":
            print(i.NodeGet(int(sys.argv[4])))
        if sys.argv[3]=="way":
            print(i.WayGet(int(sys.argv[4])))
        if sys.argv[3]=="relation":
            print(i.RelationGet(int(sys.argv[4])))
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
    def setUp(self):
        import shutil
        shutil.rmtree("tmp-osmbin/", True)
        InitFolder("tmp-osmbin/")
        self.a = OsmBin("tmp-osmbin/", "w")
        self.a.Import("tests/saint_barthelemy.osm.bz2")

    def tearDown(self):
        import shutil
        del self.a
        shutil.rmtree("tmp-osmbin/")

    def check_node(self, func, id, exists=True):
        res = func(id)
        if exists:
            assert res
            assert res["lat"]
            assert res["lon"]
            self.assertEquals(res["id"], id)
        else:
            if res:
                self.assertEquals(res["lat"], _Str4ToCoord(_IntToStr4(0)))
                self.assertEquals(res["lon"], _Str4ToCoord(_IntToStr4(0)))

    def check_way(self, func, id, exists=True):
        res = func(id)
        if exists:
            assert res
            assert res["nd"]
            self.assertEquals(res["tag"], {})
            self.assertEquals(res["id"], id)
        else:
            assert not res

    def check_relation(self, func, id, exists=True):
        res = func(id)
        if exists:
            assert res
            assert res["member"]
            assert res["tag"]
            self.assertEquals(res["id"], id)
        else:
            assert not res

    def check_relation_full(self, func, id, exists=True):
        res = func(id)
        if exists:
            assert res
            assert res["member"]
            assert res["tag"]
            self.assertEquals(res["id"], id)
        else:
            assert not res

    def test_copy_relation(self):
        o1 = TestCountObjects()
        self.a.CopyRelationTo(o1)
        self.assertEquals(o1.num_nodes, 0)
        self.assertEquals(o1.num_ways, 0)
        self.assertEquals(o1.num_rels, 16)

    def test_node(self):
        del self.a
        self.a = OsmBin("tmp-osmbin/", "r")
        self.check_node(self.a.NodeGet, 266053077)
        self.check_node(self.a.NodeGet, 2619283351)
        self.check_node(self.a.NodeGet, 2619283352)
        self.check_node(self.a.NodeGet, 1, False)
        self.check_node(self.a.NodeGet, 266053076, False)
        self.check_node(self.a.NodeGet, 2619283353, False)

    def test_way(self):
        self.check_way(self.a.WayGet, 24473155)
        self.check_way(self.a.WayGet, 255316725)
        self.check_way(self.a.WayGet, 1, False)
        self.check_way(self.a.WayGet, 24473154, False)
        self.check_way(self.a.WayGet, 255316726, False)

    def test_relation(self):
        del self.a
        self.a = OsmBin("tmp-osmbin/", "r")
        self.check_relation(self.a.RelationGet, 47796)
        self.check_relation(self.a.RelationGet, 2707693)
        self.check_relation(self.a.RelationGet, 1, False)
        self.check_relation(self.a.RelationGet, 47795, False)
        self.check_relation(self.a.RelationGet, 2707694, False)

    def test_relation_full(self):
        res = self.a.RelationFullRecur(529891)
        assert res
        self.assertEquals(res[0]["type"], "relation")
        self.assertEquals(res[0]["data"]["id"], 529891)
        self.assertEquals(res[1]["type"], "node")
        self.assertEquals(res[1]["data"]["id"], 670634766)
        self.assertEquals(res[2]["type"], "node")
        self.assertEquals(res[2]["data"]["id"], 670634768)

        self.a.Update("tests/saint_barthelemy.osc.gz")
        res = self.a.RelationFullRecur(7800)
        assert res
        self.assertEquals(res[0]["type"], "relation")
        self.assertEquals(res[0]["data"]["id"], 7800)
        self.assertEquals(res[1]["type"], "node")
        self.assertEquals(res[1]["data"]["id"], 78)
        self.assertEquals(res[2]["type"], "node")
        self.assertEquals(res[2]["data"]["id"], 79)
        self.assertEquals(res[3]["type"], "way")
        self.assertEquals(res[3]["data"]["id"], 780)
        self.assertEquals(res[4]["type"], "node")
        self.assertEquals(res[4]["data"]["id"], 78)
        self.assertEquals(res[5]["type"], "node")
        self.assertEquals(res[5]["data"]["id"], 79)

    def test_relation_full_missing(self):
        with self.assertRaises(MissingDataError) as cm:
            self.a.RelationFullRecur(47796)
        self.assertEquals(str(cm.exception), "MissingDataError(missing way 82217912)")

    def test_relation_full_loop(self):
        self.a.Update("tests/saint_barthelemy.osc.gz")
        with self.assertRaises(RelationLoopError) as cm:
            self.a.RelationFullRecur(7801)
        self.assertEquals(str(cm.exception), "RelationLoopError(member loop [7801, 7802, 7801])")

    def test_update(self):
        self.check_node(self.a.NodeGet, 1759873129)
        self.check_node(self.a.NodeGet, 1759883953)
        self.check_node(self.a.NodeGet, 1973325505)
        self.check_way(self.a.WayGet, 24552609)
        self.check_way(self.a.WayGet, 24552626)
        self.check_way(self.a.WayGet, 24552826)
        self.check_relation(self.a.RelationGet, 529891)
        self.check_relation(self.a.RelationGet, 1106302)
        self.check_node(self.a.NodeGet, 78, False)
        self.check_node(self.a.NodeGet, 79, False)
        self.check_way(self.a.WayGet, 780, False)
        self.check_relation(self.a.RelationGet, 7800, False)
        self.a.Update("tests/saint_barthelemy.osc.gz")
        self.check_node(self.a.NodeGet, 1759873129, False)
        self.check_node(self.a.NodeGet, 1759883953, False)
        self.check_node(self.a.NodeGet, 1973325505, False)
        self.check_way(self.a.WayGet, 24552609, False)
        self.check_way(self.a.WayGet, 24552626, False)
        self.check_way(self.a.WayGet, 24552826, False)
        self.check_relation(self.a.RelationGet, 529891, False)
        self.check_relation(self.a.RelationGet, 1106302, False)
        self.check_node(self.a.NodeGet, 78)
        self.check_node(self.a.NodeGet, 79)
        self.check_way(self.a.WayGet, 780)
        self.check_relation(self.a.RelationGet, 7800)
