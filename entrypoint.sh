#!/bin/sh

set -o errexit
set -o nounset

postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect("${DATABASE_URL}")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

redis_ready() {
python << END
import sys
import redis
r = redis.from_url("${REDIS_URL}")
try:
    r.ping()
except (redis.exceptions.ConnectionError):
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

until redis_ready; do
  >&2 echo 'Waiting for Redis to become available...'
  sleep 1
done
>&2 echo 'Redis is available'

exec "$@"
