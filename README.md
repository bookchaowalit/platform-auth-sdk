# Solo Empire service auth

Moved out of solo-empire `packages/service-auth` on 2026-10-11 with its history (subtree split).
Canonical home of the library; consumers (`accounts/services/accounts-metadata-api`,
`integrations`, `saas-catalog`, `knowledge-api`, `ai-usage`) carry a **vendored copy**
under `vendor/service-auth` (private repos cannot pull this over HTTPS in a Railway/Docker build without
credentials). Update here, then re-copy `service_auth/`, `pyproject.toml` and `tests/` into each consumer.

Installed library for the owner-private metadata services. Install it
alongside the owning service with `python3 -m pip install .` (or `./vendor/service-auth` in a consumer).
Runtime imports use `service_auth`; no repository path is added.

`AuthPolicy.from_env(prefix, audience, required_scope)` validates local PEM
RSA public-key configuration. `authenticate(headers)` returns only sanitized
`Identity(subject, tenant_id, scope)` or safe `AuthError(status, code, message)`.
Configuration never contains a signing private key. RS256 is fixed, remote key
headers are rejected, subjects are allowlisted, tenant is always `owner`,
and scope must match exactly. Required issuer is an exact HTTPS origin;
audience is a single service name. All dates must be finite numeric values.
Required `iat/nbf/exp/jti`, 120-second maximum lifetime and 5-second clock
leeway bound token validity. JWT IDs identify requests; this read-only library
does not maintain a replay database.

See [PyJWT API](https://pyjwt.readthedocs.io/en/latest/api.html) for fixed
algorithm selection and required-claim verification. Dependency is
`PyJWT[crypto]>=2.10.1,<3`.

Development uses [uv](https://docs.astral.sh/uv/) with the committed `uv.lock`
(the same steps run in CI through the shared `ci-python.yml`):

```bash
uv sync --frozen --all-extras
uv run ruff check . && uv run ruff format --check .
uv run mypy .            # strict, see [tool.mypy] in pyproject.toml
uv run pytest --cov      # CI gate: 99% line coverage
```

The tests are plain `unittest`, so `python3 -m unittest discover -s tests -v` also works in a
consumer's vendored copy. What the library is and is not: [PRODUCT.md](PRODUCT.md).
