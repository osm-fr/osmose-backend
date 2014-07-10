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

    only_for = ["FR", "NC"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30321] = { "item": 3032, "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Watch multiple tags") }
        self.errors[50201] = { "item": 5020, "level": 2, "tag": ["tag", "name", "fix:chair"], "desc": T_(u"Improve name from the land registry") }
        self.errors[30324] = { "item": 3032, "level": 2, "tag": ["highway", "maxspeed", "fix:survey"], "desc": T_(u"incoherent maxspeed") }
        self.errors[30325] = { "item": 3032, "level": 2, "tag": ["highway", "ref", "fix:chair"], "desc": T_(u"Invalid reference") }
        self.errors[30326] = { "item": 2100, "level": 3, "tag": ["fix:chair"], "desc": T_(u"In France all pharmacies deliver drungs under prescription") }
        self.errors[13] = { "item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"FANTOIR object type not match OSM feature") }

        self.school = {
            u"elementaire": u"élémentaire",
            u"maternelle": u"maternelle",
            u"primaire": u"primaire",
            u"college": u"collège",
            u"lycee": u"lycée",
            u"secondaire": u"secondaire",
        }
        country = self.father.config.options.get("country")
        if country == "NC":
            self.Ref = re.compile(r"^(RT|RP|VU|VE|VDE|RPN|RM|CR)[-\s]?[0-9]?", re.IGNORECASE)
        else: # "FR"
            self.Ref = re.compile(r"^([ANDMCVR]|RN|RD|VC|CR|CE)[-\s]?[0-9]?", re.IGNORECASE)

    def node(self, data, tags):
        err = []

        if "school:FR" in tags and "amenity" not in tags:
            err.append((30321, 5, {"en": u"Need tag amenity=nursery|kindergarten|school besides on school:FR", "fr": u"Il faut un tag amenity=nursery|kindergarten|school en plus de school:FR"}))
        if "name" in tags and "amenity" in tags and tags["amenity"] == "school" and "school:FR" not in tags:
            canonicalSchool = self.ToolsStripAccents(tags['name']).lower()
            for s in self.school:
                if s in canonicalSchool:
                    err.append((30321, 6, {"en": u"Add school:FR tag", "fr": u"Ajouter le tag school:FR", "fix": {"+": {"school:FR": self.school[s]}}}))
                    break

        if "amenity" in tags and tags["amenity"] == "pharmacy" and (not "dispensing" in tags or tags["dispensing"] != "yes"):
            err.append((30326, 7, {"fix": [{"+": {"dispensing": "yes"}}, {"-": ["amenity"], "+": {"shop": "chemist"}}]}))

        if not "addr:housenumber" in tags and "ref:FR:FANTOIR" in tags and len(tags["ref:FR:FANTOIR"]) == 10:
            fantoir_key = tags["ref:FR:FANTOIR"][5]
            if fantoir_key.isdigit():
                if not ("type" in tags and tags["type"] == "associatedStreet") and not ("highway" in tags):
                    err.append((13, 1, {"en": u"FANTOIR numeric type is for ways"}))
            #elif fantoir_key == "A":
            elif fantoir_key >= "B" and fantoir_key <= "W":
                if not ("place" in tags and tags["place"] in ("locality", "hamlet", "isolated_dwelling")):
                    err.append((13, 1, {"en": u"FANTOIR B to W type is for locality, hamlet or isolated_dwelling"}))

        return err

    def way(self, data, tags, nds):
        err = self.node(data, tags)

        if "name" in tags and tags["name"].startswith("Chemin Rural dit "):
            err.append((50201, 0, {"fix": {"~": {"name": tags["name"].replace("Chemin Rural dit ", "Chemin ")}}}))

        if "highway" in tags:
            if tags["highway"] == "living_street" and "zone:maxspeed" in tags and tags["zone:maxspeed"] != "FR:20":
                err.append((30324, 0, {"en": u"A living_street in France is a Zone 20", "fr": u"Un living_street en France est une Zone 20"}))
            elif "zone:maxspeed" in tags and tags["zone:maxspeed"] == "FR:20" and tags["highway"] != "living_street":
                err.append((30324, 1, {"en": u"A Zone 20 in France is a living_street", "fr": u"Une Zone 20 en France est un living_street"}))
            elif "zone:maxspeed" in tags and "maxspeed" in tags:
                if tags["zone:maxspeed"] == "FR:20" and tags["maxspeed"] != "20":
                    err.append((30324, 3, {"en": u"A Zone 20 is limited to 20 km/h", "fr": u"Une Zone 20 est limité à 20 km/h"}))
                elif tags["zone:maxspeed"] == "FR:30" and tags["maxspeed"] != "30":
                    err.append((30324, 4, {"en": u"A zone 30 is limited to 30 km/h", "fr": u"Une Zone 30 est limité à 30 km/h"}))

        if ("highway" in tags and
            tags["highway"] in ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "path", "track", "service", "footway", "pedestrian", "cycleway", "road", "bridleway"] and
            "ref" in tags and not self.Ref.match(tags["ref"])):
            err.append((30325, 4, {"en": tags["ref"]}))

        return err

    def relation(self, data, tags, members):
        return self.way(data, tags, None)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_MultipleTag_FR(None)
        class _config:
            options = {"country": "FR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for t in [{"amenity":"school", "name":u"École maternelle Clos Montesquieu"},
                  {"amenity":"school", "name":u"École élémentaire"},
                  {"name":u"Chemin Rural dit de la Borne Trouée"},
                  {"highway":"living_street", "zone:maxspeed": "30"},
                  {"highway":"primary", "zone:maxspeed": "FR:20"},
                  {"highway":"primary", "zone:maxspeed": "FR:30", "maxspeed": "70"},
                  {"highway":"living_street", "zone:maxspeed": "FR:20", "maxspeed": "30"},
                  {"highway":"trunk", "ref": "3"},
                  {"amenity":"pharmacy"},
                  {"ref:FR:FANTOIR":"90123D123D", "highway": "residential"},
                 ]:
            self.check_err(a.way(None, t, None), t)

        for t in [{"highway":"trunk", "ref": u"D\u20073"},
                  {"highway":"primary", "zone:maxspeed": "FR:50"},
                  {"highway":"primary", "zone:maxspeed": "FR:30", "maxspeed": "30"},
                  {"highway":"living_street"},
                  {"highway":"living_street", "zone:maxspeed": "FR:20", "maxspeed": "20"},
                  {"ref:FR:FANTOIR":"90123D123D", "place": "hamlet"},
                  {"ref:FR:FANTOIR":"330633955T", "type": "associatedStreet"},
                 ]:
            assert not a.way(None, t, None), t
