"""
This file is courtesy of Martijn Pieters,
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
"""

from hashlib import pbkdf2_hmac
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

kdf_len = 32
backend = default_backend()
iterations = 100_000


def _derive_key(password: bytes,
                salt: bytes,
                iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=kdf_len,
                     salt=salt,
                     iterations=iterations,
                     backend=backend)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes,
                     password: str,
                     iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(64)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(b'%b%b%b' % (
        salt,
        iterations.to_bytes(16, 'big'),
        b64d(Fernet(key).encrypt(message)),
    ))


def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:64], decoded[64:80], b64e(decoded[80:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)
