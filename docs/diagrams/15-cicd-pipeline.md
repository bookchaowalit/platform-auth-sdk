# 15 — CI/CD pipeline

workflow เดียว `CI` (`.github/workflows/ci.yml`) เรียก reusable workflows ของ `bookchaowalit/platform-ci-workflows` @ `87dc5e1c` (v1.1.1); ไม่มี CD (library ไม่มี deploy)

```mermaid
flowchart TD
    T1["push to main"] --> CI
    T2["pull_request"] --> CI
    T3["workflow_dispatch"] --> CI
    CI["CI workflow, permissions contents read, concurrency ci-ref cancel-in-progress"]
    CI --> SDK["job sdk: ci-python.yml python 3.12, coverage-threshold 99"]
    CI --> SEC["job security: security.yml defaults"]
    subgraph SDKsteps["ci-python python job (ubuntu-24.04)"]
        S1["Checkout"] --> S2["setup-uv + Python"] --> S3["uv sync --frozen --all-extras (uv.lock present)"]
        S3 --> S4["Ruff check + format --check"] --> S5["mypy . ([tool.mypy] present)"]
        S5 --> S6["pytest -q --cov"] --> S7["Coverage gate fail-under 99, precision 2"]
    end
    subgraph SECjobs["security jobs (ubuntu-24.04)"]
        G["gitleaks"]
        SG["semgrep p/default"]
        O["osv-scanner"]
        TV["trivy-fs HIGH,CRITICAL vuln,misconfig"]
    end
    SDK --> SDKsteps
    SEC --> SECjobs
```

ทั้งสอง job รันขนานกัน (ไม่มี `needs`) Renovate (`renovate.json`) เปิด PR update ทุกจันทร์ก่อน 9 โมง (Asia/Bangkok) และ lock maintenance วันที่ 1 ของเดือน

ประวัติ run (`gh run list`): 3 runs ทั้งหมด success — PR #1 (2026-10-17), push main `ec1e2d6` (2026-10-17), push main `0907a40` (2026-10-23)

Sources: `.github/workflows/ci.yml`, platform-ci-workflows `.github/workflows/ci-python.yml` และ `security.yml` @ `87dc5e1c7e0416886a6371d5a101bb2ccba38edd` (inputs/defaults, jobs, steps), `renovate.json`, `uv.lock`, `pyproject.toml`
