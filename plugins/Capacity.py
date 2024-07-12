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

from modules.Stablehash import stablehash64
from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from plugins.Plugin import TestPluginCommon
from plugins.modules.units import parseNumberUnitString
import re

class Capacity(Plugin):
    def init(self, logger):
        Plugin.init(self, logger)

        self.errors[30912] = self.def_class(
            item=3091,
            level=2,
            tags=["tag"],
            title=T_("Invalid capacity value"),
            detail=T_("""Capacity tags should be positive integers. For some objects it can also be used to indicate the effective volume of that object (by default in m³)."""),
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

        # Officially only m³ and l are supported
        self.re_volumeUnits = re.compile(r'''
            \w[3³]$ # Assume anything that ends with a 3 is a volume
            |^cu(bic)?\s # Anything that starts with cu(bic) is a volume
            |^([mcdhkMGT]|da|milli|centi|deci|deca|hecto|kilo|mega|tera)?[lL](it(er|re)s?)?$ # liter
            |\b[gG]al(lon)?s?$ # gallons
            |\bbar(rels?)?$ # barrels
            |^(k|M{1,2}|G)?(bbl|cf)$ # imperial abbreviations with k, M, MM, G prefixes
        ''', re.X)

    def node(self, data, tags):
        errors = []
        if ("capacity" not in tags
                # Ignore errors that should be reported by generic analysers
                or tags["capacity"] in ("", "unknown")):
            return []

        c = parseNumberUnitString(tags["capacity"])
        if c is None:
            # Not parseable as a numeric value
            return [{
                "class": 30912,
                "subclass": stablehash64('6capacity'),
                "text": T_('"{0}" value "{1}" is not an integer nor a volume', "capacity", tags["capacity"]),
            }]

        if c["value"] < 0:
            # Whether volume or integer, capacity should never be < 0
            errors.append({
                "class": 30912,
                "subclass": stablehash64('5capacity'),
                "text": T_('"{0}" value "{1}" is negative', "capacity", tags["capacity"]),
            })

        # Exclude tags that are likely volumes. Volumes don't have to be integers and can be unitless (meaning m³, the default)
        if "man_made" in tags or "water" in tags or ("amenity" in tags and tags["amenity"] in ("waste_disposal", "recycling", "grit_bin", "waste_basket")):
            return errors

        if c["unit"] is not None:
            # If a unit is specified it should be a volume. Tags like "capacity=1 bus" are bad, they should be capacity:bus=1
            if not re.search(self.re_volumeUnits, c["unit"]):
                errors.append({
                    "class": 30912,
                    "subclass": stablehash64('7capacity'),
                    "text": T_('"{0}" value "{1}" is not an integer nor a volume', "capacity", tags["capacity"]),
                })
            return errors

        total_capacity = None
        if errors == []:
            try:
                # Not using c["value"] (a float) here because int(30.000) won't error, but int("30.000") will
                total_capacity = int(tags["capacity"])
            except:
                errors.append({
                    "class": 30912,
                    "subclass": stablehash64('4capacity'),
                    "text": T_('"{0}" value "{1}" is not an integer', "capacity", tags["capacity"]),
                })

        for key, value in tags.items():
            if (
                not key.startswith("capacity:")
                # Ignore errors that should be reported by generic prefix analysers
                or key == "capacity:"
                or value in ("", "yes", "no", "unknown")
            ):
                continue

            try:
                capacity_int = int(value)
                if total_capacity is not None and capacity_int > total_capacity:
                    errors.append({
                        "class": 30913,
                        "subclass": stablehash64('1' + key),
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
                        "subclass": stablehash64('5' + key),
                        "text": T_('"{0}" value "{1}" is negative', key, value),
                    })
            except ValueError:
                errors.append({
                    "class": 30912,
                    "subclass": stablehash64('4' + key),
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

        self.check_err(a.node(None, {"capacity": "a"}), expected={"class": 30912})
        self.check_err(a.node(None, {"capacity": "3 ducks"}), expected={"class": 30912})
        self.check_err(a.node(None, {"capacity": "-2 L"}), expected={"class": 30912})
        self.check_err(a.node(None, {"capacity": "-1"}), expected={"class": 30912})
        self.check_err(a.node(None, {"capacity": "-0.1"}), expected={"class": 30912})
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "-1"}),
            expected={"class": 30912},
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "a", "amenity": "parking"}),
            expected={"class": 30912},
        )
        self.check_err(
            a.node(None, {"capacity": "1", "capacity:disabled": "2"}),
            expected={"class": 30913},
        )
        self.check_err(
            a.node(None, {"capacity": "3", "capacity:disabled": "2.5"}),
            expected={"class": 30912},
        )
        self.check_err(
            a.node(None, {"capacity": "1.8", "amenity": "parking"}),
            expected={"class": 30912},
        )
        self.check_err(
            a.node(None, {"capacity": "30.000", "leisure": "stadium"}),
            expected={"class": 30912},
        )

        assert not a.node(None, {"amenity": "restaurant"})
        assert not a.node(None, {"capacity": "1"})
        assert not a.node(None, {"capacity": "1", "capacity:wheelchair": "1"})

        assert not a.node(None, {"capacity:": "1"})
        assert not a.node(None, {"capacity:": ""})
        assert not a.node(None, {"capacity": ""})

        assert not a.node(None, {"capacity": "1", "capacity:": "a"})
        assert not a.node(None, {"capacity:wheelchair": "1"})

        assert not a.node(None, {"capacity": "123.45 l", "new_tag": "something_storage_related_not_whitelisted_yet"})
        assert not a.node(None, {"capacity": "123.45 m³", "new_tag": "something_storage_related_not_whitelisted_yet"})
        assert not a.node(None, {"capacity": "123.45 m³", "man_made": "water_tower"})
        assert not a.node(None, {"capacity": "123.45", "amenity": "waste_disposal"})
