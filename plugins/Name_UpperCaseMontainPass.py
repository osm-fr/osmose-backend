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

from plugins.Plugin import Plugin


class Name_UpperCaseMontainPass(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[803] = { "item": 5010, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Name entirely uppercase") }
        self.errors[804] = { "item": 2020, "level": 3, "tag": ["tag", "fix:survey"], "desc": T_(u"Missing altitude") }

    def node(self, data, tags):
        if u"mountain_pass" not in tags:
            return
        if tags["mountain_pass"] not in ["yes", "1"]:
            return
        err = []
        if u"ele" not in tags:
            err.append((804, 0, {}))
        if u"name" in tags and tags[u"name"].upper() == tags[u"name"] and tags[u"name"].lower() != tags[u"name"]:
            err.append((803, 0, {}))
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_UpperCaseMontainPass(None)
        a.init(None)
        for t in [{"mountain_pass": "yes"},
                  {"mountain_pass": "1"},
                  {"mountain_pass": "yes", "name": u"COL TRÈS HAUT"},
                  {"mountain_pass": "yes", "ele": "1000", "name": u"COL TRÈS HAUT"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)

        for t in [{"highway": "trunk"},
                  {"mountain_pass": "no"},
                  {"mountain_pass": "-1"},
                  {"mountain_pass": "yes", "ele": "1000"},
                  {"mountain_pass": "yes", "ele": "1000", "name": "Col des Champs"},
                 ]:
            assert not a.node(None, t), t
