# Product: Solo Empire service auth (`service_auth`)

## What it is

A small Python library (one module, `service_auth/__init__.py`) that verifies short-lived,
owner-scoped RS256 JWTs for the owner's private metadata APIs. It has no server, no CLI and
no network calls of its own.

## Who uses it

The owner's backend services, each through a **vendored copy** under `vendor/service-auth`
(accounts-metadata-api, integrations, saas-catalog, knowledge-api, ai-usage). Private Railway
builds cannot pull this repo without credentials, so consumers copy it; each copy is owned by
its consumer (no shared package between services).

## What works today

- `AuthPolicy.from_env(prefix, audience, required_scope)` loads issuer, RSA public key
  (>= 2048 bits) and allowed subjects from env vars; invalid config fails closed (503).
- `authenticate(headers)` accepts only `Bearer` RS256 tokens with all of `iss aud sub tenant_id
  scope iat nbf exp jti`, rejects remote-key headers (`jku jwk x5u x5c crit`), caps lifetime at
  120 s with 5 s leeway, requires `tenant_id == "owner"`, an allowlisted subject and the exact
  scope. Errors are `AuthError(status, code, message)` and never contain the token.
- `check_read_auth(...)` allows a static bearer token only in an unconfigured `development`
  environment.
- `readiness(...)` reports store and auth state without exposing exception text.
- `is_loopback(host)` helper.

## Quality

Strict mypy, Ruff, 19 tests (`tests/`), 99% line coverage gate, shared CI
`platform-ci-workflows` v1.1.1 (`ci-python.yml` + `security.yml`).

## Limits

- No replay database: `jti` identifies a request but is not tracked.
- Consumers must re-copy the library after a change here; nothing enforces that the copies
  match.
- Not published to PyPI.

## Status

Active library, version 0.1.0. Sentry is not applicable: the scorecard finds no runtime in this
repo (errors surface in the consuming services, which own their Sentry setup).
