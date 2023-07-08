# Password Manager

In real usage, compile the scripts into an executable.

[!!] Related to that, maybe reduce the number of executables?

## Initial Setup

1. Create your master password/secret
2. Hash your master password with SHA256 and store it in a file named `hs`
   ([!!] hash function and file name can be made to be configurable later,
   also this should be made into a script)
3. Generate a key with cryptography.fernet.Fernet.generate_key() and store
   it in a file named `kok` ([!!] should be made into a script)
4. Generate a key of key (or token of key) by calling `gen_key_of_key.py`
   using single-quote wrapped master password as the argument and `kok`
   file filled with the key generated before
5. Now ready to encrypt and decrypt passwords!

## Encrypting and Decrypting

[!!] Encrypted passwords should be stored somewhere.

To get the encrypted password/secret:
`python3 ./encrypt.py [secret_to_encrypt] [master_secret]`

To get the decrypted password/secret
`python3 ./decrypt.py [token_to_decrypt] [master_secret]`

## Functionalities as of Now

1. Generate custom password with custom length or default of 42,
    `python3 gen_new_pass.py [length|DEFAULT]`
2. Encrypting and decrypting as explained above
3. One master password with two layers of security: hashed master
   password for total authorization and encrypted key for password
   encryption and decryption

## Planned Functionalities

1. Database of passwords, individual files in a directory would be
   practical
2. GUI
3. Authentication for decryption of individual password by prompting the
   master password
