import modules.password as p
from modules.encryption import password_encrypt, password_decrypt
from modules.paths import ENC_PASS_FILE, ENC_PASS_KEY_FILE


def create(password):
    password_key = p.generate(64)
    print("Generating random key for master password encryption ...")

    encrypted_password = password_encrypt(password.encode(), password_key)
    print("Encrypting master password ...")

    file = open(ENC_PASS_FILE, "wb")
    file.write(encrypted_password)
    file.close()
    print("Storing encrypted master password ...")

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


def verify(user_input):
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

    decrypted_key = password_decrypt(encrypted_password_key,
                                     encrypted_password.decode())
    print("Decrypting master password key ...")
    decrypted_password = password_decrypt(encrypted_password,
                                          decrypted_key.decode())
    print("Decrypting master password ...")

    print("Checking if entered password is correct ...")
    return user_input == decrypted_password.decode()
