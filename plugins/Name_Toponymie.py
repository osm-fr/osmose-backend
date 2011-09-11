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


class Name_Toponymie(Plugin):
    
    only_for = ["FR"]
    
    ## http://education.ign.fr/DISPLAY/000/526/725/5267258/charte_toponymie_IGN.pdf
    err_906    = 5040
    err_906_fr = u"Toponymie"
    err_906_en = u"Toponymy"
    
    def init(self, logger):
                
        # article 4.9 Majuscules et minuscules
        special  = [u""]
        
        special += [u"j", u"d", u"l", u"n", u"h"]
        
        special += [u"della"] # way 43563373
        special += [u"on"]    # Newark on Tren way/23791990
        special += [u"dit"]   # way/32519405
        special += [u"qui"]   # way/22790488
        special += [u"von"]   # way/8481714
        special += [u"van"]   # way/4254712
        special += [u"dal"]   # way/41271222

        special += [u"mon",u"ma",u"mes",u"ton",u"ta",u"tes",u"son",u"sa",u"ses",u"votre",u"vos",u"leur",u"leurs"]
        
        special += [u"bis", u"ter"]
        
        special += [u"le" , u"la" , u"les", u"l"  , u"un" , u"une"]
        
        special += [u"a"  , u"al" , u"als", u"an" , u"ar" , u"d"  , u"das", u"de",
                    u"dem", u"den", u"der", u"die", u"e"  , u"ech", u"el" ,
                    u"éla", u"els", u"en" , u"er" , u"era", u"ero", u"et" ,
                    u"eul", u"eun", u"eur", u"gli", u"het", u"i"  , u"las",
                    u"lé" , u"lo" , u"los", u"lou", u"lous",u"s"  , u"t"  ,
                    u"u"  , u"ul" , u"ur"]
        
        special += [u"au", u"aux", u"du", u"des", u"ès"]
        
        special += [u"â", u"agli", u"ai", u"al", u"als", u"am", u"as", u"beim",
                    u"dei", u"del", u"dels", u"det", u"dets", u"em", u"im",
                    u"um", u"vom", u"zum", u"zur"]
                    
        special += [u"à", u"à-bas", u"à-haut", u"au-deçà", u"au-delà", u"au-dessous",
                    u"au-dessus", u"auprès", u"bien", u"chez", u"ci-devant", u"contre",
                    u"d'", u"dans", u"de", u"deçà", u"de-ci", u"delà", u"de-là",
                    u"derrière", u"dessous", u"dessus", u"devant", u"en", u"entre",
                    u"et", u"face (à)", u"lès", u"lez", u"loin", u"(de)", u"mal",
                    u"malgré", u"mi", u"non", u"ou", u"où", u"outre", u"outre-mer",
                    u"outre-tombe", u"outre-Rhin", u"par", u"par-delà", u"par-dessous",
                    u"par-dessus", u"peu", u"près", u"sans", u"sauf", u"sous", u"sur",
                    u"sus", u"tard", u"tout", u"très", u"vers", u"vis-à-vis"]
                                                                                
        special += [u"a", u"auf", u"bei", u"cal", u"can", u"d'al laez", u"dalaé",
                    u"darios", u"darré", u"debas", u"débas", u"debat", u"débat",
                    u"delai", u"detras", u"di", u"durch", u"hinter", u"in", u"nieder",
                    u"oben", u"ober", u"op", u"over", u"soubre", u"soubré", u"tras",
                    u"tré", u"ueber", u"unter", u"vor", u"vorder", u"zu", u"zwischen"]

        special += [u"deu", u"dous"] # parlé Gascon (F. Rodrigo)

        special += [u"rural", u"exploitation"] # Chemin rural / Chemin d'exploitation
                    
        special2 = []
        for x in special:
            special2 += self._split(x)
        self.special = set(special2)
        
        self.minus = u"abcdefghijklmnopqrstuvwxyzàäâéèëêïîöôüûÿ"
                            
    def _split(self, name):
        for x in [u"’", u"\xa0", u"°", u"'", u"&amp;", u"&apos;", u"&quot;", u"/", u")", u"-", u"\"", u";", u".", u":", u"+", u"?", u"!", u",", u"|", u"*", u"Â°", u"_", u"="]:
            name = name.replace(x, u" ")
        #name = self.apostrophe.sub(u" ", name)
        return name.split(u" ")

    def node(self, data, tags):
        if u"name" not in tags:
            return
        if (u"highway" not in tags) and (u"waterway" not in tags) and (u"place" not in tags):
            return
        words = []
        split = self._split(tags[u"name"])
        if split and split[0] and split[0][0] in self.minus:
            words.append(split[0])
        for word in split:
            if word in self.special:
                continue
            if word[0] in self.minus:
                words.append(word)
        if words and (u"homme" in words) and ("Prud'homme" in tags[u"name"]):
            words.remove(u"homme")
        if words:
            return [(906, abs(hash(str(words))), {"fr": u"majuscule manquante à : %s"%u", ".join(set(words)),"en": u"missing caps letter for: %s"%u", ".join(set(words))})]
        return

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
