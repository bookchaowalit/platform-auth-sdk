# ADR-0004 — Use shared CI and security workflows pinned to platform-ci-workflows v1.1.1 with a 99% coverage gate

- Status: accepted (retro-documented)
- Date of evidence: 2026-10-17 (PR #1, `ec1e2d6`), bumped to v1.1.1 + gate in `0907a40` (2026-10-23)

## Decision
- `.github/workflows/ci.yml` เรียก reusable `ci-python.yml` (job `sdk`, python 3.12, `coverage-threshold: "99"`) และ `security.yml` (job `security`) ทั้งคู่ pin ด้วย SHA `87dc5e1c7e0416886a6371d5a101bb2ccba38edd` (v1.1.1)
- runner: GitHub-hosted (ค่า default `ubuntu-24.04` ของ reusable workflow; repo เป็น public)
- dev tooling ผ่าน uv + `uv.lock`, mypy strict, Ruff
- Renovate จัดกลุ่ม update ของ platform-ci-workflows เป็น PR เดียว และเปิด vulnerability alerts

## Consequences
- gate เดียวกับ repo อื่นใน platform; coverage จริง 99% (108 stmts, miss 1)
- ไม่มี branch protection บน main (`gh api .../branches/main/protection` → 404) จึง CI ไม่ได้บล็อก direct push

Evidence: `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, `renovate.json`, platform-ci-workflows `ci-python.yml` / `security.yml` @ `87dc5e1c`, `gh run list`, `gh api repos/bookchaowalit/platform-auth-sdk/branches/main/protection`; ops record: ci-hosting-policy (2026-11-03)
