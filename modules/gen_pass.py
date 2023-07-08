"""
Copyright (C) 2023  Aranggi J. Toar <at@aranggitoar.com>
Full GPL-3.0 notice https://www.gnu.org/licenses/gpl-3.0.txt
"""

import random, sys

# UTF8 code points integer representations
UTF8_CPS = list(range(128))

# Sort from the highest as to not confuse the deletion with `del LIST[i]` later
# as the deletion is by index and not value
filtered_cps = [39, 34, 32] # whitespace, double and single quote

for code_point in filtered_cps:
    del UTF8_CPS[code_point]

# Get all UTF8 characters except the filtered ones above and control characters
# (which would have length of repr() more than 3)
UTF8_CHAR = list(set([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in
                 UTF8_CPS]))

def gen_pass(length=42):
    password = ""

    for i in range(length):
        password += random.choice(UTF8_CHAR)

    return password
