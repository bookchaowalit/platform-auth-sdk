# 17 — Test coverage matrix

tests เป็น `unittest` 3 ไฟล์, 19 tests (22 subtests) — ทั้งหมดเป็น **unit** (ไม่มี network/DB) ไม่มี integration หรือ e2e ใน repo นี้; integration จริงอยู่ใน consumer tests (`tests/test_server.py` ของแต่ละ consumer — ไม่นับที่นี่)

| Feature | Unit | Integration | E2E | Test |
|---|---|---|---|---|
| Valid token → sanitized Identity | ✅ | — | — | `test_auth.py::test_identity_is_sanitized` |
| Signature, issuer, audience, alg (HS256, wrong key, list aud) | ✅ | — | — | `::test_signature_issuer_audience_and_algorithm` |
| Time bounds, numeric types, NaN/inf | ✅ | — | — | `::test_time_bounds_and_types` |
| All 9 claims required, empty `jti` | ✅ | — | — | `::test_all_claims_required` |
| Owner / subject / scope (403) | ✅ | — | — | `::test_owner_and_scope_authorization` |
| Remote key headers (`jku jwk x5u x5c`), oversize, missing header | ✅ | — | — | `::test_remote_key_headers_and_oversize` |
| `crit` header rejection | ❌ gap | — | — | — |
| `jti` length > 128 / control chars | ❌ gap | — | — | — (only empty `jti` tested) |
| Bad config fails closed (503) | ✅ | — | — | `::test_missing_or_invalid_configuration_fails_closed` |
| RSA key < 2048 bits rejected | ❌ gap | — | — | — |
| Key rotation | ✅ | — | — | `::test_key_rotation_rejects_previous_signature` |
| `from_env` + partial config | ✅ | — | — | `::test_environment_config_and_partial_config` |
| `check_read_auth` dev/prod/partial | ✅ | — | — | `test_check_read_auth.py` (5) |
| `readiness` labels, error hiding | ✅ | — | — | `test_readiness.py::ReadinessTests` (3) |
| `is_loopback` | ✅ | — | — | `test_readiness.py::LoopbackTests` (2) |
| Vendored copy matches canonical | ❌ gap | — | — | — |

Coverage (local `uv run pytest -q --cov --cov-report=term-missing`, 2026-11-04): `service_auth/__init__.py` 108 stmts, 1 miss (line 152), **99%**; CI gate 99%

Sources: `tests/test_auth.py`, `tests/test_check_read_auth.py`, `tests/test_readiness.py`, `pyproject.toml` (`[tool.coverage.run]`), `.github/workflows/ci.yml`
