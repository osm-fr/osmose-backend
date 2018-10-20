Docker
======

You can run osmose-backend in a Docker container. The advantage is that
you do not need to setup and configure Python, Java and Postgresql on your system.

The Dockerfile provided in this repository can be used to build an image containing
osmose and a Postgresql instance.


Building
--------

To build the image run this command in the docker repository:
```
docker build -f Dockerfile -t osm-fr/osmose_backend:latest ..
```


Running a country alone
-----------------------

Taking the comoros (a quick one) as an example, once you have the image, you can
run osmose checks like this:
```
docker run -it --rm osm-fr/osmose_backend ./osmose_run.py --country=comoros
```
This will run interactively and you will see the output scrolling on your screen. The
container will be deleted at the end of the process and all data will wiped.

To run with the password file and enable result upload to the frontend
you can use the following command line:
```
docker run -it --rm -v $PWD/osmose_config_password.py:/opt/osmose-backend/osmose_config_password.py osm-fr/osmose_backend ./osmose_run.py --country=comoros
```


Develop analyser with docker
============================

Running and keep results
------------------------

If you want to keep the output files locally you can add a volume in the right
location, like this:
```
docker run -it --rm -v $PWD/work:/data/work/osmose osm-fr/osmose_backend ./osmose_run.py --country=comoros
```
The directory on your host, `work` in this case, needs to be writable by anyone, as the
`osmose` user in the container will have some random UID (probably 1000).


Enter the container to test and debug
-------------------------------------

Override the Osmose source code in the contrainer with the working
directory. Use the local source directory as volume to override source in
the container.
```
docker run -it --rm -v $PWD/..:/opt/osmose-backend osm-fr/osmose_backend bash
```

On docker container you can run analyser:
```
./osmose_run.py --no-clean --country=comoros
```

Open psql shell on database (after `--no-clean` run of `osmose_run.py`):
```
psql
```


Docker-Compose - Run and show the result on a map
=================================================

First, build the osmose-frontend.

Quick setup:
```
git clone https://github.com/osm-fr/osmose-frontend.git
cd osmose-frontend
docker build -t osm-fr/osmose_frontend:latest .
```

For detailled procedure see https://github.com/osm-fr/osmose-frontend

Use the docker-compose tool to run osmose-backend and send the result on the osmose-frontend.
```
docker-compose -p osmose up
```

Wait for the end of the process, depends on the area you process, but it may be long or longer:
```
...
backend_1   | 2018-01-25 20:19:04   DROP SCHEMA comoros
backend_1   | 2018-01-25 20:19:04   DROP SCHEMA IF EXISTS comoros CASCADE;
backend_1   | 2018-01-25 20:19:04 end of analyses
o_backend_1 exited with code 4
```

Enjoy at: http://localhost:20009/en/map/

End with `Ctrl+C` (only once and wait).

While the frontend is still running you can enter in with:
```
docker-compose -p o exec -u osmose frontend bash
source osmose-frontend-venv/bin/activate
```
