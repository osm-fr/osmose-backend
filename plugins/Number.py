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

class Number(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3091] = { "item": 3091, "desc": {"en": u"Number value", "fr": u"Valuer numérique"} }
        self.tag_number = ["height", "maxheight", "width", "maxwidth", "length", "maxlength", "maxweight"]
        self.Number = re.compile(u"^((?:[0-9]+(?:[.][0-9]+)?)|(?:[.][0-9]+))(?: ?(?:m|ft|cm|km|lbs|tons|t|T))?$")

    def node(self, data, tags):
        for i in self.tag_number:
            if i in tags:
                m = self.Number.match(tags[i])
                if not m and not (i=="width" and tags[i]=="narrow"):
                    return (3091, 1, {"fr": u"Nombre \"%s\" incorrecte" % tags[i], "en": u"Bad number \"%s\"" % tags[i]})
                elif m and i=="height" and float(m.group(1)) > 500:
                    return (3091, 2, {"fr": u"C'est très haut, voir ele=*", "en": u"Really tall, look at ele=*"})

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
