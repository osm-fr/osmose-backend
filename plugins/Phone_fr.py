#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Francois Gouget fgouget free.fr 2017                       ##
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


class Phone_fr(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)

        import re
        self.BadShort = re.compile(r"^(\+33 *)([0-9]{4})$")
        self.BadInter = re.compile(r"^(\+33 *0)([0-9 ]{8,})$")
        self.National = re.compile(r"^(0 *)([1-9][0-9 ]{8,})$")
        self.errors[30921] = { "item": 3092, "level": 2, "tag": ["value", "fix:chair"], "desc": T_(u"Extra \"0\" after international code") }
        self.errors[30922] = { "item": 3092, "level": 2, "tag": ["value", "fix:chair"], "desc": T_(u"National short code can't be internationalized") }
        self.errors[30923] = { "item": 3092, "level": 3, "tag": ["value", "fix:chair"], "desc": T_(u"Missing international prefix") }

    def node(self, data, tags):
        for tag in (u"contact:fax", u"contact:phone", u"fax", u"phone"):
            if tag not in tags:
                continue
            phone = tags[tag]

            r = self.BadInter.match(phone)
            if r:
                return [{"class":30921, "fix": {tag: "+33 " + r.group(2)}}]

            r = self.BadShort.match(phone)
            if r:
                 return [{"class":30922, "fix": {tag: r.group(2)}}]

            r = self.National.match(phone)
            if r:
                return [{"class":30923, "fix": {tag: "+33 " + r.group(2)}}]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Phone_fr(None)
        a.init(None)
        for (d, f) in [(u"+33 0102030405", u"+33 102030405"),
                       (u"+330102030405", u"+33 102030405"),
                       (u"+33 01 02 03 04 05", u"+33 1 02 03 04 05"),
                       (u"+33 3631", u"3631"),
                       (u"0102030405", u"+33 102030405"),
                       (u"01 02 03 04 05", u"+33 1 02 03 04 05"),
                      ]:
            self.check_err(a.node(None, {"phone": d}), ("phone='%s'" % d))
            self.assertEquals(a.node(None, {"phone": d})[0]["fix"]["phone"], f)

        for d in [u"118987",
                 ]:
            assert not a.node(None, {"phone": f}), ("phone='%s'" % f)
