# 09 — ERD

**Status: not_applicable** — library ไม่มี persisted data: ไม่มี schema, migration, DB driver, file write หรือ storage binding ใน `service_auth/__init__.py`; ข้อมูลเดียวที่อ่านคือ env vars ใน `from_env` และ `jti` ไม่ถูกเก็บ (PRODUCT.md Limits: no replay database)
`SnapshotStore` เป็นเพียง Protocol ของ store ที่ **consumer** เป็นเจ้าของ

แทน ERD: in-memory value types ที่ library สร้าง (ไม่ถูกเก็บถาวร)

```mermaid
classDiagram
    class AuthPolicy {
        +str issuer
        +str audience
        +str public_key
        +frozenset subjects
        +str required_scope
        -RSAPublicKey _key
        +configured() bool
        +ready() bool
        +authenticate(headers) Identity
        +from_env(prefix, audience, required_scope) AuthPolicy
    }
    class Identity {
        +str subject
        +str tenant_id
        +str scope
    }
    class AuthError {
        +int status
        +str code
        +str message
    }
    class SnapshotStore {
        <<Protocol>>
        +snapshot() object
    }
    AuthPolicy ..> Identity : returns
    AuthPolicy ..> AuthError : raises
```

Sources: `service_auth/__init__.py`, `PRODUCT.md`
