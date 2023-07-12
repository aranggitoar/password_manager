"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import hashlib
from modules.password import generate
from modules.encryption import password_encrypt, password_decrypt
from modules.paths import ENC_PASS_FILE, ENC_PASS_KEY_FILE


def create(password: str):
    password_key = generate(64)
    print("Generating random key for master password encryption ...")

    sha3_512 = hashlib.sha3_512()
    sha3_512.update(password.encode())
    hashed_password = sha3_512.hexdigest()
    print("Creating hash of master password ...")

    encrypted_password = password_encrypt(hashed_password.encode(), password_key)
    print("Encrypting hash of master password ...")

    file = open(ENC_PASS_FILE, "wb")
    file.write(encrypted_password)
    file.close()
    print("Storing encrypted hash of master password ...")

    encrypted_password_key = password_encrypt(password_key.encode(),
                                              encrypted_password.decode())
    print("Encrypting master password key ...")

    file = open(ENC_PASS_KEY_FILE, "wb")
    file.write(encrypted_password_key)
    file.close()
    print("Storing encrypted master password key ...")

    del encrypted_password_key
    del encrypted_password
    del password_key
    del password
    print("New master password successfully created!")


def verify(user_input: str) -> bool:
    with open(ENC_PASS_KEY_FILE, "rb") as f:
        content = f.read()
        f.close()
    encrypted_password_key = content
    print("Retrieving encrypted master password key ...")

    with open(ENC_PASS_FILE, "rb") as f:
        content = f.read()
        f.close()
    encrypted_password = content
    print("Retrieving encrypted hash of master password ...")

    decrypted_key = password_decrypt(encrypted_password_key,
                                     encrypted_password.decode())
    print("Decrypting master password key ...")
    decrypted_password = password_decrypt(encrypted_password,
                                          decrypted_key.decode())
    print("Decrypting hash of master password ...")

    sha3_512 = hashlib.sha3_512()
    sha3_512.update(user_input.encode())
    hashed_user_input = sha3_512.hexdigest()

    print("Checking if the entered password is correct ...")
    return hashed_user_input == decrypted_password.decode()
