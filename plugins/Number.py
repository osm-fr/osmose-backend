#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

class Number(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3091] = { "item": 3091, "level": 2, "tag": ["value", "fix:chair"], "desc": {"en": u"Number value", "fr": u"Valeur numérique"} }
        self.tag_number = ["height", "maxheight", "maxheight:physical", "width", "maxwidth", "length", "maxlength", "maxweight", "maxspeed", "population"]
        self.Number = re.compile(u"^((?:[0-9]+(?:[.][0-9]+)?)|(?:[.][0-9]+))(?: ?(?:m|ft|cm|km|lbs|tons|t|T|mph))?$")
        self.MaxspeedExtraValue = ["none", "signals", "national", "no", "unposted", "walk", "urban", "variable"]
        self.MaxspeedClassValue = re.compile(u'^[A-Z]*:.*$')

    def node(self, data, tags):
        for i in self.tag_number:
            if i in tags:
                m = self.Number.match(tags[i])
                if not m and not (i=="width" and tags[i]=="narrow") and not (i=="maxspeed" and (tags[i] in self.MaxspeedExtraValue or self.MaxspeedClassValue.match(tags[i]))):
                    return [(3091, 1, {"fr": u"Nombre \"%s\" incorrect" % tags[i], "en": u"Bad number \"%s\"" % tags[i]})]
                elif m and i=="height" and float(m.group(1)) > 500:
                    return [(3091, 2, {"fr": u"C'est très haut %s, voir ele=*" % m.group(1), "en": u"%s is really tall, look at ele=*" % m.group(1), "fix": {"-": ["height"], "+": {"ele": tags["height"]}} })]
                elif m and i=="maxspeed" and float(m.group(1)) < 5 and not "waterway" in tags:
                    return [(3091, 3, {"fr": u"C'est très lent %s" % m.group(1), "en": u"%s is really slow" % m.group(1)})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


if __name__ == "__main__":
    import re
    a = Number(None)
    a.init(None)
    for d in ["194", "14 m", "0.6m", "18ft", "1cm", "narrow", "8 km", "400m", "14ft"]:
        if a.node(None, {"width":d}):
            print "fail: %s" % d
    for d in ["3,75", "foo", "18,4m", "4810"]:
        if not a.node(None, {"height":d}):
            print "nofail: %s" % d
    for d in ["foo", "18kph", "1"]:
        if not a.node(None, {"maxspeed":d}):
            print "nofail: %s" % d
    for d in ["50", "FR:urban"]:
        if a.node(None, {"maxspeed":d}):
            print "fail: %s" % d
    if not a.node(None, {"maxspeed":"1"}):
        print "fail maxspped"
    if a.node(None, {"maxspeed":"1", "waterway": "river"}):
        print "fail maxspped+waterway"
