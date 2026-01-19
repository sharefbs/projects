#Create a random password generator command prompt menu, GUI is not required.
#Passwords should be saved to a file with encryption.
'''
Revisit:
Clear saved passwords function to allow label-based deletion,
Multiple password generation and saving in main()

Add features:
Search function,
Password strength meter
'''

import random
import string
import os
from cryptography.fernet import Fernet
import logging

# Logging Function
logging.basicConfig(
    filename="password_generator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        logging.info(f"Generated password with length {settings['length']}")
        return ''.join(random.choice(characters) for _ in range(settings["length"]))
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        print(RED + f"Unexpected Error: {e}" + RESET)
        return None
    
def generate_multiple(settings):
    try:
        count = int(input("How many passwords?"))
        if count <= 0:
            print(RED + "Count must be positive." + RESET)
            return []
        logging.info(f"Generated passwords with length {settings['length']}")
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
    logging.info(f"Settings updated: {settings}")

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
        logging.info(f"Settings updated: {settings}")

# File Management

def save_password(label, pwd, cipher):
    if not pwd: 
        return
    try:
        token = cipher.encrypt(pwd.encode("utf-8"))
        with open("passwords.txt", "ab") as f:
            entry = f"{label}:".encode("utf-8") + token + b"\n"
            f.write(entry)
        logging.info(f"Saved password with label '{label}'")
    except Exception as e:
        logging.error(f"Error saving password: {e}")
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
                label, encrypted = line.split(b":", 1)
                decrypted = cipher.decrypt(encrypted).decode("utf-8")
                print(f"{i}. {label.decode('utf-8')} -> {decrypted}")
            except Exception as e:
                logging.error(f"Error decrypting line {i}: {e}")
                print(RED + f"Error decrypting line {i}: {e}" + RESET)
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        print(RED + f"Error reading file: {e}" + RESET)

def clear_saved_by_label(target_label):
    if not os.path.exists("passwords.txt"):
        print(YELLOW + "No saved passwords file found." + RESET)
        return

    try:
        with open("passwords.txt", "rb") as f:
            lines = f.readlines()

        new_lines = []
        removed = False

        for line in lines:
            if not line.strip():
                continue

            label, _ = line.split(b":", 1)
            if label.decode("utf-8") != target_label:
                new_lines.append(line)
            else:
                removed = True

        if not removed:
            print(RED + f"No entry found with label '{target_label}'." + RESET)
            return
        
        with open("passwords.txt", "wb") as f:
            f.writelines(new_lines)

        logging.info(f"Cleared password(s) with label '{target_label}'")
        print (GREEN + f"Password with label '{target_label}' cleared." + RESET)

    except Exception as e:
        logging.error(f"Error clearing file: {e}")
        print(RED + f"Error clearing file: {e}" + RESET)

def clear_all_saved():
    try:
        open("passwords.txt", "w").close()
        logging.info("Cleared all saved passwords")
        print(GREEN + "All saved passwords cleared." + RESET)

    except Exception as e:
        logging.error(f"Error clearing passwords: {e}")
        print(RED + f"Error clearing passwords: {e}" + RESET)

# Export/Import Functions

def export_passwords(cipher):
    if not os.path.exists("passwords.txt"):
        print(YELLOW + "No passwords to export." + RESET)
        return
    try:
        with open("passwords.txt", "rb") as f:
            lines = f.readlines()
        with open("exported_passwords.txt", "w") as out:
            for line in lines:
                if not line.strip():
                    continue
                label, encrypted = line.split(b":", 1)
                decrypted = cipher.decrypt(encrypted).decode("utf-8")
                out.write(f"{label.decode('utf-8')}:{decrypted}\n")
        logging.info("Exported passwords to exported_passwords.txt")
        print(GREEN + "Passwords exported to exported_passwords.txt" + RESET)
    except Exception as e:
        logging.error(f"Error exporting passwords: {e}")
        print(RED + f"Error exporting passwords: {e}" + RESET)

def import_passwords(cipher):
    filename = input("Enter filename to import from: ")
    if not os.path.exists(filename):
        print(RED + "File not found." + RESET)
        return
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        with open("passwords.txt", "ab") as out:
            for line in lines:
                if ":" not in line:
                    continue
                label, pwd = line.strip().split(":", 1)
                token = cipher.encrypt(pwd.encode("utf-8"))
                out.write(label.encode("utf-8") + b":" + token + b"\n")
        logging.info(f"Imported passwords from {filename}")
        print(GREEN + "Passwords imported successfuly." + RESET)
    except Exception as e:
        logging.error(f"Error importing passwords: {e}")
        print(RED + f"Error importing passwords: {e}" + RESET)

# Search Function
def search_passwords(cipher):
    term = input("Enter search term: ").lower()

    if not os.path.exists("passwords.txt"):
        print(YELLOW + "No saved passwords file found." + RESET)
        return
    
    try:
        with open("passwords.txt", "rb") as f:
            lines = f.readlines()

        matches = []

        for line in lines:
            if not line.strip():
                continue

            try:
                label, encrypted = line.split(b":", 1)
                label_text = label.decode("utf-8")

                if term in label_text.lower():
                    decrypted = cipher.decrypt(encrypted).decode("utf-8")
                    matches.append((label_text, decrypted))

                logging.info(f"Decrypted password(s) with label '{label_text}'")
                
            except Exception as e:
                logging.error(f"Error decrypting entry: {e}")
                print(RED + f"Error decrypting entry: {e}" + RESET)

        if not matches:
            print(YELLOW + "No matches found." + RESET)
        else:
            print(CYAN + f"\nMatches for '{term}':" + RESET)

            for i, (label, pwd) in enumerate(matches, start=1):
                print(f"{i}. {label} -> {pwd}")

            logging.info(f"Found password(s) with '{term}'")

    except Exception as e:
        logging.error(f"Error searching passwords: {e}")
        print(RED + f"Error searching passwords: {e}" + RESET)

# Password Strength Meter Function

def password_strength(password):
    score = 0

    # length scoring
    if len(password) >= 8:
        score += 2
    if len(password) >= 12:
        score += 2
    if len(password) >= 16:
        score += 2

    # character variety
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    # repetition penalty
    if len(set(password)) < len(password) * 0.6:
        score -= 1

    # clamp score between 0 and 10
    score = max(0, min(score, 10))

    # determine label
    if score <= 3:
        label = RED + "Weak" + RESET
    elif score <= 6:
        label = YELLOW + "Medium" + RESET
    else:
        label = GREEN + "Strong" + RESET
    
    # visual meter
    filled = "#" * score
    empty = "-" * (10 - score)
    meter = f"[{filled}{empty}]"

    print(f"Strength: {meter} {score}/10 ({label})")
    return score

# Main Program Loop

def main():
    cipher = load_or_create_key()

    settings = {
        "length": 12,
        "use_lowercase": True,
        "use_uppercase": True,
        "use_numbers": True,
        "use_symbols": True
    }

    build_character_set(settings)

    while True:
        print(BLUE + "\nPassword Generator Menu" + RESET)
        print("1. Generate a password")
        print("2. Generate multiple passwords")
        print("3. Change settings")
        print("4. View saved passwords")
        print("5. Clear saved passwords")
        print("6. Export passwords")
        print("7. Import passwords")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            pwd = generate_password(settings)
            if pwd:
                print(GREEN + "Generated: " + pwd + RESET)
                label = input("Enter a label for this password (e.g., Gmail, Bank, Steam): ")
                save_password(label, pwd, cipher)
        elif choice == "2":
            multi_label = input("Enter a label for these passwords (i.e., Outlook, Bank, Steam): ")
            pwds = generate_multiple(settings)
            for i, p in enumerate(pwds, start=1):
                if p:
                    print(GREEN + p + RESET)
                    save_password(f"{multi_label}_{i}", p, cipher)
        elif choice == "3":
            change_settings(settings)
        elif choice == "4":
            print(YELLOW + "1. View all saved passwords" + RESET)
            print(YELLOW + "2. Search saved passwords by label" + RESET)
            sub = input("Choose option: ")

            if sub == "1":
                view_saved(cipher)
            elif sub == "2":
                search_passwords(cipher)
            else:
                print(RED + "Invalid choice." + RESET)
                continue
        elif choice == "5":
            print(YELLOW + "1. Clear by label" + RESET)
            print(YELLOW + "2. Delete all saved passwords" + RESET)
            sub = input("Choose Option: ")

            if sub == "1":
                label = input("Enter label to delete: ")
                clear_saved_by_label(label)
            elif sub == "2":
                confirm_delete_all = input("Type 'YES' to confirm deletion of ALL passwords: ")
                if confirm_delete_all == "YES":
                    clear_all_saved()
                else:
                    print(YELLOW + "Canceling clear operation." + RESET)
            else:
                print(RED + "Invalid choice." + RESET)
                continue
        elif choice == "6":
            print(RED + "WARNING: Exported passwords will be in plain text." + RESET)
            confirm_export = input("Type 'YES' to confirm export: ")
            if confirm_export == "YES":
                export_passwords(cipher)
            else:
                print(YELLOW + "Canceling export operation." + RESET)
                continue
        elif choice == "7":
            import_passwords(cipher)
        elif choice == "8":
            print(GREEN + "Goodbye." + RESET)
            break
        else: 
            print(RED + "Invalid choice. Try again." + RESET)
            continue

if __name__ == "__main__":
    main()