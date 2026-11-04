# 04 — Traceability (RTM)

ไม่มี `specs/`; requirement มาจาก `PRODUCT.md` §"What works today" (R1–R6) และ §"Quality" (R7) และ §"Limits" (L1–L3)
release/workflow = CI workflow `CI` (`.github/workflows/ci.yml`) บน main; library ไม่มี tag หรือ GitHub release (`git tag`, `gh release list` ว่าง)

| ID | Requirement (PRODUCT.md) | Code (`service_auth/__init__.py`) | Test | Release / workflow |
|---|---|---|---|---|
| R1 | `from_env` โหลด issuer, RSA public key ≥ 2048 bits, subjects; config ผิด fail closed (503) | `AuthPolicy.from_env`, `__post_init__`, `ready`, `authenticate` (503 `reads_disabled`) | `test_auth.py::test_environment_config_and_partial_config`, `::test_missing_or_invalid_configuration_fails_closed` | CI `sdk` job |
| R2a | รับเฉพาะ `Bearer` RS256 ที่มีครบ 9 claims | `authenticate`: scheme check, `alg` check, `jwt.decode(... require=[...])` | `::test_signature_issuer_audience_and_algorithm`, `::test_all_claims_required` | CI `sdk` |
| R2b | ปฏิเสธ remote-key headers `jku jwk x5u x5c crit` | `authenticate` header check | `::test_remote_key_headers_and_oversize` (ทดสอบ 4 ตัว, **ไม่มีเคส `crit`**) | CI `sdk` |
| R2c | lifetime ≤ 120 s, leeway 5 s, ค่าเวลาเป็นตัวเลข finite | `authenticate` time checks | `::test_time_bounds_and_types` | CI `sdk` |
| R2d | `tenant_id == "owner"`, subject ใน allowlist, scope ตรงตัว (403) | `authenticate` final check | `::test_owner_and_scope_authorization` | CI `sdk` |
| R2e | error ไม่มี token | `AuthError`, `raise invalid from None` | `rejected()` helper ตรวจ `assertNotIn(token, ...)` | CI `sdk` |
| R3 | `check_read_auth` อนุญาต static token เฉพาะ `development` ที่ไม่ได้ config | `check_read_auth` | `tests/test_check_read_auth.py` (5 tests) | CI `sdk` |
| R4 | `readiness` รายงาน store/auth โดยไม่เปิดเผย exception | `readiness`, `SnapshotStore` | `tests/test_readiness.py::ReadinessTests` | CI `sdk` |
| R5 | `is_loopback(host)` | `is_loopback` | `tests/test_readiness.py::LoopbackTests` | CI `sdk` |
| R6 | key rotation: key ใหม่ปฏิเสธลายเซ็นเก่า | single `_key` per policy | `::test_key_rotation_rejects_previous_signature` | CI `sdk` |
| R7 | strict mypy, Ruff, 19 tests, coverage gate 99% | `pyproject.toml` `[tool.mypy]`, `[tool.ruff]` | ทั้ง `tests/` (19 passed, รันในเครื่อง 2026-11-04) | `ci.yml` `coverage-threshold: "99"` |
| L1 | ไม่มี replay database | — (gap โดยเจตนา) | — | — |
| L2 | ไม่มีอะไรบังคับให้สำเนา vendored ตรงกัน | — (gap) | — | — |
| L3 | ไม่ publish ไป PyPI | `pyproject.toml` ไม่มี publish workflow | — | — |

Gaps ที่พบ:
- `crit` header ไม่มี test โดยตรง
- บรรทัด 152 (`raise invalid` หลังเทียบ `iss`/`aud` ซ้ำ) ไม่ถูก cover — coverage report: 108 stmts, miss 1, 99%
- ไม่มี release artifact (tag/version bump) ที่ผูกกับ requirement; version คงที่ 0.1.0 ตั้งแต่ commit แรก

Sources: `PRODUCT.md`, `service_auth/__init__.py`, `tests/*.py`, `pyproject.toml`, `.github/workflows/ci.yml`; `uv run pytest -q --cov --cov-report=term-missing` (local run 2026-11-04)
