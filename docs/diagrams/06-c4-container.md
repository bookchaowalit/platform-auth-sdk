# 06 — C4 Container

"container" ของ library คือ Python package ที่ถูก copy เข้า image ของ consumer แต่ละตัว

```mermaid
C4Container
    title service_auth as an installed package inside a consumer image
    System_Ext(issuer, "Token issuer", "Holds the signing private key")
    Container_Boundary(img, "Consumer image (python:3.12-slim per ci.yml comment)") {
        Container(server, "Consumer server.py", "Python http.server handler", "Calls check_read_auth and readiness")
        Container(lib, "service_auth package", "Python 3.11+, vendor/service-auth", "AuthPolicy, Identity, AuthError, helpers")
        Container(pyjwt, "PyJWT[crypto] >=2.10.1,<3", "Python dependency", "Decode and verify JWT")
        Container(crypto, "cryptography", "Python dependency via PyJWT[crypto]", "Load PEM public key")
    }
    ContainerDb(envv, "Process environment", "Env vars", "PREFIX_AUTH_ISSUER, PREFIX_AUTH_PUBLIC_KEY, PREFIX_AUTH_SUBJECTS")
    Rel(issuer, server, "Authorization: Bearer token")
    Rel(server, lib, "Python call")
    Rel(lib, pyjwt, "jwt.get_unverified_header, jwt.decode")
    Rel(lib, crypto, "load_pem_public_key")
    Rel(lib, envv, "os.environ.get")
```

Sources: `pyproject.toml` (`requires-python`, dependencies), `service_auth/__init__.py` (imports, `from_env`), `.github/workflows/ci.yml` (comment: consumer images python:3.12-slim), consumer `Dockerfile` (`COPY vendor/service-auth`)

หมายเหตุ: ชื่อ "http.server handler" ไม่ได้ยืนยันกับ consumer ทุกตัว — ยืนยันจากชื่อ class `IntegrationsRequestHandler` ใน platform-integrations-api `server.py` เท่านั้น
