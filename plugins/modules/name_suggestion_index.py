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

# Gets all valid (shop, amenity, ...) names that exist within a certain country
# country: the lowercase 2-letter country code of the country of interest
# nsi: the parsed NSI database obtained from download_nsi()
# nsiprefix: 'brands/', 'operators/', 'flags/' or 'transit/'
def whitelist_from_nsi(country, nsi = download_nsi(), nsiprefix = 'brands/'):
    whitelist = set()
    for tag, details in nsi.items():
        if tag.startswith(nsiprefix) and "items" in details:
            for preset in details["items"]:
                if "locationSet" in preset:
                    if ("include" in preset["locationSet"] and
                            country not in preset["locationSet"]["include"] and
                            "001" not in preset["locationSet"]["include"]): # 001 = worldwide
                        continue
                    if "exclude" in preset["locationSet"] and country in preset["locationSet"]["exclude"]:
                        continue
                if "name" in preset["tags"]:
                    whitelist.add(preset["tags"]["name"])
                whitelist.add(preset["displayName"])
    return whitelist
