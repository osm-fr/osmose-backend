#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "osmose" <<-EOSQL
    ALTER ROLE osmose RENAME TO osmose_owner;
    ALTER USER osmose_owner PASSWORD NULL;

    CREATE USER osmose WITH PASSWORD '-osmose-';
    GRANT CONNECT ON DATABASE osmose TO osmose;

    GRANT USAGE ON SCHEMA public TO osmose;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO osmose;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO osmose;

    GRANT USAGE ON SCHEMA monaco TO osmose;
    GRANT SELECT ON ALL TABLES IN SCHEMA monaco TO osmose;
    ALTER DEFAULT PRIVILEGES IN SCHEMA monaco GRANT SELECT ON TABLES TO osmose;

    ALTER USER postgres PASSWORD NULL;
EOSQL
