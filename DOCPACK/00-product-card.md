---
title: solo-service-auth — Product Card
doc_id: CARD-solo-service-auth
doc_type: product-card
verdict: showcase
version: 0.1
date: 2026-10-11
status: ร่างเพื่อพิจารณา
owner: Product owner (Book Dev)
---

# solo-service-auth — Product Card

## 1. สรุปคุณค่าในหนึ่งประโยค

ช่วยบริการภายในของ Solo Empire ตรวจ JWT RS256 อย่างเข้มงวดและคืนเฉพาะ identity ที่ปลอดภัย

## 2. ปัญหาและผู้ใช้เป้าหมาย

- ปัญหา: หลายบริการต้องใช้กติกา JWT เดียวกัน (issuer, audience, scope, อายุ token)
- ผู้ใช้: บริการภายในของเจ้าของ (accounts, integrations, saas-catalog, knowledge-api, ai-usage)

## 3. สิ่งที่ทำได้จริงตอนนี้

- `AuthPolicy.from_env(prefix, audience, required_scope)` ตรวจ PEM public key; `authenticate(headers)` คืน `Identity(subject, tenant_id, scope)` หรือ `AuthError`
- ตรึง RS256, ปฏิเสธ remote key header, อนุญาต subject ตาม allowlist, tenant คือ `owner`, scope ตรงตัว, token อายุไม่เกิน 120 วินาที, leeway 5 วินาที (ตาม README)
- ไม่เก็บ private key; ไม่มีฐานข้อมูล replay

## 4. หลักฐานสถานะ

| รายการ | ค่า (ตรวจจาก repository) |
|---|---|
| Stack | Python (PyJWT) |
| Commits | 2 (แรก 2026-10-04 → ล่าสุด 2026-10-11) |
| Source | ประมาณ 268 บรรทัดใน 2 ไฟล์ (ไม่รวมเทสต์) |
| Tests | 1 ไฟล์ |
| CI | ไม่มี |
| Deploy config | ไม่มี (เป็นไลบรารี `pip install .`) |
| Live URL | ไม่มี (ไม่ได้ตรวจ) |
| README | 32 บรรทัด |

## 5. คุณค่าและจุดต่าง

- Consumer แต่ละตัวถือสำเนา `vendor/service-auth` เพราะ build บน Railway ดึง private repo ไม่ได้
- มุมรายได้: ไม่มี

## 6. ช่องว่างสำคัญ

- การกระจายด้วยสำเนา ทำให้ drift ได้ ต้อง re-copy ทุกครั้งที่แก้
- ไม่มี CI ไม่มี replay protection (README ระบุ)
- เทสต์มี 1 ไฟล์

## 7. คำตัดสิน

**`showcase`** — ไลบรารีเล็กที่เจตนาชัดและใช้จริงภายใน เป็นหลักฐานงาน security; จะเปลี่ยนถ้าทำเป็น package ที่ publish ให้ผู้อื่นใช้

## 8. ขั้นต่อไป

1. เพิ่ม CI รัน `python3 -m unittest discover -s tests -v`
2. ทำสคริปต์ตรวจ drift ของสำเนา `vendor/service-auth` ในแต่ละ consumer

## การอนุมัติ

| บทบาท | สถานะ | วันที่ | ลงนาม |
|---|---|---|---|
| Product owner (Book Dev) | รอพิจารณา | — | ________ |

## แหล่งข้อมูล

- `README.md`
- `service_auth/`, `tests/`, `pyproject.toml`
