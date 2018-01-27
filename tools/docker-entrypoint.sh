#!/bin/sh

set -x

/etc/init.d/postgresql start

TIMER="5"
until runuser -l postgres -c 'pg_isready' 2>/dev/null; do
  >&2 echo "PostgrSQL not yet available. Sleeping for $TIMER seconds..."
  sleep $TIMER
done

cd /opt/osmose-backend

sudo -E -u osmose ./osmose_run.py $@
