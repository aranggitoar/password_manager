import os, sys, datetime, threading, time, signal
import modules.master_password as mp
from modules.paths import ETC_DIR, DB_DIR
import modules.password as password
import modules.art as art

# Clear console
_cc = lambda: os.system("cls" if os.name == "nt" else "clear")


def _exit():
    _cc()
    print("""

░▒█▀▀▀░█░█░░▀░░▀█▀░░▀░░█▀▀▄░█▀▀▀░░░░░░░░░░░
░▒█▀▀▀░▄▀▄░░█▀░░█░░░█▀░█░▒█░█░▀▄░░░▄▄░▄▄░▄▄
░▒█▄▄▄░▀░▀░▀▀▀░░▀░░▀▀▀░▀░░▀░▀▀▀▀░░░▀▀░▀▀░▀▀

          """)
    sys.exit(0)


def _timeoutInput(prompt):
    timeout = 60
    t = threading.Timer(timeout, _timeoutCleanup, [True])
    t.start()
    command = input(prompt)
    t.cancel()
    return command


def _timeoutCleanup(hard_exit=False):
    _cc()
    print("""

░▒█▀▀▀█░█▀▀░█▀▀░█▀▀░░▀░░▄▀▀▄░█▀▀▄░░░▒█▀▀▀░█░█░▄▀▀▄░░▀░░█▀▀▄░█▀▀░█▀▄
░░▀▀▀▄▄░█▀▀░▀▀▄░▀▀▄░░█▀░█░░█░█░▒█░░░▒█▀▀▀░▄▀▄░█▄▄█░░█▀░█▄▄▀░█▀▀░█░█
░▒█▄▄▄█░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀▀░░▀░░▀░░░▒█▄▄▄░▀░▀░█░░░░▀▀▀░▀░▀▀░▀▀▀░▀▀░

          """)
    print("Left idle for too long.")
    # Uses "hard exit" of os._exit(0) as sys.exit(0) takes time here for some
    # reason.
    if hard_exit:
        os._exit(0)
    sys.exit(0)


def _password_name_search():
    print("What is the name of the password?")
    print("\t(You can search for part of the password.)")
    name = input("> ")

    while (DB_DIR / name).is_file() is False:
        contents = os.listdir(DB_DIR)
        files = []
        potentials = []

        for content in contents:
            if (DB_DIR / content).is_file():
                files.append(content)

        for file in files:
            if name in file:
                potentials.append(file)

        if potentials:
            print("There are no password with the exact name as the ", end="")
            print("name you entered, though ones that contains it exists:")
            print(str(potentials).replace("[", "").replace("]", ""))
            print("\nWhich one did you mean to get?")
            name = input("> ")
        else:
            print("Password with that name doesn't exist, nor ", end="")
            print("passwords that contains the entered name.")
            print("\nEnter another name? (y/n)")
            confirmation = input("> ")
            if confirmation.lower() == "y":
                name = input("> ")
            else:
                name = None
                break

    return name


TIMEOUT_FLAG = chr(4242)

COMMANDS = {
    "C": password.create,
    "M": password.modify,
    "R": password.get_names,
    "G": password.get,
    "E": _exit
}


def login():
    print("""

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
▒   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒
▒   ▒▒▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒     ▒▒▒▒▒▒▒   ▒   ▒▒
▓   ▓▓▓▓▓▓▓▓▓   ▓▓   ▓▓   ▓▓   ▓   ▓▓   ▓▓   
▓   ▓▓▓▓▓▓▓▓   ▓▓▓▓   ▓  ▓▓▓   ▓   ▓▓   ▓▓   
▓   ▓▓▓▓▓▓▓▓▓   ▓▓   ▓▓    ▓   ▓   ▓▓   ▓▓   
█          ████   █████████   ██   █    ██   
█████████████████████████    ████████████████

          """)
    master_password = input("Enter your master password:\n> ")
    return mp.verify(master_password)


def setup():
    print("""

░▒█▀▀▀█░█▀▀░▀█▀░█░▒█░▄▀▀▄
░░▀▀▀▄▄░█▀▀░░█░░█░▒█░█▄▄█
░▒█▄▄▄█░▀▀▀░░▀░░░▀▀▀░█░░░

          """)
    new_master_password = input("Enter your new master password:\n> ")
    mp.create(new_master_password)


def alert_no_master_password():
    print("""

░█▀▀▄░█░░█▀▀░█▀▀▄░▀█▀
▒█▄▄█░█░░█▀▀░█▄▄▀░░█░
▒█░▒█░▀▀░▀▀▀░▀░▀▀░░▀░

          """)
    print("There is no master password ", end="")
    return input("set yet, create one? (y/n)\n> ")


def password_creation():
    print("""

░▒█▀▀█░█▀▀▄░█▀▀░█▀▀░█░░░█░▄▀▀▄░█▀▀▄░█▀▄░░░▒█▀▀▄░█▀▀▄░█▀▀░█▀▀▄░▀█▀░░▀░░▄▀▀▄░█▀▀▄
░▒█▄▄█░█▄▄█░▀▀▄░▀▀▄░▀▄█▄▀░█░░█░█▄▄▀░█░█░░░▒█░░░░█▄▄▀░█▀▀░█▄▄█░░█░░░█▀░█░░█░█░▒█
░▒█░░░░▀░░▀░▀▀▀░▀▀▀░░▀░▀░░░▀▀░░▀░▀▀░▀▀░░░░▒█▄▄▀░▀░▀▀░▀▀▀░▀░░▀░░▀░░▀▀▀░░▀▀░░▀░░▀

          """)
    print("What would be the name of the password?")
    print("\t(This is used to identify the password for retrieval.)")
    name = input("> ")

    print("How long would you want the password to be?")
    print("\t(The password will be randomized non-control UTF-8 characters")
    print("\t except for whitespace, single quote, and double quote)")
    length = input("> ")

    print("Enter your master password for encryption.")
    master_password = input("> ")

    return name, int(length), master_password


def password_retrieval():
    print("""

░▒█▀▀█░█▀▀▄░█▀▀░█▀▀░█░░░█░▄▀▀▄░█▀▀▄░█▀▄░░░▒█▀▀▄░█▀▀░▀█▀░█▀▀▄░░▀░░█▀▀░▄░░░▄░█▀▀▄░█░
░▒█▄▄█░█▄▄█░▀▀▄░▀▀▄░▀▄█▄▀░█░░█░█▄▄▀░█░█░░░▒█▄▄▀░█▀▀░░█░░█▄▄▀░░█▀░█▀▀░░█▄█░░█▄▄█░█░
░▒█░░░░▀░░▀░▀▀▀░▀▀▀░░▀░▀░░░▀▀░░▀░▀▀░▀▀░░░░▒█░▒█░▀▀▀░░▀░░▀░▀▀░▀▀▀░▀▀▀░░░▀░░░▀░░▀░▀▀

          """)
    name = _password_name_search()

    if name is None:
        raise Exception("pass")

    print("Enter your master password for authentication.")
    master_password = input("> ")

    return name, master_password


def password_modification():
    print("""

░▒█▀▀█░█▀▀▄░█▀▀░█▀▀░█░░░█░▄▀▀▄░█▀▀▄░█▀▄░░░▒█▀▄▀█░▄▀▀▄░█▀▄░░▀░░█▀▀░░▀░░█▀▄░█▀▀▄░▀█▀░░▀░░▄▀▀▄░█▀▀▄
░▒█▄▄█░█▄▄█░▀▀▄░▀▀▄░▀▄█▄▀░█░░█░█▄▄▀░█░█░░░▒█▒█▒█░█░░█░█░█░░█▀░█▀░░░█▀░█░░░█▄▄█░░█░░░█▀░█░░█░█░▒█
░▒█░░░░▀░░▀░▀▀▀░▀▀▀░░▀░▀░░░▀▀░░▀░▀▀░▀▀░░░░▒█░░▒█░░▀▀░░▀▀░░▀▀▀░▀░░░▀▀▀░▀▀▀░▀░░▀░░▀░░▀▀▀░░▀▀░░▀░░▀

          """)
    name = _password_name_search()

    print("Enter new name and/or new password.")
    print("\t(Keep them empty to keep the original, write ", end="")
    print("'autogen' in the password column to automatically ", end="")
    print("generate a new password.)")
    new_name = input("Name: ")
    password = input("Password: ")

    if password == 'autogen':
        print("How long would you like your password to be? Default is 42.")
        length = input("Length: ")

        password += " {}".format(length)

    print("\nEnter your master password for authentication.")
    master_password = input("> ")

    return name, new_name, password, master_password


def main_menu_loop():
    timeout = False

    while not timeout:
        print("""

░▒█▀▄▀█░█▀▀▄░░▀░░█▀▀▄░░░▒█▀▄▀█░█▀▀░█▀▀▄░█░▒█
░▒█▒█▒█░█▄▄█░░█▀░█░▒█░░░▒█▒█▒█░█▀▀░█░▒█░█░▒█
░▒█░░▒█░▀░░▀░▀▀▀░▀░░▀░░░▒█░░▒█░▀▀▀░▀░░▀░░▀▀▀

              """)
        print("Would you like to,")
        print("- (C)reate new password?")
        print("- (M)odify existing password?")
        print("- (R)etrieve list of password names?")
        print("- (G)et a stored password?")
        print("- (E)xit?")
        command = _timeoutInput(prompt="> ")

        if command not in COMMANDS:
            print("Command unknown, please enter only the ", end="")
            print("characters in parenthesis above.")
        else:
            command.upper()
            try:
                COMMANDS[command]()
            except Exception as e:
                if e.args[0] == "pass":
                    pass

        if command == TIMEOUT_FLAG:
            _timeoutCleanup()
            timeout = True


def failed_login():
    print("\nWrong password.")
    return input("Try again? (y/n)\n> ")


def failed_login_loop():
    retry_prompt = failed_login()
    retry = 0
    while retry != 3:
        if retry_prompt == "y":
            retry += 1
            passed_check = login()
        else:
            sys.exit(0)

    _cc()
    print("That's 3 failed attempts, remember your password first.")
    sys.exit(0)
