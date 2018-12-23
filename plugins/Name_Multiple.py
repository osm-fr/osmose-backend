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

from plugins.Plugin import Plugin
import re


class Name_Multiple(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[705] = { "item": 5030, "level": 1, "tag": ["name", "fix:survey"], "desc": T_(u"The name tag contains two names") }

        self.NoExtra = False
        self.HighwayOnly = False
        self.streetSubNumber = False
        self.allowSlash = False
        if self.father.config.options.get("country"):
            self.NoExtra = any(map(lambda c: self.father.config.options.get("country").startswith(c), ['DE', 'US', 'CA']))

            self.HighwayOnly = self.father.config.options.get("country").startswith('BY')

            # In Thailand street added into existing street are named like "บ้านแพะแม่คือ ซอย 5/1"
            self.streetSubNumber = any(map(lambda c: self.father.config.options.get("country").startswith(c), ['TH', 'VN', 'MY']))

            self.allowSlash = any(map(lambda c: self.father.config.options.get("country").startswith(c), ['CH', 'DJ']))

        self.streetSubNumberRe = re.compile(u".*[0-9๐๑๒๓๔๕๖๗๘๙]/[0-9๐๑๒๓๔๕๖๗๘๙].*")

    def way(self, data, tags, nds):
        if u"name" not in tags:
            return
        if u"aeroway" in tags:
            return

        if ';' in tags["name"]:
            return {"class": 705, "subclass": 0, "text": {"en": "name=%s" % tags["name"]}}

        if self.HighwayOnly and u"highway" not in tags:
            return
        if self.NoExtra:
            return

        if not self.allowSlash and '/' in tags["name"] and not (self.streetSubNumber and self.streetSubNumberRe.match(tags["name"])):
            return {"class": 705, "subclass": 1, "text": {"en": "name=%s" % tags["name"]}}
        if '+' in tags["name"][0:-1]:
            return {"class": 705, "subclass": 2, "text": {"en": "name=%s" % tags["name"]}}

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
