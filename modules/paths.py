from pathlib import Path

# Paths for master password file secrets
DB_DIR = Path("db")
ETC_DIR = DB_DIR / ".etc"
SECRETS_DIR = DB_DIR / ".secrets"
ENC_PASS_FILE = SECRETS_DIR / "emp"
ENC_PASS_KEY_FILE = SECRETS_DIR / "empk"
