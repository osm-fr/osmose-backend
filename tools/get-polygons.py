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
    else:
      list_polygons.append(str(country.polygon_id))

list_polygons = set(list_polygons)

print ",".join(list_polygons)

