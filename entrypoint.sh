#!/bin/sh
set -e

python - <<'PY'
import os
import time
import psycopg2

host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
name = os.environ.get("POSTGRES_DB", "exchange_accounting")
user = os.environ.get("POSTGRES_USER", "exchange_accounting")
password = os.environ.get("POSTGRES_PASSWORD", "")

for _ in range(30):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=name,
            user=user,
            password=password,
        )
        conn.close()
        break
    except Exception:
        time.sleep(2)
else:
    raise SystemExit("Database not ready after waiting.")
PY

python manage.py migrate --noinput
python manage.py compilemessages

exec "$@"
