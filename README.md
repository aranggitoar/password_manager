# Password Manager

This is an **offline Command Line Interface password manager**.

In real usage, compile the scripts into an executable?

[!!] Related to that, maybe reduce the number of executables?

## Initial Setup

1. Create your master password/secret
2. Create a hash of your master password using `create_master_password.py`
3. Generate a key with cryptography.fernet.Fernet.generate_key() and store
   it in a file named `kok` ([!!] should be made into a script)
4. Generate a key of key (or token of key) by calling `gen_key_of_key.py`
5. Now ready to create and get passwords!

## Creating and Getting Passwords

Usage examples will be run on commands with no arguments.

To create the password:
`python3 ./create.py`

To get the password:
`python3 ./get.py`

## Functionalities as of Now

1. Create and store a hashed master password
2. Create an encryption key using the master password
3. One master password with two layers of security: hashed master password
   for total authorization and the encrypted key for password encryption and
   decryption
4. Generate custom password with custom length or default of 42
5. Automatic encryption on password creation and automatic decryption on
   password retrieval using the above mentioned encryption key
6. Retrieve a stored password
7. Save the passwords as individual files in a default directory `db`

## Planned Functionalities

1. Graphical User Interface

## TO DO

1. Tidy up the whole source code
