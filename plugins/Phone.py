#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Francois Gouget fgouget free.fr 2017                       ##
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
from modules.Stablehash import stablehash
import re


class Phone(Plugin):

    PHONE_TAGS = set((u"contact:fax", u"contact:phone", u"fax", u"phone"))

    def init(self, logger):
        Plugin.init(self, logger)
        self.code = self.father.config.options.get("phone_code")
        if not self.code:
            return False
        self.size = self.father.config.options.get("phone_len")
        if self.size and not isinstance(self.size, list):
            self.size = [self.size]
        self.size_short = self.father.config.options.get("phone_len_short")
        if self.size_short and not isinstance(self.size_short, list):
            self.size_short = [self.size_short]
        self.format = self.father.config.options.get("phone_format")
        self.international_prefix = self.father.config.options.get("phone_international")
        self.local_prefix = self.father.config.options.get("phone_local_prefix")
        self.values_separators = self.father.config.options.get("phone_values_separators", [' / ', ' - ', ','])
        self.suffix_separators = self.father.config.options.get("suffix_separators")

        if self.format:
            self.errors[30920] = {"item": 3092, "level": 2, "tag": ["value", "fix:chair"], "desc": T_f(u"Phone number does not match the expected format")}
        if self.local_prefix:
            self.errors[30921] = {"item": 3092, "level": 2, "tag": ["value", "fix:chair"], "desc": T_f(u"Extra \"{0}\" after international code", self.local_prefix)}
        if self.size_short:
            self.errors[30922] = {"item": 3092, "level": 2, "tag": ["value", "fix:chair"], "desc": T_f(u"Local short code can't be internationalized")}
        self.errors[30923] = {"item": 3092, "level": 3, "tag": ["value", "fix:chair"], "desc": T_f(u"Missing international prefix")}
        self.errors[30924] = {"item": 3092, "level": 3, "tag": ["value", "fix:chair"], "desc": T_f(u"Bad international prefix")}
        self.errors[30925] = {"item": 3092, "level": 3, "tag": ["value", "fix:chair"], "desc": T_f(u"Unallowed char in phone number")}
        self.errors[30926] = {"item": 3092, "level": 3, "tag": ["value", "fix:chair"], "desc": T_f(u"Bad separator for multiple values")}

        country = self.father.config.options.get("country")

        if self.code and self.local_prefix:
            # Regular numbers must not have a local_prefix (aka "0") after +[code]
            self.InternationalAndLocalPrefix = re.compile(r"^[+]%s[- ./]*%s((?:[- ./]*[0-9])+)$" % (self.code, self.local_prefix))
        else:
            self.InternationalAndLocalPrefix = None

        if self.size_short:
            # Short numbers cannot be internationalized
            self.BadShort = re.compile(r"^[+]%s[- ./]*([0-9]{%s,%s})$" % (self.code, min(self.size_short), max(self.size_short)))
        else:
            self.BadShort = None

        if self.international_prefix:
            self.InternationalPrefix = re.compile(r"^%s(.*)" % self.international_prefix)
        else:
            self.InternationalPrefix = None

        if self.local_prefix:
            if country and country.startswith("FR"):
                # Local numbers to internationalize. Note that in addition to
                # short numbers this also skips special numbers starting with 08
                # or 09 since these may or may not be callable from abroad.
                self.MissingInternationalPrefix = re.compile(r"^%s[- ./]*([1-7](:?[- ./]*[0-9]){%s,%s})$" % (self.local_prefix, min(self.size) - 1, max(self.size) - 1))
            elif self.size:
                self.MissingInternationalPrefix = re.compile(r"^%s[- ./]*((:?[0-9][- ./]*){%s,%s}[0-9])$" % (self.local_prefix, min(self.size) - len(self.local_prefix) - 1, max(self.size) - len(self.local_prefix) - 1))
            else:
                self.MissingInternationalPrefix = re.compile(r"^%s[- ./]*((:?[0-9][- ./]*)+[0-9])$" % (self.local_prefix))
        else:
            self.MissingInternationalPrefix = re.compile(r"^((:?[0-9][- ./]*){%s,%s}[0-9])$" % (min(self.size) - 1, max(self.size) - 1))

        if self.format:
            self.Format = re.compile(self.format % self.code)
        else:
            self.Format = None

    def check(self, tags):
        err = []
        for tag in self.PHONE_TAGS:
            if tag not in tags:
                continue
            phone = tags[tag]
            if u';' in phone:
                continue  # Ignore multiple phone numbers

            if self.suffix_separators != None:
                phone = phone.split(self.suffix_separators, 1)[0]

            if self.values_separators:
                p = phone
                for sep in self.values_separators:
                    if sep in phone:
                        phone = phone.replace(sep, '; ')
                if p != phone:
                    phone = phone.replace('  ', ' ')
                    err.append({"class": 30926, "subclass": stablehash(tag), "fix": {tag: phone.replace(' / ', '; ').replace(' - ', '; ').replace(',', ';')}})
                    continue

            phone_test = phone
            for c in '+0123456789 -./()':
                phone_test = phone_test.replace(c, '')
            if len(phone_test) > 0:
                err.append({"class": 30925, "subclass": stablehash(tag), "text": T_f(u"Not allowed char \"{0}\" in phone number", phone_test)})
                continue

            # Before local prefix
            if self.InternationalPrefix:
                r = self.InternationalPrefix.match(phone)
                if r:
                    err.append({"class": 30924, "subclass": stablehash(tag), "fix": {tag: "+" + r.group(1)}})
                    continue

            if self.InternationalAndLocalPrefix:
                r = self.InternationalAndLocalPrefix.match(phone)
                if r:
                    err.append({"class": 30921, "subclass": stablehash(tag), "fix": {tag: "+" + self.code + " " + r.group(1)}})
                    continue

            if self.MissingInternationalPrefix:
                r = self.MissingInternationalPrefix.match(phone)
                if r:
                    err.append({"class": 30923, "subclass": stablehash(tag), "fix": {tag: "+" + self.code + " " + r.group(1)}})
                    continue

            if self.BadShort:
                r = self.BadShort.match(phone)
                if r:
                    err.append({"class": 30922, "subclass": stablehash(tag), "fix": {tag: r.group(1)}})
                    continue

            # Last
            if self.Format:
                r = self.Format.match(phone)
                if not r:
                    err.append({"class": 30920, "subclass": stablehash(tag), "text": {"en": phone}})
                    continue

        return err

    def node(self, _data, tags):
        return self.check(tags)

    def way(self, _data, tags, _nds):
        return self.check(tags)

    def relation(self, _data, tags, _members):
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_FR(self):
        p = Phone(None)
        class _config:
            options = {"country": "FR", "phone_code": "33", "phone_len": 9, "phone_len_short": [4, 6], "phone_format": r"^([+]%s([- ./]*[0-9]){8}[0-9])|[0-9]{4}|[0-9]{6}$", "phone_international": "00", "phone_local_prefix": "0"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            (u"+330102030405", u"+33 102030405"),
            (u"0033 102030405", u"+33 102030405"),
            (u"12 / 13", u"12; 13"),
            # Preserve formatting
            (u"+33 0102030405", u"+33 102030405"),
            (u"+33  01 02 03 04 05", u"+33 1 02 03 04 05"),
            (u"+33  3631", u"3631"),
            (u"0102030405", u"+33 102030405"),
            (u"01 02 03 04 05", u"+33 1 02 03 04 05"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='%s'" % bad))
            self.assertEquals(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='%s'" % good)

        # Verify we got no error for other correct numbers
        for good in (u"3631", u"118987", u"1;2"):
            assert not p.node(None, {"phone": good}), ("phone='%s'" % good)

        assert len(p.node(None, {"phone": "09.72.42.42.42", "fax": "09.72.42.42.42"})) == 2

    def test_NC(self):
        p = Phone(None)
        class _config:
            options = {"country": "NC", "phone_code": "687", "phone_len": 6, "phone_format": r"^[+]%s([- ./]*[0-9]){5}[0-9]$", "phone_international": "00"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            (u"43 43 43", u"+687 43 43 43"),
            (u"434343", u"+687 434343"),
            (u"00687297969", u"+687297969"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='%s'" % bad))
            self.assertEquals(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='%s'" % good)

        # Verify we got error for other correct numbers
        for bad in (u"3631"):
            assert p.node(None, {"phone": bad}), ("phone='%s'" % bad)

    def test_CA(self):
        p = Phone(None)
        class _config:
            options = {"country": "CA", "phone_code": "1", "phone_len": 10, "phone_format": r"^[+]%s[- ][0-9]{3}[- ][0-9]{3}[- ][0-9]{4}$"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            (u"800-555-0000", u"+1 800-555-0000"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='%s'" % bad))
            self.assertEquals(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='%s'" % good)

        # Verify we got error for other correct numbers
        for bad in (u"3631", u"(123) 123-4567", "+1 123 1234567"):
            assert p.node(None, {"phone": bad}), ("phone='%s'" % bad)

    def test_ES(self):
        p = Phone(None)
        class _config:
            options = {"country": "ES", "phone_code": "34", "phone_len": 9, "phone_len_short": [3, 4, 5], "phone_international": "00"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            (u"923 555 000", u"+34 923 555 000"),
            (u"923 55 50 00", u"+34 923 55 50 00"),
            (u"923555000", u"+34 923555000"),
            (u"0034923555000", u"+34923555000"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='%s'" % bad))
            self.assertEquals(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='%s'" % good)
