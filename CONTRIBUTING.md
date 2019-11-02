# Contributing

When contributing to this repository, please first discuss the change you
wish to make via an issue on github if you want to change the core. Feel
free to make direct pull request for a new analyzer.

## Code Style

There is no written rules about this project or any specific code style.
But please try to make the code similar to code already existing.


## Fetching josm translations

JOSM translations are used by some MapCSS plugins, and can be retrieved by bzr:
```
apt install bzr
cd po/josm
bzr checkout --lightweight lp:~openstreetmap/josm/josm_trans
```

## Connection to the "official" frontend at http://osmose.openstreetmap.fr

When you have configured the backend for the country you want to add, please
send an email to osmose-contact@openstreetmap.fr. We will then send you the
password to use to connect to the frontend.


## Run Tests

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
