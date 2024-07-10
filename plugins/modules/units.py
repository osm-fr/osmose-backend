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


# This module file contains functions to read and convert numbers with units

import re

_ftin_re = re.compile("^(-?)(?:(\\d+(?:\\.\\d+)?)(ft|')) ?(?:(\\d+(?:\\.\\d+)?)(in|\"))$") # Regex for combined feet/inch measures
_numunit_re = re.compile(r"^(-?\d+(?:\.\d+)?) ?(\D.*)?$") # Regex for any number followed by an optional unit
_si_prefixes = {
    "n": 1E-9, "u": 1E-6, "µ": 1E-6, "m": 0.001, "c": 0.01, "d": 0.1, "da": 10, "h": 100, "k": 1000, "M": 1E6, "G": 1E9, "T": 1E12,
    "nano": 1E-9, "micro": 1E-6, "milli": 0.001, "centi": 0.01, "deci": 0.1, "deca": 10, "hecto": 100, "kilo": 1000, "mega": 1E6, "giga": 1E9, "tera": 1E12,
}


# Converts strings that contain a number with a unit to a dict of {"value": float, "unit": string}
# Input:
#   string: the string to parse, e.g. "22.4 km"
#   defaultUnit: the unit if not specified (default: None)
# Returns:
#   None if conversion isn't possible
#   Otherwise a dict with keys:
#       value [float] - the number in the string
#       unit [string or None] - the unit
# For a string with multiple numbers/units, it converts it to a float of the largest unit (e.g. 3'4" becomes 3.33 ft)
def parseNumberUnitString(string, defaultUnit = None):
    if not string or not isinstance(string, str):
        return None
    string = string.strip()

    # Combined units: feet and inch
    m = re.fullmatch(_ftin_re, string)
    if m:
        return {
            "value": float(m.group(1) + m.group(2)) + float(m.group(1) + m.group(4))/12,
            "unit": "ft"
        }
    # Regular numbers with optional unit
    m = re.fullmatch(_numunit_re, string)
    if m:
        return {
            "value": float(m.group(1)),
            "unit": m.group(2) or defaultUnit
        }
    # Not a numerical value
    return None


# Converts a number in arbitrary units to the default unit
# Input:
#   x: either a string with a number + optional unit to parse, or a dict with value:[float] and unit:[string] keys
#   convertTo: the unit to convert the x-input to (the abbreviation)
#   If x is a string without unit, it assumes the default unit equals the unit of convertTo
# Returns:
#   None if the input was None or the string couldn't be parsed into a number + optional unit
#   The value [float] converted to convertTo units otherwise
# Throws:
#   If conversion wasn't possible
def convertToUnit(x, convertTo):
    if not isinstance(x, dict):
        # String input, extract value and unit
        x = parseNumberUnitString(x, convertTo)
    if not x:
        return None
    if x["unit"] == convertTo:
        return x["value"]

    # Length based conversions
    if convertTo == "m": # default for range, height, length
        if x["unit"] in ('ft', "'", 'foot', 'feet'):
            return x["value"] * 0.3048
        if x["unit"] in ('in', '"', 'inch', 'inches'):
            return x["value"] * 0.0254
        if x["unit"] == 'nmi':
            return x["value"] * 1852
        if x["unit"] in ('mi', 'mile', 'miles'):
            return x["value"] * 1609.344
        if x["unit"].replace('meters', 'meter', 1).endswith('meter'):
            return convertToUnit({"value": x["value"], "unit": x["unit"].rstrip("s")[0:-4]}, 'm')
        if x["unit"].endswith('m'):
            prefix = x["unit"][0:-1]
            if prefix in _si_prefixes:
                return x["value"] * _si_prefixes[prefix]
    if convertTo == "mm": # default for length (small scale)
        return convertToUnit(x, 'm') / _si_prefixes['milli']
    if convertTo == "km": # default for distance over land
        return convertToUnit(x, 'm') / _si_prefixes['kilo']
    if convertTo == "nmi": # default for distance over water
        return convertToUnit(x, 'm') / 1852

    raise NotImplementedError("Unknown conversion: {0} to {1}".format(str(x), convertTo))
