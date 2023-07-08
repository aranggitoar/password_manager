"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import sys, os
from cryptography.fernet import Fernet
from pathlib import Path
from modules.gen_pass import gen_pass
from modules.get_key import get_hashed_password, check_password, get_key

encrypt = lambda msg, key: Fernet(key).encrypt(msg)

def main():
    if len(sys.argv[1:]) != 3:
        print("\nUsage: python3 ./create_new.py [for_what] ", end="")
        print("[password_length], [master_password]")
        print("Example: python3 ./create_new.py 'email' 42 'mostS3c|2eTp455'\n")
        print("[!!!] WRAP STRINGS WITH SINGLE QUOTES!\n")
        sys.exit(0)

    for_what = sys.argv[1]
    password_length = int(sys.argv[2])
    master_password = sys.argv[3]

    path_to_file = Path(os.path.join("db", for_what))

    if path_to_file.is_file():
        print("File exists, if you want to change the password ", end="")
        print("instead, run change_existing program.")
        sys.exit(0)

    with open(path_to_file, 'w') as f:
        # Generate new password
        new_password = gen_pass(password_length)

        print("\nYour new password for", "'{}':".format(for_what))
        print(new_password, "\n")

        # Check master password
        passed_check = check_password(master_password.encode(), get_hashed_password())

        # Get key for encryption
        key = get_key(passed_check, master_password)

        encrypted_password = encrypt(new_password.encode(), key).decode()

        # Store encrypted password
        f.write(encrypted_password)

        print("The above password encrypted:")
        print(encrypted_password, "\n")

if __name__ == '__main__':
    main()
