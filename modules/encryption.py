"""
This code is mainly courtesy of Martijn Pieters,
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
"""

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

kdf_len = 32
salt_len = 64
iter_repr_len = 16
backend = default_backend()
iterations = 100_000


def _derive_key(password: bytes, salt: bytes, iterations: int =
                iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=kdf_len, salt=salt,
                     iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int =
                     iterations) -> bytes:
    salt = secrets.token_bytes(salt_len)
    key = _derive_key(password.encode(), salt, iterations)
    del password
    return b64e(b'%b%b%b' % (salt, iterations.to_bytes(iter_repr_len,
                                                       'big'),
                             b64d(Fernet(key).encrypt(message))))


def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:salt_len], decoded[salt_len:salt_len+iter_repr_len], b64e(decoded[salt_len+iter_repr_len:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    del password
    return Fernet(key).decrypt(token)
