#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2012                                      ##
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

from plugins.Plugin import Plugin
from modules.downloader import urlread
import re


class TagFix_Deprecated(Plugin):

    def cleanWiki(self, src):
        if src is None:
            return src
        src = src.replace("'''", "").replace("{{tag|", "").replace("{{Tag|", "").replace("}}", "").replace("<br/>", " ").replace("<br />", " ")
        src = re.sub(r'([a-z])\|\|?([a-z*])', '\\1=\\2', src)
        src = src.replace("|", "")
        src = re.sub(r' +', ' ', src).strip()
        return src


    def deprecated_list(self):
        data = urlread("http://wiki.openstreetmap.org/wiki/Template:Deprecated_features?action=raw&force_cache_20180805", 1)
        #data = open("Deprecated_features?action=raw").read()
        data = data.split("{{Deprecated features/item")
        dkey = re.compile(r"^\s*\|\s*dkey\s*=")
        dvalue = re.compile(r"\s*dvalue\s*=")
        suggestion = re.compile(r"^\s*\|\s*suggestion\s*=")
        dataMult = []
        for feature in data[1:]:
            deprecated_key = None
            deprecated_value = None
            deprecated_suggestion = None
            for line in feature.split("\n"):
                if dkey.match(line):
                    deprecated_key = line.split("|")[1].split("=")[1].strip()
                    t = line.split("|")
                    if len(t) > 2:
                        if dvalue.match(t[2]):
                            deprecated_value = t[2].split("=")[1].strip()

                if suggestion.match(line):
                    deprecated_suggestion = line.split("=")[1].strip()

                dataMult.append((deprecated_key, deprecated_value, deprecated_suggestion))

        deprecated = {}
        for line in dataMult:
            src_key = self.cleanWiki(line[0])
            src_val = self.cleanWiki(line[1])
            dest = self.cleanWiki(line[2])
            if src_key not in deprecated:
                deprecated[src_key] = {}
            deprecated[src_key][src_val] = dest
        return deprecated

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[4010] = {"item": 4010, "level": 2, "tag": ["deprecated", "value", "fix:chair"], "desc": T_(u"Deprecated tag") }

        self.Deprecated = self.deprecated_list()
        self.DeprecatedSet = set(self.Deprecated)

    def node(self, data, tags):
        err = []
        for k in set(tags).intersection(self.DeprecatedSet):
            if None in self.Deprecated[k]:
                err.append({"class": 4010, "subclass": 0, "text": T_("Tag %(tag)s is deprecated: %(depr)s", {"tag": k, "depr": self.Deprecated[k][None]})})
            elif tags[k] in self.Deprecated[k]:
                err.append({"class": 4010, "subclass": 1, "text": T_("Tag %(tag)s=%(value)s is deprecated: %(depr)s", {"tag": k, "value": tags[k], "depr": self.Deprecated[k][tags[k]]})})
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Deprecated(None)
        a.init(None)
        for d in [{"amenity":"ev_charging"},
                  {"highway":"incline_steep"},
                  {"power_source":"pedalier"},
                  {"highway":"ford"},
                 ]:
            self.check_err(a.node(None, d), d)
            self.check_err(a.way(None, d, None), d)
            self.check_err(a.relation(None, d, None), d)

        for d in [{"onway":"yes"},
                  {"waterway":"stream"},
                  {"highway":"primary"}]:
            assert not a.node(None, d), d
