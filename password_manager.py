import csv
import os
import random
import sqlite3
import string
from cryptography.fernet import Fernet

# --- Setup Database ---
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    encrypted_password TEXT NOT NULL
)
""")
conn.commit()

# --- Generate a Secret Key for Encryption ---
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# --- Load Encryption Key ---
def load_key():
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        generate_key()
        return load_key()

key = load_key()
cipher = Fernet(key)

# --- Password Generator ---
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# --- Save Password to Database ---
def save_password(website, username, password):
    encrypted_password = cipher.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO passwords (website, username, encrypted_password) VALUES (?, ?, ?)", 
                   (website, username, encrypted_password))
    conn.commit()
    print("✅ Password saved successfully!")

# --- Retrieve Password ---
def retrieve_password(website):
    cursor.execute("SELECT username, encrypted_password FROM passwords WHERE website = ?", (website,))
    result = cursor.fetchone()
    if result:
        username, encrypted_password = result
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        print(f"🔑 Website: {website}\n👤 Username: {username}\n🔒 Password: {decrypted_password}")
    else:
        print("❌ No password found for this website.")

# --- Main Menu ---
def main():
    while True:
        print("\n🔐 Password Manager")
        print("1️⃣ Generate Password")
        print("2️⃣ Save Password")
        print("3️⃣ Retrieve Password")
        print("4️⃣ Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            length = int(input("Enter password length: "))
            new_password = generate_password(length)
            print(f"🆕 Generated Password: {new_password}")

        elif choice == "2":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password to save (or press Enter to generate one): ")
            if not password:
                password = generate_password()
                print(f"🔑 Generated Password: {password}")
            save_password(website, username, password)

        elif choice == "3":
            website = input("Enter website to retrieve password: ")
            retrieve_password(website)

        elif choice == "4":
            print("👋 Exiting Password Manager...")
            break

        else:
            print("❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()


