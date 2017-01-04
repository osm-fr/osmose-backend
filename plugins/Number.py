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
        self.errors[3091] = { "item": 3091, "level": 2, "tag": ["value", "fix:chair"], "desc": T_(u"Numerical value") }
        self.tag_number = ["height", "maxheight", "maxheight:physical", "width", "maxwidth", "length", "maxlength", "maxweight", "maxspeed", "population", "admin_level", "ele"]
        self.Number = re.compile(u"^((?:[0-9]+(?:[.][0-9]+)?)|(?:[.][0-9]+))(?: ?(?:m|ft|cm|km|lbs|tons|t|T|mph|knots)|'(?:[0-9]*(?:[.][0-9]+)?\")?|\")?$")
        self.MaxspeedExtraValue = ["none", "default", "signals", "national", "no", "unposted", "walk", "urban", "variable"]
        self.MaxspeedClassValue = re.compile(u'^[A-Z]*:.*$')
        self.MaxheightExtraValue = ["default", "below_default", "no_indications", "no_sign", "none", "unsigned"]

    def node(self, data, tags):
        for i in self.tag_number:
            if i in tags:
                m = self.Number.match(tags[i])
                if (not m and
                    not (i == "width" and tags[i] == "narrow") and
                    not (i == "maxspeed" and (
                        tags[i] in self.MaxspeedExtraValue or
                        self.MaxspeedClassValue.match(tags[i]) or
                        (tags[i] == "implicit" and ("traffic_sign" in tags) and "maxspeed" in tags["traffic_sign"].split(";"))
                    )) and
                    not (i == "maxheight" and tags[i] in self.MaxheightExtraValue)
                ):
                    return {"class": 3091, "subclass": 1, "text": T_(u"Incorrect number \"%s\"", tags[i])}
                elif m and i=="height" and float(m.group(1)) > 500:
                    return {"class": 3091, "subclass": 2, "text": T_(u"height=%s is really tall, look at ele=*", m.group(1)),
                             "fix": {"-": ["height"], "+": {"ele": tags["height"]}} }
                elif m and i=="maxspeed" and float(m.group(1)) < 5 and not "waterway" in tags:
                    return {"class": 3091, "subclass": 3, "text": T_(u"%s is really slow", m.group(1))}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Number(None)
        a.init(None)
        for d in ["194", "14 m", "0.6m", "18ft", "1cm", "narrow", "8 km", "400m", "14ft", "10'", "10'11\"", "1'9.8\"", "1.18\""]:
            assert not a.node(None, {"width":d}), ("width='%s'" % d)

        for d in ["3,75", "foo", "18,4m", "4810"]:
            self.check_err(a.node(None, {"height":d}), ("height='%s'" % d))
            self.check_err(a.way(None, {"height":d}, None), ("height='%s'" % d))
            self.check_err(a.relation(None, {"height":d}, None), ("height='%s'" % d))

        for d in ["foo", "18kph", "1", "30 km/h", "30 c"]:
            self.check_err(a.node(None, {"maxspeed":d}), ("maxspeed='%s'" % d))

        for d in ["50", "FR:urban", "35 mph", "10 knots"]:
            assert not a.node(None, {"maxspeed":d}), ("maxspeed='%s'" % d)

        t = {"maxspeed":"1", "waterway": "river"}
        assert not a.node(None, {"maxspeed":"1", "waterway": "river"}), t

        assert not a.node(None, {"maxspeed": "implicit", "traffic_sign": "maxspeed"})
        assert not a.node(None, {"maxspeed": "default"})

        assert not a.node(None, {"maxheight": "default"})
