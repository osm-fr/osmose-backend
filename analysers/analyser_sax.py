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

from Analyser import Analyser

import re, sys, os, time, bz2
from modules import OsmoseLog

###########################################################################

class Analyser_Sax(Analyser):

    def __init__(self, config, logger = OsmoseLog.logger()):
        Analyser.__init__(self, config, logger)

    def __enter__(self):
        # open database connections
        self._load_reader()
        self._load_parser()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections
        self._log(u"Closing reader and parser")
        del self.parser
        del self._reader

    def analyser(self):
        self._load_plugins()
        self._load_output()
        self._run_analyse()
        self._close_plugins()
        self._close_output()
        
    ################################################################################
    #### Fonctions utiles
    
    def ToolsGetFilePath(self, filename):
        return os.path.join(self.config.dir_scripts, filename)

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

    def UserGet(self, UserId):
        return self._reader.UserGet(UserId)

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

    def ExtendData(self, data):
        if "uid" in data and not "user" in data:
            user = self.UserGet(data["uid"])
            if user:
                data["user"] = user
        return data
    ################################################################################
    #### Logs
        
    def _log(self, txt):
        self.logger.log(txt)

    def _sublog(self, txt):
        self.logger.sub().log(txt)
    
    def _cpt(self, txt):
        self.logger.cpt(txt)

    def _subcpt(self, txt):
        self.logger.sub().cpt(txt)

    def dumpxmlfix(self, outxml, type, id, fixes):
        fixes = self.fixdiff(fixes)
        outxml.startElement("fixes", {})
        for fix in fixes:
            outxml.startElement("fix", {})
            f = fix[0]
            outxml.startElement(type, {'id': str(id)})
            for opp, tags in f.items():
                for k in tags:
                    if opp in '~+':
                        outxml.Element('tag', {'action': self.FixTable[opp], 'k': k, 'v': tags[k]})
                    else:
                        outxml.Element('tag', {'action': self.FixTable[opp], 'k': k})
            outxml.endElement(type)
            outxml.endElement('fix')
        outxml.endElement('fixes')

    ################################################################################
    #### Parsage d'un node

    def fixxml(self, outxml, type, id, fix):
        # Normalise fix in e
        # Normal for is [{'+':{'k1':'v1', 'k2', 'v2'}, '-':{'k3':'v3'}, '=':{'k4','v4'}}, {...}]
        e = []
        fix = fix if isinstance(fix, list) else [fix]
        for f in fix:
            if not f.has_key('~') and not f.has_key('-') and not f.has_key('+'):
                e.append({'~': f})
            else:
                e.append(f)
        # Dump
        outxml.startElement("fixes", {})
        for f in e:
            outxml.startElement("fix", {})
            for opp, tags in f.items():
                for k in tags:
                    if opp in '~+':
                        outxml.Element(self.FixTable[opp], {'type': type, 'id': str(id), 'k': k, 'v': tags[k]})
                    else:
                        outxml.Element(self.FixTable[opp], {'type': type, 'id': str(id), 'k': k})
            outxml.endElement('fix')
        outxml.endElement('fixes')

    def NodeCreate(self, data):
        
        # Initialisation
        err  = []
        tags = data[u"tag"]

        if tags == {}:
            return

        # On execute les jobs
        for meth in self.pluginsNodeMethodes:
            res = meth(data, tags)
            if res:
                err += res
        
        # Enregistrement des erreurs
        if err:
            lat = data[u"lat"]
            lon = data[u"lon"]
            data = self.ExtendData(data)
            for e in err:
                try:
                    self._outxml.startElement("error", {"class": str(e[0]), "subclass": str(e[1] % 2147483647)})
                    self._outxml.Element("location", {"lat": str(lat), "lon": str(lon)})
                    for k, v in e[2].items():
                        if k != "fix":
                            self._outxml.Element("text", {"lang": k, "value": v})
                        else:
                            self.dumpxmlfix(self._outxml, "node", data["id"], v)
                    self._outxml.NodeCreate(data)
                    self._outxml.endElement("error")

                except:
                    print "Error on error", e, "from", err
                    raise

    def NodeUpdate(self, data):
	self.NodeDelete(data)
	self.NodeCreate(data)

    def NodeDelete(self, data):
        self._outxml.Element("delete", {"type": "node", "id": str(data["id"])})

    ################################################################################
    #### Parsage d'un way
    
    def WayCreate(self, data):
        
        # Initialisation
        err  = []
        tags = data[u"tag"]
        nds  = data[u"nd"]
        
        # On execute les jobs
        for meth in self.pluginsWayMethodes:
            res = meth(data, tags, nds)
            if res:
                err += res
        
        # Enregistrement des erreurs
        if err:
            node = self.NodeGet(nds[len(nds)/2])
            if not node:
                node = {u"lat":0, u"lon":0}
            lat = node[u"lat"]
            lon = node[u"lon"]
            data = self.ExtendData(data)
            for e in err:
                try:
                    self._outxml.startElement("error", {"class": str(e[0]), "subclass": str(e[1] % 2147483647)})
                    self._outxml.Element("location", {"lat": str(lat), "lon": str(lon)})
                    for k, v in e[2].items():
                        if k != "fix":
                            self._outxml.Element("text", {"lang": k, "value": v})
                        else:
                            self.dumpxmlfix(self._outxml, "way", data["id"], v)
                    self._outxml.WayCreate(data)
                    self._outxml.endElement("error")

                except:
                    print "Error on error", e, "from", err
                    raise

    def WayUpdate(self, data):
	self.WayDelete(data)
	self.WayCreate(data)

    def WayDelete(self, data):
        self._outxml.Element("delete", {"type": "way", "id": str(data["id"])})
    
    ################################################################################
    #### Parsage d'une relation
    
    def RelationCreate(self, data):
        
        # Initialisation
        
        err  = []
        tags = data[u"tag"]
        members = data[u"member"]
        
        # On execute les jobs
        for meth in self.pluginsRelationMethodes:
            res = meth(data, tags, members)
            if res:
                err += res
                        
        # Enregistrement des erreurs
        if err and data[u"member"]:
            node = None
            for memb in data[u"member"]:
                if memb[u"type"] == u"node":
                    node = self.NodeGet(memb[u"ref"])
                elif memb[u"type"] == "way":
                    way = self.WayGet(memb[u"ref"])
                    if way:
                        node = self.NodeGet(way[u"nd"][0])
                if node:
                    break
            if not node:
                node = {u"lat":0, u"lon":0}
            lat = node[u"lat"]
            lon = node[u"lon"]
            data = self.ExtendData(data)
            for e in err:
                try:
                    self._outxml.startElement("error", {"class":str(e[0]),"subclass":str(e[1]%2147483647)})
                    self._outxml.Element("location", {"lat":str(lat), "lon":str(lon)})
                    for k, v in e[2].items():
                        if k != "fix":
                            self._outxml.Element("text", {"lang":k, "value":v})
                        else:
                            self.dumpxmlfix(self._outxml, "relation", data["id"], v)
                    self._outxml.RelationCreate(data)
                    self._outxml.endElement("error")
                except:
                    print "Error on error", e, "from", err
                    raise

    def RelationUpdate(self, data):
	self.RelationDelete(data)
	self.RelationCreate(data)
    
    def RelationDelete(self, data):
        self._outxml.Element("delete", {"type": "relation", "id": str(data["id"])})

    ################################################################################

    def _load_reader(self):
        if hasattr(self.config, 'db_string'):
            from modules import OsmOsis
            self._reader = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema)
            return

        try:
            from modules import OsmBin
            self._reader = OsmBin.OsmBin("/data/work/osmbin/data")
            return
        except IOError:
            pass

        from modules import OsmSaxAlea
        self._reader = OsmSaxAlea.OsmSaxReader(self.config.src)

    ################################################################################

    def _load_parser(self):
        if self.config.src.endswith(".pbf"):
            from modules.OsmPbf import OsmPbfReader
            self.parser = OsmPbfReader(self.config.src, self.logger.sub())
            self.parsing_change_file = False
        elif (self.config.src.endswith(".osc") or
              self.config.src.endswith(".osc.gz") or
              self.config.src.endswith(".osc.bz2")):
            from modules.OsmSax import OscSaxReader
            self.parser = OscSaxReader(self.config.src, self.logger.sub())
            self.parsing_change_file = True
        elif (self.config.src.endswith(".osm") or
              self.config.src.endswith(".osm.gz") or
              self.config.src.endswith(".osm.bz2")):
            from modules.OsmSax import OsmSaxReader
            self.parser = OsmSaxReader(self.config.src, self.logger.sub())
            self.parsing_change_file = False
        else:
            raise Exception, "File extension '%s' is not recognized" % self.config.src
        
    ################################################################################

    def _load_plugins(self):
        
        self._log(u"Chargement des plugins")
        self._Err = {}
        d = {}
        import plugins
        self.plugins = {}
        self.pluginsNodeMethodes = []
        self.pluginsWayMethodes = []
        self.pluginsRelationMethodes = []
        _order = ["pre_pre_","pre_", "", "post_", "post_post_"]
        _types = ["way", "node", "relation"]
        
        for x in _order:
            for y in _types:
                d[x+y] = []

        conf_limit = set()
        for i in ("country", "language"):
            if i in self.config.options:
                conf_limit.add(self.config.options[i])

        # Chargement
        re_desc = re.compile("^err_[0-9]+_[a-z]+$")
        re_item = re.compile("^err_[0-9]+$")
        for plugin in sorted(self.ToolsListDir("plugins")):
            if not plugin.endswith(".py") or plugin in ("__init__.py", "Plugin.py"):
                continue
            pluginName = plugin[:-3]
            __import__("plugins."+pluginName)
            pluginClazz = eval("plugins."+pluginName+"."+pluginName)
            
            if "only_for" in dir(pluginClazz):
                if conf_limit.isdisjoint(set(pluginClazz.only_for)):
                    self._sublog(u"skip "+plugin[:-3])
                    continue

            pluginInstance = pluginClazz(self)
            pluginAvailableMethodes = pluginInstance.availableMethodes()
            self.plugins[pluginName] = pluginInstance

            # Récupération des fonctions à appeler
            if "node" in pluginAvailableMethodes:
                self.pluginsNodeMethodes.append(pluginInstance.node)
            if "way" in pluginAvailableMethodes:
                self.pluginsWayMethodes.append(pluginInstance.way)
            if "relation" in pluginAvailableMethodes:
                self.pluginsRelationMethodes.append(pluginInstance.relation)
            
            # Initialisation du plugin
            self._sublog(u"init "+pluginName+" ("+", ".join(self.plugins[pluginName].availableMethodes())+")")
            self.plugins[pluginName].init(self.logger.sub().sub())

            # Liste des erreurs générées
            for (cl, v) in self.plugins[pluginName].errors.items():
                if cl in self._Err:
                    raise Exception, "class %d already present as item %d" % (cl, self._Err[cl]['item'])
                self._Err[cl] = v
                    
    ################################################################################
    
    def _load_output(self):
        
        # Fichier de sortie xml
        if self.config.dst.endswith(".bz2"):
            self._output = bz2.BZ2File(self.config.dst, "w")
        else:
            self._output = open(self.config.dst, "w")
        from modules.OsmSax import OsmSaxWriter
        self._outxml = OsmSaxWriter(self._output, "UTF-8")
        self._outxml.startDocument()
        if self.parsing_change_file:
            self._outxml.startElement("analyserChange", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        else:
            self._outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
                    
        # Création des classes dans le fichier xml
        for (cl, item) in self._Err.items():
            options = {"id":str(cl), "item": str(item["item"])}
            if "level" in item:
                options["level"] = str(item["level"])
            if "tag" in item:
                options["tag"] = ",".join(item["tag"])
            self._outxml.startElement("class", options)
            for (lang, title) in item['desc'].items():
                self._outxml.Element("classtext", {"lang":lang, "title":title})
            self._outxml.endElement("class")
            
    ################################################################################

    def _run_analyse(self):
        self._log(u"Analyse des données: "+self.config.src)
        self.parser.CopyTo(self)
        self._log(u"Analyse terminée")
        
    ################################################################################

    def _close_plugins(self):
        # Fermeture des plugins
        self._log(u"Déchargement des Plugins")
        for y in sorted(self.plugins.keys()):
            self._sublog(u"end "+y)
            self.plugins[y].end(self.logger.sub().sub())
                    
    def _close_output(self):
        # Fin du fichier xml
        if self.parsing_change_file:
            self._outxml.endElement("analyserChange")
        else:
            self._outxml.endElement("analyser")
        self._output.close()
        

    ################################################################################


if __name__=="__main__":
    # Check argument
    if len(sys.argv)!=3:
        print "Syntax: analyser_sax.py <fichier_source.osm> <fichier_dest.xml.bz2>"
        sys.exit(-1)
        
    # Prepare configuration
    class config:
        pass
    analyser_conf = config()
    analyser_conf.dir_scripts = '.'
    analyser_conf.options = {"country":  "FR",
                             "language": "fr",
                            }
    analyser_conf.src = sys.argv[1]
    analyser_conf.dst = sys.argv[2] 
    
    # Start analyser
    with Analyser_Sax(analyser_conf) as analyser_obj:
        analyser_obj.analyser()
