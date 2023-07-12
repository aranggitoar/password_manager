"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import os
import modules.prompts as prompts
from modules.encryption import password_encrypt, password_decrypt
from modules.paths import DB_DIR, SECRETS_DIR, ETC_DIR, ENC_PASS_FILE


def main():
    # Check if a master password is setup
    try:
        file = open(ENC_PASS_FILE, "r+")
        file.close()
        setup = ""
    except:
        setup = prompts.alert_no_master_password()

    if setup == "y":
        # Setup directories
        if DB_DIR.is_dir() is False:
            os.makedirs(DB_DIR)
        if SECRETS_DIR.is_dir() is False:
            os.makedirs(SECRETS_DIR)
        # Setup master password
        prompts.setup()

    passed_check = prompts.login()

    if passed_check:
        prompts.main_menu_loop()
    else:
        prompts.failed_login_loop()


if __name__ == '__main__':
    main()
