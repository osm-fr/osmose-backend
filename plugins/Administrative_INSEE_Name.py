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


class Administrative_INSEE_Name(Plugin):

    only_for = ["FR", "NC"]

    def init(self, logger):
        """
        Chargement du dictionnaires des noms de communes de l'INSEE
        """
        Plugin.init(self, logger)
        self.errors[800] = { "item": 6030, "level": 1, "tag": ["place", "fix:survey"], "desc": T_(u"Place node without name tag") }
        self.errors[801] = { "item": 6040, "level": 1, "tag": ["place", "fix:chair"], "desc": T_(u"INSEE code cannot be found in INSEE database") }
        self.errors[802] = { "item": 6040, "level": 1, "tag": ["place", "fix:chair"], "desc": T_(u"Municipality name does not match INSEE code") }

        lst = self.father.ToolsReadList("dictionnaires/BddCommunes")
        self.communeNameIndexedByInsee = {}

        for x in lst:
            x = x.split("\t")
            code_insee = x[0]
            name_insee = x[1]
            self.communeNameIndexedByInsee[code_insee] = name_insee

    def _check_insee_name(self, code_insee, name_osm, name_alt_osm):

        if code_insee not in self.communeNameIndexedByInsee:
            # Le code INSEE n'est pas connus
            return [(801, 0, {"en": code_insee})]

        name_insee = self.communeNameIndexedByInsee[code_insee]
        if name_osm != name_insee and (not name_alt_osm or name_alt_osm != name_insee):
            simpleName = self.ToolsStripAccents(name_osm.lower().replace(u"-", u" ").replace(u" ", u"")).strip()
            simpleInseeName = self.ToolsStripAccents(name_insee.lower().replace(u"-", u" ").replace(u" ", u"")).strip()
            msg = u"OSM=" + name_osm + u" => COG=" + name_insee
            fix = {"name": name_insee}
            if simpleName == simpleInseeName:
                if ((u"œ" in name_insee) or (u"æ" in name_insee) or
                     (u"Œ" in name_insee) or (u"Æ" in name_insee)):
                    pass # Pas de correction de ligature (ML talk-fr 03/2009)
                else:
                    return [(802, 1, {"en":msg, "fix":{"~":fix}})]
            else:
                return [(802, 2, {"en":msg, "fix":fix})]

    def node(self, data, tags):
        if u"place" in tags:
            if u"name" not in tags:
                # Le nom est obligatoire en complément du tag place.
                return [(800, 0, {"en": u"Node with place=%s without name" % tags[u"place"], "fr": u"Nœud avec place=%s sans name" % tags[u"place"]})]
            if u"ref:INSEE" in tags:
                # Si en plus on a un ref:Insee, on verifie la coohérance des noms
                return self._check_insee_name(tags[u"ref:INSEE"], tags[u"name"], tags[u"alt_name"] if u"alt_name" in tags else None)

    def relation(self, relation, tags, members):
        if tags.get(u"boundary") == u"administrative" and tags.get(u"admin_level") == u"8":
            # Seul le niveau 8 contient des INSEE qui nous interresse
            # Le niveau 7 contient d'autre code INSEE (sur 3 chiffres)

            if u"name" not in tags:
                # Le nom est obligatoire en complément du tag place.
                return [(800, 0, {})]

            if u"ref:INSEE" in tags:
                # Si en plus on a un ref:Insee, on verifie la coohérance des noms
                return self._check_insee_name(tags[u"ref:INSEE"], tags[u"name"], tags[u"alt_name"] if u"alt_name" in tags else None)
