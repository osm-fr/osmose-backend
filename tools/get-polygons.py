#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append(".")
import osmose_config

list_polygons = []

for country in osmose_config.config.values():
  if country.polygon_id and country.polygon_id != 1403916:
    list_polygons.append(str(country.polygon_id))

print ",".join(list_polygons)

