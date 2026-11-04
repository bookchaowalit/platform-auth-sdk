# ADR-0002 — Distribute the library as a vendored copy in each consumer

- Status: accepted (retro-documented)
- Date of evidence: 2026-10-11 (commit `05f510f` "moved-from note and vendoring policy")

## Context
library ย้ายออกจาก solo-empire `packages/service-auth` เมื่อ 2026-10-11 (subtree split) README ให้เหตุผลว่า private repo ดึง package ผ่าน HTTPS ใน Railway/Docker build ไม่ได้ถ้าไม่มี credentials

## Decision
- consumer ถือสำเนาใต้ `vendor/service-auth` และอ้างผ่าน uv path source (`solo-empire-service-auth = { path = "vendor/service-auth" }`) พร้อม dependency `solo-empire-service-auth>=0.1.0,<0.2`
- แก้ที่ repo นี้ก่อน แล้ว re-copy `service_auth/`, `pyproject.toml`, `tests/` ไปทุก consumer
- ไม่ publish ไป PyPI (PRODUCT.md Limits)

## Consequences
- build ของ consumer ไม่ต้องใช้ credential
- drift: ณ origin/main 2026-11-04 สำเนาทั้ง 5 ต่างจาก canonical (3 ตัวเป็นรุ่นก่อน strict-mypy 149 บรรทัด, integrations ต่าง 23 บรรทัด, knowledge-api fork เพิ่ม extra keys) ดู [16-deployment.md](../16-deployment.md)
- ไม่มีอะไรตรวจว่าสำเนาตรงกัน (PRODUCT.md Limits)
- หมายเหตุ: repo นี้เป็น PUBLIC แล้ว (`gh repo view`, commit `fceff08` "before going public") เหตุผลเรื่อง credential จึงอาจไม่ใช้แล้ว — open question

Evidence: `README.md`, `PRODUCT.md`, `git log`; consumer `pyproject.toml` / `Dockerfile` (origin/main)
