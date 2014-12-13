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


class Name_Dictionary_fr(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[703] = { "item": 5010, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Word not found in dictionary") }
        self.errors[704] = { "item": 5010, "level": 1, "tag": ["value", "fix:chair"], "desc": T_(u"Encoding problem") }

        self.DictKnownWords = [""]
        self.DictCorrections = {}
        self.DictUnknownWords = []

        # Externals dictionaries

        # Dictionaries
        for d in self.father.ToolsListDir("dictionaries/fr"):
            if d[-1] == "~": continue
            if d[:4] != "Dico": continue
            self.DictKnownWords += self.father.ToolsReadList("dictionaries/" + d)

        # Corrections
        for d in self.father.ToolsListDir("dictionaries"):
            if d[-1] == "~": continue
            if d[:4] != "Corr": continue
            self.DictCorrections = dict( self.DictCorrections.items() + self.father.ToolsReadDict("dictionaries/" + d, ":").items() )

        # Common words
        self.DictCommonWords = [""] + [ x for x in self.father.ToolsReadList("dictionaries/ResultCommonWords") if x in self.DictKnownWords]

        # Numbering en letters

        # 1a 1b 1c
        for i in range(1,2000):
            self.DictKnownWords.append(str(i).decode("utf-8") + u"a")
            self.DictKnownWords.append(str(i).decode("utf-8") + u"b")
            self.DictKnownWords.append(str(i).decode("utf-8") + u"c")

        # Capitals
        for i in range(65,91):
            self.DictKnownWords.append(chr(i).decode("utf-8"))

        # Numbers 1..10000
        for i in range(0,10000):
            self.DictKnownWords.append(str(i).decode("utf-8"))

        # Numbers 01..09
        for i in range(0,10):
            self.DictKnownWords.append(u"0" + str(i).decode("utf-8"))

        # Latin language

        # Encoding
        self.DirctEncoding = {}
        for c in (u"à", u"é", u"è", u"ë", u"ê", u"î", u"ï", u"ô", u"ö", u"û", u"ü", u"ÿ", u"ç", u"À", u"É", u"É", u"È", u"Ë", u"Ê", u"Î", u"Ï", u"Ô", u"Ö", u"Û", u"Ü", u"Ÿ", u"Ç", u"œ", u"æ", u"Œ", u"Æ"):
            ustr = "".join([unichr(int(i.encode('hex'), 16)) for i in c.encode('utf-8')])
            self.DirctEncoding[ustr] = c

        self.DirctEncoding[u"s‎"] = u"s"
        self.DirctEncoding[u"`"] = u"'"
        self.DirctEncoding[u"n‎"] = u"n"

        # French

        # Apostrophes
        self.apostrophe = re.compile('\b[djl](?:\'|â€™|&quot;)(?=\w)', re.I)

        # Roman numbers
        for i in [u"",u"X",u"XX"]:
            for j in [u"I",u"II",u"III",u"IV",u"V",u"VI",u"VII",u"VIII",u"IX",u"X"]:
                self.DictKnownWords.append(i + j)
                self.DictKnownWords.append(i + j + u"ème")
                self.DictKnownWords.append(i + j + u"è")
                self.DictKnownWords.append(i + j + u"e")
                self.DictKnownWords.append(i + j + u"ième")

        # Enumations
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

        # Incohérences : mots dans bad dict et dans dict
        #self.LogInformation(u"Mot(s) à corriger et à accepter")
        #for k in self.DictCorrectionsK:
        #    if k in self.DictKnownWords:
        #        self.DictKnownWords.remove(k)
        #        self.LogInformation(u"  " + k)

        # Incohérences : 
        #self.LogInformation(u"Correction(s) absentes du dictionnaire")
        #for k in self.DictCorrectionsK:
        #    for v in self.DictCorrections[k].split("|"):
        #        if v not in self.DictKnownWords:
        #            self.LogInformation(u"  " + k + " => " + self.DictCorrections[k])
        #            self.DictCorrectionsK.remove(k)
        #            self.DictCorrections.pop(k)
        #            break

        self.DictKnownWords = set(self.DictKnownWords)
        self.DictUnknownWords = set(self.DictUnknownWords)


    def _get_err(self, name):
        initialName = name

        err = []

        for x in [u"&amp;", u"&apos;", u"&quot;", u"/", u")", u"-", u"\"", u";", u".", u":", u"+", u"?", u"!", u",", u"|", u"*", u"Â°", u"_", u"="]:
            name = name.replace(x, " ")
        name = self.apostrophe.sub(' ', name)

        for WordComplet in name.split(" "):
            if WordComplet in self.DictCommonWords: continue
            elif WordComplet in self.DictKnownWords: continue
            elif WordComplet in self.DictCorrections:
                if self.DictCorrections[WordComplet]:
                    err.append((703, abs(hash(WordComplet)), {"fix": {"name": initialName.replace(WordComplet, self.DictCorrections[WordComplet])} }))
                else:
                    raise Exception("Could not find correction for %s" % WordComplet)
            else:
                PbEncodage = False
                for x in self.DirctEncoding:
                    if x in WordComplet:
                        PbEncodage = True
                        err.append((704, 0, {"fix": {"name": initialName.replace(x, self.DirctEncoding[x])} }))
                if PbEncodage: continue
                #if WordComplet in self.DictUnknownWords: continue
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
                self.DictUnknownWords.add(WordComplet)

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
    #    for x in self.DictUnknownWords:
    #        f.write(x.encode("utf-8") + "\n")
    #    #logger.log(u"%d mots à trier"%len(self.DictUnknownWords))
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
        a = Name_Dictionary_fr(father())
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
