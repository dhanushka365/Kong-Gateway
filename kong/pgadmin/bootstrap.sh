#!/bin/sh
set -eu

# Saved DB passwords for auto-connect after UI login (must be mode 600, owned by pgAdmin UID)
cp /tmp/pgpass.source /var/lib/pgadmin/pgpass
chown 5050:5050 /var/lib/pgadmin/pgpass
chmod 600 /var/lib/pgadmin/pgpass

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
else
  echo "[bootstrap] pgAdmin did not become ready; skipping server import"
fi

wait "$ENTRY_PID"
