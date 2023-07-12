# Password Manager

This is an **offline Command Line Interface password manager**.

## Setup

Install requirements for running from source or bulding the source using pip
python package installer by running, `python pip install -r requirements`. Then
run the app with `python password_manager.py` or build the app with
`pyinstaller password_manager.py`.

**OR**

Download the [latest
release](https://github.com/aranggitoar/password_manager/releases) and run the
executable that's built for your OS. It is a standalone portable application.

## Usage

Simply run the app, and it will walk you through master password creation. Then
you can start creating, modifying, and retrieving passwords. For now it will
always ask for your master password on every creation, modification, and
retrieval.

![Demo of the application.](./demo.gif)

(The demo and the current application might differ a little bit.)

## Exporting Data

Simply copy the directory `./db/` into the directory where you have the source
code or executable.

Master password and master key (automatically generated on master password
creation) is stored in `./db/.secrets/`. Passwords are stored as individual
files by their names inside `./db/`.

## Acknowledgements

ASCII text arts are courtesy of [texteditor.com](https://texteditor.com/multiline-text-art/).
