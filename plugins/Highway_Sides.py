#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Osmose project 2022                                        ##
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
            title = T_('Conflicting tags for sides of the way'),
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
              tag_default = tag.replace(":both:", ":", 1).replace(":left", "", 1).replace(":right", "", 1)
            if tag_default == tag:
                continue # tag does not contain :both/:left/:right
            allowedAlternativeValues = []
            if tag_default in tags:
                # Some tags allow left/right/both as values, e.g. sidewalk=both equals sidewalk:both=yes
                if self.simplifyValue(tags[tag]) == "no":
                    allowedAlternativeValues = ["separate", "opposite"]
                    if "both" not in tag.split(":"):
                        allowedAlternativeValues.extend(["yes"] + list(filter(lambda t: t not in tag.split(":"), ["left", "right"])))
                else:
                    allowedAlternativeValues = ["yes", "left", "right", "both"]
            else:
                tag_default = tag.replace(":left", ":both", 1).replace(":right", ":both", 1)

            if tag_default in tags:
                tt = self.simplifyValue(tags[tag])
                ttd = self.simplifyValue(tags[tag_default])
                if tag[0:5] == "name:" and tt in ttd:
                    continue # 'name' probably equals "name:left" + "/" + name:right, handled by Name_Multiple
                if tt != ttd and not ttd in allowedAlternativeValues:
                    err.append({"class": 33601, "subclass": 1 + stablehash64(tag), "text": T_("Conflicting values of \"{0}\" and \"{1}\"", tag_default, tag)})

        if err != []:
            return err

    def simplifyValue(self, val):
        if val in ["none"]:
            return "no"
        return val.replace("opposite_", "", 1)


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
                  {"highway": "residential", "name": "StreetA / StreetB", "name:left": "StreetA", "name:right": "StreetB"},
                  {"highway": "residential", "cycleway": "opposite_lane", "cycleway:left": "lane"}, # dubious whether equal, but opposite* is deprecated anyway
                  {"highway": "residential", "cycleway": "opposite", "cycleway:left": "no"}, # dubious whether equal, but opposite* is deprecated anyway
                  {"highway": "residential", "cycleway": "opposite", "cycleway:both": "no"}, # dubious whether equal, but opposite* is deprecated anyway
                  {"highway": "residential", "sidewalk": "separate", "sidewalk:left": "separate", "sidewalk:right": "no"},
                  {"highway": "residential", "sidewalk": "yes", "sidewalk:right": "no", "sidewalk:left": "yes"},
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "residential", "cycleway:right": "lane", "cycleway": "shared_lane"},
                  {"highway": "residential", "sidewalk": "no", "sidewalk:left": "yes"},
                  {"highway": "residential", "sidewalk": "separate", "sidewalk:left": "yes", "sidewalk:right": "separate"},
                  {"highway": "residential", "sidewalk:both": "separate", "sidewalk:left": "separate", "sidewalk:right": "no"},
                  {"highway": "residential", "sidewalk:both": "yes", "sidewalk:left": "no"},
                  {"highway": "residential", "cycleway:both:surface": "asphalt", "cycleway:surface": "paving_stones"},
                  {"highway": "residential", "cycleway:right:surface": "asphalt", "cycleway:surface": "paving_stones"},
                  {"highway": "residential", "sidewalk": "both", "sidewalk:right": "no"},
                  {"highway": "residential", "sidewalk": "left", "sidewalk:left": "no"},
                  {"highway": "residential", "sidewalk": "left", "sidewalk:both": "no"},
                 ]:
            assert a.way(None, t, None), a.way(None, t, None)

        # Ensure xxx:both_ways is harmless
        t = {"highway": "residential", "xxx:both_ways": "yyy", "xxx_ways": "zzz", "xxx": "zzz"}
        assert not a.way(None, t, None), a.way(None, t, None)
