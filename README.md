Backend part of Osmose QA tool
==============================

This is the part of osmose [http://osmose.openstreetmap.fr] which analyses OSM
and send results to frontend. This works as following:

  - an .osm.pbf extract is downloaded
  - analyses are run directly on .osm.pbf file, or on the database
  - analyses resultat are uploaded to the frontend
  - by default, temporary extract files and database are purged

Fetching josm translations
--------------------------

JOSM translations are used by some MapCSS plugins, and can be retrieved by bzr:
```
apt install bzr
cd po/josm
bzr checkout --lightweight lp:~openstreetmap/josm/josm_trans
```

Run
---

Look at the osmose_run.py help for options
```
osmose_run.py -h
```


Connection to the "official" frontend at http://osmose.openstreetmap.fr
-----------------------------------------------------------------------

When you have configured the backend for the country you want to add, please
send an email to osmose-contact@openstreetmap.fr. We will then send you the
password to use to connect to the frontend.


Run Tests
---------

Setup a `~/.pgpass` file to allow pgsql to connect to the test database without asking for password:
```
hostname:port:database:username:password
```

Create a test database `osmose_test` and initialize it:
```
createdb -O fred osmose_test
psql -c "CREATE extension hstore; CREATE extension fuzzystrmatch; CREATE extension unaccent; CREATE extension postgis;" osmose_test
psql -c "GRANT SELECT,UPDATE,DELETE ON TABLE spatial_ref_sys TO osmose;" osmose_test
psql -c "GRANT SELECT,UPDATE,DELETE,INSERT ON TABLE geometry_columns TO osmose;" osmose_test
```

Finally run the tests:
```
nosetests analysers/Analyser_Osmosis.py
nosetests analysers/analyser_sax.py
```
