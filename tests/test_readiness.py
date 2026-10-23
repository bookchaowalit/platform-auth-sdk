"""readiness() and is_loopback(): health output must never leak store errors."""

import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from service_auth import AuthPolicy, is_loopback, readiness


class OkStore:
    def snapshot(self) -> object:
        return {"rows": 1}


class BrokenStore:
    def snapshot(self) -> object:
        raise RuntimeError("/secret/path/catalog.db is locked")


def ready_policy() -> AuthPolicy:
    public = (
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        .public_key()
        .public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode()
    )
    return AuthPolicy(
        "https://solo.example",
        "accounts-api",
        public,
        frozenset({"oidc-owner"}),
        "accounts:read",
    )


UNCONFIGURED = AuthPolicy("", "accounts-api", "", frozenset(), "accounts:read")


class ReadinessTests(unittest.TestCase):
    def test_ready_when_store_and_auth_ready(self) -> None:
        status, body = readiness(ready_policy(), "production", OkStore())
        self.assertEqual(status, 200)
        self.assertEqual(
            body, {"status": "ready", "source": "available", "auth": "ready"}
        )

    def test_store_failure_is_not_ready_and_hides_error(self) -> None:
        status, body = readiness(ready_policy(), "production", BrokenStore())
        self.assertEqual(status, 503)
        self.assertEqual(body["source"], "unavailable")
        self.assertNotIn("secret", repr(body))

    def test_auth_state_labels(self) -> None:
        self.assertEqual(
            readiness(UNCONFIGURED, "development", OkStore()),
            (
                503,
                {"status": "not_ready", "source": "available", "auth": "development"},
            ),
        )
        self.assertEqual(
            readiness(UNCONFIGURED, "production", OkStore())[1]["auth"], "disabled"
        )


class LoopbackTests(unittest.TestCase):
    def test_loopback_hosts(self) -> None:
        for host in ("localhost", "127.0.0.1", "127.8.9.10", "::1"):
            with self.subTest(host=host):
                self.assertTrue(is_loopback(host))

    def test_non_loopback_hosts(self) -> None:
        for host in ("0.0.0.0", "10.0.0.1", "example.com", "localhost.evil", ""):
            with self.subTest(host=host):
                self.assertFalse(is_loopback(host))


if __name__ == "__main__":
    unittest.main(verbosity=2)
