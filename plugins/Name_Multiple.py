#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Yoann Arnaud <yarnaud@crans.org> 2009                      ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
import re


class Name_Multiple(Plugin):

    not_for = ["ES-O", "ES-NA", "ES-BI", "ES-SS", "ES-VI"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[705] = self.def_class(item = 5030, level = 1, tags = ['name', 'fix:survey'],
            title = T_('The name tag contains two names'),
            detail = T_(
'''The tag `name=*` contains multiple names, separated by a semicolon,
a "/", a "\\" or a "+". This issue was probably produced by merging two
ways and the concatenation of the names of the streets.'''),
            fix = T_(
'''* If duplicate name, delete one.
* Otherwise, a survey is required: check if it is a street whose name
changes at a crossroads, if this is the case, split the street and set the
proper names of both parts.'''),
            trap = T_(
'''Some streets do not have the same name on both sides, especially if
the houses on one side are in a different city. In this case, you can use
the tag `name:left=*` and `name:right=*`.'''))
        self.errors[50301] = self.def_class(item = 5030, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Conflicting names'),
            detail = T_(
'''This is a street with different names on each side of the way, given by the keys `name:left` and `name:right`.
These names do not match with the value of `name`.
The tag `name` should have the value `name:right / name:left` or `name:left / name:right`.'''),
            trap = T_(
'''The warning also shows up if `name:left` or `name:right` is spelled incorrectly.'''))

        self.NoExtra = False
        self.HighwayOnly = False
        self.allowSlash = False

        if self.father.config.options.get("country"):
            self.NoExtra = any(map(lambda c: self.father.config.options.get("country").startswith(c), ['DE', 'US', 'CA']))

            self.HighwayOnly = self.father.config.options.get("country").startswith('BY')

            self.allowSlash = any(map(lambda c: self.father.config.options.get("country").startswith(c), ['CH', 'DJ', 'DK']))

        self.streetSubNumberRe = re.compile(u".*[0-9๐๑๒๓๔๕๖๗๘๙]/[0-9๐๑๒๓๔๕๖๗๘๙].*")

    def way(self, data, tags, nds):
        if u"name" not in tags:
            return
        if u"aeroway" in tags:
            return

        if ';' in tags["name"]:
            return {"class": 705, "subclass": 0, "text": {"en": "name={0}".format(tags["name"])}}

        if self.HighwayOnly and u"highway" not in tags:
            return
        if self.NoExtra:
            return

        if '+' in tags["name"][0:-1] and not 'P+R' in tags["name"]:
            return {"class": 705, "subclass": 2, "text": {"en": "name={0}".format(tags["name"])}}

        if '/' in tags["name"] and not self.allowSlash:
            # Accept / in bus and tram stop names
            if "public_transport" in tags and tags["public_transport"] in ["platform", "stop_position"]:
                return

            if "name:left" in tags and "name:right" in tags:
                # name:left and name:right may be combined in the regular name tag, separated by a /
                nameparts = [n.strip() for n in tags["name"].split("/")]
                if tags["name:left"] in nameparts and tags["name:right"] in nameparts and len(nameparts) == 2:
                    return
                elif tags["name:right"] != tags["name:left"]:
                    return {"class": 50301, "subclass": 1,
                            "fix": {"~": {"name": tags["name:right"] + " / " + tags["name:left"]}}}

            if not self.streetSubNumberRe.match(tags["name"]):
                return {"class": 705, "subclass": 1, "text": {"en": "name={0}".format(tags["name"])}}

###########################################################################
from plugins.Plugin import TestPluginCommon, with_options

class Test(TestPluginCommon):
    def test(self):
        TestPluginCommon.setUp(self)
        p = Name_Multiple(None)
        class _config:
            options = {"country": None}
        class father:
            config = _config()
        p.father = father()

        with with_options(p, {'country': 'TH'}):
            p.init(None)
            self.check_err(p.way(None, {"name": "aueuie ; ueuaeuie"}, None))
            self.check_err(p.way(None, {"name": "aueuie / ueuaeuie"}, None))
            self.check_err(p.way(None, {"name": "aueuie + ueuaeuie"}, None))
            assert not p.way(None, {"amenity": "aueuie + ueuaeuie"}, None)
            assert not p.way(None, {"name": "aueuie + ueuaeuie", "aeroway": "yes"}, None)
            assert not p.way(None, {"name": "Profil+"}, None)
            assert not p.way(None, {"name": u"บ้านแพะแม่คือ ซอย 5/10"}, None)
            assert not p.way(None, {"name": u"บ้านแพะแม่คือ ซอย 5/๓๔๕"}, None)
            assert not p.way(None, {"name": "streetA/streetB", "public_transport": "platform"}, None)
            assert not p.way(None, {"name": u"Gas station no. 21/2356"}, None)
            assert not p.way(None, {"name": "Foobar P+R"}, None)
            assert not p.way(None, {"name": "StreetA / StreetB", "name:left": "StreetA", "name:right": "StreetB"}, None)
            assert not p.way(None, {"name": "StreetB/StreetA", "name:left": "StreetA", "name:right": "StreetB"}, None)
            self.check_err(p.way(None, {"name": "StreetC/StreetA", "name:left": "StreetA", "name:right": "StreetB"}, None))

        with with_options(p, {'country': 'US-TX'}):
            p.init(None)
            assert not p.way(None, {"name": u"County Route 7/2"}, None)
            assert not p.way(None, {"name": u"16 5/10 Road"}, None)

        with with_options(p, {'country': 'BY'}):
            p.init(None)
            assert not p.way(None, {"name": u"д/с №68"}, None)
            assert p.way(None, {"name": u"д/с №68", "highway": "terciary"}, None)

        with with_options(p, {'country': 'CH'}):
            p.init(None)
            assert not p.way(None, {"name": u"Waffenplatz-/Bederstrasse"}, None)

        with with_options(p, {'country': 'DJ'}):
            p.init(None)
            assert not p.way(None, {"name": u"Avenue 17 / جادة 17"}, None)
