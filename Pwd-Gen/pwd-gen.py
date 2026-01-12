#Create a random password generator with full functioning GUI and menu
'''
Generate multpiple passwords,
Change settings,
View saved passwords,
Clear saved passwords
'''

import random
import string

# Password Generation Algrithm

def generate_password():
    length = int(input("Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choise(characters) for _ in range(length))
    print("Generated password:", password)

# Password Generation Functions

def generate_password(settings):
    length = settings["length"]
    characters = settings["characters"]
    return ''.join(random.choice(characters) for _ in range(length))

def generate_multiple(settings):
    count = int(input("How many passwords?"))
    return [generate_password(settings) for _ in range(count)]

# Settings Managament

def change_settings(settings):
    print("\nChange Settings")
    print("1. Toggle symbols")
    print("2. Toggle numbers")
    print("3. Toggle uppercase letters")
    print("4. Toggle lowercase letters")
    print("5. Change password length")
    print("6. Back")

    choice = input("choose an option: ")

    if choice == "1":
        settings["use_symbols"] = not settings["use_symbols"]
    elif choice == "2":
        settings["use_numbers"] = not settings["use_numbers"]
    elif choice == "3":
        settings["use_uppercase"] = not settings["use_uppercase"]
    elif choice == "4":
        settings["use_lowercase"] = not settings["use_lowercase"]
    elif choice == "5":
        settings["length"] = int(input("Enter new length: "))

    update_character_set(settings)

def update_character_set(settings):
    chars = ""
    if settings["use_lowercase"]:
        chars += string.ascii_lowercase
    if settings["use_uppercase"]:
        chars += string.ascii_uppercase
    if settings["use_numbers"]:
        chars += string.digits
    if settings["use_symbols"]:
        chars += string.punctuation
    
    settings["characters"] = chars

# File Management

def save_password(pwd):
    with open("passwords.txt", "a") as f:
        f.write(pwd + "\n")

def view_saved():
    try:
        with open("passwords.txt", "r") as f:
            print("\n Saved Passwords")
            print(f.read())
    except FileNotFoundError:
        print("No saved passwords yet.")

def clear_saved():
    open("paswords.txt", "w").close()
    print("Saved passwords cleared.")

# Main Program Loop

def main():
    settings = {
        "length": 12,
        "use_lowercase": True,
        "use_uppercase": True,
        "use_numbers": True,
        "use_symbols": True,
        "characters": ""
    }

    update_character_set(settings)

    while True:
        print("\nPassword Generator Menu")
        print("1. Generate a password")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            generate_password()
        elif choice == "2":
            pwds = generate_multiple(settings)
            for p in pwds:
                print(p)
                save_password(p)
        elif choice == "3":
            change_settings(settings)
        elif choice == "4":
            view_saved()
        elif choice == "5":
            clear_saved()
        elif choice == "6":
            print("Goodbye.")
            break
        else: print("Invalid choice. Try again.")

main()