"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import io, hashlib, hmac, sys, os
from modules.fernet_w_pass import password_decrypt

# Folder names
DB_FOLDER = "db"
INFO_FOLDER = "info"

# File names
HASHED_MASTER_PASSWORD = "hp"
KEY_OF_KEY = "kok"

def get_hashed_password():
    hashed_password = ''
    path = os.path.join(DB_FOLDER, INFO_FOLDER, HASHED_MASTER_PASSWORD)
    with open(path, "rb") as f:
        for line in f.readlines():
            hashed_password = line[:-1].decode()

    return hashed_password

hash = lambda x: hashlib.sha256(x).hexdigest()

def check_password(password, hashed):
    rehashed = hash(password)
    if rehashed == hashed:
        return True
    else:
        return False

def get_key(passed_check, password):
    if passed_check:
        key = b''
        path = os.path.join(DB_FOLDER, INFO_FOLDER, KEY_OF_KEY)
        with open(path, "rb") as f:
            for line in f.readlines():
                # line[:-1] because on file buffer reading the last character
                # is always a newline control "\n"
                key = password_decrypt(line[:-1], password)

        return key.decode()
    else:
        print("\nKey check failed.")
        print("Enter the right master password OR regenerate your key,")
        print("though the old password you have would be locked out forever.")
        sys.exit(0)

def main():
    if len(sys.argv[1:]) != 1:
        print("\nUsage: python3 ./get_key.py [password]")
        print("Example: python3 ./get_key.py 'mostS3c|2eTp455'\n")
        print("[!!!] WRAP SECRET WITH SINGLE QUOTES!\n")
        sys.exit(0)

    password = sys.argv[1]
    passed_check = check_password(password.encode(), get_hashed_password())

    print(get_key(passed_check, password))

if __name__ == '__main__':
    main()
