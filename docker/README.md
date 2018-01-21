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
docker build -f Dockerfile -t osmose-backend ..
```


Running a country alone
-----------------------

Taking the comoros (a quick one) as an example, once you have the image, you can
run osmose checks like this:
```
docker run -it --rm osmose-backend --country=comoros
```
This will run interactively and you will see the output scrolling on your screen. The
container will be deleted at the end and no data will be saved on disk.

If, instead, you want to keep the output files locally you can add a volume in the right
location, like this:
```
docker run -it --rm -v /tmp:/data/work/osmose osmose-backend --country=comoros
```
The directory on your host, `/tmp` in this case, needs to be writable by everyone, as the
`osmose` user in the container will have some random UID (probably 1000).

Finally, to run with the password file and enable result upload to the frontend you can
use the following command line:
```
docker run -it --rm -v $PWD/osmose_config_password.py:/opt/osmose-backend/osmose_config_password.py osmose-backend --country=comoros
```
