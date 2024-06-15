#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose project 2024                                        ##
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
from modules.downloader import urlread


class TagFix_Tree(Plugin):

    def _read_leaf_properties_table(self):
        # The documented values, excluding:
        # - mixed leaf types/cycles: not compatible with `species`
        # - leaf_cycle = semi_*: might be climate dependent and unclear difference between semi_evergreen and semi_deciduous, see #2224 first comment
        allowed_leaf_type = ("broadleaved", "needleleaved", "leafless")
        allowed_leaf_cycle = ("evergreen", "deciduous")

        data = urlread(u"https://wiki.openstreetmap.org/w/index.php?title=Tag:natural%3Dtree/List_of_Species&action=raw", 1)
        data = list(map(lambda x: list(filter(lambda z: len(z) > 0, map(lambda y: y.strip(), x.split("|")))), data.split("|-")[1:-1]))
        species_map = {}
        for row in data: # data: list of [species, species:wikidata, leaf_cycle, leaf_type]
            this_species = {}
            if row[2] in allowed_leaf_cycle:
                this_species['leaf_cycle'] = row[2]
            if row[3] in allowed_leaf_type:
                this_species['leaf_type'] = row[3]
            if len(this_species) > 0:
                if len(row[1]) > 2 and row[1][0] == "Q":
                    this_species['species:wikidata'] = row[1]
                species_map[row[0]] = this_species
        return species_map

    def init(self, logger):
        Plugin.init(self, logger)

        self.errors[31201] = self.def_class(item = 3120, level = 3, tags = ['tree', 'natural', 'fix:chair'],
            title = T_('Conflicting tree properties'),
            detail = T_(
'''The leaf type and/or leaf cycle does not match with the species.'''),
            fix = T_(
'''Verify that the species is correct, before adding the leaf properties.'''),
            resource = 'https://wiki.openstreetmap.org/wiki/Tag:natural%3Dtree/List_of_Species')

        # Read the wiki
        self.species_map = self._read_leaf_properties_table()

    def _check_leaf_properties(self, tags):
        err = []

        if "species" in tags and tags["species"] in self.species_map:
            expected_tags = self.species_map[tags["species"]]

            if "leaf_cycle" in tags and tags["leaf_cycle"].startswith("semi_"):
                # Ignore leaf_cycle if it already has a value `semi_*`. This might be climate dependent,
                # and unclear difference between semi_evergreen and semi_deciduous, see #2224 first comment
                expected_tags = {x: expected_tags[x] for x in filter(lambda x: x != "leaf_cycle", expected_tags)}

            # The tags do not match with the data on the wiki. Don't check for wikidata (handled in item 3031)
            mismatches = set(filter(lambda t: t in tags and expected_tags[t] != tags[t] and t != "species:wikidata", expected_tags.keys()))
            if len(mismatches) > 0:
                err.append({
                    "class": 31201,
                    "text": T_("Conflict between `{0}` and `{1}`", "`, `".join(mismatches), "species"),
                    "fix": [
                        {"~": {x: expected_tags[x] for x in mismatches}, "+": {x: expected_tags[x] for x in list(filter(lambda t: t not in tags, expected_tags.keys()))}},
                        {"-": ["species"]}
                ]})

        return err

    def node(self, data, tags):
        if "natural" in tags and tags["natural"] == "tree":
            return self._check_leaf_properties(tags)

    def way(self, data, tags, nds):
        if "natural" in tags and tags["natural"] == "tree_row":
            return self._check_leaf_properties(tags)



###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Tree(None)
        a.init(None)

        for t in [{"natural": "tree"},
                  {"natural": "tree", "leaf_type": "broadleaved"},
                  {"natural": "tree", "leaf_cycle": "deciduous"},
                  {"natural": "tree", "leaf_cycle": "deciduous", "leaf_type": "broadleaved"},
                  {"natural": "tree", "leaf_cycle": "deciduous", "leaf_type": "broadleaved", "species": "Acer buergerianum"},
                  {"natural": "tree", "leaf_cycle": "semi_deciduous", "leaf_type": "broadleaved", "species": "Acer buergerianum"}, # Ignore semi_*, see #2224 first comment
                  {"natural": "tree", "leaf_cycle": "deciduous", "leaf_type": "broadleaved", "species": "Acer buergerianum", "species:wikidata": "Q941891"},
                  {"natural": "tree", "leaf_cycle": "deciduous", "leaf_type": "broadleaved", "species": "Acer buergerianum", "species:wikidata": "Q123456789"}, # Bad wikidata is handled by item 3031
                  {"natural": "tree", "leaf_cycle": "deciduous", "leaf_type": "broadleaved", "species": "Unknown species"},
                  {"natural": "tree", "species": "Unknown species"},
                 ]:
          assert not a.node(None, t), a.node(None, t)

        # Mismatching properties
        for t in [{"natural": "tree", "leaf_cycle": "deciduous", "leaf_type": "needleleaved", "species": "Acer buergerianum"},
                  {"natural": "tree", "leaf_cycle": "evergreen", "leaf_type": "broadleaved", "species": "Acer buergerianum"},
                  {"natural": "tree", "leaf_cycle": "evergreen", "leaf_type": "broadleaved", "species": "Acer buergerianum", "species:wikidata": "Q941891"},
                  {"natural": "tree", "leaf_cycle": "evergreen", "leaf_type": "needleleaved", "species": "Acer buergerianum"},
                  {"natural": "tree", "leaf_cycle": "evergreen", "species": "Acer buergerianum"},
                 ]:
            assert a.node(None, t), a.node(None, t)
