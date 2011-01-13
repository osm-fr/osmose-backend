#!/usr/bin/env python
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

import re, commands, sys, os, time, bz2, urllib
from modules import OsmoseLog

###########################################################################

class analyser:
    
    def __init__(self, config, logger = OsmoseLog.logger()):
        self._config  = config
        self._rootlog = logger
        
        self._load_modules()
        self._load_reader()
        self._load_plugins()
        self._load_output()
        self._run_analyse()
        self._run_end()
        
    ################################################################################
    #### Fonctions utiles
    
    def ToolsGetFilePath(self, filename):
        return os.path.join(self._config.dir_scripts, filename)

    def ToolsOpenFile(self, filename, mode):
        return open(self.ToolsGetFilePath(filename).encode("utf8"), mode)

    def ToolsListDir(self, dirname):
        return [x.decode("utf8") for x in os.listdir(self.ToolsGetFilePath(dirname))]

    def ToolsReadList(self, filename):
        f = self.ToolsOpenFile(filename, "r")
        d = []
        for x in f.readlines():
            x = x.strip().decode("utf-8")
            if not x: continue
            if x[0] == "#": continue
            d.append(x)
        f.close()
        return d

    def ToolsReadDict(self, filename, separator):
        f = self.ToolsOpenFile(filename, "r")
        d = {}
        for x in f.readlines():
            x = x.strip().decode("utf-8")
            if x and separator in x:
                x = x.split(separator)
                d[x[0]] = x[1]
        f.close()
        return d
    
    def ToolsStripAccents(self, mot):
        mot = mot.replace(u"à", u"a").replace(u"â", u"a")
        mot = mot.replace(u"é", u"e").replace(u"è", u"e").replace(u"ë", u"e").replace(u"ê", u"e")
        mot = mot.replace(u"î", u"i").replace(u"ï", u"i")
        mot = mot.replace(u"ô", u"o").replace(u"ö", u"o")
        mot = mot.replace(u"û", u"u").replace(u"ü", u"u")
        mot = mot.replace(u"ÿ", u"y")
        mot = mot.replace(u"ç", u"c")
        mot = mot.replace(U"À", U"A").replace(u"Â", u"A")
        mot = mot.replace(U"É", U"E").replace(U"È", U"E").replace(U"Ë", U"E").replace(U"Ê", U"E")
        mot = mot.replace(U"Î", U"I").replace(U"Ï", U"I")
        mot = mot.replace(U"Ô", U"O").replace(U"Ö", U"O")
        mot = mot.replace(U"Û", U"U").replace(U"Ü", U"U")
        mot = mot.replace(U"Ÿ", U"Y")
        mot = mot.replace(U"Ç", U"C")
        mot = mot.replace(U"œ", U"oe")
        mot = mot.replace(U"æ", U"ae")
        mot = mot.replace(U"Œ", U"OE")
        mot = mot.replace(U"Æ", U"AE")
        return mot
    
    def ToolsStripDouble(self, mot):
        mot = mot.replace(u"cc", u"c")
        mot = mot.replace(u"dd", u"d")
        mot = mot.replace(u"ee", u"e")
        mot = mot.replace(u"ff", u"f")
        mot = mot.replace(u"ll", u"l")
        mot = mot.replace(u"mm", u"m")
        mot = mot.replace(u"nn", u"n")
        mot = mot.replace(u"pp", u"p")
        mot = mot.replace(u"rr", u"r")
        mot = mot.replace(u"ss", u"s")
        mot = mot.replace(u"tt", u"t")
        return mot
    
    ################################################################################
    #### Reader
    
    def NodeGet(self, NodeId):
        return self._reader.NodeGet(NodeId)
        
    def WayGet(self, WayId):
        return self._reader.WayGet(WayId)
        
    def RelationGet(self, RelationId):
        return self._reader.RelationGet(RelationId)
    
    def LinkNode(self, NodeId):
        data = self.NodeGet(NodeId)
        if not data:
            return u"#" + str(NodeId)
        lat = data[u"lat"]
        lon = data[u"lon"]
        l  = u""
        l += u"#" + str(NodeId)
        l += u" <a href=\"http://www.openstreetmap.org/?lat="+str(lat)+"&lon="+str(lon)+"&zoom=17\">P</a>"
        l += u"<a href=\"http://www.openstreetmap.org/browse/node/"+str(NodeId)+"\">B</a>"
        l += u"<a href=\"http://www.openstreetmap.org/edit?lat="+str(lat)+"&lon="+str(lon)+"&zoom=17\">E</a>"
        l += u"<a href=\"javascript:openJOSM("+str(lon-0.003)+", "+str(lat-0.003)+", "+str(lon+0.003)+", "+str(lat+0.003)+", 'node', "+str(NodeId)+")\">J</a>"
        return l
    
    ################################################################################
    #### Logs
        
    def _log(self, txt):
        self._rootlog.log(txt)

    def _sublog(self, txt):
        self._rootlog.sub().log(txt)
    
    def _cpt(self, txt):
        self._rootlog.cpt(txt)

    def _subcpt(self, txt):
        self._rootlog.sub().cpt(txt)

    ################################################################################
    #### Parsage d'un node

    def NodeCreate(self, data):
        
        # Initialisation
        err  = []
        tags = data[u"tag"]
        
        # On execute les jobs
        for job in self._PluginsNode:
            res = job(data, tags)
            if res:
                err += res
        
        # Enregistrement des erreurs
        if err:
            lat = data[u"lat"]
            lon = data[u"lon"]
            for e in err:
                self._outxml.startElement("error", {"class":str(e[0]),"subclass":str(e[1]%2147483647)})
                self._outxml.Element("location", {"lat":str(lat), "lon":str(lon)})
                for k, v in e[2].items():
                    self._outxml.Element("text", {"lang":k, "value":v})
                self._outxml.NodeCreate(data)
                self._outxml.endElement("error")

    ################################################################################
    #### Parsage d'un way
    
    def WayCreate(self, data):
        
        # Initialisation
        err  = []
        tags = data[u"tag"]
        nds  = data[u"nd"]
        
        # On execute les jobs
        for job in self._PluginsWay:
            res = job(data, tags, nds)
            if res:
                err += res
        
        # Enregistrement des erreurs
        if err:
            node = self.NodeGet(nds[len(nds)/2])
            if not node:
                node = {u"lat":0, u"lon":0}
            lat = node[u"lat"]
            lon = node[u"lon"]
            for e in err:
                self._outxml.startElement("error", {"class":str(e[0]),"subclass":str(e[1]%2147483647)})
                self._outxml.Element("location", {"lat":str(lat), "lon":str(lon)})
                for k, v in e[2].items():
                    self._outxml.Element("text", {"lang":k, "value":v})
                self._outxml.WayCreate(data)
                self._outxml.endElement("error")
    
    ################################################################################
    #### Parsage d'une relation
    
    def RelationCreate(self, data):
        
        # Initialisation
        err  = []
        tags = data[u"tag"]
        
        # On execute les jobs
        for job in self._PluginsRelation:
            res = job(data, tags)
            if res:
                err += res
                        
        # Enregistrement des erreurs
        if err:
            memb = data[u"member"][0]
            if memb[u"type"] == u"node":
                node = self.NodeGet(memb[u"ref"])
            elif memb[u"type"] == "way":
                way = self.WayGet(memb[u"ref"])
                if way:
                    node = self.NodeGet(self.WayGet(memb[u"ref"])[u"nd"][0])
                else:
                    node = {u"lat":0, u"lon":0}
            else:
                node = {u"lat":0, u"lon":0}
            if not node:
                node = {u"lat":0, u"lon":0}
            lat = node[u"lat"]
            lon = node[u"lon"]
            for e in err:
                self._outxml.startElement("error", {"class":str(e[0]),"subclass":str(e[1]%2147483647)})
                self._outxml.Element("location", {"lat":str(lat), "lon":str(lon)})
                for k, v in e[2].items():
                    self._outxml.Element("text", {"lang":k, "value":v})
                self._outxml.RelationCreate(data)
                self._outxml.endElement("error")

    ################################################################################
    
    def _load_modules(self):
        self._log(u"Chargement des modules")
        import modules
        self.modules = {}
        for module in sorted(self.ToolsListDir("modules")):
            if not module.endswith(".py"): continue
            if module.startswith("__"): continue
            if "#" in module: continue            
            #self._sublog(module[:-3])
            __import__("modules."+module[:-3])
            self.modules[module[:-3]] = eval("modules."+module[:-3])
            self.modules[module[:-3]].father = self
    
    ################################################################################
    
    def _load_reader(self):
        #self._reader = self.modules["OsmPgsql"].OsmPgsql("dbname=osm")
        self._reader = self.modules["OsmSaxAlea"].OsmSaxReader(self._config.src_small)
        
    ################################################################################

    def _load_plugins(self):
        
        self._log(u"Chargement des plugins")
        self._ErrDesc = {}
        self._ErrItem = {}
        d = {}
        import plugins
        self.plugins = {}
        _order = ["pre_pre_","pre_", "", "post_", "post_post_"]
        _types = ["way", "node", "relation"]
        
        for x in _order:
            for y in _types:
                d[x+y] = []
                
        # Chargement
        re_desc = re.compile("^err_[0-9]+_[a-z]+$")
        re_item = re.compile("^err_[0-9]+$")
        for plugin in sorted(self.ToolsListDir("plugins")):
            if not plugin.endswith(".py"):
                continue
            if plugin.startswith("__"):
                continue
            if "#" in plugin:
                continue            
            __import__("plugins."+plugin[:-3])
            if "only_for" in dir(eval("plugins."+plugin[:-3]+".plugin")):
                if not [x for x in self._config.plugin_filter if x in eval("plugins."+plugin[:-3]+".plugin.only_for")]:
                    self._sublog(u"skip "+plugin[:-3])
                    continue
            self.plugins[plugin[:-3]] = eval("plugins."+plugin[:-3]+".plugin")()
            self.plugins[plugin[:-3]].father = self
            r = []
            for x in _order:
                for y in _types:
                    if x+y in dir(self.plugins[plugin[:-3]]):
                        r.append(x+y)
                        d[x+y].append(eval("self.plugins[plugin[:-3]]."+x+y))
            for x in dir(self.plugins[plugin[:-3]]):
                if re_desc.match(x):
                    self._ErrDesc[x[4:]] = eval("self.plugins[plugin[:-3]]."+x)
                if re_item.match(x):
                    self._ErrItem[x[4:]] = eval("self.plugins[plugin[:-3]]."+x)
                    
        # Liste des jobs par type
        self._PluginsNode     = []
        self._PluginsWay      = []
        self._PluginsRelation = []
        for x in _order:
            self._PluginsNode     += d[x+"node"]
            self._PluginsWay      += d[x+"way"]
            self._PluginsRelation += d[x+"relation"]
        
        # Initialisation des plugins
        for x in ["pre_init", "init", "post_init"]:
            self._log(u"Plugin " + x)
            for y in sorted(self.plugins.keys()):
                if x in dir(self.plugins[y]):
                    #self._sublog(y)
                    eval("self.plugins[y]."+x+"(self._rootlog.sub().sub())")
                    
    ################################################################################
    
    def _load_output(self):
        
        # Fichier de sortie xml
        self._output = bz2.BZ2File(self._config.dst, "w")
        self._outxml = self.modules["OsmSax"].OsmSaxWriter(self._output, "UTF-8")
        self._outxml.startDocument()
        self._outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
                    
        # Création des classes dans le fichier xml
        for cl in set([x.split("_")[0] for x in self._ErrDesc]+[x for x in self._ErrItem]):
            self._outxml.startElement("class", {"id":cl,"item":str(self._ErrItem[cl])})
            for lg in [x.split("_")[1] for x in self._ErrDesc if x.split("_")[0]==cl]:
                self._outxml.Element("classtext", {"lang":lg, "title":self._ErrDesc[cl+"_"+lg]}) #, "menu":self._ErrDesc[cl+"_"+lg][1]})
            self._outxml.endElement("class")
            
    ################################################################################

    def _run_analyse(self):
        self._log(u"Analyse des données")
        self.modules["OsmSax"].OsmSaxReader(self._config.src_small, self._rootlog.sub()).CopyTo(self)
        self._log(u"Analyse terminée")
        
    ################################################################################

    def _run_end(self):
        
        # Fermeture des plugins
        for x in ["pre_end", "end", "post_end"]:
            self._log(u"Plugin " + x)
            for y in sorted(self.plugins.keys()):
                if x in dir(self.plugins[y]):
                    #self._sublog(y)
                    eval("self.plugins[y]."+x+"(self._rootlog.sub().sub())")
                    
        # Fin du fichier xml
        self._outxml.endElement("analyser")
        self._output.close()
        
        # Envoi des données
        #self._log("update front-end")
        #urllib.urlretrieve(self._config.updt,"/dev/null")
