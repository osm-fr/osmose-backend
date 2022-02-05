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

        self.errors[30912] = self.def_class(
            item=3091,
            level=2,
            tags=["tag"],
            title=T_("Invalid capacity value"),
            detail=T_("""Capacity tags should be positive integers."""),
            resource="https://wiki.openstreetmap.org/wiki/Key:capacity",
        )
        self.errors[30913] = self.def_class(
            item=3091,
            level=2,
            tags=["tag"],
            title=T_("Specific capacity is greater than total capacity"),
            detail=T_("""A capacity:* value is greater than the total capacity."""),
            resource="https://wiki.openstreetmap.org/wiki/Key:capacity",
        )

    def node(self, data, tags):
        errors = []
        if ("capacity" not in tags
                # Ignore errors that should be reported by generic analysers
                or tags["capacity"] == ""):
            return []
        # capacity (non-round number in cubic meters or liters) is also for volumes: storage_tank, reservoir_covered, water_tower
        if "man_made" in tags:
            return []
        try:
            total_capacity = int(tags["capacity"])
            if total_capacity < 0:
                return [{
                    "class": 30913,
                    "subclass": 5,
                    "text": T_('"{0}" value "{1}" is negative', "capacity", total_capacity),
                }]
        except ValueError:
            errors.append({
                "class": 30912,
                "subclass": 4,
                "text": T_('"{0}" value "{1}" is not an integer', "capacity", tags["capacity"]),
            })
            total_capacity = None

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
                if total_capacity is not None and capacity_int > total_capacity:
                    errors.append({
                        "class": 30913,
                        "subclass": 1,
                        "text": T_(
                            'Specific "{0}" value "{1}" should be lower than total capacity {2}',
                            key,
                            value,
                            total_capacity,
                        ),
                    })

                if capacity_int < 0:
                    errors.append({
                        "class": 30912,
                        "subclass": 5,
                        "text": T_('"{0}" value "{1}" is negative', key, value),
                    })
            except ValueError:
                errors.append({
                    "class": 30912,
                    "subclass": 4,
                    "text": T_('"{0}" value "{1}" is not an integer', key, value),
                })
                continue

        return errors

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


class Test(TestPluginCommon):
    def test(self):
        a = Capacity(None)
        a.init(None)

        self.check_err(a.node(None, {"capacity": "a"}), {"class": 30912, "subclass": 4})
        self.check_err(
            a.node(None, {"capacity": "-1"}), {"class": 30912, "subclass": 5}
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "-1"}),
            {"class": 30912, "subclass": 5},
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "a"}),
            {"class": 30912, "subclass": 5},
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "2"}),
            {"class": 30913, "subclass": 1},
        )

        assert not a.node(None, {"amenity": "restaurant"})
        assert not a.node(None, {"capacity": "1"})
        assert not a.node(None, {"capacity": "1", "capacity:wheelchair": "1"})

        assert not a.node(None, {"capacity:": "1"})
        assert not a.node(None, {"capacity:": ""})
        assert not a.node(None, {"capacity": ""})

        assert not a.node(None, {"capacity": "1", "capacity:": "a"})
        assert not a.node(None, {"capacity:wheelchair": "1"})

        assert not a.node(None, {"capacity": "123.45 m³", "man_made": "water_tower"}
