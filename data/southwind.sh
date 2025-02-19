#!/bin/bash
set -eux

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE $POSTGRES_OUTPUT;
	GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_OUTPUT TO $POSTGRES_USER;
EOSQL