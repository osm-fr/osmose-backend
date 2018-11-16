#!/bin/bash

set -x

# It can take a bit to start the DB inside the container. Wait for it to be ready...
TIMER="5"
until pg_isready --host=postgis; do
  >&2 echo "PostgrSQL not yet available. Sleeping for $TIMER seconds..."
  sleep $TIMER
done

# workaround: when mounting docker with tmpfs on data it fails to set a proper mode on already existing paths, even it ending up as tmpfs
#chown -R osmose /data

#sudo -E -u osmose $@
$@
