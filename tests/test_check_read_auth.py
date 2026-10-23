"""check_read_auth: static dev tokens only in an unconfigured development environment."""

import time
import unittest

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from service_auth import AuthError, AuthPolicy, check_read_auth

UNCONFIGURED = AuthPolicy("", "accounts-api", "", frozenset(), "accounts:read")


class CheckReadAuthTests(unittest.TestCase):
    def test_development_without_static_token_allows_anonymous_reads(self) -> None:
        self.assertIsNone(
            check_read_auth(UNCONFIGURED, {}, environment="development", token="")
        )

    def test_development_static_token_must_match(self) -> None:
        self.assertIsNone(
            check_read_auth(
                UNCONFIGURED,
                {"authorization": "Bearer dev-token"},
                environment="development",
                token="dev-token",
            )
        )
        for headers in (
            {},
            {"authorization": "Bearer wrong"},
            {"authorization": "Basic dev-token"},
        ):
            with self.subTest(headers=headers), self.assertRaises(AuthError) as ctx:
                check_read_auth(
                    UNCONFIGURED, headers, environment="development", token="dev-token"
                )
            self.assertEqual(ctx.exception.status, 401)
            self.assertNotIn("dev-token", str(ctx.exception))

    def test_static_token_is_ignored_outside_development(self) -> None:
        # Production with no JWT config fails closed (503) even with the static token.
        with self.assertRaises(AuthError) as ctx:
            check_read_auth(
                UNCONFIGURED,
                {"authorization": "Bearer dev-token"},
                environment="production",
                token="dev-token",
            )
        self.assertEqual(ctx.exception.status, 503)

    def test_partial_config_in_development_uses_jwt_path(self) -> None:
        # Any JWT setting present means the operator meant JWT auth: no static fallback.
        partial = AuthPolicy(
            "https://solo.example", "accounts-api", "", frozenset(), "accounts:read"
        )
        with self.assertRaises(AuthError) as ctx:
            check_read_auth(
                partial,
                {"authorization": "Bearer dev-token"},
                environment="development",
                token="dev-token",
            )
        self.assertEqual(ctx.exception.status, 503)

    def test_configured_policy_returns_identity(self) -> None:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public = (
            key.public_key()
            .public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode()
        )
        policy = AuthPolicy(
            "https://solo.example",
            "accounts-api",
            public,
            frozenset({"oidc-owner"}),
            "accounts:read",
        )
        now = int(time.time())
        token = jwt.encode(
            {
                "iss": "https://solo.example",
                "aud": "accounts-api",
                "sub": "oidc-owner",
                "tenant_id": "owner",
                "scope": "accounts:read",
                "iat": now,
                "nbf": now,
                "exp": now + 60,
                "jti": "req-1",
            },
            key,
            algorithm="RS256",
        )
        identity = check_read_auth(
            policy,
            {"Authorization": "Bearer " + token},
            environment="production",
            token="",
        )
        self.assertIsNotNone(identity)
        assert identity is not None
        self.assertEqual(identity.subject, "oidc-owner")


if __name__ == "__main__":
    unittest.main(verbosity=2)
