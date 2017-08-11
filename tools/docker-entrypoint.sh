#!/bin/sh

set -x

/etc/init.d/postgresql start

cd /opt/osmose-backend

sudo -u osmose ./osmose_run.py $@

