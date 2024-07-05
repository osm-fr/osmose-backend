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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin


class Name_UpperCaseNumber(Plugin):

    only_for = ["fr", "ES", "it", "pt"] # languages fr, it, pt worldwide, Spanish (es) only for Iberian Spain (ES), hence country code

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[905] = self.def_class(item = 5010, level = 1, tags = ['name', 'fix:chair'],
            title = T_('Abbreviation of number should be in lowercase'),
            detail = T_(
'''Number written in capital letters: "N°" in place of "n°".'''))

        import re
        self.ReNUpperCase  = re.compile(u"^(|.* )N(°[0-9]+)(| .*)$")

    def node(self, data, tags):
        if "name" in tags:
            name = tags[u"name"]
            r = self.ReNUpperCase.match(name)
            if r:
                return {"class": 905, "fix": {"name": "{0}n{1}{2}".format(r.group(1), r.group(2), r.group(3))}}

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
