#!/usr/bin/env python
#-*- coding: utf8 -*-

import sys, os, math, urllib, urllib2, time
sys.path.append("..")
from modules import OsmSax
#from modules import OsmApi

folder     = "/data/project/osmose-src/backend/geodesie/" # changeset-4172024.osc  changeset-4174714.osc  changeset-4176402.osc  changeset-4181140.osc  changeset-4182372.osc  changeset-4183605.osc
#api        = OsmApi.OsmApi()
#api        = OsmApi.OsmApi(api = "osmxapi.hypercube.telascience.org")
#api        = OsmApi.OsmApi(api = "xapi.openstreetmap.org")

################################################################################
## functions

def dist(n1, n2):
    fact = math.pi/180.
    try:
        return 6371000.*math.acos(math.sin(fact*n1["lat"])*math.sin(fact*n2["lat"])+math.cos(fact*n1["lat"])*math.cos(fact*n2["lat"])*math.cos(fact*(n2["lon"]-n1["lon"])))
    except:
        return 9999.

def node_to_txt(data):
    res = [u"<b><u>infos</u></b>"]
    for x in sorted(data.keys()):
        if x in ["tag", "visible", "uid", "id"]:
            continue
        if x=="user":
            res.append(u"<b>%s =</b> <a href=\"http://www.openstreetmap.org/user/%s\">%s</a>"%(x, data[x], data[x]))
        elif x=="changeset":
            res.append(u"<b>%s =</b> <a href=\"http://www.openstreetmap.org/browse/changeset/%s\">%s</a>"%(x, data[x], data[x]))
        else:
            res.append(u"<b>%s =</b> %s"%(x, data[x]))            
    res.append(u"<b><u>tags</u></b>")
    for x in data[u"tag"]:
        if x=="url":
            res.append(u"<b>%s =</b> <a href=\"%s\">repere</a>, <a href=\"%s\">site</a>"%(x, data[u"tag"][x], data[u"tag"][x].replace(u"fiche_point.asp",u"fiche_geodesie.asp").split("&")[0]))
        else:
            res.append(u"<b>%s =</b> %s"%(x, data[u"tag"][x]))
    return u"<br>".join(res)

################################################################################
## load original data

original_n = {}
original_w = {}
original_r = {}

class OsmCache:
    
    def NodeCreate(self, data):
        original_n[data["id"]] = data
    def NodeUpdate(self, data):
        original_n[data["id"]] = data
    def NodeDelete(self, data):
        if data["id"] in original_n:
            original_n.pop(data["id"])
    
    def WayCreate(self, data):
        original_w[data["id"]] = data
    def WayUpdate(self, data):
        original_w[data["id"]] = data
    def WayDelete(self, data):
        if data["id"] in original_w:
            original_w.pop(data["id"])
        
    def RelationCreate(self, data):
        original_r[data["id"]] = data
    def RelationUpdate(self, data):
        original_r[data["id"]] = data
    def RelationDelete(self, data):
        if data["id"] in original_r:
            original_r.pop(data["id"])

for f in os.listdir(folder):
    if not f.startswith("initial-"):
        continue
    print "LOADING  %s"%f
    i = OsmSax.OscSaxReader(os.path.join(folder, f))
    o = OsmCache()
    i.CopyTo(o)
    
################################################################################
## load reimports

nod_old2new = {}
nod_new2old = {}
way_old2new = {}
way_new2old = {}
rel_old2new = {}
rel_new2old = {}

for f in os.listdir(folder):
    if not f.startswith("reimport-"):
        continue
    print "LOADING  %s"%f
    for l in open(os.path.join(folder, f)).readlines():
        l = l.split(";")
        if l[0] == "node":
            nod_old2new [int(l[1])] = int(l[2])
            nod_new2old [int(l[2])] = int(l[1])
        if l[0] == "way":
            way_old2new [int(l[1])] = int(l[2])
            way_new2old [int(l[2])] = int(l[1])
        if l[0] == "relation":
            rel_old2new [int(l[1])] = int(l[2])
            rel_new2old [int(l[2])] = int(l[1])

################################################################################
## load current data

group     = 500
current_n = {}
current_w = {}
current_r = {}

nids = original_n.keys() + nod_new2old.keys()
for i in range((len(nids)-1)/group+1):
    print "LOADING  %d nodes from api"%len(nids[group*i:group*(i+1)])
    #current_n.update(api.NodesGet(nids[group*i:group*(i+1)]))

wids = original_w.keys() + way_new2old.keys()
for i in range((len(wids)-1)/group+1):
    print "LOADING  %d ways from api"%len(wids[group*i:group*(i+1)])
    #current_w.update(api.WaysGet(wids[group*i:group*(i+1)]))

rids = original_r.keys() + rel_new2old.keys()
for i in range((len(rids)-1)/group+1):
    print "LOADING  %d relations from api"%len(rids[group*i:group*(i+1)])
    #current_n.update(api.RelationsGet(wids[group*i:group*(i+1)]))

################################################################################
## load current data


data_move_loc = []
data_move_ele = []

class OsmCheck:
    def NodeCreate(self, data):
        if data["id"] not in original_n:
            return
        data_loc = original_n.pop(data["id"])
        data_xap = data
        if (data_loc["lat"] <> data_xap["lat"]) or (data_loc["lon"] <> data_xap["lon"]):
            if dist(data_loc, data_xap) > .1:
                
                outxml.startElement("error", {"class":"1"})
                outxml.NodeCreate(data_loc)
                outxml.NodeCreate(data_xap)
                outxml.Element("location", {"lat":str(data_xap["lat"]),"lon":str(data_xap["lon"])})
                outxml.endElement("error")
                                                                             
                tmp = u"<tr>"
                tmp += u"<td valign=\"top\"><a href=\"http://www.openstreetmap.org/browse/node/%d\">%d</a></td>"%(data["id"],data["id"])
                tmp += u"<td valign=\"top\">%f m</td>"%dist(data_loc, data_xap)
                tmp += u"<td valign=\"top\">%s</td>"%node_to_txt(data_loc)
                tmp += u"<td valign=\"top\">%s</td>"%node_to_txt(data_xap)
                tmp += u"</tr>"
                data_move_loc.append(tmp)
                
        if data_loc["tag"].get("ele", None) <> data_xap["tag"].get("ele", None):
            
            outxml.startElement("error", {"class":"2"})
            outxml.NodeCreate(data_loc)
            outxml.NodeCreate(data_xap)
            outxml.Element("location", {"lat":str(data_xap["lat"]),"lon":str(data_xap["lon"])})
            outxml.endElement("error")
                
            tmp = u"<tr>"
            tmp += u"<td valign=\"top\"><a href=\"http://www.openstreetmap.org/browse/node/%d\">%d</a></td>"%(data["id"],data["id"])
            tmp += u"<td valign=\"top\">%s</td>"%node_to_txt(data_loc)
            tmp += u"<td valign=\"top\">%s</td>"%node_to_txt(data_xap)
            tmp += u"</tr>"
            data_move_ele.append(tmp)
            
    def RelationCreate(self, data):
        return
    
################################################################################

outxml_file = "/data/project/osmose-src/public_html/analyser_geodesie-france.xml"

outxml = OsmSax.OsmSaxWriter(open(outxml_file, "w"), "UTF-8")
outxml.startDocument()
outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
outxml.startElement("class", {"id":"1", "item":"0"})
outxml.Element("classtext", {"lang":"fr", "title":"Node géodésique déplacé (lat/lon)"})
outxml.Element("classtext", {"lang":"en", "title":"Geodesic node moved (lat/lon)"})
outxml.endElement("class")
outxml.startElement("class", {"id":"2", "item":"0"})
outxml.Element("classtext", {"lang":"fr", "title":"Node géodésique déplacé (ele)"})
outxml.Element("classtext", {"lang":"en", "title":"Geodesic node moved (ele)"})
outxml.endElement("class")
outxml.startElement("class", {"id":"3", "item":"0"})
outxml.Element("classtext", {"lang":"fr", "title":"Node géodésique supprimé"})
outxml.Element("classtext", {"lang":"en", "title":"Geodesic node deleted"})
outxml.endElement("class")

i = OsmSax.OsmSaxReader(sys.argv[1])
o = OsmCheck()
i.CopyTo(o)

################################################################################

data_deleted = []
for i in original_n:
    # [bbox=-6,41,10,52]
    if original_n[i]["lat"]<41.:
        continue
    if original_n[i]["lat"]>52.:
        continue
    if original_n[i]["lon"]<-6.:
        continue
    if original_n[i]["lon"]>10.:
        continue
    
    outxml.startElement("error", {"class":"3"})
    outxml.NodeCreate(original_n[i])
    outxml.Element("location", {"lat":str( original_n[i]["lat"]),"lon":str(original_n[i]["lon"])})
    outxml.endElement("error")
    
    tmp = u"<tr>"
    tmp += u"<td valign=\"top\"><a href=\"http://www.openstreetmap.org/browse/node/%d\">%d</a></td>"%(i, i)
    tmp += u"<td valign=\"top\">%s</td>"%node_to_txt(original_n[i])
    tmp += u"</tr>"
    
    data_deleted.append(tmp)
            
outxml.endElement("analyser")
outxml._out.close()

################################################################################

tmp_req = urllib2.Request("http://osmose.openstreetmap.fr/cgi-bin/update.py")
tmp_url = outxml_file
tmp_dat = urllib.urlencode([('url', tmp_url), ('code', 'xxx')])
#fd = urllib2.urlopen(tmp_req, tmp_dat)
dt = fd.read().decode("utf8").strip()
if dt <> "OK":
    print "Error updating:\n"+dt.strip()

################################################################################

html = u"""<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <style type="text/css">
    table
    {
      border-width: 1px 1px 1px 1px;
      border-style: solid;
      border-collapse: collapse;
    }
    td
    {
      border-width: 1px 1px 1px 1px;
      border-style: solid;
      margin: 0px;
      padding: 5px;
    }
      a:link {
      color: black;
    }
      a:visited {
      color: black;
    }
      a:hover {
      color: black;
    }
</style>
</head>
<body>

<a href="#ml">MOVED LOCATION : %d</a><br>
<a href="#me">MOVED ELE : %d</a><br>
<a href="#dn">DELETED NODES : %d</a><br>
<!--"-->

<a name="ml"></a><h1>MOVED LOCATION</h1>
<table>
<tr>
<td width="100"><b>node</b></td>
<td width="100"><b>distance</b></td>
<td width="200"><b>initial data</b></td>
<td width="200"><b>current data</b></td>
</tr>
%s
</table>

<a name="me"></a><h1>MOVED ELE</h1>
<table>
<tr>
<td width="100"><b>node</b></td>
<td width="200"><b>initial data</b></td>
<td width="200"><b>current data</b></td>
</tr>
%s
</table>

<a name="dn"></a><h1>DELETED NODES</h1>
<table>
<tr>
<td width="100"><b>node</b></td>
<td width="200"><b>initial data</b></td>
</tr>
%s
</table>

</body>
</html>
"""%(len(data_move_loc), len(data_move_ele), len(data_deleted), u"\n".join(data_move_loc), u"\n".join(data_move_ele), u"\n".join(data_deleted))

open(sys.argv[2],"w").write(html.encode("utf8"))
