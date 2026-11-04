# Core 22 SDLC diagram pack — platform-auth-sdk

ชุดภาพ Core 22 ตาม SDLC Diagram Catalog v2 วาดจากโค้ดและ config ใน repo นี้ (ณ `origin/main` `0907a40`, 2026-10-23; ตรวจ 2026-11-04)
repo นี้คือ **library** Python (`service_auth`, package `solo-empire-service-auth` 0.1.0) ตรวจ RS256 service JWT แบบ owner-scoped ให้ metadata API ส่วนตัว 5 ตัว ซึ่งถือ **vendored copy** ใต้ `vendor/service-auth`; ไม่มี hosted runtime
ภาพจึงวาด library ภายใน consumer และ "deployment" = การ copy เข้า consumer

ทุกไฟล์มี `Sources:` ใต้ภาพ และ "Open questions" สำหรับสิ่งที่ยืนยันจากโค้ดไม่ได้ ข้อมูลฝั่ง consumer อ่านจาก worktree `~/work/core22/platform-*` ที่ origin/main (read-only)

| # | Item | Status | File | Sources read |
|---|---|---|---|---|
| 01 | Business process As-Is / To-Be | done (To-Be = open question) | [01-business-process.md](01-business-process.md) | `service_auth/__init__.py`, `README.md`, `PRODUCT.md`, `DOCPACK/00-product-card.md`, consumer `pyproject.toml`/`Dockerfile` |
| 02 | Use cases | done | [02-use-cases.md](02-use-cases.md) | `service_auth/__init__.py`, `tests/`, consumer `server.py`, consumer READMEs |
| 03 | User flows | done | [03-user-flows.md](03-user-flows.md) | `README.md`, consumer `pyproject.toml`/`Dockerfile`/`server.py`, `git log` |
| 04 | Traceability (RTM) | done | [04-traceability.md](04-traceability.md) | `PRODUCT.md`, `service_auth/__init__.py`, `tests/`, `ci.yml`, local pytest run |
| 05 | C4 Context | done | [05-c4-context.md](05-c4-context.md) | `README.md`, `PRODUCT.md`, consumer `server.py`/READMEs, `gh repo view` |
| 06 | C4 Container | done | [06-c4-container.md](06-c4-container.md) | `pyproject.toml`, `service_auth/__init__.py`, `ci.yml`, consumer `Dockerfile` |
| 07 | C4 Component | done | [07-c4-component.md](07-c4-component.md) | `service_auth/__init__.py` |
| 08 | ADRs | done (4) | [08-adr/](08-adr/) | `service_auth/__init__.py`, `README.md`, `PRODUCT.md`, `ci.yml`, `renovate.json`, `git log`, consumer vendored copies |
| 09 | ERD | not_applicable (no persisted data; in-memory class diagram instead) | [09-erd.md](09-erd.md) | `service_auth/__init__.py`, `PRODUCT.md` |
| 10 | Sequences | done | [10-sequences.md](10-sequences.md) | `service_auth/__init__.py`, `tests/` |
| 11 | State machines | done (policy config state, readiness label) | [11-state-machines.md](11-state-machines.md) | `service_auth/__init__.py`, `tests/` |
| 12 | API & integrations | done (Python API, no network) | [12-api-integration.md](12-api-integration.md) | `service_auth/__init__.py`, `pyproject.toml`, `uv.lock` |
| 13 | Threat model | done | [13-threat-model.md](13-threat-model.md) | `service_auth/__init__.py`, `tests/`, `PRODUCT.md`, `renovate.json`, `security.yml`, branch protection API |
| 14 | Backup & DR | not_applicable (no runtime data or hosted service) | [14-backup-dr.md](14-backup-dr.md) | `service_auth/__init__.py`, `.github/workflows/`, `README.md` |
| 15 | CI/CD pipeline | done | [15-cicd-pipeline.md](15-cicd-pipeline.md) | `ci.yml`, platform-ci-workflows `ci-python.yml`/`security.yml` @ `87dc5e1c`, `renovate.json`, `gh run list` |
| 16 | Deployment | done (distribution by vendored copy) | [16-deployment.md](16-deployment.md) | `README.md`, `PRODUCT.md`, consumer `vendor/service-auth`, `pyproject.toml`, `Dockerfile` |
| 17 | Test coverage matrix | done | [17-test-coverage-matrix.md](17-test-coverage-matrix.md) | `tests/`, `pyproject.toml`, `ci.yml`, local coverage run |
| 18 | Git & release workflow | done | [18-git-release-workflow.md](18-git-release-workflow.md) | `git log`, `gh pr list`, `gh run list`, branch protection API |
| 19 | Service dependency map | done | [19-service-dependency-map.md](19-service-dependency-map.md) | `pyproject.toml`, `uv.lock`, `service_auth/__init__.py`, consumer `server.py` |
| 20 | Observability | done (library emits no telemetry; signals for consumers + repo) | [20-observability.md](20-observability.md) | `service_auth/__init__.py`, `PRODUCT.md`, `renovate.json`, `security.yml`, consumer READMEs |
| 21 | Incident response | done (library vulnerability/defect flow) | [21-incident-response.md](21-incident-response.md) | `renovate.json`, `ci.yml`, `README.md`, `PRODUCT.md` |
| 22 | DORA | done (4/5 computed; recovery time not computable, no failures) | [22-dora.md](22-dora.md) | `git log`, `gh pr list`, `gh run list` |

## ADR list

- [ADR-0001](08-adr/ADR-0001-local-pem-rs256-no-remote-keys.md) RS256 กับ PEM public key ในเครื่อง, ปฏิเสธ remote key headers
- [ADR-0002](08-adr/ADR-0002-distribute-by-vendored-copy.md) กระจายด้วย vendored copy ในแต่ละ consumer
- [ADR-0003](08-adr/ADR-0003-fail-closed-and-sanitized-errors.md) Fail closed และคืนเฉพาะ identity/error ที่ปลอดภัย
- [ADR-0004](08-adr/ADR-0004-shared-ci-v1.1.1-coverage-gate.md) Shared CI v1.1.1 + coverage gate 99%

## Key findings

- สำเนา vendored ทั้ง 5 ใน consumer (origin/main 2026-11-04) ไม่ตรงกับ canonical; knowledge-api เป็น fork ที่เพิ่ม extra public keys
- ไม่มี replay protection (`jti` ไม่ถูกเก็บ), ไม่มี branch protection บน main, ไม่มี tag/release
- Test gaps: header `crit`, `jti` ยาว/มี control char, RSA < 2048, บรรทัด 152
- `check_read_auth` dev path หา header `authorization` แบบตัวเล็กเท่านั้น (ต่างจาก `authenticate`)

## Existing docs (reused, not copied)

- [`PRODUCT.md`](../../PRODUCT.md), [`README.md`](../../README.md), [`DOCPACK/00-product-card.md`](../../DOCPACK/00-product-card.md) (L0 card 2026-10-11; บางค่าในนั้นล้าสมัยแล้ว เช่น "CI: ไม่มี", "Tests 1 ไฟล์")
