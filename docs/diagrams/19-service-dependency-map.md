# 19 — Service dependency map

runtime dependency ของ library มีแค่ Python packages และ env ของ consumer; ไม่มี service, DB, API หรือ CDN

```mermaid
flowchart TD
    subgraph Consumers["Consumers (runtime hosts)"]
        A["accounts-metadata-api"]
        AI["ai-usage-api"]
        I["integrations-api"]
        K["knowledge-api (fork)"]
        S["saas-catalog-api"]
    end
    Lib["service_auth 0.1.0"]
    A & AI & I & K & S --> Lib
    Lib --> PyJWT["PyJWT[crypto] >=2.10.1,<3"]
    PyJWT --> Crypto["cryptography"]
    Lib --> Std["stdlib: ipaddress, math, os, secrets, time, urllib.parse"]
    Lib --> Env["Consumer env: PREFIX_AUTH_ISSUER, PREFIX_AUTH_PUBLIC_KEY, PREFIX_AUTH_SUBJECTS"]
    Issuer["Token issuer (no runtime call, trust via public key)"] -.-> Env
```

Dev/CI dependencies: `pytest>=8`, `pytest-cov>=6`, `mypy>=1.13`, `ruff>=0.8` (extra `dev`), uv, platform-ci-workflows v1.1.1

Sources: `pyproject.toml`, `uv.lock`, `service_auth/__init__.py` (imports), consumer `server.py`
