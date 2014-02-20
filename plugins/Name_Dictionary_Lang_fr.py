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

from .Name_Dictionary import P_Name_Dictionary
import re


class Name_Dictionary_Lang_fr(P_Name_Dictionary):

    only_for = ["fr"]

    def init(self, logger):
        P_Name_Dictionary.init(self, logger)

    def init_dictionaries(self):
        self.load_external_dictionaries('fr')
        self.laod_numbering()
        self.load_latin_language()

        # French

        # Roman numbers
        for i in [u"",u"X",u"XX"]:
            for j in [u"I",u"II",u"III",u"IV",u"V",u"VI",u"VII",u"VIII",u"IX",u"X"]:
                self.DictKnownWords.append(i + j)
                self.DictKnownWords.append(i + j + u"ème")
                self.DictKnownWords.append(i + j + u"è")
                self.DictKnownWords.append(i + j + u"e")
                self.DictKnownWords.append(i + j + u"ième")

        # Enurations
        self.DictKnownWords.append("1e")
        self.DictKnownWords.append("1er")
        for i in range(2,2000):
            self.DictKnownWords.append(str(i).decode("utf-8") + u"ème")
            self.DictKnownWords.append(str(i).decode("utf-8") + u"è")
            self.DictKnownWords.append(str(i).decode("utf-8") + u"e")
            self.DictKnownWords.append(str(i).decode("utf-8") + u"ième")

        for i in range(2,2000):
            self.DictCorrections[str(i).decode("utf-8") + u"ieme"] = str(i).decode("utf-8") + u"ième"
            self.DictCorrections[str(i).decode("utf-8") + u"eme"] = str(i).decode("utf-8") + u"ème"
            self.DictCorrections[str(i).decode("utf-8") + u"éme"] = str(i).decode("utf-8") + u"ème"
            #BadDict[str(i).decode("utf-8") + u"e"] = str(i).decode("utf-8") + u"è"

        # France

        # Dictionaries : Routes
        for i in range(0,2000):
            self.DictKnownWords.append(u"A" + str(i).decode("utf-8"))
            self.DictKnownWords.append(u"D" + str(i).decode("utf-8"))
            self.DictKnownWords.append(u"N" + str(i).decode("utf-8"))
            self.DictKnownWords.append(u"C" + str(i).decode("utf-8"))
            self.DictKnownWords.append(u"E" + str(i).decode("utf-8"))
            self.DictKnownWords.append(u"RN" + str(i).decode("utf-8"))


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        import modules.config as config
        from analysers.analyser_sax import Analyser_Sax
        class _config:
            options = {"language": "fr"}
            dir_scripts = config.dir_osmose
        class father(Analyser_Sax):
            config = _config()
            def __init__(self):
                pass
        a = Name_Dictionary_Lang_fr(father())
        a.init(None)
        assert not a.node(None, {"highway": "Pont des Anes"})
        name = [(u"Pont des Anes", u"Pont des Ânes"),
                (u"Pont des Ânes", None),
                (u"Rue Saint-AndrÃ©", u"Rue Saint-André"),
                (u"Rue Saint-André", None),
                (u"Rue de l`Acadie", u"Rue de l'Acadie"),
                (u"200ième rue", None),
                (u"199ème avenue", None),
                (u"199ème Avenude", u"199ème Avenue"),
                (u"199ème Avenue", None),
                (u"\u00c3\u0087a", u"Ça"),
                (u"Ça", None),
               ]
        for (n, f) in name:
            rdp = a.node(None, {"name": n})
            if f:
                self.check_err(rdp, ("name='%s'" % n))
                fix = rdp[0]["fix"]["name"]
                self.assertEquals(fix, f, u"name='%s' - fix = wanted='%s' / got='%s'" % (n, f, fix))
            else:
                assert not rdp, ("name='%s'" % n)

        assert not a.way(None, {"highway": u"Rue Saint-AndrÃ©"}, None)
        assert not a.relation(None, {"highway": u"Rue Saint-AndrÃ©"}, None)
        assert not a.way(None, {"name": u"Rue Saint-André"}, None)
        assert not a.relation(None, {"name": u"Rue Saint-André"}, None)
        self.check_err(a.way(None, {"name": u"Rue Saint-AndrÃ©"}, None))
        self.check_err(a.relation(None, {"name": u"Rue Saint-AndrÃ©"}, None))

        # code that is not reachable in normal cases
        from nose.tools import assert_raises
        a.DictCorrections["buebdgxrtsuei"] = None
        assert_raises(Exception, a.node, None, {"name": "ceci est buebdgxrtsuei"})
