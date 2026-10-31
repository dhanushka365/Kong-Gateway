"""
Generate Kong Gateway local stack release Word document.
Run from repo root: py scripts/generate_kong_gateway_stack_release_docx.py

Uses the shared Smarter Appliances release template from the woees repo.
Output is local-only (gitignored): docs/RELEASE_*.docx
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

WOEES_SCRIPTS = Path(r"E:\smarter works\woees\scripts")
if str(WOEES_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(WOEES_SCRIPTS))

from release_docx_template import ImpactedGroup, ReleaseDocContent, write_release_document

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "RELEASE_1.0.0_Kong_Gateway_Local_Stack.docx"


def main() -> None:
    path = write_release_document(
        ReleaseDocContent(
            output_path=OUTPUT,
            version="1.0.0",
            release_date=date(2026, 10, 31),
            system_name="Kong Gateway — Local API Gateway Stack",
            org_name="Smarter Appliances Ltd",
            developers="Platform / DevOps",
            project_manager="Platform / DevOps",
            support_contact="the Platform / DevOps team",
            executive_summary=(
                "This release delivers a local Docker Compose Kong Gateway stack with PostgreSQL "
                "config storage, Konga admin UI, pgAdmin for database browsing, and HTTP basic-auth "
                "login in front of Kong Manager and the Admin API. Host ports are remapped to avoid "
                "clashes with Work Order and other local Kong usage."
            ),
            why_done=(
                "Teams needed a shared, documented local Kong environment for gateway work, with "
                "UI access (Konga / Manager), DB visibility (pgAdmin), and a login gate on Manager "
                "because Kong OSS Manager has no built-in authentication."
            ),
            features=[
                (
                    "Kong + Postgres config DB",
                    "Kong 3.9.4 runs with Postgres 16 for durable gateway configuration "
                    "(migrations bootstrap on first start).",
                    "Local Kong state survives restarts and can be inspected in pgAdmin.",
                ),
                (
                    "Konga dashboard",
                    "Konga 0.14.9 on :1337 with its own Postgres 11 database (required by archived Konga).",
                    "Register an admin, connect to http://kong:8001, and manage Kong via UI.",
                ),
                (
                    "pgAdmin with UI login",
                    "pgAdmin on :5051 with email/password login; Kong and Konga servers pre-registered "
                    "with pgpass so DB passwords are not re-prompted after UI sign-in.",
                    "One place to browse both Postgres instances after a single web login.",
                ),
                (
                    "Kong Manager basic-auth login",
                    "nginx kong-auth gates Manager (:18002) and Admin API (:18001) with admin/admin. "
                    "Konga still reaches Kong on the Docker network without basic auth.",
                    "Dashboard and host Admin API are no longer open without credentials.",
                ),
                (
                    "Conflict-safe host ports",
                    "Proxy 18000, Admin 18001, Manager 18002, Konga 1337, pgAdmin 5051, "
                    "Postgres 15432/15433.",
                    "Runs alongside Work Order (:8002) and other local services without port fights.",
                ),
            ],
            impacted_groups=[
                ImpactedGroup(
                    title="Developers — local Kong",
                    impact=(
                        "Start the stack with docker compose up -d. Manager and host Admin API "
                        "require basic auth (admin/admin). Konga remains the preferred full UI "
                        "with its own registration login."
                    ),
                    action_required=(
                        "Pull latest main, run docker compose up -d, open http://localhost:18002 "
                        "and sign in with admin/admin, then confirm Konga at :1337 and pgAdmin at :5051."
                    ),
                ),
                ImpactedGroup(
                    title="Ops / platform",
                    impact=(
                        "Compose layout uses two Postgres services (Kong PG16, Konga PG11) and "
                        "kong-auth for Manager/Admin login. Direct publish of Admin/Manager from "
                        "the kong container was removed in favour of the auth proxy."
                    ),
                    action_required=(
                        "Update any runbooks that pointed at unauthenticated :18001/:18002; "
                        "use -u admin:admin for curl against the Admin API from the host."
                    ),
                ),
            ],
            support_checks=[
                "docker compose ps shows kong, kong-auth, kong-database, konga, konga-database, and pgadmin healthy/up.",
                "http://localhost:18002 returns 401 without credentials and loads Manager after admin/admin.",
                "curl -u admin:admin http://localhost:18001/ returns Kong Admin JSON.",
                "http://localhost:1337 allows Konga registration/login; connection URL http://kong:8001 works.",
                "http://localhost:5051 accepts admin@local.dev / admin and opens Kong/Konga DBs without a second password prompt.",
            ],
            support_intro=(
                "This is a local development stack. Report compose, login, or connectivity issues "
                "early so the shared environment stays reliable."
            ),
        )
    )
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
