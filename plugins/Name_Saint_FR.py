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


class Name_Saint_FR(Plugin):

    only_for = ["FR", "NC"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3033] = self.def_class(item = 3033, level = 3, tags = ['name', 'fix:chair'],
            title = {'en': 'Saint'},
            detail = T_(
'''In France the rule is that a hyphen is used when we refer to a a holy
thing ("Saint-*" in French).'''),
            fix = T_(
'''Add a hyphen.'''),
            trap = T_(
'''This rule does not apply in particular to the Belgium.'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/0/08/Osmose-eg-error-3033.png)

Name should be the "Saint-Esprit".'''))

        import re
        self.Saint = re.compile(u".*((Sainte?) +).+")

    def node(self, data, tags):
        if tags.get("name") not in (None, "Saint Algue"):
            r = self.Saint.match(tags["name"])
            if r:
                return {"class": 3033, "subclass": 1, "text": T_(u"Missing hyphen after \"Saint(e)\""),
                         "fix": {"name": tags["name"].replace(r.group(1), "%s-" % r.group(2))}}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def setUp(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Saint_FR(None)
        self.p.init(None)

    def test(self):
        self.check_err(self.p.node(None, {"name": "Saint Pierre"}))
        self.check_err(self.p.way(None, {"name": "Sainte Julie"}, None))
        assert not self.p.relation(None, {"name": "Saint-Matthieu"}, None)
        assert not self.p.way(None, {"name": "Sainte-Sophie"}, None)
