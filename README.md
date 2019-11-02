Backend part of Osmose QA tool
==============================

This is the part of osmose [http://osmose.openstreetmap.fr] which analyses OSM
and send results to frontend. This works as following:

  - an .osm.pbf extract is downloaded
  - analyses are run directly on .osm.pbf file, or on the database
  - analyses resultat are uploaded to the frontend
  - by default, temporary extract files and database are purged

Run
---

Look at the osmose_run.py help for options
```
osmose_run.py -h
```
