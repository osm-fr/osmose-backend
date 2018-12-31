#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2014-2015                                 ##
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
from modules.downloader import urlread
import re


class TagFix_Postcode(Plugin):

    def parse_format(self, reline, format):
        format = format.replace('optionally ', '')
        if format[-1] == ')':
            format = map(lambda x: x.strip(), format[:-1].split('('))
        elif ' or ' in format:
            format = format.split(' or ')
        elif ', ' in format:
            format = format.split(', ')
        else:
            format = [format]

        regexs = []
        for f in format:
            if reline.match(f):
                regexs.append(f.replace(" ", "").replace("-", "").replace(".", "").replace("N", "[0-9]").replace("A", "[A-Z]").replace("CC", "(:?"+self.Country+")?"))

        if len(regexs) > 1:
            return "^(("+(")|(".join(regexs))+"))$"
        elif len(regexs) == 1:
            return "^"+regexs[0]+"$"

    def list_postcode(self):
        reline = re.compile("^[-CAN ]+$")
        # remline = re.compile("^[-CAN ]+ *\([-CAN ]+\)$")
        data = urlread(u"https://en.wikipedia.org/wiki/List_of_postal_codes?action=raw", 1)
        data = filter(lambda t: len(t)>2 and (t[1] != "- no codes -" or t[2] != ""), map(lambda x: list(map(lambda y: y.strip(), x.split("|")))[5:8], data.split("|-")[1:-1]))
        postcode = {}
        for line in data:
            iso = line[0][0:2]
            format_area = line[1]
            format_street = line[2]
            # note = line[3]

            postcode[iso] = {}
            if format_area != '':
                postcode[iso]['area'] = self.parse_format(reline, format_area)
            if format_street != '':
                postcode[iso]['street'] = self.parse_format(reline, format_street)

        return postcode

    def init(self, logger):
        Plugin.init(self, logger)
        if self.father.config.options.get("project") != 'openstreetmap':
            return False
        self.errors[31901] = {"item": 3190, "level": 3, "tag": ["postcode", "fix:chair"], "desc": T_(u"Invalid postcode") }

        self.Country = None
        if self.father.config.options.get("country"):
            self.Country = self.father.config.options.get("country")
        self.CountryPostcodeArea = None
        self.CountryPostcodeStreet = None
        if not self.Country or self.Country == 'GB': # Specific plugin for GB
            return
        postcode = self.list_postcode()
        if self.Country in postcode:
            if 'area' in postcode[self.Country] and postcode[self.Country]['area'] is not None:
                self.CountryPostcodeArea = re.compile(postcode[self.Country]['area'])
            if 'street' in postcode[self.Country] and postcode[self.Country]['street'] is not None:
                self.CountryPostcodeStreet = re.compile(postcode[self.Country]['street'])
            elif 'area' in postcode[self.Country] and postcode[self.Country]['area'] is not None:
                self.CountryPostcodeStreet = self.CountryPostcodeArea

    def node(self, data, tags):
        err = []
        if self.CountryPostcodeArea and 'postal_code' in tags and not self.CountryPostcodeArea.match(tags['postal_code'].replace(" ", "").replace("-", "").replace(".", "")):
            err.append({"class": 31901, "subclass": 1, "text": T_("Invalid area postcode %(postcode)s for country code %(country)s", {"postcode": tags['postal_code'], "country": self.Country})})
        if self.CountryPostcodeStreet and 'addr:postcode' in tags and not self.CountryPostcodeStreet.match(tags['addr:postcode'].replace(" ", "").replace("-", "").replace(".", "")):
            err.append({"class": 31901, "subclass": 2, "text": T_("Invalid street level postcode %(postcode)s for country code %(country)s", {"postcode": tags['addr:postcode'], "country": self.Country})})
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_FR(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "FR", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert a.node(None, {"addr:postcode":"la bas"})
        assert a.way(None, {"addr:postcode":"la bas"}, None)
        assert a.relation(None, {"addr:postcode":"la bas"}, None)
        assert not a.node(None, {"addr:postcode":"75000"})
        assert not a.node(None, {"postal_code":"75000"})
        assert not a.node(None, {"addr:postcode":"75 000"})

    def test_no_country(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.node(None, {"addr:postcode":"la bas"})
        assert not a.node(None, {"addr:postcode":"75000"})
        assert not a.node(None, {"postal_code":"75000"})

    def test_NL(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "NL", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert a.node(None, {"addr:postcode":"la bas"})
        assert not a.node(None, {"addr:postcode":"1234 AB"})
        assert not a.node(None, {"addr:postcode":"1234AB"})
        assert not a.node(None, {"addr:postcode":"12 34AB"})
        assert a.node(None, {"addr:postcode":"12241AB"})
        assert a.node(None, {"addr:postcode":"1224"})
        assert not a.node(None, {"postal_code":"1224"})

    def test_MD(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "MD", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.node(None, {"addr:postcode":"3100"})
        assert not a.node(None, {"addr:postcode":"MD3100"})
        assert a.node(None, {"addr:postcode":"0"})
        assert a.node(None, {"addr:postcode":"12-190"})
        assert a.node(None, {"addr:postcode":"1211901"})

    def test_BI(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "BI", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.node(None, {"addr:postcode":"3100"})
        assert not a.node(None, {"addr:postcode":"MD3100"})

    def test_BR(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "BR", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.node(None, {"postal_code":"01001"})
        assert not a.node(None, {"addr:postcode":"99990-970"})
        assert not a.node(None, {"addr:postcode":"99.990 970"})
        assert a.node(None, {"postal_code":"plop"})
        assert a.node(None, {"addr:postcode":"plop"})

    def test_BM(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "BM", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.node(None, {"addr:postcode":"HM HX"})
        assert not a.node(None, {"addr:postcode":"HM 02"})
        assert a.node(None, {"addr:postcode":"plopplop"})

    def test_US(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "US", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.node(None, {"postal_code":"30318"})
        assert not a.node(None, {"postal_code":"30318-2522"})
