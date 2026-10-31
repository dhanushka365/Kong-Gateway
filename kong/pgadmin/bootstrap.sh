#!/bin/sh
set -eu

# In SERVER mode, PassFile "/pgpass" is relative to the logged-in user's storage dir:
#   /var/lib/pgadmin/storage/<email_with_@_->/
STORAGE_DIR="/var/lib/pgadmin/storage/admin_local.dev"
mkdir -p "$STORAGE_DIR"
cp /tmp/pgpass.source "$STORAGE_DIR/pgpass"
chown -R 5050:0 "$STORAGE_DIR"
chmod 700 "$STORAGE_DIR"
chmod 600 "$STORAGE_DIR/pgpass"

# Start pgAdmin (server mode = email/password login page)
/entrypoint.sh &
ENTRY_PID=$!

# Wait until the web UI responds, then import preconfigured servers with PassFile
i=0
while [ "$i" -lt 90 ]; do
  if wget -qO- http://127.0.0.1:80/misc/ping >/dev/null 2>&1; then
    break
  fi
  i=$((i + 1))
  sleep 2
done

if wget -qO- http://127.0.0.1:80/misc/ping >/dev/null 2>&1; then
  echo "[bootstrap] Importing servers for admin@local.dev..."
  /venv/bin/python3 /pgadmin4/setup.py load-servers \
    /pgadmin4/servers.import.json \
    --replace \
    --user admin@local.dev \
    || echo "[bootstrap] load-servers failed (may already be imported)"
  # Ensure pgpass is still present after import (setup may recreate storage)
  mkdir -p "$STORAGE_DIR"
  cp /tmp/pgpass.source "$STORAGE_DIR/pgpass"
  chown -R 5050:0 "$STORAGE_DIR"
  chmod 700 "$STORAGE_DIR"
  chmod 600 "$STORAGE_DIR/pgpass"
  echo "[bootstrap] pgpass ready at $STORAGE_DIR/pgpass"
else
  echo "[bootstrap] pgAdmin did not become ready; skipping server import"
fi

wait "$ENTRY_PID"
