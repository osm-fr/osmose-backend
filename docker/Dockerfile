FROM ubuntu:16.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends sudo \
                                git \
                                python \
                                python-dateutil \
                                python-imposm-parser \
                                python-lockfile \
                                python-polib \
                                python-poster \
                                python-psycopg2 \
                                python-shapely \
                                python-regex \
                                python-geojson \
                                postgresql \
                                postgresql-contrib \
                                postgresql-9.5-postgis-2.2 \
                                openjdk-8-jre-headless && \
    apt-get clean

RUN mkdir -p /data/work/osmose
RUN useradd -s /bin/bash -d /data/work/osmose osmose
RUN chown osmose /data/work/osmose

ADD . /opt/osmose-backend/

WORKDIR /opt/osmose-backend
ENV PYTHONPATH /opt/osmose-backend

ENTRYPOINT ["/opt/osmose-backend/tools/docker-entrypoint.sh"]
