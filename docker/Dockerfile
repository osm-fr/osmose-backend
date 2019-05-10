FROM python:3.5

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        git \
        libboost-python-dev \
        libosmpbf-dev \
        libprotobuf-dev \
        locales \
        make \
        openjdk-8-jre-headless \
        pkg-config \
        postgis \
        postgresql-client \
        protobuf-compiler \
        python-dev \
        python-pip \
        python-setuptools \
        python-wheel && \
    apt-get clean

RUN mkdir -p /data/work/osmose && \
    useradd -s /bin/bash -d /data/work/osmose osmose && \
    chown osmose /data/work/osmose && \
    locale-gen en_US.UTF-8 && \
    localedef -i en_US -f UTF-8 en_US.UTF-8

ADD modules/osm_pbf_parser /opt/osmose-backend/modules/osm_pbf_parser
RUN cd /opt/osmose-backend/modules/osm_pbf_parser && make

ADD requirements.txt /opt/osmose-backend/requirements.txt
ADD requirements-dev.txt /opt/osmose-backend/requirements-dev.txt
WORKDIR /opt/osmose-backend
RUN pip install -r requirements.txt -r requirements-dev.txt
ENV PYTHONPATH /opt/osmose-backend

ADD . /opt/osmose-backend/

ARG GIT_VERSION
ENV OSMOSE_VERSION ${GIT_VERSION}
ENV LANG en_US.UTF-8
ENTRYPOINT ["/opt/osmose-backend/tools/docker-entrypoint.sh"]
CMD bash
