#!/usr/bin/env python

import requests
import sys

import osmose_config

main_url = 'http://polygons.openstreetmap.fr/'
relation_generation_url = main_url + 'index.py'
polygon_union_url = main_url + 'get_poly.py'

fails = []
for c in osmose_config.config.values():
    if not hasattr(c, 'polygon_id'):
        continue
    if not c.polygon_id:
        continue

    print('  ', c.country, c.polygon_id)

    # generate relation boundary
    try:
        r = requests.post(relation_generation_url, params={'id': c.polygon_id}, data={'refresh': 1}, timeout=120)
    except requests.exceptions.Timeout:
        print("      Timeout")
        fails.append([c.country, c.polygon_id, 'Timeout'])
        continue
    if r.status_code == 500:
        print("      Geom Error -", r.url)
        fails.append([c.country, c.polygon_id, 'Geom Error'])
        continue
    elif r.status_code != 200:
        print("      Error -", r.url)
        fails.append([c.country, c.polygon_id, 'Error'])
        continue

    # get associated poly file
    try:
        r = requests.get(polygon_union_url, params={'id': c.polygon_id, 'params': 0}, timeout=120)
    except requests.exceptions.Timeout:
        print("      Poly Timeout")
        fails.append([c.country, c.polygon_id, 'Poly Timeout'])
        continue
    if r.status_code != 200:
        print("      Bad geom -", r.url)
        fails.append([c.country, c.polygon_id, 'Bad geom'])

if len(fails) > 0:
    print(fails)
    sys.exit(1)
