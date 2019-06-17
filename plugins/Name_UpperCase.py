#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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
import regex as re

# Whitelist of allowed capitals by country code
UpperCase_WhiteList = {
    "FR": ["CNFPT", "COSEC", "EHPAD", "MACIF", "MEDEF", "URSSAF"]
}

class Name_UpperCase(Plugin):

    not_for = ["CU"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[803] = { "item": 5010, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Name with uppercase") }
        self.UpperTitleCase = re.compile(u".*[\p{Lu}\p{Lt}]{5,}")
        self.RomanNumber = re.compile(u".*[IVXCDLM]{5,}")

        if "country" in self.father.config.options:
            country = self.father.config.options.get("country")[:2]
            self.whitelist = UpperCase_WhiteList.get(country, None)
        else:
            self.whitelist = None

    def node(self, data, tags):
        err = []
        if u"name" in tags:
            # first check if the name *might* match
            if self.UpperTitleCase.match(tags[u"name"]) and not self.RomanNumber.match(tags[u"name"]):
                if self.whitelist is None:
                    err.append({"class": 803, "text":{"en":tags[u"name"]}})
                else:
                    # Check if we match the whitelist and if so re-try
                    name = " ".join(i for i in tags[u"name"].split() if not i in self.whitelist)
                    if self.UpperTitleCase.match(name) and not self.RomanNumber.match(name):
                        err.append({"class": 803, "text":{"en":tags[u"name"]}})
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_UpperCase(None)
        class _config:
            options = {"country": "FR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for t in [{u"name": u"COL TRÈS HAUTTT"},
                  {u"name": u"EHPAD MAGEUSCULE"},
                  {u"name": u"AÇǱÞΣSSὩΙST"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)

        for t in [{u"name": u"Col des Champs XIIVVVIM"},
                  {u"name": u"EHPAD La Madelon"},
                  {u"name": u"ƻאᎯᚦ京"},
                 ]:
            assert not a.node(None, t), t
