#!/bin/bash
set -e

host="$1"
shift

until pg_isready -h "$host" -p 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

python3 manage.py makemigrations
python3 manage.py migrate

>&2 echo "Postgres is up - executing command"
exec "$@"
