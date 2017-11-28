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

import sys, os
import importlib
import time
from modules import OsmoseLog

###########################################################################

class Analyser_Sax(Analyser):

    def __init__(self, config, logger = OsmoseLog.logger()):
        Analyser.__init__(self, config, logger)
        self.resume_from_timestamp = None

    def __enter__(self):
        Analyser.__enter__(self)
        # open database connections
        self._load_reader()
        self._load_parser()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections
        self._log(u"Closing reader and parser")
        del self.parser
        del self._reader
        Analyser.__exit__(self, exc_type, exc_value, traceback)

    def analyser(self):
        self._load_plugins()
        self._load_output(change=self.parsing_change_file)
        self._run_analyse()
        self._close_plugins()
        self._close_output()

    def analyser_resume(self, timestamp, already_issued_objects):
        self.resume_from_timestamp = timestamp
        self.already_issued_objects = already_issued_objects

        self.config.timestamp = self.parser.timestamp()
        self._load_plugins()
        self._load_output(change=True)
        self._run_analyse()

        for id in self.already_issued_objects['N']:
            self.error_file.node_delete(id)
        for id in self.already_issued_objects['W']:
            self.error_file.way_delete(id)
        for id in self.already_issued_objects['R']:
            self.error_file.relation_delete(id)

        self._close_output()

    ################################################################################
    #### Useful functions

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

    ################################################################################
    #### Node parsing

    def NodeCreate(self, data):
        if self.resume_from_timestamp:
            if data.has_key("timestamp") and data["timestamp"] <= self.resume_from_timestamp:
                if data["id"] in self.already_issued_objects['N']:
                    self.already_issued_objects['N'].remove(data["id"])
                return

            elif data["id"] in self.already_issued_objects['N']:
                self.already_issued_objects['N'].remove(data["id"])
                self.error_file.node_delete(data["id"])

        # Initialisation
        err  = []
        tags = data[u"tag"]

        if tags == {}:
            return

        # On execute les jobs
        for meth in self.pluginsNodeMethodes:
            res = meth(data, tags)
            if res:
                if isinstance(res, dict):
                    err.append(res)
                else:
                    err += res

        # Enregistrement des erreurs
        if err:
            if not "uid" in data and not "user" in data:
                data = self.NodeGet(data["id"]) or data
            data = self.ExtendData(data)
            for e in err:
                try:
                    classs = e["class"]
                    subclass = e.get("subclass", 0)
                    text = e.get("text", {})
                    fix = e.get("fix")

                    self.error_file.error(
                        classs,
                        subclass,
                        text,
                        [data["id"]],
                        ["node"],
                        fix,
                        {"position": [data], "node": [data]})
                except:
                    print("Error on error", e, "from", err)
                    raise

    def NodeUpdate(self, data):
        self.NodeDelete(data)
        self.NodeCreate(data)

    def NodeDelete(self, data):
        self.error_file.node_delete(data["id"])

    ################################################################################
    #### Way parsing

    def WayCreate(self, data):
        if self.resume_from_timestamp and data.has_key("timestamp"):
            self.already_issued_objects['W'].remove(data["id"])
            if data["timestamp"] <= self.resume_from_timestamp:
                return

        # Initialisation
        err  = []
        tags = data[u"tag"]
        nds  = data[u"nd"]

        # On execute les jobs
        for meth in self.pluginsWayMethodes:
            res = meth(data, tags, nds)
            if res:
                if isinstance(res, dict):
                    err.append(res)
                else:
                    err += res

        # Enregistrement des erreurs
        if err:
            if not "uid" in data and not "user" in data:
                tmp_data = self.WayGet(data["id"]) or data
                if tmp_data:
                    # way from reader can be None if there is only one node on it
                    data = tmp_data
            node = self.NodeGet(nds[len(nds)/2])
            if not node:
                node = {u"lat":0, u"lon":0}
            data = self.ExtendData(data)
            for e in err:
                try:
                    classs = e["class"]
                    subclass = e.get("subclass", 0)
                    text = e.get("text", {})
                    fix = e.get("fix")

                    self.error_file.error(
                        classs,
                        subclass,
                        text,
                        [data["id"]],
                        ["way"],
                        fix,
                        {"position": [node], "way": [data]})
                except:
                    print("Error on error", e, "from", err)
                    raise

    def WayUpdate(self, data):
        self.WayDelete(data)
        self.WayCreate(data)

    def WayDelete(self, data):
        self.error_file.way_delete(data["id"])

    ################################################################################
    #### Relation parsing

    def locateRelation(self, data, recur_control = []):
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
            for memb in data[u"member"]:
                if memb[u"type"] == u"relation":
                    ref = memb[u"ref"]
                    if ref == data["id"] or ref in recur_control:
                        # don't reread the same relation
                        continue
                    rel = self.RelationGet(memb[u"ref"])
                    if rel:
                        node = self.locateRelation(rel, recur_control=recur_control+[data["id"]])
                if node:
                    break
        return node

    def RelationCreate(self, data):
        if self.resume_from_timestamp and data.has_key("timestamp"):
            self.already_issued_objects['R'].remove(data["id"])
            if data["timestamp"] <= self.resume_from_timestamp:
                return

        # Initialisation

        err  = []
        tags = data[u"tag"]
        members = data[u"member"]

        # On execute les jobs
        for meth in self.pluginsRelationMethodes:
            res = meth(data, tags, members)
            if res:
                if isinstance(res, dict):
                    err.append(res)
                else:
                    err += res

        # Enregistrement des erreurs
        if err and data[u"member"]:
            if not "uid" in data and not "user" in data:
                data = self.RelationGet(data["id"]) or data
            node = self.locateRelation(data)
            if not node:
                node = {u"lat":0, u"lon":0}
            data = self.ExtendData(data)
            for e in err:
                try:
                    classs = e["class"]
                    subclass = e.get("subclass", 0)
                    text = e.get("text", {})
                    fix = e.get("fix")

                    self.error_file.error(
                        classs,
                        subclass,
                        text,
                        [data["id"]],
                        ["relation"],
                        fix,
                        {"position": [node], "relation": [data]})
                except:
                    print("Error on error", e, "from", err)
                    raise

    def RelationUpdate(self, data):
        self.RelationDelete(data)
        self.RelationCreate(data)

    def RelationDelete(self, data):
        self.error_file.relation_delete(data["id"])

    ################################################################################

    def _load_reader(self):
        if hasattr(self.config, 'db_string') and self.config.db_string:
            from modules import OsmOsis
            self._reader = OsmOsis.OsmOsis(self.config.db_string, self.config.db_schema)
            return

        try:
            from modules import OsmBin
            self._reader = OsmBin.OsmBin("/data/work/osmbin/data")
            return
        except IOError:
            pass

        if hasattr(self.config, "reader"):
            self._reader = self.config.reader

        else:
            from modules import OsmSaxAlea
            self._reader = OsmSaxAlea.OsmSaxReader(self.config.src, self.config.src_state)

    ################################################################################

    def _load_parser(self):
        if self.config.src.endswith(".pbf"):
            from modules.OsmPbf import OsmPbfReader
            self.parser = OsmPbfReader(self.config.src, getattr(self.config, 'src_state', None), self.logger.sub())
            self.parsing_change_file = False
        elif (self.config.src.endswith(".osc") or
              self.config.src.endswith(".osc.gz") or
              self.config.src.endswith(".osc.bz2")):
            from modules.OsmSax import OscSaxReader
            self.parser = OscSaxReader(self.config.src, getattr(self.config, 'src_state', None), self.logger.sub())
            self.parsing_change_file = True
        elif (self.config.src.endswith(".osm") or
              self.config.src.endswith(".osm.gz") or
              self.config.src.endswith(".osm.bz2")):
            from modules.OsmSax import OsmSaxReader
            self.parser = OsmSaxReader(self.config.src, getattr(self.config, 'src_state', None), self.logger.sub())
            self.parsing_change_file = False
        else:
            raise Exception("File extension '%s' is not recognized" % self.config.src)

    ################################################################################

    def _load_plugins(self):

        self._log(u"Loading plugins")
        self._Err = {}
        d = {}
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
                if isinstance(self.config.options[i], basestring):
                    conf_limit.add(self.config.options[i])

        # load plugins
        for plugin in sorted(self.ToolsListDir("plugins")):
            if not plugin.endswith(".py") or plugin in ("__init__.py", "Plugin.py"):
                continue
            pluginName = plugin[:-3]
            pluginModule = importlib.import_module("plugins."+pluginName)
            available_classes = getattr(pluginModule, "available_plugin_classes", [pluginName])
            for pluginName in available_classes:
                pluginClazz = getattr(pluginModule, pluginName)

                if "only_for" in dir(pluginClazz):
                    if conf_limit.isdisjoint(set(pluginClazz.only_for)):
                        self._sublog(u"skip "+plugin[:-3])
                        continue

                if "not_for" in dir(pluginClazz):
                    if not conf_limit.isdisjoint(set(pluginClazz.not_for)):
                        self._sublog(u"skip "+plugin[:-3])
                        continue

                # Initialisation du plugin
                pluginInstance = pluginClazz(self)
                self._sublog(u"init "+pluginName+" ("+", ".join(pluginInstance.availableMethodes())+")")
                if pluginInstance.init(self.logger.sub().sub()) != False:

                    pluginAvailableMethodes = pluginInstance.availableMethodes()
                    self.plugins[pluginName] = pluginInstance

                    # Récupération des fonctions à appeler
                    if "node" in pluginAvailableMethodes:
                        self.pluginsNodeMethodes.append(pluginInstance.node)
                    if "way" in pluginAvailableMethodes:
                        self.pluginsWayMethodes.append(pluginInstance.way)
                    if "relation" in pluginAvailableMethodes:
                        self.pluginsRelationMethodes.append(pluginInstance.relation)

                    # Liste des erreurs générées
                    for (cl, v) in self.plugins[pluginName].errors.items():
                        if cl in self._Err:
                            raise Exception("class %d already present as item %d" % (cl, self._Err[cl]['item']))
                        self._Err[cl] = v

    ################################################################################

    def _load_output(self, change):
        self.error_file.analyser(self.parser.timestamp(), change=change)

        # Création des classes dans le fichier des erreurs
        for (cl, item) in sorted(self._Err.items()):
            self.error_file.classs(
                cl,
                item["item"],
                item.get("level"),
                item.get("tag"),
                item['desc'])

    ################################################################################

    def _run_analyse(self):
        self._log(u"Analysing file "+self.config.src)
        self.parser.CopyTo(self)
        self._log(u"Analyse finished")

    ################################################################################

    def _close_plugins(self):
        # Fermeture des plugins
        self._log(u"Unloading plugins")
        for y in sorted(self.plugins.keys()):
            self._sublog(u"end "+y)
            self.plugins[y].end(self.logger.sub().sub())

    def _close_output(self):
        self.error_file.analyser_end()

################################################################################
from Analyser import TestAnalyser
import datetime

class TestAnalyserOsmosis(TestAnalyser):

    class MockupReader(object):
        def NodeGet(self, id):
            return { "id": id, "lat": 0, "lon": 0, "tag": {} };

        def WayGet(self, id):
            return { "id": id, "nd": [0], "tag": {} };

        def RelationGet(self, id):
            return { "id": id, "member": [{"type": "node", "ref": 0}], "tag": {} };

        def UserGet(self, id):
            return None

        def timestamp(self):
            import datetime
            return datetime.datetime.now()


    def setUp(self):

        class config:
            dir_scripts = '.'
            options = {"project": "openstreetmap"}
            src = "tests/saint_barthelemy.osm.gz"
            src_state = "tests/saint_barthelemy.state.txt"
            dst = None
            polygon_id = None
            reader = TestAnalyserOsmosis.MockupReader()
        self.config = config()

        # create directory for results
        import os
        self.dirname = "tests/out/"
        try:
          os.makedirs(self.dirname)
        except OSError:
          if os.path.isdir(self.dirname):
            pass
          else:
            raise

    def test(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.xml")
        self.config.dst = self.xml_res_file
        self.config.options = {"project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=37)

    def test_resume(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test_resume.xml")
        self.config.dst = self.xml_res_file
        self.config.options = {"project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser_resume("2012-07-18T11:04:56Z", {'N': set([1]), 'W': set(), 'R': set()})

        self.compare_results("tests/results/sax.test_resume.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=13)

    def test_FR(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.FR.xml")
        self.xml_res_file = "tests/out/sax.test.FR.xml"
        self.config.dst = self.xml_res_file
        self.config.options = {"country": "FR", "project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.FR.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=53)

    def test_fr(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.fr.xml")
        self.config.dst = self.xml_res_file
        self.config.options = {"language": "fr", "project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.fr.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=41)

    def test_fr_nl(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.fr_nl.xml")
        self.config.dst = self.xml_res_file
        self.config.options = {"language": ["fr", "nl"], "project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.fr_nl.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=37)


################################################################################

if __name__=="__main__":
    # Check argument
    if len(sys.argv)!=3:
        print("Syntax: analyser_sax.py <fichier_source.osm> <fichier_dest.xml.bz2>")
        sys.exit(-1)

    # Prepare configuration
    class config:
        dir_scripts = '.'
        options = {"country": "FR", "language": "fr"}
        src = sys.argv[1]
        dst = sys.argv[2]
        polygon_id = None

    # Start analyser
    with Analyser_Sax(config()) as analyser_obj:
        analyser_obj.analyser()
