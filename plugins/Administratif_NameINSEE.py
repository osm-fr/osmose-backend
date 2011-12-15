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


class Administratif_NameINSEE(Plugin):
    
    only_for = ["FR"]


    def init(self, logger):
        """
        Chargement du dictionnaires des noms de communes de l'INSEE
        """
        Plugin.init(self, logger)
        self.errors[800] = { "item": 6030, "desc": {"en": u"Node place without name tag", "fr": u"Node place sans tag name"} }
        self.errors[801] = { "item": 6040, "desc": {"en": u"INSEE code cannot be found in INSEE database", "fr": u"Le code INSEE est introuvable dans la Base de l'INSEE"} }
        self.errors[802] = { "item": 6040, "desc": {"en": u"Municipality name does not correspond to INSEE code", "fr": u"Le nom de commune ne correspond pas au code INSEE"} }

        lst = self.father.ToolsReadList("dictionnaires/BddCommunes")
        self.communeNameIndexedByInsee = {}

        for x in lst:
            x = x.split("\t")
            code_insee = x[0]
            name_insee = x[1]
            self.communeNameIndexedByInsee[code_insee] = name_insee
    
    
    def _check_insee_name(self, code_insee, name_osm):
        
        if code_insee not in self.communeNameIndexedByInsee:
            # Le code INSEE n'est pas connus
            return [(801, 0, {"en": code_insee})]
            
        name_insee = self.communeNameIndexedByInsee[code_insee]    
        if name_osm <> name_insee:
            simpleName = self.father.ToolsStripAccents(name_osm.lower().replace(u"-", u" ").replace(u" ", u"")).strip()
            simpleInseeName = self.father.ToolsStripAccents(name_insee.lower().replace(u"-", u" ").replace(u" ", u"")).strip()
            msg = u"OSM=" + name_osm + u" => COG=<a href=http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/commune.asp?depcom="+code_insee+">" + name_insee + "</a>"
            if simpleName == simpleInseeName:
                if ((u"œ" in name_insee) or (u"æ" in name_insee) or
                     (u"Œ" in name_insee) or (u"Æ" in name_insee)):
                    pass # Pas de correction de ligature (ML talk-fr 03/2009)
                else:
                    return [(802, 1, {"en":msg})]
                
            else:
                return [(802, 2, {"en":msg})]
        
    def node(self, data, tags):
        if u"place" in tags:
            
            if u"name" not in tags:
                # Le nom est obligatoire en complément du tag place.
                return [(800, 0, {})]
        
            if u"ref:INSEE" in tags:
                # Si en plus on a un ref:Insee, on verifie la coohérance des noms
                return self._check_insee_name(tags[u"ref:INSEE"], tags[u"name"])

    def relation(self, relation, tags, members):
        if tags.get(u"boundary") == u"administrative" and tags.get(u"admin_level") == u"8":
            # Seul le niveau 8 contient des INSEE qui nous interresse
            # Le niveau 7 contient d'autre code INSEE (sur 3 chiffres)
            
            if u"name" not in tags:
                # Le nom est obligatoire en complément du tag place.
                return [(800, 0, {})]
            
            if u"ref:INSEE" in tags:
                # Si en plus on a un ref:Insee, on verifie la coohérance des noms
                return self._check_insee_name(tags[u"ref:INSEE"], tags[u"name"])
