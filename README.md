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

| Service | URL |
|---------|-----|
| Kong proxy | http://localhost:8000 |
| Kong Admin API | http://localhost:8001 |
| Kong Manager | http://localhost:8002 |
| Konga | http://localhost:1337 |
| pgAdmin | http://localhost:5050 |
| Postgres | `localhost:15432` |

### Credentials

- **Postgres:** user `kong` / password `kong` (databases: `kong`, `konga`)
- **pgAdmin:** `admin@local.dev` / `admin`

### Konga first login

1. Open http://localhost:1337 and register an admin user.
2. Add a connection with Kong Admin URL: `http://kong:8001`.
