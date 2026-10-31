# Kong Gateway

Local Kong API Gateway stack with PostgreSQL, pgAdmin, and Konga.

## Quick start

```bash
docker compose up -d
```

```bash
docker compose down
# wipe DB volumes:
docker compose down -v
```

## URLs

Host ports avoid clashes with Work Order (`:8002`) and other local Kong/k8s usage (`:8000`).

| Service | URL |
|---------|-----|
| Kong proxy | http://localhost:18000 |
| Kong Admin API | http://localhost:18001 |
| Kong Manager | http://localhost:18002 |
| Konga | http://localhost:1337 |
| pgAdmin | http://localhost:5051 |
| Kong Postgres | `localhost:15432` (`kong` / `kong`) |
| Konga Postgres | `localhost:15433` (`konga` / `konga`) |

### Credentials

- **pgAdmin:** `admin@local.dev` / `admin`
- **Kong DB (PG16):** `kong` / `kong`
- **Konga DB (PG11):** `konga` / `konga`

Konga is archived and only works with Postgres ≤ 11, so it gets its own `konga-database`. Kong uses modern Postgres 16.

### Konga first login

1. Open http://localhost:1337 and register an admin user.
2. Add a connection with Kong Admin URL: `http://kong:8001` (docker network name — not localhost).
