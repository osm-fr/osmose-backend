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
import re


class Name_Dictionary(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[703] = { "item": 5010, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Word not found in dictionary") }
        self.errors[704] = { "item": 5010, "level": 1, "tag": ["value", "fix:chair"], "desc": T_(u"Encoding problem") }

        self.DictMotsConnus   = [""]
        self.DictCorrections  = {}
        self.DictMotsInconnus = []

        # Dictionnaires : Externes
        for d in self.father.ToolsListDir("dictionnaires"):
            if d[-1] == "~": continue
            if d[:4] != "Dico": continue
            self.DictMotsConnus += self.father.ToolsReadList("dictionnaires/" + d)

        # Dictionnaires : Enumération
        self.DictMotsConnus.append("1e")
        self.DictMotsConnus.append("1er")
        for i in range(2,2000):
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"ème")
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"è")
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"e")
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"ième")

        # Dictionnaires : Romain
        for i in [u"",u"X",u"XX"]:
            for j in [u"I",u"II",u"III",u"IV",u"V",u"VI",u"VII",u"VIII",u"IX",u"X"]:
                self.DictMotsConnus.append(i + j)
                self.DictMotsConnus.append(i + j + u"ème")
                self.DictMotsConnus.append(i + j + u"è")
                self.DictMotsConnus.append(i + j + u"e")
                self.DictMotsConnus.append(i + j + u"ième")

        # Dictionnaires : 1a 1b 1c
        for i in range(1,2000):
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"a")
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"b")
            self.DictMotsConnus.append(str(i).decode("utf-8") + u"c")

        # Dictionnaires : Alphabet majuscule
        for i in range(65,91):
            self.DictMotsConnus.append(chr(i).decode("utf-8"))

        # Dictionnaires : Nombres 1..10000
        for i in range(0,10000):
            self.DictMotsConnus.append(str(i).decode("utf-8"))

        # Dictionnaires : Nombres 01..09
        for i in range(0,10):
            self.DictMotsConnus.append(u"0" + str(i).decode("utf-8"))

        # Dictionnaires : Routes
        for i in range(0,2000):
            self.DictMotsConnus.append(u"A" + str(i).decode("utf-8"))
            self.DictMotsConnus.append(u"D" + str(i).decode("utf-8"))
            self.DictMotsConnus.append(u"N" + str(i).decode("utf-8"))
            self.DictMotsConnus.append(u"C" + str(i).decode("utf-8"))
            self.DictMotsConnus.append(u"E" + str(i).decode("utf-8"))
            self.DictMotsConnus.append(u"RN" + str(i).decode("utf-8"))

        # Corrections : Externes
        for d in self.father.ToolsListDir("dictionnaires"):
            if d[-1] == "~": continue
            if d[:4] != "Corr": continue
            self.DictCorrections = dict( self.DictCorrections.items() + self.father.ToolsReadDict("dictionnaires/" + d, ":").items() )

        # Corrections : Enumeration
        for i in range(2,2000):
            self.DictCorrections[str(i).decode("utf-8") + u"ieme"] = str(i).decode("utf-8") + u"ième"
            self.DictCorrections[str(i).decode("utf-8") + u"eme"]  = str(i).decode("utf-8") + u"ème"
            self.DictCorrections[str(i).decode("utf-8") + u"éme"]  = str(i).decode("utf-8") + u"ème"
            #BadDict[str(i).decode("utf-8") + u"e"]   = str(i).decode("utf-8") + u"è"

        # Incohérences : mots dans bad dict et dans dict
        #self.LogInformation(u"Mot(s) à corriger et à accepter")
        #for k in self.DictCorrectionsK:
        #    if k in self.DictMotsConnus:
        #        self.DictMotsConnus.remove(k)
        #        self.LogInformation(u"  " + k)

        # Incohérences : 
        #self.LogInformation(u"Correction(s) absentes du dictionnaire")
        #for k in self.DictCorrectionsK:
        #    for v in self.DictCorrections[k].split("|"):
        #        if v not in self.DictMotsConnus:
        #            self.LogInformation(u"  " + k + " => " + self.DictCorrections[k])
        #            self.DictCorrectionsK.remove(k)
        #            self.DictCorrections.pop(k)
        #            break

        # Dictionnaires : Noms apparaissant régulièrement
        self.DictCommonWords = [""] + [ x for x in self.father.ToolsReadList("dictionnaires/ResultCommonWords") if x in self.DictMotsConnus]

        self.DictMotsConnus   = set(self.DictMotsConnus)
        self.DictMotsInconnus = set(self.DictMotsInconnus)

        # Dictionnaire d'encodage
        self.DicoEncodage = {}
        for c in (u"à", u"é", u"è", u"ë", u"ê", u"î", u"ï", u"ô", u"ö", u"û", u"ü", u"ÿ", u"ç", u"À", u"É", u"É", u"È", u"Ë", u"Ê", u"Î", u"Ï", u"Ô", u"Ö", u"Û", u"Ü", u"Ÿ", u"Ç", u"œ", u"æ", u"Œ", u"Æ"):
            ustr = "".join([unichr(int(i.encode('hex'), 16)) for i in c.encode('utf-8')])
            self.DicoEncodage[ustr] = c

        self.DicoEncodage[u"s‎"]  = u"s"
        self.DicoEncodage[u"`"]  = u"'"
        self.DicoEncodage[u"n‎"]  = u"n"

        self.apostrophe = re.compile('\b[djl](?:\'|â€™|&quot;)(?=\w)', re.I)

    def _get_err(self, name):
        initialName = name

        err = []

        for x in [u"&amp;", u"&apos;", u"&quot;", u"/", u")", u"-", u"\"", u";", u".", u":", u"+", u"?", u"!", u",", u"|", u"*", u"Â°", u"_", u"="]:
            name = name.replace(x, " ")
        name = self.apostrophe.sub(' ', name)

        for WordComplet in name.split(" "):
            if WordComplet in self.DictCommonWords: continue
            elif WordComplet in self.DictMotsConnus: continue
            elif WordComplet in self.DictCorrections:
                if self.DictCorrections[WordComplet]:
                    err.append((703, abs(hash(WordComplet)), {"fix": {"name": initialName.replace(WordComplet, self.DictCorrections[WordComplet])} }))
                else:
                    raise Exception("Could not find correction for %s" % WordComplet)
            else:
                PbEncodage = False
                for x in self.DicoEncodage:
                    if x in WordComplet:
                        PbEncodage = True
                        err.append((704, 0, {"fix": {"name": initialName.replace(x, self.DicoEncodage[x])} }))
                if PbEncodage: continue
                #if WordComplet in self.DictMotsInconnus: continue
                if "0" in WordComplet: continue
                if "1" in WordComplet: continue
                if "2" in WordComplet: continue
                if "3" in WordComplet: continue
                if "4" in WordComplet: continue
                if "5" in WordComplet: continue
                if "6" in WordComplet: continue
                if "7" in WordComplet: continue
                if "8" in WordComplet: continue
                if "9" in WordComplet: continue
                self.DictMotsInconnus.add(WordComplet)

        return err

    def node(self, data, tags):
        if u"name" not in tags:
            return
        return self._get_err(tags[u"name"])

    def way(self, data, tags, nodes):
        if u"name" not in tags:
            return
        return self._get_err(tags[u"name"])

    def relation(self, data, tags, members):
        if u"name" not in tags:
            return
        return self._get_err(tags[u"name"])

    #def end(self, logger):
    #    f = self.father.ToolsOpenFile("ResultMotsATrier", "w")
    #    for x in self.DictMotsInconnus:
    #        f.write(x.encode("utf-8") + "\n")
    #    #logger.log(u"%d mots à trier"%len(self.DictMotsInconnus))
    #    f.close()
    #    return

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
        a = Name_Dictionary(father())
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
                fix = rdp[0][2]["fix"]["name"]
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
