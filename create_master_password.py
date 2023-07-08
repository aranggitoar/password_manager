"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import hashlib, sys, os
from pathlib import Path

def main():
    if len(sys.argv[1:]) < 1:
        print("\nUsage: python3 ./create_master_password.py ", end="")
        print("[master_password] [delete_previous_password]")
        print("Example: python3 ./gen_key_of_key.py 'mostS3c|2eTp455' 0\n")
        print("[!!!] WRAP STRINGS WITH SINGLE QUOTES!\n")
        sys.exit(0)

    path = Path(os.path.join("db", "info", "hp"))
    try:
        delete_previous_password = int(sys.argv[2])
    except:
        delete_previous_password = 0
        pass

    if delete_previous_password:
        try:
            os.remove(path)
            print("\nFile deleted.\n")
        except FileNotFoundError:
            print("\nFile doesn't exist, continue creating.\n")
            pass
    else:
        if path.is_file():
            print("\nPassword exists, if you forgot it you can recreate ", end="")
            print("it by running this program with 1 as the second argument.\n")
            sys.exit(0)

    master_password = sys.argv[1].encode()

    encrypted_password = hashlib.sha256(master_password).hexdigest()

    with open(path, 'w') as f:
        f.write(encrypted_password)

    print("Master password:\n", master_password.decode(), sep="")
    print("Encrypted into:\n", encrypted_password, sep="")
    print("\n[!!!] Don't forget your password.")
    print("[!!!] This is a one-way encryption.")
    print("[!!!] Though the same password would always result the same ", end="")
    print("encrypted version.\n")


if __name__ == '__main__':
    main()
