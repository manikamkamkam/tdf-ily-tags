import argparse
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from getpass import getpass
from datetime import datetime, timedelta

# Define the data directory
DATA_DIR = 'data'

# File paths
USER_DB = os.path.join(DATA_DIR, 'encrypted_users.json')
SECRET_KEY_FILE = os.path.join(DATA_DIR, 'secret.key')

# Load or generate encryption key
def load_or_generate_key():
    if not os.path.exists(SECRET_KEY_FILE):
        key = Fernet.generate_key()
        with open(SECRET_KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        key = open(SECRET_KEY_FILE, "rb").read()
    return key

# Encrypt and decrypt functions
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

# Save and load encrypted data
def save_encrypted_data(filepath, data, key):
    encrypted_data = encrypt_data(json.dumps(data), key)
    with open(filepath, 'wb') as file:
        file.write(encrypted_data)

def load_encrypted_data(filepath, key):
    with open(filepath, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    return json.loads(decrypted_data)

# User registration and authentication
def register_user(users):
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists.")
        return None
    password = getpass("Enter a password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    users[username] = {
        'password': password_hash,
        'data': None
    }
    save_encrypted_data(USER_DB, users, load_or_generate_key())
    print("Registration successful.")
    return username

def login_user(users):
    username = input("Enter your username: ")
    if username not in users:
        print("Username not found.")
        return None
    password = getpass("Enter your password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if users[username]['password'] != password_hash:
        print("Incorrect password.")
        return None
    print("Login successful.")
    return username

# User data management
def enter_user_data(username, users, key):
    name = input("Enter your name: ")
    dob = input("Enter your date of birth (DD-MM-YYYY): ")
    email = input("Enter your email: ")
    ssn = input("Enter your social security number: ")
    user_data = json.dumps({'name': name, 'dob': dob, 'email': email, 'ssn': ssn})
    encrypted_data = encrypt_data(user_data, key)
    users[username]['data'] = encrypted_data.decode()
    save_encrypted_data(USER_DB, users, key)
    print("Data entered and encrypted successfully.")

def view_user_data(username, users, key):
    encrypted_data = users[username]['data']
    if not encrypted_data:
        print("No data found.")
        return
    decrypted_data = decrypt_data(encrypted_data.encode(), key)
    user_data = json.loads(decrypted_data)
    print(f"Name: {user_data['name']}")
    print(f"Date of Birth: {user_data['dob']}")
    print(f"Email: {user_data['email']}")
    print(f"Social Security Number: {user_data['ssn']}")

def edit_user_data(username, users, key):
    print("Editing user data:")
    enter_user_data(username, users, key)

# Menu system
def menu(username, users, key):
    last_active = datetime.now()
    while True:
        if datetime.now() - last_active > timedelta(minutes=1):
            print("You have been logged out due to inactivity.")
            return False

        print("\nMenu:")
        print("1. Enter data")
        print("2. View data")
        print("3. Edit data")
        print("4. Logout")

        choice = input("Select an option: ")

        if choice == '1':
            enter_user_data(username, users, key)
        elif choice == '2':
            view_user_data(username, users, key)
        elif choice == '3':
            edit_user_data(username, users, key)
        elif choice == '4':
            print("Logged out successfully.")
            return True
        else:
            print("Invalid option. Please try again.")

        last_active = datetime.now()

# Main function
def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    users = load_encrypted_data(USER_DB, load_or_generate_key()) if os.path.exists(USER_DB) else {}
    key = load_or_generate_key()

    while True:
        parser = argparse.ArgumentParser(description="User Data Encryption CLI")
        parser.add_argument('--register', action='store_true', help="Register a new user")
        parser.add_argument('--login', action='store_true', help="Login as an existing user")
        args = parser.parse_args()

        if args.register:
            username = register_user(users)
        elif args.login:
            username = login_user(users)
        else:
            print("Please provide an argument: --register or --login")
            continue

        if username:
            session_active = menu(username, users, key)
            if not session_active:
                print("Returning to login/register due to inactivity.")

if __name__ == "__main__":
    main()
