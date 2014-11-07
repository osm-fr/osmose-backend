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


class Name_UpperCaseNumber(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[905] = { "item": 5010, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Uppercase number") }

        import re
        self.ReNUpperCase  = re.compile(u"^(|.* )N(°[0-9]+)(| .*)$")

    def node(self, data, tags):
        if "name" in tags:
            name = tags[u"name"]
            r = self.ReNUpperCase.match(name)
            if r:
                return [(905, 0, {"fix":{"name":"%sn%s%s" % (r.group(1), r.group(2), r.group(3))}})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_UpperCaseNumber(None)
        a.init(None)
        for n in [u"N°189",
                  u"ue ure u N°18989 i ui, u",
                  u"N°18989 i ui, u",
                 ]:
            self.check_err(a.node(None, {"name": n}), n)
            self.check_err(a.way(None, {"name": n}, None), n)
            self.check_err(a.relation(None, {"name": n}, None), n)

        for n in [u"n°189",
                  u"ue ure u n°18989 i ui, u",
                  u"n°18989 i ui, u",
                 ]:
            assert not a.node(None, {"name": n}), n
            assert not a.way(None, {"name": n}, None), n
            assert not a.relation(None, {"name": n}, None), n
