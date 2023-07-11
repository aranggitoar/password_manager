import os, sys, datetime, threading, time, signal
import modules.master_password as mp
from modules.paths import ETC_DIR, DB_DIR
import modules.password as password

# Clear console
cc = lambda: os.system("cls" if os.name == "nt" else "clear")

TIMEOUT_FLAG = chr(4242)

COMMANDS = {
    "C": password.create,
    "M": password.modify,
    "R": password.get_names,
    "G": password.get
}


def _timeoutInput(prompt):
    timeout = 120
    t = threading.Timer(timeout, _timeoutCleanup, [True])
    t.start()
    command = input(prompt)
    t.cancel()
    return command


def _timeoutCleanup(hard_exit=False):
    cc()
    print("Session is expired.")
    print("Exiting ...")
    # Uses "hard exit" of os._exit(0) as sys.exit(0) takes time here for some
    # reason.
    if hard_exit:
        os._exit(0)
    sys.exit(0)


def login():
    print("\n-----\nLOGIN\n-----\n")
    master_password = input("Enter your master password:\n> ")
    return mp.verify(master_password)


def setup():
    print("\n-----\nSETUP\n-----\n")
    new_master_password = input("Enter your new master password:\n> ")
    mp.create(new_master_password)


def alert_no_master_password():
    print("\n-----\nALERT\n-----\n")
    print("There is no master password ", end="")
    return input("set yet, create one? (y/n)\n> ")


def password_creation():
    print("\n------------\nNEW PASSWORD\n------------\n")
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
    print("\n-----------------\nRETRIEVE PASSWORD\n-----------------\n")
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
            print("\nWhich one would you like to retrieve?")
            name = input("> ")
        else:
            print("Password with that name doesn't exist, nor ", end="")
            print("passwords that contains the entered name.")
            print("\nEnter another name? (y/n)")
            confirmation = input("> ")
            if confirmation.lower() == "y":
                name = input("> ")
            else:
                break

    print("Enter your master password for authentication.")
    master_password = input("> ")

    return name, master_password


def password_modification():
    print("\n-----------------\nRETRIEVE PASSWORD\n-----------------\n")
    print("What is the name of the password?")
    print("\t(You can search for part of the password.)")
    name = input("> ")


def main_menu_loop():
    timeout = False

    while not timeout:
        print("\n---------\nMAIN MENU\n---------\n")
        print("Would you like to,")
        print("- (C)reate new password?")
        print("- (M)odify existing password?")
        print("- (R)etrieve list of password names?")
        print("- (G)et a stored password?")
        command = _timeoutInput(prompt="> ")

        if command not in COMMANDS:
            print("Command unknown, please enter only the ", end="")
            print("characters in parenthesis above.")
        else:
            command.upper()
            COMMANDS[command]()

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

    cc()
    print("That's 3 failed attempts, remember your password first.")
    sys.exit(0)
