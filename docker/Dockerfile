FROM ubuntu:18.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends sudo \
                                git \
                                python \
                                python-dateutil \
                                python-imposm-parser \
                                python-lockfile \
                                python-pip \
                                python-polib \
                                python-poster \
                                python-psycopg2 \
                                python-shapely \
                                python-regex \
                                python-geojson \
                                python-requests \
                                python-setuptools \
                                python-wheel \
                                postgresql \
                                postgresql-contrib \
                                postgresql-10-postgis-2.4 \
                                postgresql-10-postgis-2.4-scripts \
                                openjdk-8-jre-headless && \
    apt-get clean

RUN mkdir -p /data/work/osmose
RUN useradd -s /bin/bash -d /data/work/osmose osmose
RUN chown osmose /data/work/osmose

ADD . /opt/osmose-backend/

WORKDIR /opt/osmose-backend
RUN pip install -r requirements.txt
ENV PYTHONPATH /opt/osmose-backend

ENTRYPOINT ["/opt/osmose-backend/tools/docker-entrypoint.sh"]
