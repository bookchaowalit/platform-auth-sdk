# Solo Empire service auth

Installed library for the four owner-private metadata services. Install it
alongside the owning service with `python3 -m pip install ./packages/service-auth ./services/accounts-api`.
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

Test using an environment where the package is installed:

```bash
python3 -m unittest discover -s packages/service-auth/tests -v
```
