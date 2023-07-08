"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import sys, os
from cryptography.fernet import Fernet
from pathlib import Path
from modules.get_key import get_hashed_password, check_password, get_key

decrypt = lambda tok, key: Fernet(key).decrypt(tok)

def main():
    if len(sys.argv[1:]) != 2:
        print("\nUsage: python3 ./get.py [for_what] [master_password]")
        print("Example: python3 ./get.py 'email' 'mostS3c|2eTp455'\n")
        print("[!!!] WRAP STRINGS WITH SINGLE QUOTES!\n")
        sys.exit(0)

    for_what = sys.argv[1]
    master_password = sys.argv[2]

    path_to_file = Path(os.path.join("db", for_what))

    if path_to_file.is_file():
        # Check master password
        passed_check = check_password(master_password.encode(), get_hashed_password())

        # Get key for encryption
        key = get_key(passed_check, master_password)

        with open(path_to_file, 'rb') as f:
            for line in f.readlines():

                # Get the encrypted password
                print("\nYour password for", "{}:".format(for_what))
                print(decrypt(line, key).decode(), "\n")
    else:
        print("\nPassword for that doesn't exist", end="")
        print("run create_new to generate one.\n")

if __name__ == '__main__':
    main()
