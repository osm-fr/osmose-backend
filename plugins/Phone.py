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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from modules.Stablehash import stablehash64
import re


class Phone(Plugin):

    PHONE_TAGS = set(("contact:fax", "contact:phone", "fax", "phone"))

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
            self.errors[30920] = self.def_class(item = 3092, level = 2, tags = ['value', 'fix:chair'],
                title = T_('Phone number does not match the expected format'))
        if self.local_prefix:
            self.errors[30921] = self.def_class(item = 3092, level = 2, tags = ['value', 'fix:chair'],
                title = T_('Extra "{0}" after international code', self.local_prefix))
        if self.size_short:
            self.errors[30922] = self.def_class(item = 3092, level = 2, tags = ['value', 'fix:chair'],
                title = T_('Local short code can not be internationalized'))
        self.errors[30923] = self.def_class(item = 3092, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Missing international prefix'))
        self.errors[30924] = self.def_class(item = 3092, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Bad international prefix'))
        self.errors[30925] = self.def_class(item = 3092, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Prohibited char in phone number'))
        self.errors[30926] = self.def_class(item = 3092, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Bad separator for multiple values'))

        country = self.father.config.options.get("country")

        if self.code and self.local_prefix:
            # Regular numbers must not have a local_prefix (aka "0") after +[code]
            self.InternationalAndLocalPrefix = re.compile(r"^[+]{0}[- ./]*{1}((?:[- ./]*[0-9])+)$".format(self.code, self.local_prefix))
        else:
            self.InternationalAndLocalPrefix = None

        if self.size_short:
            # Short numbers cannot be internationalized
            self.BadShort = re.compile(r"^[+]{0}[- ./]*([0-9]{{{1},{2}}})$".format(self.code, min(self.size_short), max(self.size_short)))
        else:
            self.BadShort = None

        if self.international_prefix:
            self.InternationalPrefix = re.compile(r"^{0}(.*)".format(self.international_prefix))
        else:
            self.InternationalPrefix = None

        if self.local_prefix:
            if country and country.startswith("FR"):
                # Local numbers to internationalize. Note that in addition to
                # short numbers this also skips special numbers starting with 08
                # or 09 since these may or may not be callable from abroad.
                self.MissingInternationalPrefix = re.compile(r"^{0}[- ./]*([1-7](:?[- ./]*[0-9]){{{1},{2}}})$".format(self.local_prefix, min(self.size) - 1, max(self.size) - 1))
            elif country and country.startswith("BE"):
                # Local numbers to internationalize. Note that in addition to
                # short numbers this also skips special numbers starting with 070,
                # 077, 078, 0800, or 090x since these may or may not be callable from abroad.
                # not merged into 07x 08x 09x because severals local numbers inside those prefix
                self.MissingInternationalPrefix = re.compile(r"^(?:-{0}|{0})[- ./]*(?!70|77|78|800|90[0-9])([1-9](:?[- ./]*[0-9]){{{1},{2}}})$".format(self.local_prefix, min(self.size) - 1, max(self.size) - 1))
            elif country and country.startswith("DE"):
                # Local numbers to internationalize. Note that 0800 toll-free numbers
                # are not callable from abroad and should not be internationalized.
                self.MissingInternationalPrefix = re.compile(r"^{0}[- ./]*(?!800)((:?[0-9][- ./]*){{{1},{2}}}[0-9])$".format(self.local_prefix, min(self.size) - len(self.local_prefix) - 1, max(self.size) - len(self.local_prefix) - 1))
            elif self.size:
                self.MissingInternationalPrefix = re.compile(r"^{0}[- ./]*((:?[0-9][- ./]*){{{1},{2}}}[0-9])$".format(self.local_prefix, min(self.size) - len(self.local_prefix) - 1, max(self.size) - len(self.local_prefix) - 1))
            else:
                self.MissingInternationalPrefix = re.compile(r"^{0}[- ./]*((:?[0-9][- ./]*)+[0-9])$".format(self.local_prefix))
        else:
            if country and country.startswith("IT"):
                # Only non toll-free numbers are callable from abroad.
                self.MissingInternationalPrefix = re.compile(r"^([03](:?[0-9][- ./]*){{{0},{1}}})$".format(min(self.size) - 1, max(self.size) - 1))
            else:
                self.MissingInternationalPrefix = re.compile(r"^((:?[0-9][- ./]*){{{0},{1}}}[0-9])$".format(min(self.size) - 1, max(self.size) - 1))

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
            if ';' in phone:
                continue  # Ignore multiple phone numbers

            if self.suffix_separators is not None:
                phone = phone.split(self.suffix_separators, 1)[0]

            if self.values_separators:
                p = phone
                for sep in self.values_separators:
                    if sep in phone:
                        phone = phone.replace(sep, '; ')
                if p != phone:
                    phone = phone.replace('  ', ' ')
                    err.append({"class": 30926, "subclass": stablehash64(tag), "text": T_("Concerns tag: `{0}`", '='.join([tag, phone])), "fix": {tag: phone.replace(' / ', '; ').replace(' - ', '; ').replace(',', ';')}})
                    continue

            phone_test = phone
            for c in '+0123456789 -./()':
                phone_test = phone_test.replace(c, '')
            if len(phone_test) > 0:
                err.append({"class": 30925, "subclass": stablehash64(tag), "text": T_("Not allowed char \"{0}\" in phone number tag \"{1}\"", phone_test, tag)})
                continue

            # Detection and correction of invalid prefixes (e.g., "-", "-+")
            if phone.startswith('-'):
                # Case 1: Prefix "-+" (e.g., "-+32...")
                if phone.startswith('-+'):
                    phone_stripped = phone[2:]
                    if phone_stripped.startswith(self.code + " "):
                        err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Bad international prefix"), "fix": {tag: "+" + phone_stripped}})
                        continue
                    elif self.InternationalPrefix and self.InternationalPrefix.match(phone_stripped):
                        err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Bad international prefix"), "fix": {tag: "+" + phone_stripped}})
                        continue
                    elif self.MissingInternationalPrefix and self.MissingInternationalPrefix.match(phone_stripped):
                        err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Bad international prefix"), "fix": {tag: "+" + self.code + " " + phone_stripped}})
                        continue
                # Case 2: Prefix "-" before an international prefix (e.g., "-32...")
                elif len(phone) > 1 and phone[1:].startswith(self.code):
                    phone_stripped = phone[1:]
                    if phone_stripped.startswith(self.code + " "):
                        err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Bad international prefix"), "fix": {tag: "+" + phone_stripped}})
                        continue
                    elif self.InternationalPrefix and self.InternationalPrefix.match(phone_stripped):
                        err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Bad international prefix"), "fix": {tag: "+" + phone_stripped}})
                        continue
                # Case 3: Prefix "-" before a local prefix (e.g., "-0...")
                elif len(phone) > 1 and phone[1:].startswith(self.local_prefix):
                    phone_stripped = phone[1:]
                    if self.MissingInternationalPrefix and self.MissingInternationalPrefix.match(phone_stripped):
                        err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Bad international prefix"), "fix": {tag: "+" + self.code + " " + phone_stripped.replace(self.local_prefix, '', 1)}})
                        continue
                # If the number remains invalid, report an error without proposing a fix
                err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Invalid phone number")})
                continue

            # Before local prefix
            if self.InternationalPrefix:
                r = self.InternationalPrefix.match(phone)
                if r:
                    err.append({"class": 30924, "subclass": stablehash64(tag), "text": T_("Concerns tag: `{0}`", '='.join([tag, phone])), "fix": {tag: "+" + r.group(1)}})
                    continue

            if self.InternationalAndLocalPrefix:
                r = self.InternationalAndLocalPrefix.match(phone)
                if r:
                    err.append({"class": 30921, "subclass": stablehash64(tag), "text": T_("Concerns tag: `{0}`", '='.join([tag, phone])), "fix": {tag: "+" + self.code + " " + r.group(1)}})
                    continue

            if self.MissingInternationalPrefix:
                r = self.MissingInternationalPrefix.match(phone)
                if r:
                    err.append({"class": 30923, "subclass": stablehash64(tag), "text": T_("Concerns tag: `{0}`", '='.join([tag, phone])), "fix": {tag: "+" + self.code + " " + r.group(1)}})
                    continue

            if self.BadShort:
                r = self.BadShort.match(phone)
                if r:
                    err.append({"class": 30922, "subclass": stablehash64(tag), "text": T_("Concerns tag: `{0}`", '='.join([tag, phone])), "fix": {tag: r.group(1)}})
                    continue

            # Last
            if self.Format:
                r = self.Format.match(phone)
                if not r:
                    err.append({"class": 30920, "subclass": stablehash64(tag), "text": T_("Concerns tag: `{0}`", '='.join([tag, phone])) })
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
            ("+330102030405", "+33 102030405"),
            ("0033 102030405", "+33 102030405"),
            ("12 / 13", "12; 13"),
            # Preserve formatting
            ("+33 0102030405", "+33 102030405"),
            ("+33  01 02 03 04 05", "+33 1 02 03 04 05"),
            ("+33  3631", "3631"),
            ("0102030405", "+33 102030405"),
            ("01 02 03 04 05", "+33 1 02 03 04 05"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        # Verify we got no error for other correct numbers
        for good in ("3631", "118987", "1;2"):
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

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
            ("43 43 43", "+687 43 43 43"),
            ("434343", "+687 434343"),
            ("00687297969", "+687297969"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        # Verify we got error for other correct numbers
        for bad in ("3631"):
            assert p.node(None, {"phone": bad}), ("phone='{0}'".format(bad))

    def test_CA(self):
        p = Phone(None)
        class _config:
            options = {"country": "CA", "phone_code": "1", "phone_len": 10, "phone_format": r"^[+]%s[- ][0-9]{3}[- ][0-9]{3}[- ][0-9]{4}$"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            ("800-555-0000", "+1 800-555-0000"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        # Verify we got error for other correct numbers
        for bad in ("3631", "(123) 123-4567", "+1 123 1234567"):
            assert p.node(None, {"phone": bad}), ("phone='{0}'".format(bad))

    def test_ES(self):
        p = Phone(None)
        class _config:
            options = {"country": "ES", "phone_code": "34", "phone_len": 9, "phone_len_short": [3, 4, 5], "phone_international": "00"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            ("923 555 000", "+34 923 555 000"),
            ("923 55 50 00", "+34 923 55 50 00"),
            ("923555000", "+34 923555000"),
            ("0034923555000", "+34923555000"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

    def test_IT(self):
        p = Phone(None)
        class _config:
            options = {"country": "IT", "phone_code": "39", "phone_len": [6, 11], "phone_len_short": [3, 4], "phone_international": "00", "phone_format": r"^(?:(?:[+]%s[- ]*[03])|[18])[0-9]+(?:[- ][0-9]+)?(?:(?:[- ][0-9]+)|$)$"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            ("0212345", "+39 0212345"),
            ("02 12345", "+39 02 12345"),
            ("0171 1234567", "+39 0171 1234567"),
            ("01711234567", "+39 01711234567"),
            ("003901711234567", "+3901711234567"),
            ("333 123456", "+39 333 123456"),
            ("333 123 4567", "+39 333 123 4567"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        # Verify we got no error for other correct numbers
        for good in ("800 123", "112", "1515"):
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

    def test_BE(self):
        p = Phone(None)
        class _config:
            options = {"country": "BE", "phone_code": "32", "phone_len": [8, 9], "phone_len_short": [3, 4], "phone_format": r"^([+]%s([- ./]*[0-9]){7,8}[0-9])|[0-9]{3,4}$", "phone_international": "00", "phone_local_prefix": "0"}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            ("+32021231212", "+32 21231212"),
            ("0032 21231212", "+32 21231212"),
            ("12 / 13", "12; 13"),
            # Preserve formatting
            ("+32 021231212", "+32 21231212"),
            ("+32 02 123 12 12", "+32 2 123 12 12"),
            ("+32 1307", "1307"),
            ("021231212", "+32 21231212"),
            ("-021231212", "+32 21231212"),
            ("-32 2 123 12 12", "+32 2 123 12 12"),
            ("-+32 2 123 12 12", "+32 2 123 12 12"),
            ("02 123 12 12", "+32 2 123 12 12"),
            ("0474 56 78 90", "+32 474 56 78 90"),
        ):
            # Check the bad number's error and fix
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertIn("fix", err[0], f"No fix proposed for phone number: {bad}")
            self.assertEqual(err[0]["fix"]["phone"], good)

            # The correct number does not need fixing
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        # Verify we got no error for other correct numbers
        for good in ("1307", "112", "1;2"):
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        assert len(p.node(None, {"phone": "02.123.12.12", "fax": "02.123.12.12"})) == 2

    def test_DE(self):
        p = Phone(None)
        class _config:
            options = {"country": "DE", "phone_code": "49", "phone_len": [10, 11], "phone_international": "00", "phone_local_prefix": "0", "phone_values_separators": [","]}
        class father:
            config = _config()
        p.father = father()
        p.init(None)

        for (bad, good) in (
            ("030 12345678", "+49 30 12345678"),
            ("0049 30 12345678", "+49 30 12345678"),
            ("0711 1234567", "+49 711 1234567"),
        ):
            err = p.node(None, {"phone": bad})
            self.check_err(err, ("phone='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"]["phone"], good)

            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))

        # 0800 toll-free numbers must not be internationalized
        for good in ("0800 1234567", "08001234567", "+49 800 1234567"):
            assert not p.node(None, {"phone": good}), ("phone='{0}'".format(good))
