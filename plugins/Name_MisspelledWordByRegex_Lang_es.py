#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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

from __future__ import unicode_literals
from plugins.Name_MisspelledWordByRegex import P_Name_MisspelledWordByRegex


class Name_MisspelledWordByRegex_Lang_es(P_Name_MisspelledWordByRegex):

    only_for = ["es"]

    def init(self, logger):
        P_Name_MisspelledWordByRegex.init(self, logger)

        import re
        self.ReTests = {}
        self.ReTests[(100, u"Circunvalación\\2")] = [re.compile(r"^Circunvalación(| .*)$"),
                                                  re.compile(r"^([Cc][Ii][Rr][Cc][Uu][Nn]?[Vv][Aa][Ll][Aa][Cc][Ii].[Nn])(| .*)$")]
        self.ReTests = self.ReTests.items()


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_MisspelledWordByRegex_Lang_es(None)
        a.init(None)
        for (d, f) in [(u"Circunvalacion", u"Circunvalación"),
                      ]:
            self.check_err(a.node(None, {"name": d}), ("name='%s'" % d))
            self.assertEquals(a.node(None, {"name": d})["fix"]["name"], f)
            assert not a.node(None, {"name": f}), ("name='%s'" % f)
