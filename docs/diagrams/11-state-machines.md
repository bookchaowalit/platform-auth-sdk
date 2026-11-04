# 11 — State machines

ไม่มี entity ที่มี status field ถาวร; lifecycle ที่โค้ดมีจริงคือ **สถานะ config ของ `AuthPolicy`** (คำนวณจาก `configured` และ `ready`) และ **label `auth` ใน `readiness`**

## AuthPolicy configuration state

```mermaid
stateDiagram-v2
    [*] --> Unconfigured: issuer, public_key, subjects all empty
    [*] --> Partial: any one set but validation fails
    [*] --> Ready: __post_init__ loads _key
    Unconfigured: configured false, ready false
    Partial: configured true, ready false
    Ready: configured true, ready true
    Unconfigured --> DevFallback: check_read_auth with environment development
    Unconfigured --> Disabled503: authenticate in any other environment
    Partial --> Disabled503: authenticate
    Ready --> Verifying: authenticate(headers)
    Verifying --> Accepted: all checks pass
    Verifying --> Rejected401: token invalid
    Verifying --> Rejected403: owner, subject or scope mismatch
```

policy เป็น frozen dataclass: เปลี่ยนสถานะได้ด้วยการสร้าง policy ใหม่ (ปกติคือ restart consumer หลังเปลี่ยน env) เท่านั้น

## readiness `auth` label

```mermaid
stateDiagram-v2
    [*] --> ready: policy.ready
    [*] --> development: not ready, environment development, not configured
    [*] --> disabled: otherwise
```

`status` = `ready` (HTTP 200) เฉพาะเมื่อ `source == available` และ `auth == ready`; นอกนั้น `not_ready` (503) — แม้ใน development

Sources: `service_auth/__init__.py` (`configured`, `ready`, `authenticate`, `check_read_auth`, `readiness`), `tests/test_readiness.py::test_auth_state_labels`, `tests/test_auth.py::test_environment_config_and_partial_config`
