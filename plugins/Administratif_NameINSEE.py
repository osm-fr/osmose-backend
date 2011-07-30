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

class plugin:
    
    only_for = ["FR"]
    
    err_800    = 6030
    err_800_fr = u"Node place sans tag name"
    err_800_en = u"Node place without name tag"
    
    err_801    = 6040
    err_801_fr = u"Le code INSEE est introuvable dans la Base de l'INSEE"
    err_801_en = u"INSEE code cannot be found in INSEE database"
    
    err_802    = 6040
    err_802_fr = u"Le nom de commune ne correspond pas au code INSEE"
    err_802_en = u"Municipality name does not correspond to INSEE code"

    def Simplify(self, x):
        x = x.lower()
        x = self.father.ToolsStripAccents(x)
        x = self.father.ToolsStripDouble(x)
        x = x.replace(u"-", u" ")
        x = x.replace(u"'", u" ")
        x = x.replace(u"_", u" ")
        if x.startswith(u"le ")   : x = x[3:]
        elif x.startswith(u"la ") : x = x[3:]
        elif x.startswith(u"l ")  : x = x[2:]
        elif x.startswith(u"les "): x = x[4:]
        return x
    
    def init(self, logger):
        
        L = self.father.ToolsReadList("dictionnaires/BddCommunes")
        self.Communes = {}
        for x in L:
            x = x.split("\t")
            self.Communes[x[0]] = x
        
        self.SimpToNom  = {}
        self.SimpToCode = {}
        i = 0
        for k in self.Communes:
            i += 1
            #if not i%1000:
            #    logger.cpt(str(i)+"/"+str(len(self.Communes)))
            s1 = self.Communes[k][1]
            s2 = self.Simplify(s1)
            if s2 not in self.SimpToNom:
                self.SimpToNom[s2]  = []
                self.SimpToCode[s2] = []
            self.SimpToNom[s2].append(s1)
            self.SimpToCode[s2].append(self.Communes[k][0])
            
        self._code_n = []
        self._code_r = []
            
    #def end(self, logger):
    #    f = self.father.ToolsOpenFile("result-insee-nodes.txt", "w")
    #    for x in self.Communes.keys():
    #        if x not in self._code_n:
    #            f.write(x+"\n")
    #    f.close()
    #    f = self.father.ToolsOpenFile("result-insee-relations.txt", "w")
    #    for x in self.Communes.keys():
    #        if x not in self._code_r:
    #            f.write(x+"\n")
    #    f.close()
        
    def _insee(self, tags):
        err = []
        code_insee = tags[u"ref:INSEE"]
        if code_insee not in self.Communes:
            err.append((801, 0, {"en": code_insee}))
        elif tags[u"name"] <> self.Communes[code_insee][1]:
            if self.father.ToolsStripAccents(tags[u"name"].lower().replace(u"-", u" ").replace(u" ", u"")).strip() == self.father.ToolsStripAccents(self.Communes[code_insee][1].lower().replace(u"-", u" ").replace(u" ", u"")).strip():
                if (u"œ" in self.Communes[code_insee][1]) or (u"æ" in self.Communes[code_insee][1]) or (u"Œ" in self.Communes[code_insee][1]) or (u"Æ" in self.Communes[code_insee][1]):
                    pass # Pas de correction de ligature (ML talk-fr 03/2009)
                else:
                    e_fr = u"OSM=" + tags[u"name"] + u" => COG=<a href=http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/commune.asp?depcom="+code_insee+">" + self.Communes[code_insee][1] + "</a>"
                    e_en = e_fr
                    err.append((802, 1, {"fr":e_fr, "en":e_en}))
            else:
                e_fr = u"OSM=" + tags[u"name"] + u" => COG=<a href=http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/commune.asp?depcom="+code_insee+">" + self.Communes[code_insee][1] + "</a>"
                e_en = e_fr
                err.append((802, 2, {"fr":e_fr, "en":e_en}))
        return err

    def node(self, data, tags):
        if u"place" not in tags:
            return
        #if tags[u"place"] not in [u"town", u"city", u"village", u"hamlet"]:
        #    return
        if u"name" not in tags:
            return [(800, 0, {})]
        if u"ref:INSEE" not in tags:
            return
        self._code_n.append(tags[u"ref:INSEE"])
        return self._insee(tags)

    def relation(self, relation, tags):
        if tags.get(u"boundary") <> u"administrative":
            # Ce n'est pas une relation administrative
            return
        if tags.get(u"admin_level") <> u"8":
            # Seul le niveau 8 contient des INSEE qui nous interresse
            # Le niveau 7 contient d'autre code INSEE (sur 3 chiffres)
            return
        if u"name" not in tags:
            return [(800, 0, {})]
        if u"ref:INSEE" not in tags:
            return

#        self._code_r.append(tags[u"ref:INSEE"])

        return self._insee(tags)
