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

from .Analyser import Analyser

import sys
import os
import importlib
import modules.config
from modules import OsmoseLog
from modules import OsmReader
from modules import SourceVersion


class Analyser_Sax(Analyser):

    def __init__(self, config, logger = OsmoseLog.logger()):
        Analyser.__init__(self, config, logger)
        if self.config.plugins:
            plugins = map(lambda plugin: self._load_plugin(plugin) if isinstance(plugin, str) else plugin, self.config.plugins)
        else:
            plugins = self._load_all_plugins()
        self._init_plugins(plugins)

    def __enter__(self):
        Analyser.__enter__(self)
        # open database connections
        self._load_reader()
        self.parser = OsmReader.open(self.config.src, self.logger.sub(), getattr(self.config, 'src_state', None))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # close database connections
        self._log(u"Closing reader and parser")
        del self.parser
        del self._reader
        Analyser.__exit__(self, exc_type, exc_value, traceback)

    def timestamp(self):
        return self.parser.timestamp()

    def analyser_version(self):
        return SourceVersion.version(*([self.__class__] + list(map(lambda p: p.__class__, self.plugins.values()))))

    def analyser(self):
        self.logger.log("run sax all")

        self._load_output(change=self.parser.is_change())
        try:
            self._run_analyse()
        finally:
            self._close_output()

    def analyser_resume(self, timestamp, already_issued_objects):
        self.logger.log("run sax changed")

        self.parser.set_filter_since_timestamp(timestamp)
        self.already_issued_objects = already_issued_objects

        self.config.timestamp = self.timestamp()
        self._load_output(change=True)

        try:
            self._run_analyse()

            if timestamp:
                filtered_nodes = set(self.parser.filtered_nodes())
                for id in self.already_issued_objects['N']:
                    if id not in filtered_nodes:
                        self.error_file.delete('node', id)
                filtered_ways = set(self.parser.filtered_ways())
                for id in self.already_issued_objects['W']:
                    if id not in filtered_ways:
                        self.error_file.delete('way', id)
                filtered_relations = set(self.parser.filtered_relations())
                for id in self.already_issued_objects['R']:
                    if id not in filtered_relations:
                        self.error_file.delete('relation', id)
        finally:
            self._close_output()

    ################################################################################
    #### Useful functions

    def ToolsGetFilePath(self, filename):
        return os.path.join(modules.config.dir_osmose, filename)

    def ToolsOpenFile(self, filename, mode):
        return open(self.ToolsGetFilePath(filename), mode, encoding="utf-8")

    def ToolsListDir(self, dirname):
        return os.listdir(self.ToolsGetFilePath(dirname))

    def ToolsReadList(self, filename):
        f = self.ToolsOpenFile(filename, "r")
        d = []
        for x in f.readlines():
            x = x.strip()
            if not x: continue
            if x[0] == "#": continue
            d.append(x)
        f.close()
        return d

    def ToolsReadDict(self, filename, separator):
        f = self.ToolsOpenFile(filename, "r")
        d = {}
        for x in f.readlines():
            x = x.strip()
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
        return self._reader.WayGet(WayId, dump_sub_elements=True)

    def RelationGet(self, RelationId):
        return self._reader.RelationGet(RelationId, dump_sub_elements=True)

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

    def _err(self, txt):
        self.logger.err(txt)

    ################################################################################
    #### Node parsing

    def NodeCreate(self, data):
        # Initialisation
        err  = []
        tags = data[u"tag"]

        if tags == {}:
            return

        # Running jobs
        for meth in self.pluginsNodeMethodes:
            try:
                res = meth(data, tags)
            except:
                self._err("Fail on {0} with {1}, {2}".format(meth, data, tags))
                raise
            if res:
                if isinstance(res, dict):
                    err.append(res)
                else:
                    err += res

        # Write the issues
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
                    allow_fix_override = e.get('allow_fix_override')

                    self.error_file.error(
                        classs,
                        subclass,
                        text,
                        [data["id"]],
                        ["node"],
                        fix,
                        {"position": [data], "node": [data]},
                        allow_override = allow_fix_override)
                except:
                    self._err("Error on error {0} from {1}".format(str(e), str(err)))
                    raise

    def NodeUpdate(self, data):
        self.NodeDelete(data)
        self.NodeCreate(data)

    def NodeDelete(self, data):
        self.error_file.delete("node", data["id"])

    ################################################################################
    #### Way parsing

    def WayCreate(self, data):
        # Initialisation
        err  = []
        tags = data[u"tag"]
        nds  = data[u"nd"]

        # Run jobs
        for meth in self.pluginsWayMethodes:
            try:
                res = meth(data, tags, nds)
            except:
                self._err("Fail on {0} with {1}, {2}, {3}".format(meth, data, tags, nds))
                raise

            if res:
                if isinstance(res, dict):
                    err.append(res)
                else:
                    err += res

        # Write the issues
        if err:
            if not "uid" in data and not "user" in data:
                tmp_data = self.WayGet(data["id"]) or data
                if tmp_data:
                    # way from reader can be None if there is only one node on it
                    data = tmp_data
            node = self.NodeGet(nds[len(nds)//2])
            if not node:
                node = {u"lat":0, u"lon":0}
            data = self.ExtendData(data)
            for e in err:
                try:
                    classs = e["class"]
                    subclass = e.get("subclass", 0)
                    text = e.get("text", {})
                    fix = e.get("fix")
                    allow_fix_override = e.get('allow_fix_override')

                    self.error_file.error(
                        classs,
                        subclass,
                        text,
                        [data["id"]],
                        ["way"],
                        fix,
                        {"position": [node], "way": [data]},
                        allow_override = allow_fix_override)
                except:
                    self._err("Error on error {0} from {1}".format(str(e), str(err)))
                    raise

    def WayUpdate(self, data):
        self.WayDelete(data)
        self.WayCreate(data)

    def WayDelete(self, data):
        self.error_file.delete("way", data["id"])

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
        # Initialisation
        err  = []
        tags = data[u"tag"]
        members = data[u"member"]

        # Run jobs
        for meth in self.pluginsRelationMethodes:
            try:
                res = meth(data, tags, members)
            except:
                self._err("Fail on {0} with {1}, {2}, {3}".format(meth, data, tags, members))
                raise
            if res:
                if isinstance(res, dict):
                    err.append(res)
                else:
                    err += res

        # Write the issues
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
                    allow_fix_override = e.get('allow_fix_override')

                    self.error_file.error(
                        classs,
                        subclass,
                        text,
                        [data["id"]],
                        ["relation"],
                        fix,
                        {"position": [node], "relation": [data]},
                        allow_override = allow_fix_override)
                except:
                    self._err("Error on error {0} from {1}".format(str(e), str(err)))
                    raise

    def RelationUpdate(self, data):
        self.RelationDelete(data)
        self.RelationCreate(data)

    def RelationDelete(self, data):
        self.error_file.delete("relation", data["id"])

    ################################################################################

    def _load_reader(self):
        if hasattr(self.config, 'osmosis_manager') and self.config.osmosis_manager:
            self._reader = self.config.osmosis_manager.osmosis()
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
            # from modules import OsmSaxAlea
            # self._reader = OsmSaxAlea.OsmSaxReader(self.config.src, self.config.src_state)
            raise RuntimeError('No OSM reader available')

    ################################################################################

    def _load_plugin(self, plugin):
        module = importlib.import_module('plugins.' + plugin)
        if getattr(module, 'P_' + plugin, None):
            pass
        else:
            return getattr(module, plugin)

    def _load_all_plugins(self):
        self._log(u"Loading plugins")

        available_plugins = []
        for plugin in sorted(self.ToolsListDir(u"plugins")):
            if not plugin.endswith(".py") or plugin in ("__init__.py", "Plugin.py"):
                continue
            pluginName = plugin[:-3]
            clazz = self._load_plugin(pluginName)
            if clazz:
                available_plugins.append(clazz)

        return available_plugins


    def _init_plugins(self, available_plugin_classes):
        self._Err = {}
        self.plugins = {}
        self.pluginsNodeMethodes = []
        self.pluginsWayMethodes = []
        self.pluginsRelationMethodes = []

        conf_limit = set()
        for i in ("country", "language"):
            if i in self.config.options:
                if isinstance(self.config.options[i], str):
                    conf_limit.add(self.config.options[i])

        for pluginClazz in available_plugin_classes:
            if "only_for" in dir(pluginClazz):
                if not any(map(lambda of: any(map(lambda co: co.startswith(of), conf_limit)), pluginClazz.only_for)):
                    self._sublog(u"skip "+pluginClazz.__name__)
                    continue

            if "not_for" in dir(pluginClazz):
                if any(map(lambda of: any(map(lambda co: co.startswith(of), conf_limit)), pluginClazz.not_for)):
                    self._sublog(u"skip "+pluginClazz.__name__)
                    continue

            # Plugin Initialisation
            pluginInstance = pluginClazz(self)
            if pluginInstance.init(self.logger.sub().sub()) is False:
                self._sublog(u"self-disabled "+pluginClazz.__name__)
                continue
            else:
                self._sublog(u"init "+pluginClazz.__name__+" ("+", ".join(pluginInstance.availableMethodes())+")")

                pluginAvailableMethodes = pluginInstance.availableMethodes()
                self.plugins[pluginClazz.__name__] = pluginInstance

                # Fetch functions to call
                if "node" in pluginAvailableMethodes:
                    self.pluginsNodeMethodes.append(pluginInstance.node)
                if "way" in pluginAvailableMethodes:
                    self.pluginsWayMethodes.append(pluginInstance.way)
                if "relation" in pluginAvailableMethodes:
                    self.pluginsRelationMethodes.append(pluginInstance.relation)

                # Liste generated issues
                for (cl, v) in self.plugins[pluginClazz.__name__].errors.items():
                    if cl in self._Err:
                        raise Exception("class {0} already present as item {1}".format(cl, self._Err[cl]['item']))
                    self._Err[cl] = v

    ################################################################################

    def _load_output(self, change):
        self.error_file.analyser(self.timestamp(), self.analyser_version(), change=change)

        # Create classes in issues file
        for (cl, item) in sorted(self._Err.items()):
            self.error_file.classs(
                id = cl,
                item = item['item'],
                level = item['level'],
                tags = item.get('tags', item.get('tag')),
                title = item.get('title', item.get('desc')),
                detail = item.get('detail'),
                fix = item.get('fix'),
                trap = item.get('trap'),
                example = item.get('example'),
                source = item.get('source'),
                resource = item.get('resource'),
            )

    ################################################################################

    def _run_analyse(self):
        self._log(u"Analysing file "+self.config.src)
        self.parser.CopyTo(self)
        self._log(u"Analyse finished")

    ################################################################################

    def _close_output(self):
        self.error_file.analyser_end()

################################################################################
from .Analyser import TestAnalyser
from modules import IssuesFileOsmose
import datetime
import dateutil

class TestAnalyserOsmosis(TestAnalyser):

    class MockupReader(object):
        def NodeGet(self, id):
            return { "id": id, "lat": 0, "lon": 0, "tag": {} }

        def WayGet(self, id, dump_sub_elements=False):
            return { "id": id, "nd": [0], "tag": {} }

        def RelationGet(self, id, dump_sub_elements=False):
            return { "id": id, "member": [{"type": "node", "ref": 0}], "tag": {} }

        def UserGet(self, id):
            return None

        def timestamp(self):
            return datetime.datetime.now()


    def setUp(self):

        class config:
            options = {"project": "openstreetmap"}
            src = "tests/saint_barthelemy.osm.gz"
            src_state = "tests/saint_barthelemy.state.txt"
            error_file = None
            reader = TestAnalyserOsmosis.MockupReader()
            source_url = 'http://example.com'
            plugins = []
        self.config = config()

        # create directory for results
        import os
        from modules import config
        self.dirname = config.dir_tmp + "/tests/"
        try:
            os.makedirs(self.dirname)
        except OSError:
            if os.path.isdir(self.dirname):
                pass
            else:
                raise

    def test(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=33)

    def test_resume_full(self):
        # Test with an older timestamp than older object in extract
        self.xml_res_file = os.path.join(self.dirname, "sax.test_resume_full.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser_resume(dateutil.parser.parse("2000-01-01T01:01:01Z").replace(tzinfo=None), {'N': set(), 'W': set(), 'R': set()})

        self.compare_results("tests/results/sax.test_resume_full.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=13)

    def test_resume(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test_resume.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser_resume(dateutil.parser.parse("2012-07-18T11:04:56Z").replace(tzinfo=None), {'N': set([1]), 'W': set([24552698]), 'R': set()})

        self.compare_results("tests/results/sax.test_resume.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=11)

    def test_resume_empty(self):
        # Test with an younger timestamp than youngest object in extract
        self.xml_res_file = os.path.join(self.dirname, "sax.test_resume_empty.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser_resume(dateutil.parser.parse("2030-01-01T01:01:01Z").replace(tzinfo=None), {'N': set([1]), 'W': set([1000,1001]), 'R': set()})

        self.compare_results("tests/results/sax.test_resume_empty.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=0, max=0)

    def test_FR(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.FR.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"country": "FR", "project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.FR.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=47)

    def test_fr(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.Lang_fr.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"language": "fr", "project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.Lang_fr.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=37)

    def test_fr_nl(self):
        self.xml_res_file = os.path.join(self.dirname, "sax.test.Lang_fr_nl.xml")
        self.config.error_file = IssuesFileOsmose.IssuesFileOsmose(self.xml_res_file)
        self.config.options = {"language": ["fr", "nl"], "project": "openstreetmap"}
        with Analyser_Sax(self.config) as analyser_obj:
            analyser_obj.analyser()

        self.compare_results("tests/results/sax.test.Lang_fr_nl.xml")

        self.root_err = self.load_errors()
        self.check_num_err(min=34)


################################################################################

if __name__ == "__main__":
    # Check argument
    if len(sys.argv) != 3:
        print("Syntax: analyser_sax.py <fichier_source.osm> <fichier_dest.xml.bz2>")
        sys.exit(-1)

    # Prepare configuration
    class config:
        options = {"country": "FR", "language": "fr"}
        src = sys.argv[1]
        error_file = IssuesFileOsmose.IssuesFileOsmose(sys.argv[2])

    # Start analyser
    with Analyser_Sax(config()) as analyser_obj:
        analyser_obj.analyser()
