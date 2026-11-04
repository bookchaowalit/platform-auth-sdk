# ADR-0001 — Verify RS256 with one locally configured PEM public key; reject remote key headers

- Status: accepted (retro-documented)
- Date of evidence: 2026-10-04 (commit `fe16925`), unchanged in shape through `0907a40`

## Context
consumer services เป็น owner-private metadata API ที่ต้องตรวจ service JWT ที่ issuer เซ็น โดยไม่ต้องเรียก network ไปหา JWKS

## Decision
- algorithm ตรึงที่ RS256: `jwt.decode(..., algorithms=["RS256"])` และตรวจ `header["alg"] == "RS256"` ก่อน decode
- public key มาจาก env `<PREFIX>AUTH_PUBLIC_KEY` (PEM) หนึ่งก้อนต่อ policy ต้องเป็น `RSAPublicKey` ขนาด ≥ 2048 bits
- header `jku`, `jwk`, `x5u`, `x5c`, `crit` ทำให้ token ถูกปฏิเสธ
- config ไม่มี signing private key (README)

## Consequences
- ไม่มี network dependency และไม่มี key confusion จาก header
- rotation = เปลี่ยน env แล้ว restart; ไม่มีช่วงรับสอง key พร้อมกันใน canonical (test `test_key_rotation_rejects_previous_signature`) — knowledge-api จึงแยก copy ของตัวเองเพื่อเพิ่ม `AUTH_EXTRA_PUBLIC_KEY`
- ไม่ใช้ `kid`

Evidence: `service_auth/__init__.py` (`__post_init__`, `authenticate`), `README.md`, `tests/test_auth.py`; platform-knowledge-api `vendor/service-auth/service_auth/__init__.py` (origin/main, `extra_public_key`), ops record: hosted-document-store (2026-11-03)
