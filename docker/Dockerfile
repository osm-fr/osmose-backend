FROM python:3.9

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bison \
        cmake \
        extra-cmake-modules \
        flex \
        g++ \
        gcc \
        gdal-bin \
        git \
        libarchive-dev \
        libboost-python-dev \
        libosmpbf-dev \
        libprotobuf-dev \
        locales \
        make \
        openjdk-11-jre-headless \
        pkg-config \
        postgis \
        postgresql-client \
        protobuf-compiler \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        qtbase5-dev \
        && apt-get clean

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

ARG PIP_INSTALL
RUN pip install -r requirements.txt ${PIP_INSTALL}
ENV PYTHONPATH /opt/osmose-backend

ADD . /opt/osmose-backend/

ARG GIT_VERSION
ENV OSMOSE_VERSION ${GIT_VERSION}
ENV LANG en_US.UTF-8
ENTRYPOINT ["/opt/osmose-backend/tools/docker-entrypoint.sh"]
CMD bash
