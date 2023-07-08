import sys
from get_key import get_hashed_secret, check_secret
from fernet_w_pass import password_encrypt

def _gen_key_of_key(passed_check, secret):
    if passed_check:
        key = b''
        with open("kok", "rb") as f:
            for line in f.readlines():
                # If new key of key is to be generated,
                # kok has to contain the original key
                token = password_encrypt(line.decode().split("\n")[0].encode(), secret)

        return token.decode()

def main():
    if len(sys.argv[1:]) != 1:
        print("\nUsage: python3 ./gen_key_of_key.py [secret]")
        print("Example: python3 ./gen_key_of_key.py 'mostS3c|2eTp455'\n")
        print("[!!!] WRAP STRINGS WITH SINGLE QUOTES!\n")
        sys.exit(0)

    secret = sys.argv[1]
    passed_check = check_secret(secret.encode(), get_hashed_secret)

    print("\nHere is your key of key:")
    print(_gen_key_of_key(passed_check, secret), "\n")
    print("[**] Remember your password well.")
    print("There is no recovery measure for now.")
    print("")

if __name__ == '__main__':
    main()
