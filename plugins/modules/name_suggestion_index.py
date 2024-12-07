#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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


# This module file contains functions to read out the data from the
# name suggestion index (NSI) for Osmose - https://nsi.guide/

from modules.downloader import urlread
import json


# Downloads and returns the parsed NSI database
def download_nsi():
    nsi_url = "https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/dist/nsi.json"
    json_str = urlread(nsi_url, 30)
    results = json.loads(json_str)
    return results['nsi']


# Countries in NSI with different ids or spanning multiple Osmose extracts
_nsi_to_osmose_map = {
    # China
    "hk": ["cn-91"], # Hong Kong
    "mo": ["cn-92"], # Macau
    # France
    "fr-ara": [f"fr-{d:02}" for d in [1, 3, 7, 15, 26, 38, 42, 43, 63, 69, 73, 74]],  # Auvergne-Rhône-Alpes
    "fr-bfc": [f"fr-{d:02}" for d in [21, 25, 39, 58, 70, 71, 89, 90]],  # Bourgogne-Franche-Comté
    "fr-bre": [f"fr-{d:02}" for d in [22, 29, 35, 56]],  # Bretagne
    "fr-cvl": [f"fr-{d:02}" for d in [18, 28, 36, 37, 41, 45]],  # Centre-Val de Loire
    "fr-ges": [f"fr-{d:02}" for d in [8, 10, 51, 52, 54, 55, 57, 67, 68, 88]],  # Grand Est
    "fr-hdf": [f"fr-{d:02}" for d in [2, 59, 60, 62, 80]],  # Hauts-de-France
    "fr-idf": [f"fr-{d:02}" for d in [75, 77, 78, 91, 92, 93, 94, 95]],  # Île-de-France
    "fr-nor": [f"fr-{d:02}" for d in [14, 27, 50, 61, 76]],  # Normandie
    "fr-naq": [f"fr-{d:02}" for d in [16, 17, 19, 23, 24, 33, 40, 47, 64, 79, 86, 87]],  # Nouvelle-Aquitaine
    "fr-occ": [f"fr-{d:02}" for d in [9, 11, 12, 30, 31, 32, 34, 46, 48, 65, 66, 81, 82]],  # Occitanie
    "fr-pac": [f"fr-{d:02}" for d in [4, 5, 6, 13, 83, 84]],  # Provence-Alpes-Côte d'Azur
    "fr-pdl": [f"fr-{d:02}" for d in [44, 49, 53, 72, 85]],  # Pays de la Loire
    "fr-20r": ["fr-2a", "fr-2b"],  # Corse
    "fx": ['fr-2a', 'fr-2b'] + [f"fr-{d:02}" for d in range(1,96)], # continental France
    "gf": ["fr-gf"], # French Guiana
    "gp": ["fr-gp"], # Guadeloupe
    "mf": ["fr-mf"], # Saint-Martin, French part
    "mq": ["fr-mq"], # Martinique
    "pf": ["fr-pf"], # French Polynesia
    "re": ["fr-re"], # Réunion
    "yt": ["fr-yt"], # Mayotte
    # Other
    "el": ["gr"], # Greece
    "ic": ["es-gc", "es-tf"], # Canary Islands
    "id-jw": ["id-jb", "id-ji", "id-jt", "id-jk", "id-bt"], # Java
    "ja": ["jm"], # Jamaica
    "kv": ["xk"], # Kosovo
    "pi": ["ph"], # Philippines
    "ra": ["ar"], # Argentina
    "us-vi": ["vi"], # Virgin Islands
}

# Convert NSI country codes to Osmose country codes if possible
def _nsi_to_osmose_extracts(regionlist):
    out = []
    if not regionlist:
        return out
    for c in regionlist:
        if not isinstance(c, str):
            continue # Coordinates (with optional radius) rather than an extract, unsupported
        c = c.lower().replace('.geojson', '', 1)
        if c in _nsi_to_osmose_map:
            out.extend(_nsi_to_osmose_map[c])
        else:
            out.append(c)
    return out


# Check if the locationSet object from NSI matches the country
def nsi_rule_applies(locationSet, country):
    if not "include" in locationSet and not "exclude" in locationSet:
        return True
    incl = _nsi_to_osmose_extracts(locationSet.get("include"))
    excl = _nsi_to_osmose_extracts(locationSet.get("exclude"))
    # For extract with country="AB-CD-EF", check "AB-CD-EF", then "AB-CD", then "AB", then worldwide ("001")
    for c in ['-'.join(country.lower().split("-")[:i]) for i in range(country.count("-")+1, 0, -1)]:
        if c in excl:
            return False
        if c in incl:
            return True
    return len(incl) == 0 or "001" in locationSet["include"]


# Gets all valid (shop, amenity, ...) names that exist within a certain country
# country: the lowercase 2-letter country code of the country of interest
# nsi: the parsed NSI database obtained from download_nsi()
# nsiprefix: 'brands/', 'operators/', 'flags/' or 'transit/'
def whitelist_from_nsi(country, nsi = download_nsi(), nsiprefix = 'brands/'):
    whitelist = set()
    for tag, details in nsi.items():
        if tag.startswith(nsiprefix) and "items" in details:
            for preset in details["items"]:
                if "locationSet" in preset and not nsi_rule_applies(preset["locationSet"], country):
                    continue
                if "name" in preset["tags"]:
                    whitelist.add(preset["tags"]["name"])
                whitelist.add(preset["displayName"])
    return whitelist




# Get a list of regions in NSI that aren't covered yet
#import osmose_config as o_c
#_debug_osmose_countries = list(filter(None, map(lambda c: c.analyser_options.get("country"), o_c.config.values())))
#_debug_osmose_missing_countries = set()
#def _debug_list_unsupported_countries(cc):
#    if isinstance(cc, str):
#        cc = cc.replace('.geojson', '', 1).upper()
#        if cc not in _debug_osmose_countries and cc.lower() not in _nsi_to_osmose_map and not any(filter(lambda c: c.startswith(cc + "-"), _debug_osmose_countries)):
#            _debug_osmose_missing_countries.add(cc.lower())
#nsi = download_nsi()
#for details in nsi.values():
#    if "items" in details:
#        for preset in details["items"]:
#            if "locationSet" in preset:
#                list(map(_debug_list_unsupported_countries, preset["locationSet"].get("include", [])))
#                list(map(_debug_list_unsupported_countries, preset["locationSet"].get("exclude", [])))
#print("Unsupported countries from NSI: " + ", ".join(sorted(_debug_osmose_missing_countries)))
