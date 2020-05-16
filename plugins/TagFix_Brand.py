# -*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2020                                         ##
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

from plugins.Plugin import TestPluginCommon
from plugins.Plugin import Plugin
from modules.downloader import urlread
import json

#TODO : handle country codes

class TagFix_Brand(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        doc = dict(
                detail = T_(
'''This object has a very common name that is likely to be a brand.'''),
                fix = T_(
'''If this is indeed a brand, add `brand` and `brand:wikidata` tags.
If not, report it to the [name-suggestion-index project](https://github.com/osmlab/name-suggestion-index/blob/master/CONTRIBUTING.md)
which is used here to link frequent names to brands'''))

        self.errors[31301] = self.def_class(item=3130, level=2, tags=['brand', 'fix:chair'],
                                            title=T_(
                                                "This name is very common, is it a brand ?"),
                                            resource='https://nsi.guide/', **doc)

        self.frequent_names_from_nsi = self._get_frequent_names()
        self.brands_from_nsi = self._get_brands()

    def _get_frequent_names(self):
        nsi_url_for_names = "https://raw.githubusercontent.com/osmlab/name-suggestion-index/master/dist/names_keep.json"
        json_str = urlread(nsi_url_for_names, 30)
        results = json.loads(json_str)
        return [elem.lower() for elem in results.keys()]

    def _get_brands(self):
        nsi_url_for_brands = "https://raw.githubusercontent.com/osmlab/name-suggestion-index/master/dist/brands.json"
        json_str = urlread(nsi_url_for_brands, 30)
        results = json.loads(json_str)
        additional_brands = {}
        for brand_nsi_name, brand in results["brands"].items():
            if "matchTags" in brand:
                for additional_tag in brand["matchTags"]:
                    nsi_key = "{}|{}".format(additional_tag, brand_nsi_name.split("|")[1])
                    additional_brands[nsi_key.lower()]=brand
            if "matchNames" in brand:
                for additional_name in brand["matchNames"]:
                    nsi_key = "{}|{}".format(brand_nsi_name.split("|")[0], additional_name)
                    additional_brands[nsi_key.lower()]=brand
            additional_brands[brand_nsi_name.lower()]=brand
        return additional_brands

    def node(self, data, tags):
        if "name" in tags and not "brand" in tags:
            for main_key in ["shop", "amenity"]:
                if main_key in tags :
                    nsi_key = "{}/{}|{}".format(main_key, tags[main_key], tags["name"]).lower()
                    if nsi_key in self.frequent_names_from_nsi:
                        if nsi_key in self.brands_from_nsi.keys():
                            brands_tags = self.brands_from_nsi[nsi_key]["tags"]
                            tags_to_add = {}
                            for tag in brands_tags:
                                if not tags.get(tag):
                                    tags_to_add[tag] = brands_tags[tag]
                            return {"class": 31301, "subclass": 0,
                                "fix": {"+": tags_to_add }}
                        else:
                            return {"class": 31301, "subclass": 1,
                                "fix": {"+": {"brand": tags["name"]}}}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################


class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Brand(None)
        a.init(None)

        assert a.node(None, {"name": "Kiabi", "shop":"clothes"})
        assert not a.node(None, {"brand": "Kiabi", "shop":"clothes", "name":"Kiabi"})
