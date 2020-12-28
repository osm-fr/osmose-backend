Docker
======

You can run osmose-backend in a Docker container. The advantage is that
you do not need to setup and configure Python, Java and PostgreSQL on
your system. The PostgreSQL and eventually the Osmose Frontend are
dependencies.


Setup
-----

Install Docker and docker-compose. Due to known bugs, use at least
version 1.19.0 of docker-compose. It's always recommended to use a recent
version.

Confirmed to be working with docker `18.09.1` and docker-compose `1.23.2`.

To build the docker image run this command from the docker repository:
```
docker-compose build
```


Running on a single country
===========================

The `./work` directory on your host must to be writable by anyone, as the
`osmose` user in the container will have some random UID (probably 1000).
```
chmod a+w ./work
```

Taking the Monaco (a quick and small one) as an example, once you have
the docker image, you can run Osmose analysers like this:
```
docker-compose --project-name monaco run --rm backend ./osmose_run.py --country=monaco
docker-compose --project-name monaco down # Destroy the loaded data base
```

This will run interactively and you will see the output scrolling on your
screen. The container will be deleted at the end of the process. All
downloaded and output data will be saved in the `./work` directory.

To run with a password file and enable results to be uploaded to the
frontend you must adapt `osmose_config_password.py`.


Tuning
======

The database configuration can be tuned using the SQL in the environment
variable `POSTGRESQL_POSTCREATION`. It is executed at startup by the
postgres user.


Develop on Osmose with docker
=============================

* A Backend alone with the **Jupyter** web editor and visualizer can be
used.
* Alternatively, with docker-compose you can run a **full development
environment** with backend and frontend. In develop mode the Backend can
run an analysis and send the results to the local Frontend without
requiring extra configuration or upload password.


## Build the develop tools

Build the docker image with develop tools included:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml build
```


## Start Docker Backend container

At the first time only:
```
chmod a+w ../modules/osm_pbf_parser/
```

Enter the container with:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm backend
```

At the first time only, compile the OSM PBF parser:
```
cd modules/osm_pbf_parser/ && make && cd -
```

Note: when exiting the backend, the dependency Database container will still be
running. You can stop them with `docker-compose stop`.


## Access to the Database

After data load (see later) the Database will contain the OSM data. You
can enter to explore and test SQL directly. Open a psql shell on database
from within the Backend container with:
```sh
psql -h postgis
```
Password: `-osmose-`.

Then on Postgres shell:
```
osmose=> set search_path to monaco,public;
```

You can Reset the Database and the docker containers with:
```
docker-compose down -v
```


## Run the tests

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details. But, for short:
```
pytest plugins/TagFix_Housenumber.py
./tools/pytest.sh lint
./tools/pytest.sh mypy
./tools/pytest.sh sax # Run all plugins tests
./tools/pytest.sh merge # Not required, run all test on merge from analysers directory
./tools/pytest.sh other # Not required, run all other analysers and non analyser tests
```


## Alternative 1: Develop with Jupyter

Download and load a country into the Database:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run -p 8888:8888 --rm backend ./osmose_run.py --no-clean --country=monaco --skip-analyser --skip-upload
```
You does not need to load the country each time. It saves in the Database.


Then run the jupyter-notebook web server:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run -p 8888:8888 --rm backend jupyter-notebook
```
Note the `8888:8888`, which expose the port `8888` to localhost.

Follow the displayed link on http://localhost:8888/...


Start by reading the index documentation, and copy template to test your
own analyzer code.


## Alternative 2: Develop with Full environment

From docker container you can test analysers:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm backend
```

From docker container you can test analyzer:
```
./osmose_run.py --no-clean --country=monaco --analyser=osmosis_highway_floating_islands
```

For running one plugin only use:
```
./osmose_run.py --no-clean --country=monaco --analyser=sax --plugin=Name_Multiple
```

The execution time of the process, depending on the area, may be long
or longer:
```
[...]
2018-01-25 20:19:04   DROP SCHEMA monaco
2018-01-25 20:19:04   DROP SCHEMA IF EXISTS monaco CASCADE;
2018-01-25 20:19:04 end of analyses
```

The files containing the results will be in `./work/results`.

To debug, stay on container, edit the python files from the outside, then run
again `osmose-run`. You can add the option `--skip-init` to speedup.

### Showing the results on the Osmose Frontend Map

Quick Osmose Frontend setup:
```
git clone https://github.com/osm-fr/osmose-frontend.git
cd osmose-frontend/docker
curl http://osmose.openstreetmap.fr/export/osmose-menu.sql.bz2 | bzcat > osmose-menu.sql
docker-compose build
docker-compose -f docker-compose.yml -f docker-compose-test.yml up
```

For a detailed description of the procedure see
https://github.com/osm-fr/osmose-frontend/tree/master/docker


To upload the results of the analysis to the frontend use:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml -f docker-compose-frontend.yml run --rm backend bash
```

The result will be available at: http://localhost:20009/map?useDev=all
