#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
## Copyrights Joan Montané     2015                                      ##
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


class Name_PoorlyWrittenWayType_es(P_Name_PoorlyWrittenWayType):

    only_for = ["ca"]

    def init(self, logger):
        P_Name_PoorlyWrittenWayType.init(self, logger)

        self.ReTests = {}
        # Captial at start already checked by Toponymie plugin
        self.ReTests[(200, u"Avinguda")]  = self.generator(u"Av|inguda")
        self.ReTests[(201, u"Avinguda")]  = re.compile(u"^([A][Vv]([Dd][Aa]?)?\.?) .*$")
        self.ReTests[(202, u"Carrer")]    = self.generator(u"C|arrer")
        self.ReTests[(203, u"Carrer")]    = re.compile(u"^([C]([Ll]\.?|/)) .*$")
        self.ReTests[(204, u"Carretera")]= re.compile(u"^([C][Aa][Rr][Rr][Ee][Tt][Ee][Rr][Aa]) .*$")
        self.ReTests[(204, u"Carretera")]= re.compile(u"^([C][Tt][Rr][Aa]\.?) .*$")
        # Check for Spanish way descriptions
        self.ReTests[(205, u"Avinguda")]  = self.generator(u"Ave|nida")
        self.ReTests[(206, u"Carrer")]    = self.generator(u"C|alle")
        self.ReTests[(207, u"Plaça")]    = self.generator(u"^([P][Ll]([aA][çÇzZ][aA])?\.?) .*$")
        self.ReTests[(208, u"Camí")]  = self.generator(u"^Camino")
        self.ReTests[(209, u"Camí")]  = self.generator(u"^CM")
        self.ReTests[(210, u"Passatge")]  = self.generator(u"^Pasaje")
        self.ReTests[(211, u"Passatge")]  = self.generator(u"^PGE")
        self.ReTests = self.ReTests.items()


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_PoorlyWrittenWayType_ca(None)
        a.init(None)
        for d in [u"AVINGUDA ", u"Ave. ", u"Ave ", u"Av ", u"Avd. ", u"Avda. ", u"Cl. Grande", u"C/ A", u"Ctra. "]:
            self.check_err(a.node(None, {"name": d}), ("name='%s'" % d))
            assert not a.node(None, {"highway": d}), ("highway='%s'" % d)

        for d in [u"Avinguda Gran"]:
            assert not a.node(None, {"name": d}), ("name='%s'" % d)
