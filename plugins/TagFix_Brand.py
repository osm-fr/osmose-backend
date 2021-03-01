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

from modules.OsmoseTranslation import T_
from plugins.Plugin import TestPluginCommon
from plugins.Plugin import Plugin
from modules.downloader import urlread
import json


class TagFix_Brand(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31301] = self.def_class(item=3130, level=3, tags=['brand'],
            title=T_("This name is very common, is this store part of the brand network?"),
            detail=T_(
'''This object has a very common name that probably corresponds to a brand name. All objects of the same brand should be tagged the same way.'''),
            fix=T_(
'''If this is indeed a brand, add `brand` and `brand:wikidata` tags.
If not, see if you can improve the [name-suggestion-index project](https://github.com/osmlab/name-suggestion-index/blob/master/CONTRIBUTING.md) which is used to link frequent names to brands and their tags.'''),
            resource="https://nsi.guide/")

        self.errors[31302] = self.def_class(item=3130, level=3, tags=['operator'],
            title=T_("Operator can be completed with operator:wikidata"),
            detail=T_(
'''The name of the operator on this object is generally associated with additional tags, especially operator:wikidata. All objects with the same operator should be tagged the same way.'''),
            fix=T_(
'''If this is indeed the operator in question, add `operator:wikidata`.
If not, see if you can improve the [name-suggestion-index project](https://github.com/osmlab/name-suggestion-index/blob/master/CONTRIBUTING.md) which is used to register common operators.'''),
            resource="https://nsi.guide/")

        if not self.father.config.options.get("country"):
            return False
        self.country_code = self.father.config.options.get("country").split("-")[0].lower()

        nsi = self._download_nsi()
        self.brands_from_nsi = self._parse_category_from_nsi(nsi, "brands/", "brand")
        self.operators_from_nsi = self._parse_category_from_nsi(nsi, "operators/", "operator")

    def _download_nsi(self):
        nsi_url = "https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/dist/nsi.json"
        json_str = urlread(nsi_url, 30)
        results = json.loads(json_str)
        return results['nsi']

    def _parse_category_from_nsi(self, nsi, nsiprefix, key):
        additional_presets = {}
        for tag, details in nsi.items():
            if tag.startswith(nsiprefix) and "items" in details:
                nsi_name = tag[len(nsiprefix):]
                for preset in details["items"]:
                    if "locationSet" in preset:
                        if ("include" in preset["locationSet"] and
                                self.country_code not in preset["locationSet"]["include"] and
                                "001" not in preset["locationSet"]["include"]):
                            continue
                        if "exclude" in preset["locationSet"] and self.country_code in preset["locationSet"]["exclude"]:
                            continue
                    if "matchTags" in preset:
                        for additional_tag in preset["matchTags"]:
                            nsi_key = "{}|{}".format(additional_tag, preset["tags"][key])
                            additional_presets[nsi_key.lower()] = preset
                    if "matchNames" in preset:
                        for additional_name in preset["matchNames"]:
                            nsi_key = "{}|{}".format(nsi_name, additional_name)
                            additional_presets[nsi_key.lower()] = preset
                    if "name" in preset["tags"]:
                        additional_presets["{}|{}".format(nsi_name, preset["tags"]["name"]).lower()] = preset
                    additional_presets["{}|{}".format(nsi_name, preset["displayName"]).lower()] = preset
        return additional_presets

    def node(self, data, tags):
        if "name" in tags and (not "brand" in tags or not "brand:wikidata" in tags):
            for main_key in ["shop", "amenity"]:
                if main_key in tags:
                    if "brand" in tags:
                        nsi_key = "{}/{}|{}".format(main_key, tags[main_key], tags["brand"]).lower()
                    else:
                        nsi_key = "{}/{}|{}".format(main_key, tags[main_key], tags["name"]).lower()
                    if nsi_key in self.brands_from_nsi:
                        brands_tags = self.brands_from_nsi[nsi_key]["tags"]
                        tags_to_add = {}
                        for tag in brands_tags:
                            if not tags.get(tag):
                                tags_to_add[tag] = brands_tags[tag]
                        if tags_to_add:
                            return {"class": 31301, "subclass": 0, "fix": {"+": tags_to_add}}

        if "operator" in tags and not "operator:wikidata" in tags:
            for main_key in ["shop", "amenity", "emergency"]:
                if main_key in tags:
                    nsi_key = "{}/{}|{}".format(main_key, tags[main_key], tags["operator"]).lower()
                    if nsi_key in self.operators_from_nsi:
                        operators_tags = self.operators_from_nsi[nsi_key]["tags"]
                        tags_to_add = {}
                        for tag in operators_tags:
                            if not tags.get(tag):
                                tags_to_add[tag] = operators_tags[tag]
                        if tags_to_add:
                            return {"class": 31302, "subclass": 0, "fix": {"+": tags_to_add}}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################


class Test(TestPluginCommon):
    def test_FR(self):
        a = TagFix_Brand(None)
        class _config:
            options = {"country": "FR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        # Brands
        assert a.node(None, {"name": "Kiabi", "shop": "clothes"})
        assert a.node(None, {"name": "Kiabi", "shop": "clothes", "brand": "Kiabi"})
        assert not a.node(None, {"brand": "Kiabi", "shop": "clothes", "name": "Kiabi","brand:wikidata": "Q3196299"})
        assert not a.node(None, {"name": "National Bank", "amenity": "bank", "atm": "yes"})

        # Operators
        assert a.node(None, {"name": "Beautify fire station", "amenity": "fire_station", "operator": "Bataillon de marins-pompiers de Marseille"})
        assert not a.node(None, {"name": "Beautify fire station", "amenity": "fire_station", "operator": "Bataillon de marins-pompiers de Marseille", "operator:wikidata": "Q2891011"})
        assert not a.node(None, {"name": "Beautify fire station", "amenity": "fire_station", "operator": "Unknown firestation"})


    def test_CA(self):
        a = TagFix_Brand(None)
        class _config:
            options = {"country": "CA"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert a.node(None, {"name": "National Bank", "amenity": "bank", "atm": "yes"})
