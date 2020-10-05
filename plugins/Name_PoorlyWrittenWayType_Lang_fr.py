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


class Name_PoorlyWrittenWayType_Lang_fr(P_Name_PoorlyWrittenWayType):

    only_for = ["fr"]

    def init(self, logger):
        P_Name_PoorlyWrittenWayType.init(self, logger, True)

        self.ReTests = {}
        # Captial at begining already checked by French Toponymie plugin
        self.ReTests[( 0, 'Allée')]      = re.compile(r'^([A][Ll][Ll]?[EÉée][Ee]?|[Aa][Ll][Ll]\.) .*$')
        self.ReTests[( 0, 'Allées')]     = re.compile(r'^([A][Ll][Ll]?[EÉée][Ee]?[sS]) .*$')
        self.ReTests[( 1, 'Boulevard')]  = re.compile(r'^([B]([Oo][Uu][Ll][Ll]?[Ee]?)?[Vv]?([Aa][Rr])?[Dd]\.?) .*$')
        self.ReTests[( 2, 'Avenue')]     = self.generator(r'Av|enue')
        self.ReTests[( 4, 'Chemin')]     = self.generator(r'Che|min')
        self.ReTests[( 5, 'Route')]      = re.compile(r'^([R]([Oo][Uu])?[Tt][Ee]?\.?) .*$')
        self.ReTests[( 6, 'Esplanade')]  = re.compile(r'^([EÉ][Ss][Pp][Ll][Aa][Nn][Aa][Dd][Ee]) .*$')
        self.ReTests[( 7, 'Rue')]        = self.generator(r'R|ue')
        self.ReTests[( 8, 'Giratoire')]  = re.compile(r'^([G][Ii][Rr][Aa][Tt][Oo][Ii][Rr][Ee]) .*$')
        self.ReTests[( 9, 'Rond-Point')] = re.compile(r'^([R][Oo][Nn][Dd][- ][Pp][Oo][Ii][Nn][Tt]) .*$')
        self.ReTests[( 9, 'Rondpoint')]  = re.compile(r'^([R][Oo][Nn][Dd][Pp][Oo][Ii][Nn][Tt]) .*$')
        self.ReTests[(10, 'Carrefour')]  = re.compile(r'^([C][Aa][Rr][Rr][Ee][Ff][Oo][Uu][Rr]) .*$')
        self.ReTests[(11, 'Place')]      = self.generator(r'Pl|ace')
        self.ReTests[(12, 'Impasse')]    = self.generator(r'Imp|asse')
        self.ReTests[(13, 'Quai')]       = self.generator(r'Qu|ai')
        self.ReTests[(14, 'Square')]     = self.generator(r'Sq|uare')
        self.ReTests[(15, 'Route Forestière')] = re.compile(r'^([R][Ff]) .*$')
        self.ReTests = self.ReTests.items()



###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_PoorlyWrittenWayType_Lang_fr(None)
        a.init(None)
        for d in [u"ALLÉE ", u"AllÉes grandioses", u"BOUleVARD ", "Av. ", "Av ", "Bvd. ", "Rte ", "Rt. ", "Rond Point O", "RF "]:
            self.check_err(a.way(None, {"highway": "h", "name": d}, None), ("name='{0}'".format(d)))
            assert not a.way(None, {"highway": d}, None), ("highway='{0}'".format(d))

        for d in [u"Allée ", u"Allées fleuries", u"Boulevard ", "Rte", "route "]:
            assert not a.way(None, {"highway": "h", "name": d}, None), ("name='{0}'".format(d))
