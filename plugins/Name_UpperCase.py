#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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
import regex as re


class Name_UpperCase(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[803] = { "item": 5010, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Uppercase name") }
        self.UpperTitleCase = re.compile(u".*[\p{Lu}\p{Lt}]{5,}")
        self.RomanNumber = re.compile(u".*[IVXCDLM]{5,}")

    def node(self, data, tags):
        err = []
        print(self.UpperTitleCase.match(tags[u"name"]))
        print(self.RomanNumber.match(tags[u"name"]))
        if u"name" in tags and self.UpperTitleCase.match(tags[u"name"]) and not self.RomanNumber.match(tags[u"name"]):
            err.append((803, 0, {}))
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_UpperCase(None)
        a.init(None)
        for t in [{u"name": u"COL TRÈS HAUTTT"},
                  {u"name": u"AÇǱÞΣSSὩΙST"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)

        for t in [{u"name": u"Col des Champs XIIVVVIM"},
                  {u"name": u"ƻאᎯᚦ京"},
                 ]:
            assert not a.node(None, t), t
