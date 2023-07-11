"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

from modules.encryption import password_decrypt
from modules.paths import SECRETS_DIR, ENC_PASS_FILE, ENC_PASS_KEY_FILE


def get():
    with open(ENC_PASS_KEY_FILE, "rb") as f:
        content = f.read()
        f.close()
    encrypted_password_key = content
    print("Retrieving encrypted master password key ...")

    with open(ENC_PASS_FILE, "rb") as f:
        content = f.read()
        f.close()
    encrypted_password = content
    print("Retrieving encrypted master password ...")

    return password_decrypt(encrypted_password_key,
                            encrypted_password.decode()).decode()
