#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import sys
sys.path.append(".")
import osmose_config

list_polygons = []

for country in osmose_config.config.values():
  if country.polygon_id:
    if re.match("france_.*", country.country) and country.analyser_options["proj"] == 2154:
      list_polygons.append(str(1403916))
    elif re.match("^italy_.*", country.country):
      list_polygons.append(str(365331))
    elif re.match("^belgium_.*", country.country):
      list_polygons.append(str(52411))
    elif re.match("^netherlands_.*", country.country) and country.analyser_options["proj"] == 23032:
      list_polygons.append(str(47796))
    elif re.match("^czech_republic_.*", country.country):
      list_polygons.append(str(51684))
    elif re.match("^poland.*", country.country):
      list_polygons.append(str(49715))
    elif re.match("^germany.*", country.country):
      list_polygons.append(str(1111111))
    elif re.match("^spain_.*", country.country):
      list_polygons.append(str(1311341))
    elif re.match("^austria_.*", country.country):
      list_polygons.append(str(16239))
    elif re.match("^slovakia_.*", country.country):
      list_polygons.append(str(14296))
    elif re.match("^united_kingdom_england_.*", country.country):
      list_polygons.append(str(58447))
    elif re.match("^australia_.*", country.country):
      list_polygons.append(str(80500))
    elif re.match("^canada_.*", country.country):
      list_polygons.append(str(1428125))
    else:
      list_polygons.append(str(country.polygon_id))

list_polygons = set(list_polygons)

print(",".join(list_polygons))

