#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER osmose;
    ALTER ROLE osmose WITH PASSWORD '-osmose-';
    CREATE DATABASE osmose OWNER osmose TEMPLATE template0 ;
    GRANT ALL PRIVILEGES ON DATABASE osmose TO osmose;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "osmose" <<-EOSQL
    CREATE extension IF NOT EXISTS hstore;
    CREATE extension IF NOT EXISTS fuzzystrmatch;
    CREATE extension IF NOT EXISTS unaccent;
    CREATE extension IF NOT EXISTS postgis;
    GRANT SELECT,UPDATE,DELETE ON TABLE spatial_ref_sys TO osmose;
    GRANT SELECT,UPDATE,DELETE,INSERT ON TABLE geometry_columns TO osmose;
EOSQL
