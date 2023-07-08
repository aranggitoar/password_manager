"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import os

def main():
    path = os.path.abspath("db")
    files = os.listdir(path)

    files.remove("info")

    print("\nThere are passwords for:")
    print(files, "\n")

if __name__ == '__main__':
    main()
