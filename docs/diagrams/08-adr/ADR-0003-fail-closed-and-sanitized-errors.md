# ADR-0003 — Fail closed on bad config and return only sanitized identity and errors

- Status: accepted (retro-documented)
- Date of evidence: 2026-10-04 (`fe16925`); `readiness` and `check_read_auth` documented in PRODUCT.md (`0907a40`)

## Decision
- config ใดไม่ผ่าน `__post_init__` (issuer ไม่ใช่ exact HTTPS origin, key ไม่ใช่ RSA ≥ 2048, subjects ว่างหรือมี whitespace, audience/scope ว่าง) → `_key` เป็น `None` → `authenticate` raise `AuthError(503, "reads_disabled", ...)`
- error ทุกตัวเป็น `AuthError(status, code, message)` ข้อความคงที่ และ `raise invalid from None` เพื่อไม่ส่ง exception ของ PyJWT ต่อ
- `Identity` มีเฉพาะ `subject`, `tenant_id` (คงที่ `"owner"`), `scope` — claim อื่นถูกทิ้ง
- `readiness` จับ exception ของ store แล้วรายงานแค่ `available`/`unavailable`
- static token ใช้ได้เฉพาะ `environment == "development"` และ policy ไม่ได้ config เลย (`configured` เป็น false); config บางส่วนถือว่าตั้งใจใช้ JWT

## Consequences
- service ที่ config ผิดจะไม่เปิดอ่านแบบไม่มี auth ใน non-development
- consumer ต้องส่ง `environment` ถูกต้อง: ถ้าส่ง `"development"` ใน production ที่ไม่ได้ config จะเปิด anonymous read (ความรับผิดชอบของ consumer; integrations-api บังคับ `production` เมื่อ host ไม่ใช่ loopback)

Evidence: `service_auth/__init__.py`, `tests/test_auth.py::test_missing_or_invalid_configuration_fails_closed`, `::test_identity_is_sanitized`, `tests/test_check_read_auth.py`, `tests/test_readiness.py`; platform-integrations-api `server.py` บรรทัด 463–467
