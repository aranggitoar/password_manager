"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import random, sys, os
import modules.prompts as prompts
import modules.master_password as mp
import modules.key as k
from modules.encryption import password_encrypt, password_decrypt
from modules.paths import DB_DIR, ETC_DIR, SECRETS_DIR

# UTF8 code points integer representations
UTF8_CPS = list(range(128))

# Sort from the highest as to not confuse the deletion with `del LIST[i]` later
# as the deletion is by index and not value
filtered_cps = [39, 34, 32]  # whitespace, double and single quote

for code_point in filtered_cps:
    del UTF8_CPS[code_point]

# Get all UTF8 characters except the filtered ones above and control characters
# (which would have length of repr() more than 3)
UTF8_CHAR = list(
    set([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in UTF8_CPS]))


def _generate(length=42):
    password = ""

    for i in range(length):
        password += random.choice(UTF8_CHAR)

    return password


def create():
    name, length, master_password = prompts.password_creation()

    path_to_file = DB_DIR / name

    if path_to_file.is_file():
        print("Password with name {} exists.".format(name))
        print("Would you like to modify that password? (y/n)")
        input("> ")

    with open(path_to_file, 'w') as f:
        # Check master password
        passed_check = mp.verify(master_password)

        if passed_check:
            # Generate new password
            new_password = _generate(length)

            print("\nYour new password for '{}':".format(name))
            print(new_password, "\n")

            # Encrypt the newly generated password
            key = k.get()
            encrypted_password = password_encrypt(new_password.encode(),
                                                  key).decode()

            # Store encrypted password
            f.write(encrypted_password)

            print("\nThe above password encrypted:")
            print(encrypted_password, "\n")
        else:
            print("\nWrong master password.")
            print("Back to main menu.")


def get():
    name, master_password = prompts.password_retrieval()

    path_to_file = DB_DIR / name

    if path_to_file.is_file():
        # Check master password
        passed_check = mp.verify(master_password)

        if passed_check:
            # Get key for encryption
            key = k.get()

            with open(path_to_file, 'rb') as f:
                for line in f.readlines():

                    # Get the encrypted password
                    print("\nYour password for '{}':".format(name))
                    print(password_decrypt(line, key).decode(), "\n")
        else:
            print("Wrong master password.")
    else:
        print("\nPassword for that doesn't exist", end="")
        print("run create_new to generate one.\n")


def get_names():
    files = os.listdir(DB_DIR)

    files.remove(ETC_DIR.parts[-1])
    files.remove(SECRETS_DIR.parts[-1])

    print("\nThere are passwords with the following names:")
    print(str(files).replace("[", "").replace("]", ""))


def modify():
    print("Modifying existing password.")
