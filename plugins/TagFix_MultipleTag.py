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


class TagFix_MultipleTag(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30320] = { "item": 3032, "level": 1, "tag": ["tag", "highway", "fix:chair"], "desc": {"en": u"Watch multiple tags"} }
        self.errors[30323] = { "item": 3032, "level": 3, "tag": ["tag", "fix:chair"], "desc": {"en": u"Watch multiple tags"} }
        self.errors[20800] = { "item": 2080, "level": 1, "tag": ["tag", "highway", "roundabout", "fix:chair"], "desc": {"en": u"Tag highway missing on junction=roundabout", "fr": u"Tag highway manquant sur junction=roundabout"} }
        self.errors[20801] = { "item": 2080, "level": 1, "tag": ["tag", "highway", "fix:chair"], "desc": {"en": u"Tag highway missing on oneway", "fr": u"Tag highway manquant sur sens unique"} }
        self.errors[20301] = { "item": 2030, "level": 1, "tag": ["tag", "highway", "cycleway", "fix:survey"], "desc": {"en": u"Opposite cycleway without oneway", "fr": u"Contre sens cyclable sans sens unique"} }
        self.errors[71301] = { "item": 7130, "level": 3, "tag": ["tag", "highway", "maxheight", "fix:survey"], "desc": {"en": u"Mising maxheight tag", "fr": u"Manque le tag maxheight"} }
        self.errors[1050] = { "item": 1050, "level": 1, "tag": ["highway", "roundabout", "fix:chair"], "desc": {"fr":"Rond-point à l'envers", "en":"Reverse roundabout"} }
#        self.errors[70401] = { "item": 7040, "level": 2, "tag": ["tag", "power", "fix:chair"], "desc": {"en": u"Bad power line kind", "fr": u"Mauvais type de ligne"} }
        self.driving_side_right = not(self.father.config.options.get("driving_side") == "left")
        self.driving_direction = "anticlockwise" if self.driving_side_right else "clockwise"

    def node(self, data, tags):
        err = []
        if "highway" in tags and tags["highway"] == "mini_roundabout" and "direction" in tags:
            clockwise = tags["direction"] == "clockwise"
            anticlockwise = tags["direction"] in ["anticlockwise", "anti_clockwise"]
            if (self.driving_side_right and clockwise) or (not self.driving_side_right and anticlockwise):
                err.append((1050, 1000, {"en": u"Standard mini roundabout direction on country is \"%s\"" % self.driving_direction, "fr": u"Le sens des minis giratoires sur le pays est normalement \"%s\"" % self.driving_direction, "fix": {"-": ["direction"]}}))
            if (self.driving_side_right and anticlockwise) or (not self.driving_side_right and clockwise):
                err.append((1050, 1001, {"en": u"Mini roundabout direction on country is \"%s\" by default, useless direction tag" % self.driving_direction, "fr": u"Le sens des minis giratoires est par défaut \"%s\", tag direction inutile" % self.driving_direction, "fix": {"-": ["direction"]}}))

        return err

    def way(self, data, tags, nds):
        err = []
        if "highway" in tags and "fee" in tags:
            err.append((30320, 1000, {"en": u"Use tags \"toll\" in place of \"fee\"", "fr": u"Utiliser \"toll\" à la place de \"fee\"", "fix": {"-": ["fee"], "+": {"toll": tags["fee"]}} }))

        if u"junction" in tags and u"highway" not in tags:
            err.append((20800, 0, {}))

        if u"oneway" in tags and not (u"highway" in tags or u"railway" in tags or u"aerialway" in tags or u"waterway" in tags or u"aeroway" in tags):
            err.append((20801, 0, {}))

        if "area" in tags and tags["area"] == "yes" and not "barrier" in tags and not "highway" in tags:
            err.append((30323, 1001, {"en": u"Bad usage of area=yes", "fr": u"Mauvais usage de area=yes"}))
        if "area" in tags and tags["area"] == "no" and not "aeroway" in tags and not "building" in tags and not "landuse" in tags and not "leisure" in tags and not "natural":
            err.append((30323, 1002, {"en": u"Bad usage of area=no", "fr": u"Mauvais usage de area=no"}))

        if "highway" in tags and "cycleway" in tags and tags["cycleway"] in ("opposite", "opposite_lane") and ("oneway" not in tags or ("oneway" in tags and tags["oneway"] == "no")):
            err.append((20301, 0, {}))

        if "highway" in tags and tags["highway"] in ("motorway_link", "trunk_link", "primary", "primary_link", "secondary", "secondary_link") and not "maxheight" in tags and not "maxheight:physical" in tags and (("tunnel" in tags and tags["tunnel"] != "no") or ("covered" in tags and tags["covered"] != "no")):
            err.append((71301, 0, {}))

#        if "power" in tags and tags["power"] in ("line", "minor_line") and "voltage" in tags:
#            voltage = map(int, filter(lambda x: x.isdigit(), map(lambda x: x.strip(), tags["voltage"].split(";"))))
#            if voltage:
#                voltage = max(voltage)
#                print voltage
#                if voltage > 45000 and tags["power"] == "minor_line":
#                    err.append((70401, 0, {"fix": {"~": {"power": "line"}}}))
#                elif voltage <= 45000 and tags["power"] == "line":
#                    err.append((70401, 1, {"fix": {"~": {"power": "minor_line"}}}))

        return err


if __name__ == "__main__":
    a = TagFix_MultipleTag(None)
    class config:
        options = {}
    class father:
        config = config()
    a.father = father()
    a.init(None)
    for d in ["clockwise", "anticlockwise"]:
        if not a.node(None, {"highway":"mini_roundabout", "direction":d}):
            print "nofail: %s" % d
    a.father.config.options["driving_side"] = "left"
    for d in ["clockwise", "anticlockwise"]:
        if not a.node(None, {"highway":"mini_roundabout", "direction":d}):
            print "nofail: %s" % d
    if not a.way(None, {"highway":"", "cycleway": "opposite"}, None):
        print "fail"
    if a.way(None, {"highway":"", "cycleway": "opposite", "oneway": "yes"}, None):
        print "fail"
    if not a.way(None, {"highway":"primary", "tunnel": "yes"}, None):
        print "fail3"
#    if not a.way(None, {"power":"line", "voltage": "1"}, None):
#        print "fail4"
