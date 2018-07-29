#!/bin/bash

set -x

# if data directory does not exist, clean up and recreate it
if [ ! -d "$(pg_conftool -s show data_directory)" ]; then
   POSTGRES_VERSION=$(psql --version |grep -E -o '[0-9]{1,}\.[0-9]{1,}')
   pg_dropcluster "$POSTGRES_VERSION" main
   pg_createcluster "$POSTGRES_VERSION" main
fi

/etc/init.d/postgresql start

# It can take a bit to start the DB inside the container. Wait for it to be ready...
TIMER="5"
until runuser -l postgres -c 'pg_isready' 2>/dev/null; do
  >&2 echo "PostgrSQL not yet available. Sleeping for $TIMER seconds..."
  sleep $TIMER
done

# set up database in case it is not yet existing, eg because container has mounted a tmpfs as db storage path
# if it is already there the commands will simply complain and continue without changes
runuser -l postgres -c $'createuser osmose'
runuser -l postgres -c $'psql -c "ALTER ROLE osmose WITH PASSWORD \'-osmose-\';"'
runuser -l postgres -c $'createdb -E UTF8 -T template0 -O osmose osmose'
runuser -l postgres -c $'psql -c "CREATE extension IF NOT EXISTS hstore; CREATE extension IF NOT EXISTS fuzzystrmatch; CREATE extension IF NOT EXISTS unaccent; CREATE extension IF NOT EXISTS postgis;" osmose'
runuser -l postgres -c $'psql -c "GRANT SELECT,UPDATE,DELETE ON TABLE spatial_ref_sys TO osmose;" osmose'
runuser -l postgres -c $'psql -c "GRANT SELECT,UPDATE,DELETE,INSERT ON TABLE geometry_columns TO osmose;" osmose'
# allow optional settings to be made after database creation. SQL string must be provided in environment
if  [ -v POSTGRESQL_POSTCREATION ]; then
  printf '%s\n' "$POSTGRESQL_POSTCREATION" | runuser -l postgres -c "psql -d osmose"
fi
/etc/init.d/postgresql restart

# wait again for database to be available
until runuser -l postgres -c 'pg_isready' 2>/dev/null; do
  >&2 echo "PostgrSQL not yet available. Sleeping for $TIMER seconds..."
  sleep $TIMER
done

# workaround: when mounting docker with tmpfs on data it fails to set a proper mode on already existing paths, even it ending up as tmpfs
chown -R osmose /data

cd /opt/osmose-backend || exit 2

sudo -E -u osmose ./osmose_run.py "$@"
