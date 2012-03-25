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


class Name_Dictionnaire(Plugin):
    
    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[703] = { "item": 5010, "desc": {"en": u"Word not present in dictionary", "fr": u"Mot absent du dictionnaire"} }
        self.errors[704] = { "item": 5010, "desc": {"en": u"Encoding problem", "fr": u"Problème d'encodage"} }

        self.DictMotsConnus   = [""]
        self.DictCorrections  = {}
        self.DictMotsInconnus = []

        # Dictionnaires : Externes
        for d in self.father.ToolsListDir("dictionnaires"):
            if d[-1] == "~": continue
            if d[:4] <> "Dico": continue
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
            if d[:4] <> "Corr": continue
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
        self.DicoEncodage[u"Ã "] = u"à"
        self.DicoEncodage[u"Ã©"] = u"é"
        self.DicoEncodage[u"Ãš"] = u"è"
        self.DicoEncodage[u"Ã«"] = u"ë"
        self.DicoEncodage[u"Ãª"] = u"ê"
        self.DicoEncodage[u"Ã®"] = u"î"
        self.DicoEncodage[u"Ã¯"] = u"ï"
        self.DicoEncodage[u"ÃŽ"] = u"ô"
        self.DicoEncodage[u"Ã¶"] = u"ö"
        self.DicoEncodage[u"Ã»"] = u"û"
        self.DicoEncodage[u"ÃŒ"] = u"ü"
        self.DicoEncodage[u"Ã¿"] = u"ÿ"
        self.DicoEncodage[u"Ã§"] = u"ç"
        self.DicoEncodage[u"Ã�"] = u"À"        
        self.DicoEncodage[u"Ã‰"] = u"É"
        self.DicoEncodage[u"Ã�"] = u"É"
        self.DicoEncodage[u"Ã�"] = u"È"
        self.DicoEncodage[u"Ã�"] = u"Ë"
        self.DicoEncodage[u"Ã�"] = u"Ê"
        self.DicoEncodage[u"Ã�"] = u"Î"
        self.DicoEncodage[u"Ã�"] = u"Ï"
        self.DicoEncodage[u"Ã�"] = u"Ô"
        self.DicoEncodage[u"Ã�"] = u"Ö"
        self.DicoEncodage[u"Ã�"] = u"Û"
        self.DicoEncodage[u"Ã�"] = u"Ü"
        self.DicoEncodage[u"Åž"] = u"Ÿ"
        self.DicoEncodage[u"Ã�"] = u"Ç"
        self.DicoEncodage[u"Å�"] = u"œ"
        self.DicoEncodage[u"ÃŠ"] = u"æ"
        self.DicoEncodage[u"Å�"] = u"Œ"
        self.DicoEncodage[u"Ã�"] = u"Æ"
        
        self.DicoEncodage[u"s‎"]  = u"s"
        self.DicoEncodage[u"�"]  = u"é"
        self.DicoEncodage[u"ᵉ"]  = u"ème - caratère absent de beaucoup de polices"
        self.DicoEncodage[u"�"]  = u"è"
        self.DicoEncodage[u"`"]  = u"'"
        self.DicoEncodage[u"�"]  = u"ê"
        self.DicoEncodage[u"n‎"]  = u"n"
         
        self.apostrophe = re.compile('\b[djl](?:\'|â€™|&quot;)(?=\w)', re.I)
        
    def _get_err(self, name):

        err = []

        for x in [u"&amp;", u"&apos;", u"&quot;", u"/", u")", u"-", u"\"", u";", u".", u":", u"+", u"?", u"!", u",", u"|", u"*", u"Â°", u"_", u"="]:
            name = name.replace(x, " ")
        name = self.apostrophe.sub(' ', name)

        for WordComplet in name.split(" "):
            if WordComplet in self.DictCommonWords: continue
            elif WordComplet in self.DictMotsConnus: continue
            elif WordComplet in self.DictCorrections:
                if self.DictCorrections[WordComplet]:
                    err.append((703, abs(hash(WordComplet)), {"fix": {"name": self.DictCorrections[WordComplet]} }))
                else:
                    err.append((703, abs(hash(WordComplet)), {"en": WordComplet}))
            else:
                PbEncodage = False
                for x in self.DicoEncodage:
                    if x in WordComplet:
                        PbEncodage = True
                        err.append((704, 0, {"fix": {"name": self.DicoEncodage[x]} }))
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
