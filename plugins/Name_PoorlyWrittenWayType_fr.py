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

from plugins.Name_PoorlyWrittenWayType import P_Name_PoorlyWrittenWayType
import re


class Name_PoorlyWrittenWayType_fr(P_Name_PoorlyWrittenWayType):

    only_for = ["fr"]

    def init(self, logger):
        P_Name_PoorlyWrittenWayType.init(self, logger, True)

        self.ReTests = {}
        # Captial at begining already checked by French Toponymie plugin
        self.ReTests[( 0, u"Allée")]     = re.compile(u"^([A][Ll][Ll]?[EÉée][Ee]?|[Aa][Ll][Ll]\.) .*$")
        self.ReTests[( 0, u"Allées")]    = re.compile(u"^([A][Ll][Ll]?[EÉée][Ee]?[sS]) .*$")
        self.ReTests[( 1, u"Boulevard")] = re.compile(u"^([B]([Oo][Uu][Ll][Ll]?[Ee]?)?[Vv]?([Aa][Rr])?[Dd]\.?) .*$")
        self.ReTests[( 2, u"Avenue")]    = self.generator(u"Av|enue")
        self.ReTests[( 4, u"Chemin")]    = self.generator(u"Che|min")
        self.ReTests[( 5, u"Route")]     = re.compile(u"^([R]([Oo][Uu])?[Tt][Ee]?\.?) .*$")
        self.ReTests[( 6, u"Esplanade")] = re.compile(u"^([EÉ][Ss][Pp][Ll][Aa][Nn][Aa][Dd][Ee]) .*$")
        self.ReTests[( 7, u"Rue")]       = self.generator(u"R|ue")
        self.ReTests[( 8, u"Giratoire")] = re.compile(u"^([G][Ii][Rr][Aa][Tt][Oo][Ii][Rr][Ee]) .*$")
        self.ReTests[( 9, u"Rond-Point")]= re.compile(u"^([R][Oo][Nn][Dd][- ][Pp][Oo][Ii][Nn][Tt]) .*$")
        self.ReTests[( 9, u"Rondpoint")] = re.compile(u"^([R][Oo][Nn][Dd][Pp][Oo][Ii][Nn][Tt]) .*$")
        self.ReTests[(10, u"Carrefour")] = re.compile(u"^([C][Aa][Rr][Rr][Ee][Ff][Oo][Uu][Rr]) .*$")
        self.ReTests[(11, u"Place")]     = self.generator(u"Pl|ace")
        self.ReTests[(12, u"Impasse")]   = self.generator(u"Imp|asse")
        self.ReTests[(13, u"Quai")]      = self.generator(u"Qu|ai")
        self.ReTests[(14, u"Square")]    = self.generator(u"Sq|uare")
        self.ReTests[(15, u"Route Forestière")] = re.compile(u"^([R][Ff]) .*$")
        self.ReTests = self.ReTests.items()



###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_PoorlyWrittenWayType_fr(None)
        a.init(None)
        for d in [u"ALLÉE ", u"AllÉes grandioses", u"BOUleVARD ", "Av. ", "Av ", "Bvd. ", "Rte ", "Rt. ", "Rond Point O", "RF "]:
            self.check_err(a.way(None, {"highway": "h", "name": d}, None), ("name='%s'" % d))
            assert not a.way(None, {"highway": d}, None), ("highway='%s'" % d)

        for d in [u"Allée ", u"Allées fleuries", u"Boulevard ", "Rte", "route "]:
            assert not a.way(None, {"highway": "h", "name": d}, None), ("name='%s'" % d)
