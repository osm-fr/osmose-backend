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

from modules.Stablehash import stablehash64
from plugins.Plugin import Plugin
import re


class P_Name_Dictionary(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[703] = self.def_class(item = 5010, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Word not found in dictionary'),
            fix = T_(
'''Probably missing a capital.'''))
        self.errors[704] = self.def_class(item = 5010, level = 1, tags = ['value', 'fix:chair'],
            title = T_('Encoding problem'))

        self.DictKnownWords = [""]
        self.DictCorrections = {}
        self.DictUnknownWords = []
        self.DictCommonWords = [""]
        self.DictEncoding = {}
        self.apostrophe = None

        self.init_dictionaries()

        # Inconsistencies: words and dict and bad dict
        #self.LogInformation(u"Mot(s) à corriger et à accepter")
        #for k in self.DictCorrectionsK:
        #    if k in self.DictKnownWords:
        #        self.DictKnownWords.remove(k)
        #        self.LogInformation(u"  " + k)

        # Inconsistencies:
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

    def load_external_dictionaries(self, lang):
        # Dictionaries
        for d in self.father.ToolsListDir("dictionaries/%s" % lang):
            if d[-1] == "~": continue
            if d[:4] != "Dico": continue
            self.DictKnownWords += self.father.ToolsReadList("dictionaries/%s/%s" % (lang, d))

        # Corrections
        for d in self.father.ToolsListDir("dictionaries/%s" % lang):
            if d[-1] == "~": continue
            if d[:4] != "Corr": continue
            self.DictCorrections.update(self.father.ToolsReadDict("dictionaries/%s/%s" % (lang, d), ":"))

        # Common words
        self.DictCommonWords += [x for x in self.father.ToolsReadList("dictionaries/%s/ResultCommonWords" % lang) if x in self.DictKnownWords]

    def laod_numbering(self):
        # 1a 1b 1c
        for i in range(1,2000):
            self.DictKnownWords.append(u"{0}a".format(i))
            self.DictKnownWords.append(u"{0}b".format(i))
            self.DictKnownWords.append(u"{0}c".format(i))

        # Capitals
        for i in range(65,91):
            self.DictKnownWords.append(u"{0}".format(chr(i)))

        # Numbers 1..10000
        for i in range(0,10000):
            self.DictKnownWords.append(u"{0}".format(i))

        # Numbers 01..09
        for i in range(0,10):
            self.DictKnownWords.append(u"0{0}".format(i))

    def load_latin_language(self):
        # Apostrophes
        self.apostrophe = re.compile(r'\b[djl](?:\'|â€™|&quot;)(?=\w)', re.I)

        for c in (u"à", u"é", u"è", u"ë", u"ê", u"î", u"ï", u"ô", u"ö", u"û", u"ü", u"ÿ", u"ç", u"À", u"É", u"É", u"È", u"Ë", u"Ê", u"Î", u"Ï", u"Ô", u"Ö", u"Û", u"Ü", u"Ÿ", u"Ç", u"œ", u"æ", u"Œ", u"Æ"):
            ustr = "".join(([chr(i) for i in c.encode('utf-8')]))
            self.DictEncoding[ustr] = c

        self.DictEncoding[u"`"] = u"'"


    def init_dictionaries(self):
        pass


    def _get_err(self, tag, name):
        initialName = name

        for x in [u"&amp;", u"&apos;", u"&quot;", u"/", u")", u"-", u"\"", u";", u".", u":", u"+", u"?", u"!", u",", u"|", u"*", u"Â°", u"_", u"="]:
            name = name.replace(x, " ")
        if self.apostrophe:
            name = self.apostrophe.sub(' ', name)

        for WordComplet in name.split(" "):
            if WordComplet in self.DictCommonWords: continue
            elif WordComplet in self.DictKnownWords: continue
            elif WordComplet in self.DictCorrections:
                if self.DictCorrections[WordComplet]:
                    return {"class": 703, "subclass": stablehash64(tag), "fix": {"name": initialName.replace(WordComplet, self.DictCorrections[WordComplet])}}
                else:
                    raise Exception("Could not find correction for %s" % WordComplet)
            else:
                for x in self.DictEncoding:
                    if x in WordComplet:
                        return {"class": 704, "subclass": stablehash64(tag), "fix": {"name": initialName.replace(x, self.DictEncoding[x])}}

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


    def node(self, data, tags):
        err = []
        for name in [u"name", u"name_1", u"name_2", u"alt_name", u"loc_name", u"old_name", u"official_name", u"short_name", u"addr:street:name"]:
            if name in tags:
                e = self._get_err(name, tags[name])
                if e is not None:
                    err.append(e)
        return err

    def way(self, data, tags, nodes):
        return self.node(None, tags)

    def relation(self, data, tags, members):
        return self.node(None, tags)

    #def end(self, logger):
    #    f = self.father.ToolsOpenFile("ResultMotsATrier", "w")
    #    for x in self.DictUnknownWords:
    #        f.write(x + "\n")
    #    #logger.log(u"%d mots à trier"%len(self.DictUnknownWords))
    #    f.close()
    #    return


available_plugin_classes = []
