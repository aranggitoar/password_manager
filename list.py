import os

def main():
    path = os.path.abspath("db")
    files = os.listdir(path)

    files.remove("info")

    print("\nThere are passwords for:")
    print(files, "\n")

if __name__ == '__main__':
    main()
