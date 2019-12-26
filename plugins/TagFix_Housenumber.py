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

import re
from collections import defaultdict

from plugins.Plugin import Plugin


class TagFix_Housenumber(Plugin):

    not_for = ("RU", "BG")

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[10] = {"item": 2060, "level": 3, "tag": ["addr", "fix:survey"], "desc": T_(u"Invalid addr:housenumber value")}
        self.errors[14] = {"item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Invalid tag on interpolation way")}
        self.errors[15] = {"item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Invalid addr:interpolation or addr:inclusion value")}
        self.Country = None
        if self.father.config.options.get("country"):
            self.Country = self.father.config.options.get("country")[0:2]

        # By default, validate that house number starts with 1-9
        self.housenumberRegexByCountry = defaultdict(lambda: re.compile("^[1-9]"))

        # More specific rules by country

        # From open data from cantons Zurich and Bern. See also https://github.com/ltog/osmi-addresses/issues/93
        # Plus allows commas with multiple numbers
        ch_number = "[1-9][0-9]{0,3}( ?[a-zA-Z])?"
        self.housenumberRegexByCountry["CH"] = re.compile("^(:?{0})(:?,{0})?$".format(ch_number))
        # https://wiki.openstreetmap.org/wiki/Cs:WikiProject_Czech_Republic/Address_system
        self.housenumberRegexByCountry["CZ"] = re.compile("^(ev\.)?[1-9]")
        # From open data from CACLR, https://data.public.lu/en/datasets/registre-national-des-localites-et-des-rues/
        self.housenumberRegexByCountry["LU"] = re.compile("^[1-9][0-9]{0,3}([A-Z]){0,3}(-[1-9][0-9]{0,3}([A-Z]){0,3})?$")
        # Allow "snc" (Senza numero civico) in Italy
        self.housenumberRegexByCountry["IT"] = re.compile("(:?^[1-9])|(^snc$)")
        # Baseline:
        #   https://imbag.github.io/catalogus/hoofdstukken/attributen--relaties#734-huisnummertoevoeging
        #   (7.3.2 huisnummer, 7.3.3 huisletter and 7.3.4 huisnummertoevoeging)
        # Exceptions to the rule:
        #   https://nl.wikipedia.org/wiki/Huisnummer
        # This pattern isn't exhaustive, but it should catch most weirdness.
        self.housenumberRegexByCountry["NL"] = re.compile(
                # Houseboats, 't/o X' stands for 'opposite X', where 'X' is an address on shore
                r"^(t/o )?"
                # 'Pekela'-style exception, leading letter (e.g., 'C54')
                "(([A-Z][1-9][0-9]{0,3})|"
                # Normal base numbers, no leading zero, not exceeding 5 digits.
                "([1-9][0-9]{0,4}))"
                # Up to four optional extensions (can have leading zeroes in the extension part, e.g., '2K-008')
                "([ -/]?(([0-9]{1,4})|([A-Za-z]{1,5}))){0,4}$")

    def node(self, data, tags):
        err = []
        if "addr:housenumber" in tags and (len(tags["addr:housenumber"]) == 0 or not (self.housenumberRegexByCountry[self.Country].match(tags["addr:housenumber"]))):
            err.append({"class": 10, "subclass": 1})

        return err

    def way(self, data, tags, nds):
        err = self.node(data, tags)
        interpolation = tags.get("addr:interpolation")
        if interpolation:
            if any(filter(lambda x: x.startswith("addr:") and x not in ('addr:interpolation', 'addr:inclusion'), tags.keys())):
                err.append({"class": 14, "subclass": 1})
            if interpolation not in ('even', 'odd', 'all', 'alphabetic') and not interpolation.isdigit():
                err.append({"class": 15, "subclass": 1, "text": {'en': 'addr:interpolation=%s' % [interpolation]}})

        inclusion = tags.get("addr:inclusion")
        if inclusion and inclusion not in ('actual', 'estimate', 'potential'):
            err.append({"class": 15, "subclass": 2, "text": {'en': 'addr:inclusion=%s' % [inclusion]}})

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

        assert a.way(None, {"addr:housenumber": "ev.387"}, None) # CZ housenumbers not valid outside CZ

        assert a.node(None, {"addr:housenumber": "корпус"})

    def test_CH(self):
        a = TagFix_Housenumber(None)
        class _config:
            options = {"country": "CH"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "313A"})
        assert not a.node(None, {"addr:housenumber": "1"})
        assert not a.node(None, {"addr:housenumber": "1,2"})
        assert a.node(None, {"addr:housenumber": "1;2"})

    def test_CZ(self):
        a = TagFix_Housenumber(None)
        class _config:
            options = {"country": "CZ"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.way(None, {"addr:housenumber": "ev.387"}, None)  # In CZ

    def test_LU(self):
        a = TagFix_Housenumber(None)
        class _config:
            options = {"country": "LU"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "42A-44A"})
        assert not a.node(None, {"addr:housenumber": "42BIS"})

    def test_LU(self):
        a = TagFix_Housenumber(None)
        class _config:
            options = {"country": "IT"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "42"})
        assert not a.node(None, {"addr:housenumber": "snc"})

    def test_NL(self):
        a = TagFix_Housenumber(None)
        class _config:
            options = {"country": "NL"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {"addr:housenumber": "42"})
        assert not a.node(None, {"addr:housenumber": "18A"})
        assert not a.node(None, {"addr:housenumber": "123-24"})
        assert not a.node(None, {"addr:housenumber": "2K-008"})
        assert not a.node(None, {"addr:housenumber": "10t-13"})
        assert not a.node(None, {"addr:housenumber": "13-bv"})
        assert not a.node(None, {"addr:housenumber": "13 bv"})
        assert not a.node(None, {"addr:housenumber": "1-TRAF"})
        assert not a.node(None, {"addr:housenumber": "19p-8"})
        assert not a.node(None, {"addr:housenumber": "44d-G"})
        assert not a.node(None, {"addr:housenumber": "3-0072"})

        # Groningen-style extension.
        assert not a.node(None, {"addr:housenumber": "16/1"})

        # Naval base in Den Helder
        assert not a.node(None, {"addr:housenumber": "100D-G29B"})

        # Pekela
        assert not a.node(None, {"addr:housenumber": "B54"})

        # Graan voor Visch, Hoofddorp
        assert not a.node(None, {"addr:housenumber": "19601U"})

        # Woonboot
        assert not a.node(None, {"addr:housenumber": "t/o 56"})

        # Utrecht
        assert not a.node(None, {"addr:housenumber": "113B Bis A"})

        assert not a.node(None, {"addr:housenumber": "7 bis"})

        assert a.node(None, {"addr:housenumber": "1;2"})
        assert a.node(None, {"addr:housenumber": " 1 "})
        assert a.node(None, {"addr:housenumber": "1 "})
        assert a.node(None, {"addr:housenumber": " 1"})

        # Non-ASCII numerics.
        assert a.node(None, {"addr:housenumber": "１"})

        # Non-ASCII letters.
        assert a.node(None, {"addr:housenumber": "1Ｂ"})

        assert a.node(None, {"addr:housenumber": "123--A3"})
        assert a.node(None, {"addr:housenumber": "123 -A3"})
        assert a.node(None, {"addr:housenumber": "123  A3"})

        # Mixed up tags.
        assert a.node(None, {"addr:housenumber": "Dorpsstraat"})

        # Trolls, bogus input.
        assert a.node(None, {"addr:housenumber": "1234567890abcdefghijklmnopqrstuvwxyz"})
