#Create a random password generator with full functioning GUI and menu
'''
Password strength presets,
Color + UI polishing w/ ANSI codes:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m",
Error handling,
Clean architecture
'''

import random
import string

# Color Codes for UI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Password Generation Algrithm

def generate_password():
    length = int(input("Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choise(characters) for _ in range(length))
    print("Generated password:", password)

# Password Generation Functions

def generate_password(settings):
    try:
        characters = update_character_set(settings)
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
        print("1. Toggle symbols")
        print("2. Toggle numbers")
        print("3. Toggle uppercase letters")
        print("4. Toggle lowercase letters")
        print("5. Change password length")
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
    try:
        with open("passwords.txt", "a") as f:
            f.write(pwd + "\n")
    except Exception as e:
        print(RED + f"Error saving password: {e}" + RESET)

def view_saved():
    print(CYAN + "\n Saved Passwords:" + RESET)
    try:
        with open("passwords.txt", "r") as f:
            content = f.read().strip()
            if content:
                print(content)
            else:
                print(YELLOW + "No saved passwords." + RESET)
    except FileNotFoundError:
        print(YELLOW + "No saved passwords file found." + RESET)

def clear_saved():
    try:
        open("paswords.txt", "w").close()
        print(GREEN + "Saved passwords cleared." + RESET)
    except Exception as e:
        print(RED + f"Error clearing file: {e}" + RESET)

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
        elif choice == "2":
            pwds = generate_multiple(settings)
            for p in pwds:
                if p:
                    print(GREEN + p + RESET)
                    save_password(p)
        elif choice == "3":
            change_settings(settings)
        elif choice == "4":
            view_saved()
        elif choice == "5":
            clear_saved()
        elif choice == "6":
            print(GREEN + "Goodbye." + RESET)
            break
        else: 
            print(RED + "Invalid choice. Try again." + RESET)

main()