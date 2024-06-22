Docker
======

osmose-backend can be run in a Docker container. This avoids setting
up and configuring Python, Java and PostgreSQL on your system.

Note : A PostgreSQL docker is automatically installed and run by
docker-compose and doesn't need be installed manually.
The osmose-frontend docker may also be run but is not mandatory.


Setup
-----

To build the docker image run this command from the docker folder:
```
docker-compose build
```

For production setup, you may fill the `SENTRY_DSN` field in
`docker-compose.yml` to enable error report centralization.

Running on a single country
===========================

The `./work` directory on your host must be writable by anyone, as the
`osmose` user in the container will have some random UID (probably 1000).
```
chmod a+w ./work
```

Taking Monaco (a quick and small one) as an example, once the docker
image is built, you can run Osmose analyzers using:
```
docker-compose --project-name monaco run --rm backend ./osmose_run.py --country=monaco
docker-compose --project-name monaco down # Destroy the loaded data base
```

This will run interactively and you will see the output scrolling on your
screen. The container will be deleted at the end of the process. All
downloaded and output data will be saved in the `./work` directory.

To enable results to be uploaded to the frontend you must configure
the frontend passwords in `osmose_config_password.py`.


Tuning
======

The database configuration can be tuned by setting the `POSTGRESQL_POSTCREATION`
environment variable to a SQL statement. The SQL statement will be executed at
startup using the postgres user account.


Develop on Osmose using docker
==============================

* A Backend alone with the **Jupyter** web editor and visualizer can be
used.
* Alternatively, using docker-compose, you can run a **full development
environment** with backend and frontend. In develop mode, the Backend can
run an analysis and send the results to the local Frontend without
requiring extra configuration or upload password.


## Build the develop tools

Build the docker image with develop tools included:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml build
```


## Start Docker Backend container

On the first execution only:
```
chmod a+w ../modules/osm_pbf_parser/
```

Enter the container with:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm backend
```

On the first execution only, compile the OSM PBF parser:
```
cd modules/osm_pbf_parser/ && make && cd -
```

Note: when exiting the backend, the dependency Database container will still be
running. You can stop it with `docker-compose stop`.


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
You do not need to load the country each time. It remains in the Database.


Then run the jupyter-notebook web server:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run -p 8888:8888 --rm backend jupyter-notebook
```
Note the `8888:8888`, which exposes port `8888` to localhost.

Follow the displayed link on http://localhost:8888/...


Start by reading the index documentation, and copy template to test your
own analyzer code.


## Alternative 2: Develop with Full environment

From docker container you can test all the analyzers using:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml run --rm backend
```

To test a specific analyzer:
```
./osmose_run.py --no-clean --country=monaco --analyser=osmosis_highway_floating_islands
```

To run one plugin only use:
```
./osmose_run.py --no-clean --country=monaco --analyser=sax --plugin=Name_Multiple
```

The execution time of the process may be pretty long, depending on the area:
```
[...]
2018-01-25 20:19:04   DROP SCHEMA monaco
2018-01-25 20:19:04   DROP SCHEMA IF EXISTS monaco CASCADE;
2018-01-25 20:19:04 end of analyses
```

The files containing the results will be in `./work/results`.

To debug, keep the container running, edit the python files from outside the container,
then run `osmose-run` again. You can add the `--skip-init` parameter to speed up the execution.

### Showing the results on the Osmose Frontend Map

Quick Osmose Frontend setup.

First time build
```
git clone https://github.com/osm-fr/osmose-frontend.git
cd osmose-frontend/docker
curl https://osmose.openstreetmap.fr/export/osmose-menu.sql.bz2 | bzcat > osmose-menu.sql
docker-compose build
docker-compose -f docker-compose.yml -f docker-compose-test.yml up -d postgres
# Wait fwe seconds for postgres ready
docker-compose -f docker-compose.yml -f docker-compose-test.yml run --rm api bash -c "cd web_api/static && npm run build"
docker-compose -f docker-compose.yml -f docker-compose-test.yml stop postgres
```

Run the frontend
```
docker-compose -f docker-compose.yml -f docker-compose-test.yml up
```

For a detailed description of the procedure see
https://github.com/osm-fr/osmose-frontend/tree/master/docker


To upload the results of the analysis to the frontend, use:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml -f docker-compose-frontend.yml run --rm backend bash
```

The result will be available at: http://127.0.0.1:8080/en/issues/open?item=xxxx&useDevItem=all
