# 01 — Business process (As-Is / To-Be)

repo นี้คือ **library** Python หนึ่ง module (`service_auth/__init__.py`, package `solo-empire-service-auth` 0.1.0) ไม่มี server, CLI หรือ network call ของตัวเอง
"business process" ของ repo จึงเป็นกระบวนการของ consumer service ที่ใช้ library ตรวจ request และกระบวนการกระจาย library ไปยัง consumer (vendored copy)

## As-Is (จากโค้ดวันนี้)

### A. ตรวจ request ใน consumer service

```mermaid
flowchart LR
    Req["HTTP request to consumer API"] --> Env{"environment == development and policy not configured?"}
    Env -->|"no"| Auth["AuthPolicy.authenticate(headers)"]
    Env -->|"yes"| Static{"static token set?"}
    Static -->|"no"| Anon["allow, return None"]
    Static -->|"yes"| Cmp{"Bearer value equals token (compare_digest)?"}
    Cmp -->|"yes"| Anon
    Cmp -->|"no"| E401a["AuthError 401 unauthorized"]
    Auth -->|"key not loaded"| E503["AuthError 503 reads_disabled"]
    Auth -->|"bad header, signature, claims or time"| E401["AuthError 401 unauthorized"]
    Auth -->|"tenant, subject or scope mismatch"| E403["AuthError 403 forbidden"]
    Auth -->|"all checks pass"| Id["Identity(subject, owner, scope)"]
```

Sources: `service_auth/__init__.py` (`check_read_auth`, `AuthPolicy.authenticate`), `tests/test_check_read_auth.py`, `tests/test_auth.py`

### B. กระจาย library ไปยัง consumer

```mermaid
flowchart LR
    Dev["Maintainer edits service_auth here"] --> CI["CI: ci-python + security (v1.1.1)"]
    CI --> Main["push to main"]
    Main --> Copy["Maintainer re-copies service_auth/, pyproject.toml, tests/ into each consumer vendor/service-auth"]
    Copy --> Cons["Consumer commits copy, uv path source, Dockerfile COPY"]
    Cons --> Img["Consumer image build (Railway/Docker)"]
```

Sources: `README.md` (บรรทัด 3–7), `PRODUCT.md` (Who uses it, Limits), `.github/workflows/ci.yml`; consumer `pyproject.toml` `[tool.uv.sources]` และ `Dockerfile` ใน worktree ของ platform-accounts-api, platform-ai-usage-api, platform-integrations-api, platform-knowledge-api, platform-saas-catalog-api (origin/main 2026-11-04)

ข้อสังเกต (As-Is): ขั้น "re-copy" ทำด้วยมือ ไม่มี script หรือ CI ตรวจ ณ origin/main ของ consumer ทั้ง 5 สำเนาไม่ตรงกับ `service_auth/__init__.py` ที่นี่ (ดู [16-deployment.md](16-deployment.md))

## To-Be

repo ไม่มี `specs/`, `docs/UPGRADE-PLAN.md` หรือ GitHub issue (`gh issue list --state all` ว่าง) และ `PRODUCT.md` บอกเฉพาะ Limits ไม่ได้บอกแผน จึงไม่วาด To-Be

Open questions:
- ทิศทางต่อจากนี้คืออะไร: คงการ vendor หรือ publish package (PyPI / git SHA pin แบบ platform-backend-core)? `DOCPACK/00-product-card.md` §8 เสนอ "สคริปต์ตรวจ drift ของสำเนา" แต่ยังไม่มีสถานะ approve
- จะ merge ส่วนที่ knowledge-api เพิ่ม (extra trusted public keys) กลับมาที่ canonical หรือไม่
- จะเพิ่ม replay protection (`jti` tracking) หรือไม่ (PRODUCT.md Limits)
