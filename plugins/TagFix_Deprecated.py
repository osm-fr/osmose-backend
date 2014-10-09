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
        src = src.replace("'''", "").replace("{{tag|", "").replace("{{Tag|", "").replace("}}", "").replace("<br/>", " ").replace("<br />", " ")
        src = re.sub(r'([a-z])\|\|?([a-z*])', '\\1=\\2', src)
        src = src.replace("|", "")
        src = re.sub(r' +', ' ', src).strip()
        return src


    def deprecated_list(self):
        data = urlread("http://wiki.openstreetmap.org/wiki/Deprecated_features?action=raw", 1)
        #data = open("Deprecated_features?action=raw").read()
        data = data[:data.index('\n|}\n')].split("|-")
        dataMult = []
        for line in data[2:]:
            item = line[2:].split(" || ")
            ss = item[1].replace('<br />', '<br/>').split('<br/>')
            for s in ss:
                dataMult.append([s, item[3]])
        deprecated = {}
        for line in dataMult:
            src = self.cleanWiki(line[0])
            dest = self.cleanWiki(line[1])
            s = src.split('=')
            if s[0] not in deprecated:
                deprecated[s[0]] = {}
            if len(s) == 2:
                deprecated[s[0]][s[1]] = dest
            else:
                deprecated[s[0]][None] = dest
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
                err.append((4010, 0, {"fr": u"Tag \"%s\" déprécié : %s" % (k, self.Deprecated[k][None]), "en": u"Deprecated tag \"%s\" : %s" % (k, self.Deprecated[k][None])}))
            elif tags[k] in self.Deprecated[k]:
                err.append((4010, 1, {"fr": u"Tag \"%s=%s\" déprécié : %s" % (k, tags[k], self.Deprecated[k][tags[k]]), "en": u"Deprecated tag \"%s=%s\" : %s" % (k, tags[k], self.Deprecated[k][tags[k]])}))
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
        for d in [{"amenity":"bakers"},
                  {"highway":"incline_steep"},
                  {"power_source":"pedalier"},
                  {"highway":"ford"},
                 ]:
            self.check_err(a.node(None, d), d)

        for d in [{"onway":"yes"}]:
            assert not a.node(None, d), d
