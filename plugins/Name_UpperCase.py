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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
import regex as re
from modules.downloader import urlread
import json

# Whitelist of allowed capitals by country code
UpperCase_WhiteList = {
    "FR": ["CNFPT", "COSEC", "EHPAD", "MEDEF", "URSSAF"],
}

class Name_UpperCase(Plugin):

    not_for = ["CU", "JP"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[803] = self.def_class(item = 5010, level = 1, tags = ['name', 'fix:chair'],
            title = T_('Name with uppercase'),
            detail = T_(
'''This feature is tagged with a name which contains a fully uppercase word (or words).
 This is not expected for the majority of named features.'''),
            fix = T_(
'''acronyms must be set in `short_name` tag.'''),
            trap = T_(
'''While uncommon, it is possible for a name to have uppercase words.
 This is particularly the case for corporate/branded locations as well as acronyms.''')
        )
        self.Letter = re.compile(r"^\p{Letter}{5,}$")
        self.UpperTitleCase = re.compile(r".*[\p{Uppercase_Letter}\p{Titlecase_Letter}]{5,}")
        self.RomanNumber = re.compile(r".*[IVXCDLM]{5,}")

        if "country" in self.father.config.options:
            country = self.father.config.options.get("country")[:2]
            self.whitelist = set(UpperCase_WhiteList.get(country, []))
            nsi = self._download_nsi()
            self.whitelist.update(self._whitelist_from_nsi(nsi, "brands/", country.lower()))
        else:
            self.whitelist = set()

    def _download_nsi(self):
        nsi_url = "https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/dist/nsi.json"
        json_str = urlread(nsi_url, 30)
        results = json.loads(json_str)
        return results['nsi']

    def _whitelist_from_nsi(self, nsi, nsiprefix, country):
        whitelist = set()
        for tag, details in nsi.items():
            if tag.startswith(nsiprefix) and "items" in details:
                for preset in details["items"]:
                    if "locationSet" in preset:
                        if ("include" in preset["locationSet"] and
                                country not in preset["locationSet"]["include"] and
                                "001" not in preset["locationSet"]["include"]):
                            continue
                        if "exclude" in preset["locationSet"] and country in preset["locationSet"]["exclude"]:
                            continue
                    if "name" in preset["tags"]:
                        for name in preset["tags"]["name"].split():
                            if self.Letter.match(name) and not self.RomanNumber.match(name):
                                whitelist.add(name.upper())
                    for name in preset["displayName"].split():
                        if self.Letter.match(name) and not self.RomanNumber.match(name):
                            whitelist.add(name.upper())
        return whitelist

    def node(self, data, tags):
        err = []
        if u"name" in tags:
            # first check if the name *might* match
            if self.UpperTitleCase.match(tags[u"name"]) and not self.RomanNumber.match(tags[u"name"]):
                if not self.whitelist:
                    err.append({"class": 803, "text": T_("Concerns tag: `{0}`", '='.join(['name', tags['name']])) })
                else:
                    # Check if we match the whitelist and if so re-try
                    name = " ".join(i for i in tags[u"name"].split() if not i in self.whitelist)
                    if self.UpperTitleCase.match(name) and not self.RomanNumber.match(name):
                        err.append({"class": 803, "text": T_("Concerns tag: `{0}`", '='.join(['name', tags['name']])) })
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_FR(self):
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

    def test_ES(self):
        a = Name_UpperCase(None)
        class _config:
            options = {"country": "ES-GC"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        for t in [{"name": "FREMAP"},
                  {"name": "CEPSA"},
                 ]:
            assert not a.node(None, t), t
