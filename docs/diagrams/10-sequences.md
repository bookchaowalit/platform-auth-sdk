# 10 — Sequences

## 1. Production read: `check_read_auth` → `authenticate` (สำเร็จ)

```mermaid
sequenceDiagram
    participant C as Caller
    participant S as Consumer server.py
    participant L as service_auth
    participant J as PyJWT
    C->>S: GET with Authorization Bearer token
    S->>L: check_read_auth(policy, headers, environment, token)
    L->>L: environment is not development or policy.configured
    L->>L: authenticate(headers)
    L->>L: key loaded? scheme bearer, token length <= 8192, no surrounding whitespace
    L->>J: get_unverified_header(token)
    J-->>L: header
    L->>L: alg == RS256, no jku jwk x5u x5c crit
    L->>J: decode(token, key, RS256, issuer, audience, leeway 5, strict_aud, require 9 claims)
    J-->>L: claims
    L->>L: iss and aud equal policy, iat nbf exp finite numbers
    L->>L: 0 < exp-iat <= 120, iat-5 <= nbf < exp, now-125 <= iat <= now+5
    L->>L: jti is str, 1..128 chars, no char <= 0x20
    L->>L: tenant_id owner, sub in subjects, scope equals required_scope
    L-->>S: Identity(sub, owner, scope)
    S-->>C: data response
```

## 2. Rejections

```mermaid
sequenceDiagram
    participant S as Consumer server.py
    participant L as service_auth
    S->>L: authenticate(headers)
    alt _key is None
        L-->>S: AuthError 503 reads_disabled
    else header, signature, claim or time check fails, or PyJWTError ValueError TypeError OverflowError
        L-->>S: AuthError 401 unauthorized
    else tenant_id, sub or scope mismatch
        L-->>S: AuthError 403 forbidden
    end
```

## 3. Local development fallback

```mermaid
sequenceDiagram
    participant S as Consumer server.py
    participant L as check_read_auth
    S->>L: environment development, policy not configured
    alt token empty
        L-->>S: None (anonymous read)
    else Bearer value matches token (secrets.compare_digest)
        L-->>S: None
    else mismatch or other scheme
        L-->>S: AuthError 401 unauthorized
    end
```

หมายเหตุ: path นี้อ่าน `headers.get("authorization")` ตัวเล็กเท่านั้น ส่วน `authenticate` หา header แบบไม่สนตัวพิมพ์

## 4. Readiness

```mermaid
sequenceDiagram
    participant S as Consumer health handler
    participant R as readiness
    participant St as SnapshotStore (consumer)
    S->>R: readiness(policy, environment, store)
    R->>St: snapshot()
    alt raises any Exception
        R->>R: source unavailable
    else returns
        R->>R: source available
    end
    R-->>S: 200 ready or 503 not_ready, auth ready / development / disabled
```

Sources: `service_auth/__init__.py`, `tests/test_auth.py`, `tests/test_check_read_auth.py`, `tests/test_readiness.py`
