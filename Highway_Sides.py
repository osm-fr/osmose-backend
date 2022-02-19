#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights osmose project 2022                                        ##
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

class Highway_Sides(Plugin):
    def init(self, logger):
        Plugin.init(self, logger)

        self.errors[33601] = self.def_class(item = 3360, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Conflicting tag values'),
            detail = T_(
'''A tag with `:right`, `:left` or `:both` conflicts with the same tag without side specification, or a tag with `:right` or `:left` conflicts with the tag with `:both`.'''))


    def way(self, data, tags, nds):
        if not "highway" in tags:
            return
        err = []

        for tag in tags:
            if tag[-5:] == ":both":
              tag_default = tag[0:-5] # special handling because :both_ways also exists
            else:
              tag_default = tag.replace(":both:", ":").replace(":left", "").replace(":right", "")
            if tag_default == tag:
                continue # tag does not contain :both/:left/:right
            allowedAlternativeValues = []
            if tag_default in tags:
                # Some tags allow left/right/both as values, e.g. sidewalk=both equals sidewalk:both=yes
                allowedAlternativeValues = ["left", "right", "both", "yes"]
            else:
                tag_default = tag.replace(":left", ":both").replace(":right", ":both")
            if tag_default in tags:
                tt = tags[tag].replace("none", "no").replace("opposite_", "")
                ttd = tags[tag_default].replace("none", "no").replace("opposite_", "")
                if tt != ttd and not ttd in allowedAlternativeValues:
                    err.append({"class": 33601, "subclass": 1 + stablehash64(tag), "text": T_("Conflicting values of \"{0}\" and \"{1}\"", tag_default, tag)})

        if err != []:
            return err


from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Highway_Sides(None)
        a.init(None)

        for t in [{"highway": "residential", "cycleway:right": "lane"},
                  {"highway": "residential", "cycleway:right": "lane", "cycleway:left": "lane"},
                  {"highway": "residential", "cycleway": "lane"},
                  {"highway": "residential", "cycleway:right": "lane", "cycleway": "lane"}, # redundant, not conflicting
                  {"highway": "residential", "cycleway:right:surface": "asphalt", "cycleway:surface": "asphalt"}, # redundant, not conflicting
                  {"highway": "residential", "cycleway:right:surface": "asphalt", "cycleway:both:surface": "asphalt"}, # redundant, not conflicting
                  {"highway": "residential", "sidewalk": "left", "sidewalk:left": "yes"}, # redundant, not conflicting
                  {"highway": "residential", "sidewalk:both": "yes", "sidewalk:left": "yes"}, # redundant, not conflicting
                  {"highway": "residential", "sidewalk": "yes", "sidewalk:left": "yes", "sidewalk:right": "yes", "sidewalk:both": "yes"}, # redundant, not conflicting
                  {"highway": "residential", "sidewalk": "right", "sidewalk:left": "no"}, # redundant, not conflicting
                  {"highway": "residential", "sidewalk": "none", "sidewalk:left": "no"}, # redundant, not conflicting
                  {"highway": "residential", "cycleway": "opposite_lane", "cycleway:left": "lane"}, # dubious whether equal
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "residential", "cycleway:right": "lane", "cycleway": "shared_lane"},
                  {"highway": "residential", "sidewalk": "no", "sidewalk:left": "yes"},
                  {"highway": "residential", "sidewalk:both": "yes", "sidewalk:left": "no"},
                  {"highway": "residential", "cycleway:both:surface": "asphalt", "cycleway:surface": "paving_stones"},
                  {"highway": "residential", "cycleway:right:surface": "asphalt", "cycleway:surface": "paving_stones"},
                 ]:
            assert a.way(None, t, None), a.way(None, t, None)

        # Ensure xxx:both_ways is harmless
        t = {"highway": "residential", "xxx:both_ways": "yyy", "xxx_ways": "zzz", "xxx": "zzz"}
        assert not a.way(None, t, None), a.way(None, t, None)
