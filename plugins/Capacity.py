from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from plugins.Plugin import TestPluginCommon

###########################################################################
##                                                                       ##
## Copyrights Éric Gillet 2020                                           ##
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


class Capacity(Plugin):
    def init(self, logger):
        Plugin.init(self, logger)

        self.errors[35001] = self.def_class(
            item=3500,
            level=2,
            tags=["tag"],
            title=T_("Invalid capacity value"),
            detail=T_("""A capacity tag value is incorrect."""),
            resource="https://wiki.openstreetmap.org/wiki/Key:capacity",
        )

    def node(self, data, tags):
        if ("capacity" not in tags
                # Ignore errors that should be reported by generic prefix analysers
                or tags["capacity"] == ""):
            return
        try:
            total_capacity = int(tags["capacity"])
        except ValueError:
            return {
                "class": 35001,
                "subclass": 0,
                "text": T_('Invalid "{0}" value: {1}', "capacity", tags["capacity"]),
            }

        if total_capacity < 0:
            return {
                "class": 35001,
                "subclass": 0,
                "text": T_('Invalid "{0}" value: {1}', "capacity", total_capacity),
            }

        for key, value in tags.items():
            if (
                not key.startswith("capacity:")
                # Ignore errors that should be reported by generic prefix analysers
                or key == "capacity:"
                or value == ""
                or value in ("yes", "no")
            ):
                continue

            try:
                capacity_int = int(value)
            except ValueError:
                return {
                    "class": 35001,
                    "subclass": 0,
                    "text": T_('Invalid "{0}" value: {1}', key, value),
                }

            if capacity_int > total_capacity:
                return {
                    "class": 35001,
                    "subclass": 1,
                    "text": T_(
                        'Specific "{0}" value {1} is larger than total capacity {2}',
                        key,
                        value,
                        total_capacity,
                    ),
                }
            if capacity_int < 0:
                return {
                    "class": 35001,
                    "subclass": 0,
                    "text": T_('Invalid "{0}" value: {1}', key, tags["capacity"]),
                }

    def way(self, data, tags, nds):
        # Same check as node
        return self.node(data, tags)

    def relation(self, data, tags, members):
        # Same check as node
        return self.node(data, tags)


class Test(TestPluginCommon):
    def test(self):
        a = Capacity(None)
        a.init(None)

        self.check_err(a.node(None, {"capacity": "a"}), {"class": 35001, "subclass": 0})
        self.check_err(
            a.node(None, {"capacity": "-1"}), {"class": 35001, "subclass": 0}
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "-1"}),
            {"class": 35001, "subclass": 1},
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "a"}),
            {"class": 35001, "subclass": 1},
        )

        assert a.node(None, {"amenity": "restaurant"}) is None
        assert a.node(None, {"capacity": "1", "capacity:wheelchair": "1"}) is None
        assert a.node(None, {"capacity:": "1"}) is None
        assert a.node(None, {"capacity:": ""}) is None
        assert a.node(None, {"capacity": ""}) is None

        assert a.node(None, {"capacity": "1", "capacity:": "a"}) is None
        assert a.node(None, {"capacity:wheelchair": "1"}) is None
        assert a.node(None, {"capacity:wheelchair": "1"}) is None
