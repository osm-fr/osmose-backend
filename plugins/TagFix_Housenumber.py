#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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


class TagFix_Housenumber(Plugin):

    not_for = ("RU", "BG")

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[10] = {"item": 2060, "level": 3, "tag": ["addr", "fix:survey"], "desc": T_(u"addr:housenumber does not start by a number")}
        self.errors[14] = {"item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Invalid tag on interpolation way")}
        self.errors[15] = {"item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Invalid addr:interpolation or addr:inclusion value")}
        self.Country = self.father.config.options.get("country")
        import re
        from collections import defaultdict

        # By default, validate that house number starts with 1-9
        housenumberRegexByCountry = defaultdict(re.compile("^[1-9]"))

        # More specific rules by country

        # From open data from cantons Zurich and Bern. See also https://github.com/ltog/osmi-addresses/issues/93
        housenumberRegexByCountry["CH"] = re.compile("^[1-9][0-9]{0,3}( ?[a-zA-Z])?$")

        # https://wiki.openstreetmap.org/wiki/Cs:WikiProject_Czech_Republic/Address_system
        housenumberRegexByCountry["CZ"] = re.compile("^(ev\.)?[1-9]")

        # From open data from CACLR, https://data.public.lu/en/datasets/registre-national-des-localites-et-des-rues/
        housenumberRegexByCountry["LU"] = re.compile("^[1-9][0-9]{0,3}([A-Z]){0,3}(-[1-9][0-9]{0,3}([A-Z]){0,3})?$")

    def node(self, data, tags):
        err = []
        if "addr:housenumber" in tags and (len(tags["addr:housenumber"]) == 0 or not (housenumberRegexByCountry[self.Country].match(tags["addr:housenumber"]))):
            err.append((10, 1, {}))

        return err

    def way(self, data, tags, nds):
        err = self.node(data, tags)
        interpolation = tags.get("addr:interpolation")
        if interpolation:
            if len(filter(lambda x: x.startswith("addr:") and x not in ('addr:interpolation', 'addr:inclusion'), tags.keys())) > 0:
                err.append((14, 1, {}))
            if interpolation not in ('even', 'odd', 'all', 'alphabetic') and not interpolation.isdigit():
                err.append((15, 1, {'en': 'addr:interpolation=%s' % [interpolation]}))

        inclusion = tags.get("addr:inclusion")
        if inclusion and inclusion not in ('actual', 'estimate', 'potential'):
            err.append((15, 2, {'en': 'addr:inclusion=%s' % [inclusion]}))

        return err

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Housenumber(None)

        class _config:
            options = {"country": "XY"}

        class father:
            config = _config()

        a.father = father()
        a.init(None)

        assert not a.node(None, {})
        assert not a.node(None, {"addr:housenumber": "33"})
        assert not a.relation(None, {"addr:housenumber": "33"}, None)

        assert a.node(None, {"addr:housenumber": ""})
        assert a.node(None, {"addr:housenumber": "?"})
        assert a.relation(None, {"addr:housenumber": "?"}, None)

        assert a.way(None, {"addr:stret": "Lomlim", "addr:interpolation": "even"}, None)
        assert not a.way(None, {"addr:interpolation": "even"}, None)
        assert not a.way(None, {"addr:interpolation": "4"}, None)
        assert not a.way(None, {"addr:interpolation": "4", "addr:inclusion": "actual"}, None)
        assert a.way(None, {"addr:interpolation": "invalid"}, None)

        assert a.way(None, {"addr:housenumber": "ev.387"}, None)  # CZ housenumbers not valid outside CZ

        assert a.node(None, {"addr:housenumber": "корпус"})

    def test_withoutNumber(self):
        a = TagFix_Housenumber(None)

        class _config:
            options = {"country": "RU"}

        class father:
            config = _config()

        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "корпус"})

    def test_CH(self)
        a = TagFix_Housenumber(None)

        class _config:
            options = {"country": "CH"}

        class father:
            config = _config()

        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "313A"})

    def test_CZ(self)
        a = TagFix_Housenumber(None)

        class _config:
            options = {"country": "CZ"}

        class father:
            config = _config()

        a.father = father()
        a.init(None)

        assert not a.way(None, {"addr:housenumber": "ev.387"}, None)  # In CZ


    def test_LU(self)
        a = TagFix_Housenumber(None)

        class _config:
            options = {"country": "LU"}

        class father:
            config = _config()

        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "42A-44A"})
        assert not a.node(None, {"addr:housenumber": "42BIS"})


