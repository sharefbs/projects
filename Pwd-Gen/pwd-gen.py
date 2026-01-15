#Create a random password generator with full functioning GUI and menu
'''
Generates persistent key from key.key file,
Add encryption to saved passwords before writing to file,
Decrypts saved passwords when viewing them
'''

import random
import string
import os
from cryptography.fernet import Fernet

# Color Codes for UI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Encryption Key Management

def load_or_create_key():
    key_file = "key.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
    else:
        key =Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        print(YELLOW + "New encryption key created and saved to key.key" + RESET)
    return Fernet(key)

# Password Generation Functions

def build_character_set(settings):
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
    return chars

def generate_password(settings):
    try:
        characters = build_character_set(settings)
        if not characters:
            print(RED + "Error: No character types selected." + RESET)
            return None
        return ''.join(random.choice(characters) for _ in range(settings["length"]))
    except Exception as e:
        print(RED + f"Unexpected Error: {e}" + RESET)
        return None
    
def generate_multiple(settings):
    try:
        count = int(input("How many passwords?"))
        if count <= 0:
            print(RED + "Count must be positive." + RESET)
            return []
        return [generate_password(settings) for _ in range(count)]
    except ValueError:
        print(RED + "Invalid number." + RESET)
        return []

#PRESETS

def apply_preset(settings):
    print(CYAN + "\nStrength Presets" + RESET)
    print("1. Weak (Letters only, length 8)")
    print("2. Medium (letters and numbers)")
    print("3. Strong (letters + numbers + symbols)")
    print("4. Custom settings")

    choice = input("Choose preset: ")

    if choice == "1":
        settings.update({
            "length": 8,
            "use_lowercase": True,
            "use_uppercase": True,
            "use_numbers": False,
            "use_symbols": False
        })
    elif choice == "2":
        settings.update({
            "length": 12,
            "use_lowercase": True,
            "use_uppercase": True,
            "use_numbers": True,
            "use_symbols": False
        })
    elif choice == "3":
        settings.update({
            "length": 16,
            "use_lowercase": True,
            "use_uppercase": True,
            "use_numbers": True,
            "use_symbols": True
        })
    elif choice == "4":
        print(YELLOW + "Returning to custom settings menu ..." + RESET)
    else:
        print(RED + "Invalid choice." + RESET)

# Settings Managament

def change_settings(settings):
    while True:
        print(CYAN + "\nChange Settings" + RESET)
        print("1. Toggle symbols (currently: {})".format(settings["use_symbols"]))
        print("2. Toggle numbers (currently: {})".format(settings["use_numbers"]))
        print("3. Toggle uppercase letters (currently: {})".format(settings["use_uppercase"]))
        print("4. Toggle lowercase letters (currently: {})".format(settings["use_lowercase"]))
        print("5. Change password length (currently: {})".format(settings["length"]))
        print("6. Strength presets")
        print("7. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            settings["use_symbols"] = not settings["use_symbols"]
        elif choice == "2":
            settings["use_numbers"] = not settings["use_numbers"]
        elif choice == "3":
            settings["use_uppercase"] = not settings["use_uppercase"]
        elif choice == "4":
            settings["use_lowercase"] = not settings["use_lowercase"]
        elif choice == "5":
            try:
                new_length = int(input("Enter new length: "))
                if new_length > 0:
                    settings["length"] = new_length
                else:
                    print(RED + "Length must be positive" + RESET)
            except ValueError:
                print(RED + "Invalid number." + RESET)
        elif choice == "6":
            apply_preset(settings)
        elif choice == "7":
            break
        else:
            print(RED + "Invalid choice." + RESET)

# File Management

def save_password(pwd, cipher):
    if not pwd: 
        return
    try:
        token = cipher.encrypt(pwd.encode("utf-8"))
        with open("passwords.txt", "ab") as f:
            f.write(token + b"\n")
    except Exception as e:
        print(RED + f"Error saving password: {e}" + RESET)

def view_saved(cipher):
    print(CYAN + "\nSaved Passwords:" + RESET)
    try:
        if not os.path.exists("passwords.txt"):
            print(YELLOW + "No saved passwords file found." + RESET)
            return
        with open("passwords.txt", "rb") as f:
            lines = f.readlines()
        if not lines:
            print(YELLOW + "No saved passwords." + RESET)
            return
        for i, line in enumerate(lines, start = 1):
            line = line.strip()
            if not line:
                continue
            try:
                decrypted = cipher.decrypt(line).decode("utf-8")
                print(f"{i}. {decrypted}")
            except Exception as e:
                print(RED + f"Error decrypting line {i}: {e}" + RESET)
    except Exception as e:
        print(RED + f"Error reading file: {e}" + RESET)

def clear_saved():
    try:
        open("passwords.txt", "w").close()
        print (GREEN + "Saved passwords cleared." + RESET)
    except Exception as e:
        print(RED + f"Error clearing file: {e}" + RESET)

# Main Program Loop

def main():
    cipher = load_or_create_key()

    settings = {
        "length": 12,
        "use_lowercase": True,
        "use_uppercase": True,
        "use_numbers": True,
        "use_symbols": True,
        "characters": ""
    }

    build_character_set(settings)

    while True:
        print(BLUE + "\nPassword Generator Menu" + RESET)
        print("1. Generate a password")
        print("2. Generate multiple passwords")
        print("3. Change settings")
        print("4. View saved passwords")
        print("5. Clear saved passwords")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            pwd = generate_password(settings)
            if pwd:
                print(GREEN + "Generated: " + pwd + RESET)
                save_password(pwd, cipher)
        elif choice == "2":
            pwds = generate_multiple(settings)
            for p in pwds:
                if p:
                    print(GREEN + p + RESET)
                    save_password(p, cipher)
        elif choice == "3":
            change_settings(settings)
        elif choice == "4":
            view_saved(cipher)
        elif choice == "5":
            clear_saved()
        elif choice == "6":
            print(GREEN + "Goodbye." + RESET)
            break
        else: 
            print(RED + "Invalid choice. Try again." + RESET)

if __name__ == "__main__":
    main()