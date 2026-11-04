# 03 — User flows

library ไม่มี route หรือ page; "user" คือ developer ของ consumer service และ maintainer flow หลักมี 3 แบบ

## Flow 1 — Consumer นำ library ไปใช้ (adopt)

```mermaid
flowchart TD
    A["Copy service_auth/, pyproject.toml, tests/ into vendor/service-auth"] --> B["pyproject: dependency solo-empire-service-auth >=0.1.0,<0.2 and uv path source vendor/service-auth"]
    B --> C["Dockerfile: COPY vendor/service-auth into image"]
    C --> D["server.py: AuthPolicy.from_env(PREFIX, audience, scope)"]
    D --> E["Set PREFIX_AUTH_ISSUER, PREFIX_AUTH_PUBLIC_KEY, PREFIX_AUTH_SUBJECTS at runtime"]
    E --> F["Request handler calls check_read_auth; health handler calls readiness"]
    F --> G["main: non-loopback host forces environment production and requires policy.ready (is_loopback)"]
```

Sources: `README.md`, consumer `pyproject.toml`, `Dockerfile`, `server.py` ใน worktree ของ consumer ทั้ง 5 (origin/main 2026-11-04); พฤติกรรม non-loopback ตรวจจาก platform-integrations-api `server.py` (บรรทัด 463–467) ส่วน consumer อื่นมีการเรียก `is_loopback(args.host)` ใน `main` เช่นกันแต่ไม่ได้อ่านบรรทัดถัดไปทุกตัว

## Flow 2 — Maintainer แก้ library

```mermaid
flowchart TD
    A["Edit service_auth/__init__.py and tests"] --> B["uv sync --frozen --all-extras"]
    B --> C["ruff check, ruff format --check, mypy (strict), pytest --cov"]
    C --> D{"PR or direct push to main"}
    D --> E["CI workflow: sdk (ci-python) + security"]
    E --> F["Re-copy into each consumer (manual)"]
```

Sources: `README.md` (Development), `pyproject.toml`, `.github/workflows/ci.yml`, `git log` (6 จาก 7 commit เป็น direct push, 1 ผ่าน PR #1)

## Flow 3 — Caller ส่ง request ไป consumer

```mermaid
flowchart LR
    Caller["Caller with RS256 token from issuer"] -->|"Authorization: Bearer token"| API["Consumer API"]
    API --> Lib["service_auth checks"]
    Lib -->|"Identity"| Data["Consumer returns data"]
    Lib -->|"AuthError"| Err["Consumer maps status/code/message to response"]
```

Sources: `service_auth/__init__.py`; การ map `AuthError` เป็น HTTP response อยู่ใน consumer `server.py` (ไม่ใช่โค้ดของ repo นี้)
