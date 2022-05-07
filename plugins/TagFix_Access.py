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

class TagFix_Access(Plugin):
  def init(self, logger):
    Plugin.init(self, logger)

    self.suffixesNode = ["", ":conditional"]
    self.suffixesWay = []
    for d in ["", ":forward", ":backward", ":both_ways"]:
      self.suffixesWay.append(d)
      self.suffixesWay.append(d + ":conditional")

    # Note: emergency is excluded as it's also for hospital facilities
    self.accessKeys = ["4wd_only", "access", "agricultural", "atv", "bdouble", "bicycle", "boat", "bus", "canoe", "caravan", "carriage", "coach", "disabled", "dog", "foot", "golf_cart", "goods", "hazmat",
                       "hazmat:water", "hgv", "horse", "hov", "inline_skates", "light_rail", "minibus", "mofa", "moped", "motor_vehicle", "motorboat", "motorcar", "motorcycle", "motorhome", "psv",
                       "share_taxi", "ship", "ski:nordic", "ski", "small_electric_vehicle", "snowmobile", "speed_pedelec", "subway", "swimming", "tank", "taxi", "tourist_bus", "trailer", "train", "tram", "vehicle"]
    self.accessValuesGeneral = ["yes", "no", "private", "permissive", "permit", "destination", "delivery", "customers", "designated", "use_sidepath", "dismount", "agricultural", "forestry", "discouraged"]

    self.errors[33701] = self.def_class(item = 3370, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Uncommon access value'),
        detail = T_('''The value of the access tag is not one of the common access values: `{0}`.''', ", ".join(self.accessValuesGeneral)),
        resource="https://wiki.openstreetmap.org/wiki/Key:access",
        trap = T_('''If there is no other tag (or combination of tags) that properly describes the access permissions, custom tags may be used.'''))
    self.errors[33702] = self.def_class(item = 3370, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Transport mode in access value'),
        detail = T_('''The value of the access tag is a transport mode (such as `access=foot`). Consider replacing it with a more specific tag listing the transport mode first, for example `access=no` + `foot=yes`.'''),
        trap = T_('''Ensure that the access remains the same and does not conflict with other tags. This is especially likely if access tags are combined with directional and/or conditional access tags, or when transport modes are mixed with regular access values.'''),
        resource="https://wiki.openstreetmap.org/wiki/Key:access")


  def checkAccessKeys(self, tags, suffixes):
    err = []
    accessTags = {}
    for accesskey in self.accessKeys:
      for suffix in suffixes:
        if accesskey + suffix in tags:
          accessTags[accesskey + suffix] = {"transportMode": accesskey, "value": tags[accesskey + suffix], "suffix": suffix}

    for tag in accessTags:
      values = accessTags[tag]["value"].split(";")
      for accessVal in values:
        accessValue = accessVal
        if ":conditional" in tag and "@" in accessValue:
          accessValue = accessValue.split("@")[0].strip()
        accessValue = accessValue.strip()
        if not accessValue in self.accessValuesGeneral:
          if accessValue in self.accessKeys or accessValue == "emergency":
            propose = tag + " = ### + " + accessValue + accessTags[tag]["suffix"] + " = yes"
            if len(values) > 1 or "@" in accessVal:
              propose = propose.replace("###", "...") # i.e. access=bus;destination should become access=destination + bus=yes instead of access=no + bus=yes
            else:
              propose = propose.replace("###", "no") # assume 'no' holds for all other transport modes
            if "@" in accessVal:
              propose = propose + " @ (...)" # conditional may need to change
            err.append({"class": 33702, "subclass": 0 + stablehash64(tag + '|' + accessValue), "text": T_("Access value \"{0}\" for key \"{1}\" is a transport mode. Consider using \"{2}\" instead", accessValue, tag, propose)})
          else:
            err.append({"class": 33701, "subclass": 0 + stablehash64(tag + '|' + accessValue), "text": T_("Unknown access value \"{0}\" for key \"{1}\"", accessValue, tag)})

    if err != []:
      return err

  def way(self, data, tags, nds):
    return self.checkAccessKeys(tags, self.suffixesWay)

  def node(self, data, tags):
    return self.checkAccessKeys(tags, self.suffixesWay)

  def relation(self, data, tags, members):
    pass


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Access(None)
        a.init(None)

        # Valid nodes and ways
        for t in [{"amenity": "parking", "vehicle": "no"},
                  {"amenity": "parking", "vehicle:conditional": "no @ wet"},
                 ]:
          assert not a.way(None, t, None), a.way(None, t, None)
          assert not a.node(None, t), a.node(None, t)

        # Valid ways with directions
        for t in [{"highway": "residential", "vehicle:forward": "customers"},
                  {"highway": "residential", "vehicle:backward:conditional": "customers @ (wet); destination @ (snow)"},
                  {"highway": "residential", "vehicle:both_ways": "customers;destination"},
                  {"highway": "residential", "vehicle:both_ways": "customers; destination"},
                  {"highway": "residential", "bicycle:forward:conditional": "dismount@wet"},
                 ]:
          assert not a.way(None, t, None), a.way(None, t, None)

        # Invalid nodes and ways
        for t in [{"amenity": "parking", "vehicle": "nope"},
                  {"amenity": "parking", "vehicle:conditional": "nope @ wet"},
                 ]:
          assert a.way(None, t, None), a.way(None, t, None)
          assert a.node(None, t), a.node(None, t)

        # Invalid ways with directions
        for t in [{"highway": "residential", "vehicle:forward": "nope"},
                  {"highway": "residential", "vehicle:both_ways:conditional": "nope @ wet"},
                  {"highway": "residential", "horse:backward": "customers;nope"},
                  {"highway": "residential", "horse:backward": "nope; customers"},
                 ]:
          assert a.way(None, t, None), a.way(None, t, None)

        # Transport mode as tag value
        for t in [{"highway": "residential", "access": "foot"},
                  {"highway": "residential", "access:conditional": "foot @ yes"},
                  {"highway": "residential", "access:forward": "bus;foot"},
                  {"highway": "residential", "access": "bus; destination"},
                  {"highway": "residential", "access": "emergency"},
                 ]:
          assert a.way(None, t, None), a.way(None, t, None)
