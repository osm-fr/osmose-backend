#! /usr/bin/python

import lxml.html
import os
import requests
import sys

sys.path.append(".")
import osmose_config

main_url = "http://polygons.openstreetmap.fr/"
relation_generation_url = main_url + "index.py"
polygon_union_url = main_url + "get_poly.py"

for c in osmose_config.config.values():
  if not hasattr(c, "polygon_id"):
    continue
  if not c.polygon_id:
    continue

  country_name = c.country
  print "  ", country_name, c.polygon_id

  out_file = os.path.join("generated-polygons", country_name + ".poly")
  if os.path.exists(out_file):
    continue

  # generate relation boundary
  r = requests.get(relation_generation_url, params={"id": c.polygon_id})
  parser = lxml.html.HTMLParser(encoding='UTF-8')
  p = lxml.html.fromstring(r.text, parser=parser)

  print relation_generation_url + "?id=" + str(c.polygon_id)

  try:
    form = p.forms[1]
    x = form.inputs["x"].value
    y = form.inputs["y"].value
    z = form.inputs["z"].value
  except:
    print "    * ERROR * "
    continue

  x = 0
  y = 0.05
  z = 0.1

  if not ("%s-%s-%s" % (x, y, z)) in r.text:
    r = requests.post(relation_generation_url, params={"id": c.polygon_id}, data={"x": x, "y": y, "z": z})

#  r = requests.get(polygon_union_url, params={"id": c.polygon_id,
#                                              "params": "%s-%s-%s" % (x,y,z)})

  out_file = os.path.join("generated-polygons", country_name + ".poly")
  with open(out_file, "w") as text_file:
    text_file.write("toto")
