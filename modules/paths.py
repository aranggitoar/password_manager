"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

from pathlib import Path

# Paths for master password file secrets
DB_DIR = Path("db")
ETC_DIR = DB_DIR / ".etc"
SECRETS_DIR = DB_DIR / ".secrets"
ENC_PASS_FILE = SECRETS_DIR / "emp"
ENC_PASS_KEY_FILE = SECRETS_DIR / "empk"
