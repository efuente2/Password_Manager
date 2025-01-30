# 🔐 Password Manager

A **secure password manager** built in Python that can:
✅ **Generate strong passwords**  
✅ **Encrypt & store passwords in a CSV file**  
✅ **Retrieve and decrypt passwords when needed**  

🔒 Uses **AES encryption** with `cryptography.Fernet` to keep passwords safe.  

---

## 🚀 Installation & Setup

### 1️⃣ Install Dependencies
Make sure you have **Python 3+** installed. Then, install the required library:

```sh
pip install cryptography

### 2️⃣ Clone or Download This Repository

```sh
git clone https://github.com/yourusername/password_manager.git
cd password_manager

### 3️⃣ Run the Script

```sh
python password_manager.py


## 🔑 Features
### 1️⃣ Generate a Secure Password

Randomly generates strong passwords with letters, numbers, and special characters.
### 2️⃣ Save & Encrypt Passwords

Stores website login credentials in a CSV file (passwords.csv)
Uses AES encryption to protect passwords.
### 3️⃣ Retrieve & Decrypt Passwords

Decrypts stored passwords and displays them securely in the terminal.
### 4️⃣ Automatic File Creation

If the CSV file does not exist, it is automatically created.
Encryption key (secret.key) is generated on first run.