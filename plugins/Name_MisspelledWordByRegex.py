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


class Name_MisspelledWordByRegex(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[701] = { "item": 5010, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Badly written word") }

        import re
        self.ReTests = {}
        self.ReTests[( 0, u"École")]     = re.compile(r"^([EÉée][Cc][Oo][Ll][Ee])(| .*)$")
        self.ReTests[( 1, u"Église")]    = re.compile(r"^([EÉée][Gg][Gl][Ii][Ss][Ee])(| .*)$")
        self.ReTests[( 2, u"La")]        = re.compile(r"^([Ll][Aa])( .*)$")
        self.ReTests[( 3, u"Étang")]     = re.compile(r"^([EÉée][Tt][Tt]?[AaEe][Nn][GgTt]?)(| .*)$")
        self.ReTests[( 4, u"Saint")]     = re.compile(r"^([Ss](?:[Aa][Ii][Nn])?[Tt]\.?)( .*)$")
        self.ReTests[( 5, u"Hôtel")]     = re.compile(r"^([Hh][OoÔô][Tt][Ee][Ll])(| .*)$")
        self.ReTests[( 6, u"Château")]   = re.compile(r"^([Cc][Hh][ÂâAa][Tt][Ee][Aa][Uu])(| .*)$")
        self.ReTests[( 7, u"McDonald's")]= re.compile(r"^([Mm][Aa]?[Cc] ?[Dd][Oo](?:[Nn][Aa][Ll][Dd]'?[Ss]?)?( .+)?)$")
        self.ReTests[( 8, u"Sainte")]    = re.compile(r"^([Ss](?:[Aa][Ii][Nn])?[Tt][Ee]\.?)( .*)$")
        self.ReTests[( 9, u"Le")]        = re.compile(r"^([Ll][Ee])( .*)$")
        self.ReTests[(10, u"Les")]       = re.compile(r"^([Ll][Ee][Ss])( .*)$")
        self.ReTests = self.ReTests.items()

    def node(self, data, tags):
        if u"name" not in tags:
            return
        name = tags["name"]
        for test in self.ReTests:
            if not name.startswith(test[0][1]):
                r = test[1].match(name)
                if r:
                    add_str = r.group(2) if r.group(2) else u""
                    return [(701, test[0][0], {"fix": {"name": test[0][1] + add_str} })]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_MisspelledWordByRegex(None)
        a.init(None)
        for (d, f) in [(u"eglise ", u"Église "),
                       (u"St. Michel", u"Saint Michel"),
                       (u"Ecole", u"École"),
                       (u"Mac Donald", u"McDonald's"),
                       (u"Ste Amal et Fils Sarl", u"Sainte Amal et Fils Sarl"),
                       (u"SAiNte anne", u"Sainte anne"),
                       (u"les lesles", u"Les lesles"),
                      ]:
            self.check_err(a.node(None, {"name": d}), ("name='%s'" % d))
            self.assertEquals(a.node(None, {"name": d})[0][2]["fix"]["name"], f)
            assert not a.node(None, {"name": f}), ("name='%s'" % f)

            self.check_err(a.way(None, {"name": d}, None), ("name='%s'" % d))
            self.check_err(a.relation(None, {"name": d}, None), ("name='%s'" % d))
            assert not a.node(None, {"amenity": f}), ("amenity='%s'" % f)
