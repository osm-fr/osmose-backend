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
        self.errors[30326] = { "item": 2100, "level": 3, "tag": ["fix:chair"], "desc": T_(u"In France all pharmacies deliver drugs under prescription") }
        self.errors[206013] = { "item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"FANTOIR object type not match OSM feature") }

        self.school = {
            u"elementaire": u"élémentaire",
            u"maternelle": u"maternelle",
            u"primaire": u"primaire",
            u"college": u"collège",
            u"lycee": u"lycée",
            u"secondaire": u"secondaire",
        }
        country = self.father.config.options.get("country")
        if country and country.startswith("NC"):
            self.Ref = re.compile(r"^(RT|RP|VU|VE|VDE|RPN|RM|CR)[-\s]?[0-9]?", re.IGNORECASE)
        else: # "FR"
            self.Ref = re.compile(r"^([ANDMCVR]|RN|RD|VC|CR|CE|EV|V)[-\s]?[0-9]?", re.IGNORECASE)

    def node(self, data, tags, is_node = True):
        err = []

        if "school:FR" in tags and "amenity" not in tags:
            err.append({"class": 30321, "subclass": 5, "text": T_(u"Need tag amenity=nursery|kindergarten|school besides on school:FR")})
        if "name" in tags and tags.get("amenity") == "school" and "school:FR" not in tags:
            canonicalSchool = self.ToolsStripAccents(tags['name']).lower()
            matches = list(filter(lambda kv: kv[0] in canonicalSchool, self.school.keys()))
            if len(matches) == 1:
                err.append({"class": 30321, "subclass": 6, "text": T_(u"Add school:FR tag"), "fix": {"+": {"school:FR": self.school[matches[0]]}} })
            elif len(matches) > 1:
                err.append({"class": 30321, "subclass": 6, "text": T_(u"Add school:FR tag") })

        if tags.get("amenity") == "pharmacy" and tags.get("dispensing") != "yes":
            err.append({"class": 30326, "subclass": 7, "fix": [{"+": {"dispensing": "yes"}}, {"-": ["amenity"], "+": {"shop": "chemist"}}]})

        if not "addr:housenumber" in tags and "ref:FR:FANTOIR" in tags and len(tags["ref:FR:FANTOIR"]) == 10:
            fantoir_key = tags["ref:FR:FANTOIR"][5]
            if fantoir_key.isdigit():
                if is_node and "highway" not in tags:
                    err.append({"class": 206013, "subclass": 1, "text": T_(u"FANTOIR numeric type is for ways")})
            #elif fantoir_key == "A":
            elif fantoir_key >= "B" and fantoir_key <= "W":
                if tags.get("place") not in ("locality", "hamlet", "isolated_dwelling", "neighbourhood", "islet") and tags.get("railway") != "station" and tags.get("leisure") not in ("park", "garden"):
                    err.append({"class": 206013, "subclass": 1, "text": T_(u"FANTOIR B to W type is for locality, hamlet, isolated_dwelling, islet or neighbourhood")})

        return err

    def way(self, data, tags, nds):
        err = self.node(data, tags, is_node = False)

        if "name" in tags and tags["name"].startswith("Chemin Rural dit "):
            err.append({"class": 50201, "subclass": 0, "fix": {"~": {"name": tags["name"].replace("Chemin Rural dit ", "Chemin ")}}})

        if "highway" in tags:
            if tags["highway"] == "living_street" and tags.get("zone:maxspeed") not in (None, "FR:20"):
                err.append({"class": 30324, "subclass": 0, "text": T_(u"A living_street in France is a Zone 20")})
            elif tags.get("zone:maxspeed") == "FR:20" and tags["highway"] != "living_street":
                err.append({"class": 30324, "subclass": 1, "text": T_(u"A Zone 20 in France is a living_street")})
            elif "zone:maxspeed" in tags and "maxspeed" in tags:
                if tags["zone:maxspeed"] == "FR:20" and tags["maxspeed"] != "20":
                    err.append({"class": 30324, "subclass": 3, "text": T_(u"A Zone 20 is limited to 20 km/h")})
                elif tags["zone:maxspeed"] == "FR:30" and tags["maxspeed"] != "30":
                    err.append({"class": 30324, "subclass": 4, "text": T_(u"A zone 30 is limited to 30 km/h")})

        if (tags.get("highway") in ("motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "path", "track", "service", "footway", "pedestrian", "cycleway", "road", "bridleway") and
            "ref" in tags and not self.Ref.match(tags["ref"])):
            err.append({"class": 30325, "subclass": 4, "text": {"en": tags["ref"]}})

        return err

    def relation(self, data, tags, members):
        return self.way(data, tags, None)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_FR(self):
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
            self.check_err(a.relation(None, t, None), t)

        for t in [{"highway":"trunk", "ref": u"D\u20073"},
                  {"highway":"primary", "zone:maxspeed": "FR:50"},
                  {"highway":"primary", "zone:maxspeed": "FR:30", "maxspeed": "30"},
                  {"highway":"living_street"},
                  {"highway":"living_street", "zone:maxspeed": "FR:20", "maxspeed": "20"},
                  {"ref:FR:FANTOIR":"901230123D", "highway": "residential"},
                  {"ref:FR:FANTOIR":"90123D123D", "place": "hamlet"},
                  {"ref:FR:FANTOIR":"330633955T", "type": "associatedStreet"},
                  {"ref:FR:FANTOIR":"75116S566F", "railway": "station"},
                  {"ref:FR:FANTOIR":"75116S566F", "leisure": "park"},
                  {"ref:FR:FANTOIR":"75116S566F", "leisure": "garden"},
                  {"ref:FR:FANTOIR":"751084356J", "leisure": "garden"},
                 ]:
            assert not a.way(None, t, None), t

    def test_NC(self):
        a = TagFix_MultipleTag_FR(None)
        class _config:
            options = {"country": "NC"}
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
                  {"highway":"trunk", "ref": u"D\u20073"},
                  {"school:FR":"maternelle", "ref": u"1989898"},
                 ]:
            self.check_err(a.way(None, t, None), t)

        for t in [{"highway":"trunk", "ref": u"RPN 73"},
                  {"highway":"primary", "zone:maxspeed": "FR:50"},
                  {"highway":"primary", "zone:maxspeed": "FR:30", "maxspeed": "30"},
                  {"highway":"living_street"},
                  {"highway":"living_street", "zone:maxspeed": "FR:20", "maxspeed": "20"},
                  {"ref:FR:FANTOIR":"90123D123D", "place": "hamlet"},
                  {"ref:FR:FANTOIR":"330633955T", "type": "associatedStreet"},
                 ]:
            assert not a.way(None, t, None), t
