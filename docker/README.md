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


Running a country alone
=======================

The `./work` directory on your host must to be writable by anyone, as the
`osmose` user in the container will have some random UID (probably 1000).
```
chmod a+w ./work
```

Taking the Comoros (a quick and small one) as an example, once you have
the docker image, you can run Osmose analysers with this:
```
docker-compose --project-name comoros run --rm backend ./osmose_run.py --country=comoros
docker-compose --project-name comoros down # Destroy the loaded data base
```

This will run interactively and you will see the output scrolling on your
screen. The container will be deleted at the end of the process. All
dowloaded and output data will be saved in the `./work` directory.

To run with a password file and enable result to be uploaded to the
frontend you must adapt `osmose_config_password.py`.


Tunning
=======

The database configuration can be tunned using the SQL in environment
variable `POSTGRESQL_POSTCREATION`. It is executed at startup by the
postgres user.

Develop on Osmose with docker
=============================

Overview
--------

With docker-compose you can run a full development environment with
backend and frontend. In develop mode the backend is configured to run an
analysis and send the results to the local frontend without requiring
extra configuration or upload password.

Setup the Osmose Frontend
-------------------------

Quick setup:
```
git clone https://github.com/osm-fr/osmose-frontend.git
cd osmose-frontend/docker
docker build -f Dockerfile -t osm-fr/osmose_frontend:latest ..
```

For a detailed procedure see
https://github.com/osm-fr/osmose-frontend/tree/master/docker

Start Docker Backend container
------------------------------

Enter the container with:
```
docker-compose -f docker-compose.yml -f docker-compose-dev.yml -f docker-compose-frontend.yml run --rm backend bash
```

Note: when exiting the backend, the dependency containers will still
running. You can stop them with `docker-compose stop`.

Note: if you don't need the frontend just remove `-f
docker-compose-frontend.yml`.

Note: You will need to compile the OMS PBF parser as mentioned in the
top-level README file.

Running the analysis and showing the result on the map
------------------------------------------------------

From docker container you can test analyser:
```
./osmose_run.py --no-clean --country=comoros --analyser=osmosis_highway_floating_islands
```

Wait for the end of the process, depends on the area, but it may be long
or longer:
```
[...]
2018-01-25 20:19:04   DROP SCHEMA comoros
2018-01-25 20:19:04   DROP SCHEMA IF EXISTS comoros CASCADE;
2018-01-25 20:19:04 end of analyses
```

The results files will be at `./work/results`. There are also uploaded to
the local Osmose frontend: http://localhost:20009/map?useDev=all

To debug, stay on container, edit the pyhton files from outside, then run
again `osmose-run`. You can add the option `--skip-init` to speedup.

Access the database
-------------------

After running `osmose_run.py` with `--no-clean` the data base will
contain the OSM data. You can enter to explore and test SQL directly.
Open a psql shell on database from within the backend container:
```sh
psql -h postgis
```

Then
```
osmose=> set search_path to comoros,public;
```

Password management
-------------------

By default with `docker-compose-dev.yml` the password checks are disabled
on the frontend with `OSMOSE_UNLOCKED_UPDATE`: all updates from the
backend are accepted.
