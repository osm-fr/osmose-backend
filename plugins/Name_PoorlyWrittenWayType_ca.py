#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights jmontane 2015                                              ##
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

from plugins.Name_PoorlyWrittenWayType import P_Name_PoorlyWrittenWayType
import re


class Name_PoorlyWrittenWayType_ca(P_Name_PoorlyWrittenWayType):

    only_for = ["ca"]

    def init(self, logger):
        P_Name_PoorlyWrittenWayType.init(self, logger)

        self.ReTests = {}
        self.ReTests[(200, u"Avinguda")]  = self.generator(u"Av|inguda")
        self.ReTests[(201, u"Avinguda")]  = re.compile(u"^([Aa][Vv]([Dd][Aa]?)?\.?) .*$")
        self.ReTests[(202, u"Carrer")]    = self.generator(u"C|arrer")
        self.ReTests[(203, u"Carrer")]    = re.compile(u"^([Cc]([Ll]\.?|/)) .*$")
        self.ReTests[(204, u"Carretera")] = re.compile(u"^([Cc][Aa][Rr][Rr][Ee][Tt][Ee][Rr][Aa]) .*$")
        self.ReTests[(204, u"Carretera")] = re.compile(u"^([Cc][Tt][Rr][Aa]\.?) .*$")
        self.ReTests = self.ReTests.items()


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_PoorlyWrittenWayType_ca(None)
        a.init(None)
        for d in [u"AVINGUDA ", u"Av ", u"Avd ", u"Av. ", u"Avd. ", u"Avda. ", u"Cl. Grande", u"C/ A", u"Ctra. ", "avinguda "]:
            self.check_err(a.way(None, {"highway": "h", "name": d}, None), ("name='%s'" % d))
            assert not a.way(None, {"highway": d}, None), ("highway='%s'" % d)

        for d in [u"Avinguda Gran"]:
            assert not a.way(None, {"highway": "h", "name": d}, None), ("name='%s'" % d)
