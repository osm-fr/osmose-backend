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

def _Bytes5ToInt(txt):
    if len(txt) != 5:
        return None
    # 0 to 1.099.511.627.776
    txt = bytearray(txt)
    i0 = txt[0]
    i1 = txt[1]
    i2 = txt[2]
    i3 = txt[3]
    i4 = txt[4]
    return 4294967296*i0+16777216*i1+65536*i2+256*i3+i4

def _IntToBytes5(num):
    i0   = num//4294967296
    num -= 4294967296*i0    
    i1   = num//16777216
    num -= 16777216*i1
    i2   = num//65536
    num -= 65536*i2
    i3   = num//256
    i4   = num - 256*i3
    return bytearray([i0, i1, i2, i3, i4])

def _Bytes4ToInt(txt):
    # 0 to 4.294.967.295
    txt = bytearray(txt)
    i0 = txt[0]
    i1 = txt[1]
    i2 = txt[2]
    i3 = txt[3]
    return 16777216*i0+65536*i1+256*i2+i3

def _IntToBytes4(num):
    i0   = num//16777216
    num -= 16777216*i0
    i1   = num//65536
    num -= 65536*i1
    i2   = num//256
    i3   = num - 256*i2
    return bytearray([i0, i1, i2, i3])

def _Bytes2ToInt(txt):
    # 0 to 65535
    txt = bytearray(txt)
    i0 = txt[0]
    i1 = txt[1]
    return 256*i0+i1

def _IntToBytes2(num):
    i0   = num//256
    i1   = num - 256*i0
    return bytearray([i0, i1])

def _Bytes1ToInt(txt):
    # 0 to 255
    txt = bytearray(txt)
    return txt[0]

def _IntToBytes1(i0):
    return bytearray([i0])

def _Bytes4ToCoord(num):
    return float(_Bytes4ToInt(num)-1800000000)/10000000

def _CoordToBytes4(coord):
    return _IntToBytes4(int((coord*10000000)+1800000000))

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
    k = _IntToBytes4(0) * 2 * groupe
    f = open(os.path.join(folder, "node.crd"), "wb")
    for i in range(nb_node_max//groupe):
        f.write(k)
    f.close()
    del k

    # create way.idx
    print("Creating way.idx")
    groupe = 1000
    k = _IntToBytes5(0) * groupe
    f = open(os.path.join(folder, "way.idx"), "wb")
    for i in range(nb_way_max//groupe):
        f.write(k)
    f.close()
    del k
        
    # reset way.data
    print("Creating way.data")
    open(os.path.join(folder, "way.data"), "wb").write(b"--") # for no data at location 0
    
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
        self._fNode_crd      = open(os.path.join(folder, "node.crd"), {"w":"rb+", "r":"rb"}[mode])
        self._fWay_idx       = open(os.path.join(folder, "way.idx") , {"w":"rb+", "r":"rb"}[mode])
        self._fWay_data      = open(os.path.join(folder, "way.data"), {"w":"rb+", "r":"rb"}[mode])
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
        data["lat"] = _Bytes4ToCoord(read[:4])
        data["lon"] = _Bytes4ToCoord(read[4:])
        data["tag"] = {}
        return data
        
    def NodeCreate(self, data):
        LatBytes4 = _CoordToBytes4(data[u"lat"])
        LonBytes4 = _CoordToBytes4(data[u"lon"])
        self._fNode_crd.seek(8*data[u"id"])
        self._fNode_crd.write(LatBytes4+LonBytes4)
        
    NodeUpdate = NodeCreate

    def NodeDelete(self, data):
        LatBytes4 = _IntToBytes4(0)
        LonBytes4 = _IntToBytes4(0)
        self._fNode_crd.seek(8*data[u"id"])
        self._fNode_crd.write(LatBytes4+LonBytes4)

    #######################################################################
    ## way functions
    
    def WayGet(self, WayId, dump_sub_elements=False):
        self._fWay_idx.seek(5*WayId)
        AdrWay = _Bytes5ToInt(self._fWay_idx.read(5))
        if not AdrWay:
            return None
        self._fWay_data.seek(AdrWay)
        nbn  = _Bytes2ToInt(self._fWay_data.read(2))
        data = self._fWay_data.read(self.node_id_size*nbn)
        nds = []
        for i in range(nbn):
            nds.append(_Bytes5ToInt(data[self.node_id_size*i:self.node_id_size*(i+1)]))
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
        self._fWay_idx.write(_IntToBytes5(AdrWay))
        # File way.dat
        self._fWay_data.seek(AdrWay)
        c = _IntToBytes2(len(data[u"nd"]))
        for NodeId in data[u"nd"]:
            c += _IntToBytes5(NodeId)
        self._fWay_data.write(c)

    WayUpdate = WayCreate
    
    def WayDelete(self, data):
        # Seek to position in file containing address to node list
        self._fWay_idx.seek(5*data[u"id"])
        AdrWay = _Bytes5ToInt(self._fWay_idx.read(5))
        if not AdrWay:
            return
        # Free space
        self._fWay_data.seek(AdrWay)
        nbn = _Bytes2ToInt(self._fWay_data.read(2))
        try:
            self._free[nbn].append(AdrWay)
        except KeyError:
            print("Cannot access free[%d] for way id=%d, idx=%d" % (nbn, data[u"id"], AdrWay))
            raise
        # Save deletion
        self._fWay_idx.seek(5*data[u"id"])
        self._fWay_idx.write(_IntToBytes5(0))
        
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
        for i in range(way_idx_size // 5):
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
            from . import OsmSax
            i = OsmSax.OsmSaxReader(sys.stdin)
        elif f.endswith(".pbf"):
            from . import OsmPbf
            i = OsmPbf.OsmPbfReader(f, None)
        else:
            from . import OsmSax
            i = OsmSax.OsmSaxReader(f, None)
        i.CopyTo(self)

    def Update(self, f):
        from . import OsmSax
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
    def setUp(self):
        import shutil
        from modules import config
        self.test_dir = config.dir_tmp + "/tests/osmbin/"
        shutil.rmtree(self.test_dir, True)
        InitFolder(self.test_dir)
        self.a = OsmBin(self.test_dir, "w")
        self.a.Import("tests/saint_barthelemy.osm.bz2")

    def tearDown(self):
        import shutil
        del self.a
        shutil.rmtree(self.test_dir)

    def check_node(self, func, id, exists=True, expected=None):
        res = func(id)
        if exists:
            assert res
            assert res["lat"]
            assert res["lon"]
            self.assertEqual(res["id"], id)
            if expected:
                self.assertEqual(res["lat"], expected["lat"])
                self.assertEqual(res["lon"], expected["lon"])
        else:
            if res:
                self.assertEqual(res["lat"], _Bytes4ToCoord(_IntToBytes4(0)))
                self.assertEqual(res["lon"], _Bytes4ToCoord(_IntToBytes4(0)))

    def check_way(self, func, id, exists=True, expected=None):
        res = func(id)
        if exists:
            assert res
            assert res["nd"]
            self.assertEqual(res["tag"], {})
            self.assertEqual(res["id"], id)
            if expected:
                self.assertEqual(res["nd"], expected["nd"])
        else:
            assert not res

    def check_relation(self, func, id, exists=True, expected=None):
        res = func(id)
        if exists:
            assert res
            assert res["member"]
            assert isinstance(res["tag"], dict)
            self.assertEqual(res["id"], id)
            if expected:
                self.assertEqual(res["member"], expected["member"])
                self.assertEqual(res["tag"], expected["tag"])
        else:
            assert not res

    def test_copy_relation(self):
        o1 = MockCountObjects()
        self.a.CopyRelationTo(o1)
        self.assertEqual(o1.num_nodes, 0)
        self.assertEqual(o1.num_ways, 0)
        self.assertEqual(o1.num_rels, 16)

    def test_node(self):
        del self.a
        self.a = OsmBin(self.test_dir, "r")
        self.check_node(self.a.NodeGet, 266053077, expected={"lat": 17.9031745, "lon": -62.8363074})
        self.check_node(self.a.NodeGet, 2619283351)
        self.check_node(self.a.NodeGet, 2619283352, expected={"lat": 17.9005419, "lon": -62.8327042})
        self.check_node(self.a.NodeGet, 1, False)
        self.check_node(self.a.NodeGet, 266053076, False)
        self.check_node(self.a.NodeGet, 2619283353, False)

    def test_way(self):
        self.check_way(self.a.WayGet, 24473155)
        self.check_way(self.a.WayGet, 255316725, expected={"nd": [2610107905,2610107903,2610107901,2610107902,2610107904,2610107905]})
        self.check_way(self.a.WayGet, 1, False)
        self.check_way(self.a.WayGet, 24473154, False)
        self.check_way(self.a.WayGet, 255316726, False)

    def test_relation(self):
        del self.a
        self.a = OsmBin(self.test_dir, "r")
        self.check_relation(self.a.RelationGet, 47796)
        self.check_relation(self.a.RelationGet, 529891,
                            expected={"member": [{'type': 'node', 'ref': 670634766,  'role': ''},
                                                 {'type': 'node', 'ref': 670634768,  'role': ''}],
                                      "tag": {"name": u"Saint-Barthélemy III",
                                              "note": u"la Barriere des Quatre Vents",
                                              "ref": u"9712303",
                                              "site": u"geodesic",
                                              "source": u"©IGN 2010 dans le cadre de la cartographie réglementaire",
                                              "type": u"site",
                                              "url": u"http://ancien-geodesie.ign.fr/fiche_geodesie_OM.asp?num_site=9712303&X=519509&Y=1980304"}
                            })
        self.check_relation(self.a.RelationGet, 2324452,
                            expected={"member": [{'type': 'node', 'ref': 279149652,  'role': 'admin_centre'},
                                                 {'type': 'way',  'ref': 174027472,  'role': 'outer'},
                                                 {'type': 'way',  'ref': 53561037,  'role': 'outer'},
                                                 {'type': 'way',  'ref': 53561045,  'role': 'outer'},
                                                 {'type': 'way',  'ref': 53656098,  'role': 'outer'},
                                                 {'type': 'way',  'ref': 174027473,  'role': 'outer'},
                                                 {'type': 'way',  'ref': 174023902,  'role': 'outer'}],
                                      "tag": {"admin_level": u"8",
                                              "boundary": u"administrative",
                                              "local_name": u"Statia",
                                              "name": u"Sint Eustatius",
                                              "name:el": u"Άγιος Ευστάθιος",
                                              "name:fr": u"Saint-Eustache",
                                              "name:nl": u"Sint Eustatius",
                                              "type": u"boundary"}
                            })

        self.check_relation(self.a.RelationGet, 2707693)
        self.check_relation(self.a.RelationGet, 1, False)
        self.check_relation(self.a.RelationGet, 47795, False)
        self.check_relation(self.a.RelationGet, 2707694, False)

    def test_relation_full(self):
        res = self.a.RelationFullRecur(529891)
        assert res
        self.assertEqual(res[0]["type"], "relation")
        self.assertEqual(res[0]["data"]["id"], 529891)
        self.assertEqual(res[1]["type"], "node")
        self.assertEqual(res[1]["data"]["id"], 670634766)
        self.assertEqual(res[2]["type"], "node")
        self.assertEqual(res[2]["data"]["id"], 670634768)

        self.a.Update("tests/saint_barthelemy.osc.gz")
        res = self.a.RelationFullRecur(7800)
        assert res
        self.assertEqual(res[0]["type"], "relation")
        self.assertEqual(res[0]["data"]["id"], 7800)
        self.assertEqual(res[1]["type"], "node")
        self.assertEqual(res[1]["data"]["id"], 78)
        self.assertEqual(res[2]["type"], "node")
        self.assertEqual(res[2]["data"]["id"], 79)
        self.assertEqual(res[3]["type"], "way")
        self.assertEqual(res[3]["data"]["id"], 780)
        self.assertEqual(res[4]["type"], "node")
        self.assertEqual(res[4]["data"]["id"], 78)
        self.assertEqual(res[5]["type"], "node")
        self.assertEqual(res[5]["data"]["id"], 79)

    def test_relation_full_missing(self):
        with self.assertRaises(MissingDataError) as cm:
            self.a.RelationFullRecur(47796)
        self.assertEqual(str(cm.exception), "MissingDataError(missing way 82217912)")

    def test_relation_full_loop(self):
        self.a.Update("tests/saint_barthelemy.osc.gz")
        with self.assertRaises(RelationLoopError) as cm:
            self.a.RelationFullRecur(7801)
        self.assertEqual(str(cm.exception), "RelationLoopError(member loop [7801, 7802, 7801])")

    def test_update(self):
        self.check_node(self.a.NodeGet, 2619283352, expected={"lat": 17.9005419, "lon": -62.8327042})
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
        self.check_relation(self.a.RelationGet, 7801, False)

        self.a.Update("tests/saint_barthelemy.osc.gz")
        self.check_node(self.a.NodeGet, 2619283352, expected={"lat": 17.9005419, "lon": -62.8327042})
        self.check_node(self.a.NodeGet, 1759873129, False)
        self.check_node(self.a.NodeGet, 1759883953, False)
        self.check_node(self.a.NodeGet, 1973325505, False)
        self.check_way(self.a.WayGet, 24552609, False)
        self.check_way(self.a.WayGet, 24552626, False)
        self.check_way(self.a.WayGet, 24552826, False)
        self.check_relation(self.a.RelationGet, 529891, False)
        self.check_relation(self.a.RelationGet, 1106302, False)
        self.check_node(self.a.NodeGet, 78, expected={"lat": 18.1, "lon": -63.1})
        self.check_node(self.a.NodeGet, 79, expected={"lat": 18.2, "lon": -63.2})
        self.check_way(self.a.WayGet, 780, expected={"nd": [78,79]})
        self.check_relation(self.a.RelationGet, 7800,
                            expected={"member": [{'type': 'node', 'ref': 78,  'role': ''},
                                                 {'type': 'node', 'ref': 79,  'role': ''},
                                                 {'type': 'way',  'ref': 780, 'role': 'outer'}],
                                      "tag": {"name": u"Saint-Barthélemy III"},
                            })
        self.check_relation(self.a.RelationGet, 7801,
                            expected={"member": [{'type': 'relation', 'ref': 7802,  'role': ''}],
                                      "tag": {},
                            })
