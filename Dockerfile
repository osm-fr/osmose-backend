FROM ubuntu:14.04

MAINTAINER Daniele Venzano <venza@brownhat.org>

RUN apt-get update && \
    apt-get install -y python python-dateutil python-imposm-parser python-lockfile python-polib python-poster python-psycopg2 python-shapely python-regex openjdk-7-jre-headless && \
    apt-get clean

RUN apt-get update && \
    apt-get install -y postgresql-9.3 postgresql-contrib-9.3 postgresql-9.3-postgis-2.1 && \
    apt-get clean

RUN mkdir -p /data/work/osmose
RUN useradd -s /bin/bash -d /data/work/osmose osmose
RUN chown osmose /data/work/osmose

USER postgres
RUN /etc/init.d/postgresql start && \
    createuser osmose && \
    psql -c "ALTER ROLE osmose WITH PASSWORD '-osmose-';" && \
    createdb -E UTF8 -T template0 -O osmose osmose && \
    psql -c "CREATE extension hstore; CREATE extension fuzzystrmatch; CREATE extension unaccent; CREATE extension postgis;" osmose && \
    psql -c "GRANT SELECT,UPDATE,DELETE ON TABLE spatial_ref_sys TO osmose;" osmose && \
    psql -c "GRANT SELECT,UPDATE,DELETE,INSERT ON TABLE geometry_columns TO osmose;" osmose

USER root
ADD . /opt/osmose-backend/

WORKDIR /opt/osmose-backend
ENV PYTHONPATH /opt/osmose-backend

ENTRYPOINT ["/opt/osmose-backend/tools/docker-entrypoint.sh"]

