#-*- coding: utf-8 -*-

###########################################################################
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
import re

class TagFix_Vatin(Plugin):

    # ref:vatin is a tag to add the VAT identification number.
    # The usual syntax is <country-code><VAT-number>
    # Examples:
    # ref:vatin=IT12345678901 for a business in Italy
    # ref:vatin=DE115055186 for a business in Germany

    # XXX Enable more countries
    only_for = ["IT"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[99999] = {"item": 9999, "level": 3, "tag": ["ref"], "desc": T_(u'Invalid value of tag "ref:vatin"') }

    # https://it.wikipedia.org/wiki/Partita_IVA
    def it_vatin(self, vatin):
        if (len(vatin) != 11):
            return False

        # A Luhn algorithm implementation
        x = 0
        y = 0
        z = 0
        for i in range(0, 10, 2):
            x += int(vatin[i:i + 1])
        for i in range(1, 10, 2):
            y += 2 * (int(vatin[i:i + 1]))
            if int(vatin[i:i + 1]) >= 5:
                z = z + 1
        t = (x + y + z) % 10
        c = int(vatin[10:11])
        return c == (10 - t) % 10

    def node(self, data, tags):
        if "ref:vatin" in tags:
            x = re.split("^([A-Z]{2})(.+)$", tags["ref:vatin"])
            if (len(x) < 3):
                return {"class": 99999, "subclass": 0 }
            if x[1] == 'IT' and self.it_vatin(x[2]) == False:
                return {"class": 99999, "subclass": 1 }

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Vatin(None)
        a.init(None)

        assert not a.node(None, {"ref:vatin": "IT11111111115"})
        assert not a.way(None, {"ref:vatin": "IT11111111115"}, None)
        assert not a.relation(None, {"ref:vatin": "IT11111111115"}, None)
        assert not a.node(None, {"ref:vatin": "XXX"})
        assert a.node(None, {"ref:vatin": "XX"})
        assert a.node(None, {"ref:vatin": "11111111115"})
        assert a.node(None, {"ref:vatin": "IT11111111111"})

