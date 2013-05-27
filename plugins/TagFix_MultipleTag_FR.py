#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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


class TagFix_MultipleTag_FR(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30321] = { "item": 3032, "level": 1, "tag": ["tag"], "desc": {"en": u"Watch multiple tags"} }
        self.errors[50201] = { "item": 5020, "level": 2, "tag": ["tag", "name"], "desc": {"fr": u"Nom à améliorer depuis le cadastre"} }
        self.errors[30324] = { "item": 3032, "level": 2, "tag": ["highway", "maxspeed"], "desc": {"fr": u"maxspeed incohérent", "en": u"incoherent maxspeed"} }
        self.errors[30325] = { "item": 3032, "level": 2, "tag": ["highway", "ref"], "desc": {"fr": u"Référence invalide", "en": u"Invalid reference"} }

        self.school = {
            "elementaire": "élémentaire",
            "maternelle": "maternelle",
            "primaire": "primaire",
            "college": "collège",
            "lycee": "lycée",
            "secondaire": "secondaire",
        }
        self.Ref = re.compile(r"^([ANDMC]|RN|RD|VC|CR|CE)[-\s]?[0-9]?", re.IGNORECASE)

    def node(self, data, tags):
        err = []

        if "school:FR" in tags and "amenity" not in tags:
            err.append((30321, 5, {"fr": u"Il faut un tag amenity=nursery|kindergarten|school en plus de school:FR"}))

        if "amenity" in tags:
            if tags["amenity"] == "school" and "school:FR" not in tags:
                canonicalSchool = self.father.ToolsStripAccents(tags['name']).lower()
                for s in self.school:
                    if s in canonicalSchool:
                        err.append((30321, 6, {"fr": u"Ajouter le tag school:FR", "fix": {"+": {"school:FR": self.school[s]}}}))
                        break

        if "name" in tags and tags["name"].startswith("Chemin Rural dit "):
            err.append((50201, 0, {"fix": {"~": {"name": tags["name"].replace("Chemin Rural dit ", "Chemin ")}}}))

        if "highway" in tags:
            if tags["highway"] == "living_street" and "zone:maxspeed" in tags and tags["zone:maxspeed"] != "FR:20":
                err.append((30324, 0, {"fr": "Un living_street en France est une Zone 20"}))
            elif "zone:maxspeed" in tags and tags["zone:maxspeed"] == "FR:20" and tags["highway"] != "living_street":
                err.append((30324, 1, {"fr": "Une Zone 20 en France est un living_street"}))
            elif "zone:maxspeed" in tags and "maxspeed" in tags:
                if tags["zone:maxspeed"] == "FR:20" and tags["maxspeed"] != "20":
                    err.append((30324, 3, {"fr": "Une Zone 20 est limité à 20 km/h"}))
                elif tags["zone:maxspeed"] == "FR:30" and tags["maxspeed"] != "30":
                    err.append((30324, 4, {"fr": "Une Zone 30 est limité à 30 km/h"}))

        if "highway" in tags and "ref" in tags and not self.Ref.match(tags["ref"]):
            err.append((30325, 4, {"en": tags["ref"]}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

if __name__ == "__main__":
    a = TagFix_MultipleTag_FR(None)
    a.init(None)
    if not a.node(None, {"amenity":"school", "name":"École maternelle Clos Montesquieu"}):
        print "nofail 1"
    if not a.node(None, {"name":"Chemin Rural dit de la Borne Trouée"}):
        print "nofail 2"
    if not a.node(None, {"highway":"e", "ref": "3"}):
        print "nofail 3"
    if a.node(None, {"highway":"e", "ref": u"D\u20073"}):
        print "fail 4"
