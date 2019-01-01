#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2018                                         ##
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
import json


class TagFix_Wikidata(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30318] = {"item": 3031, "level": 2, "tag": ["value", "wikidata", "fix:chair"], "desc": T_(u"This wikidata value matches a chain store, it should be in a brand:wikidata tag.")}

        self.black_list = self.black_list()

    def black_list(self):
        wikidata_query_for_chain_store = u"https://query.wikidata.org/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20WHERE%20{%0A%20{%20%3Fitem(wdt%3AP31%2Fwdt%3AP279*)wd%3AQ507619%20}%20UNION%20{%20%3Fitem(wdt%3AP31%2Fwdt%3AP279*)%20wd%3AQ1631129%20}%0A%20SERVICE%20wikibase%3Alabel%20{%20bd%3AserviceParam%20wikibase%3Alanguage%20%22[AUTO_LANGUAGE]%2Cen%22.%20}%0A}&format=json"

        json_str = urlread(wikidata_query_for_chain_store, 30)
        results = json.loads(json_str)
        should_be_brand = [elem['item']['value'].split('/')[-1] for elem in results['results']['bindings']]

        return should_be_brand

    def node(self, data, tags):
        if "wikidata" in tags and tags["wikidata"] in self.black_list:
            if "wikipedia" in tags:
                return {"class": 30318, "subclass": 0,
                    "text": T_("Please also check the wikipedia tag."),
                    "fix": {'+': {u'brand:wikidata': tags["wikidata"]}, '-': [u'wikidata']} }
            else:
                return {"class": 30318, "subclass": 1,
                    "fix": {'+': {u'brand:wikidata': tags["wikidata"]}, '-': [u'wikidata']} }

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Wikidata(None)
        a.init(None)

        assert a.node(None, {"wikidata": "Q188326"})
        assert a.way(None, {"wikidata": "Q188326"}, None)
        assert a.relation(None, {"wikidata": "Q188326"}, None)
        assert a.node(None, {"wikidata": "Q188326", "brand:wikidata": "Q188326"})
        assert not a.node(None, {"brand:wikidata": "Q188326"})
