Install
=======

Installing Python
-----------------

Osmose QA backend requires python > 3.6.

Setup system dependencies (Debian Buster)
```
apt install git postgis python3
```

You can install python dependencies in the system or in a virtualenv.

### Alt: Python dependencies in the system

Install the following packages on the system:
```
apt install python3-dateutil python3-polib python3-psycopg2 python3-shapely python3-regex python3-requests cmake extra-cmake-modules qtbase5-dev flex bison libarchive-dev
```

### Alt: python dependencies in a virtualenv

Alternatively, install python-virtualenv and create a new virtualenv.

Setup system dependencies (Debian Stretch)
```
apt install build-essential python3-dev python3-virtualenv libpq-dev protobuf-compiler libprotobuf-dev
```

Create a python virtualenv, activate it and install python dependencies:
```
virtualenv --python=python3 osmose-backend-venv
source osmose-backend-venv/bin/activate
pip install -r requirements.txt
```

To run tests, additional packages are needed:
```
pip install -r requirements-dev.txt
```

Tests can then be run with:
```
pytest-3
```

### Compile the OMS PBF parser

Build the native python module lib to parse .osm.pbf files:
```
apt install g++ libboost-python-dev libosmpbf-dev make pkg-config python3-dev

cd modules/osm_pbf_parser/
make
```


Installing the Database
-----------------------

Setup system dependencies (Debian Buster):
```
apt install postgresql-11 postgresql-11-postgis-2.5
```

As postgres user:
```
createuser osmose
# Set your own password
psql -c "ALTER ROLE osmose WITH PASSWORD '-osmose-';"
createdb -E UTF8 -T template0 -O osmose osmose
# Enable extensions
psql -c "CREATE extension hstore; CREATE extension fuzzystrmatch; CREATE extension unaccent; CREATE extension postgis;" osmose
```


Dependencies
------------

Java JRE for osmosis:
```
apt install openjdk-11-jre-headless
```

osmosis is installed in osmosis/osmosis-0.47.4/.
osmconvert is installed in osmconvert/.


Configuration
-------------
A few paths are hardcoded in modules/config.py, and should be adapted or created.

  - dir_osmose is the path of where osmose is installed
  - dir_work is where extracts are stored, and results generated.
  - url_frontend_update is the url used to send results generated by analyses


The local postgresql database should be configured in osmose_config.py:

  - db_base = osmose # database name
  - db_user = osmose # database user
  - db_password = # database password if needed
  - db_host = # database hostname if needed

You may want to include this info in ~/.pgpass to avoid entering the database
password while processing the files.

See https://wiki.postgresql.org/wiki/Pgpass for more info.

You may use `SENTRY_DSN` environment variable to enable error report centralization.

Run Tests
---------
Setup a `~/.pgpass` file to allow pgsql to connect to the test database without asking for a password:
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
pytest-3 analysers/Analyser_Osmosis.py
pytest-3 analysers/analyser_sax.py
```
