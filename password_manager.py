import csv
import os
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet

# --- Encryption Key Management ---
KEY_FILE = "secret.key"
CSV_FILE = "passwords.csv"

def generate_key():
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    """Load the encryption key from the file, or generate a new one if not found."""
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Load encryption key
key = load_key()
cipher = Fernet(key)

# --- Ensure CSV File Exists ---
def initialize_csv():
    """Create CSV file if it doesn't exist and add headers."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Website", "Username", "Encrypted Password"])

# --- Password Generator with Constraints ---
def generate_password():
    length = int(length_entry.get())
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_special = special_var.get()

    if not any([use_upper, use_lower, use_digits, use_special]):
        messagebox.showerror("Error", "Select at least one character type!")
        return

    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_special:
        char_pool += string.punctuation

    password = ''.join(random.choice(char_pool) for _ in range(length))
    
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# --- Save Password ---
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    encrypted_password = cipher.encrypt(password.encode()).decode()

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([website, username, encrypted_password])

    messagebox.showinfo("Success", "Password saved successfully!")
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# --- Retrieve Password ---
def retrieve_password():
    website = website_entry.get()
    if not website:
        messagebox.showerror("Error", "Enter a website to search!")
        return

    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == website:
                username = row[1]
                decrypted_password = cipher.decrypt(row[2].encode()).decode()
                messagebox.showinfo("Password Found", f"Website: {website}\nUsername: {username}\nPassword: {decrypted_password}")
                return

    messagebox.showerror("Error", "No password found for this website!")

# --- Toggle Password Visibility ---
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_btn.config(text="🙈 Hide")
    else:
        password_entry.config(show="*")
        toggle_btn.config(text="👁️ Show")

# --- UI Setup ---
initialize_csv()
root = tk.Tk()
root.title("🔐 Password Manager")
root.geometry("500x600")  # Increase height to accommodate all elements
root.minsize(500, 600)  # Ensure enough space
root.configure(bg="#f4f4f4")

# Make root window flexible
root.grid_rowconfigure(6, weight=1)  # Allow vertical resizing
root.grid_columnconfigure(0, weight=1)

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 11), padding=5)
style.configure("TEntry", font=("Arial", 11), padding=5)

# Title Label
ttk.Label(root, text="🔐 Password Manager", font=("Arial", 14, "bold"), background="#f4f4f4").pack(pady=10)

# Frame for Inputs
frame = ttk.Frame(root, padding=10)
frame.pack(pady=5, fill="x")

# Labels & Entry Fields
ttk.Label(frame, text="Website:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
website_entry = ttk.Entry(frame, width=30)
website_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
username_entry = ttk.Entry(frame, width=30)
username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
password_entry = ttk.Entry(frame, width=30, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Password Toggle Button
toggle_btn = ttk.Button(frame, text="👁️ Show", command=toggle_password)
toggle_btn.grid(row=2, column=2, padx=5, pady=5)

# Password Constraints
constraints_frame = ttk.LabelFrame(root, text="Password Constraints", padding=10)
constraints_frame.pack(pady=10, fill="x")

# Length Entry
ttk.Label(constraints_frame, text="Length:").grid(row=0, column=0, padx=5, pady=5)
length_entry = ttk.Entry(constraints_frame, width=5)
length_entry.grid(row=0, column=1, padx=5, pady=5)
length_entry.insert(0, "12")

# Character Type Checkboxes
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

ttk.Checkbutton(constraints_frame, text="Uppercase", variable=upper_var).grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Checkbutton(constraints_frame, text="Lowercase", variable=lower_var).grid(row=2, column=0, padx=5, pady=5, sticky="w")
ttk.Checkbutton(constraints_frame, text="Numbers", variable=digits_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")
ttk.Checkbutton(constraints_frame, text="Special Characters", variable=special_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Buttons Frame with flexible layout
button_frame = ttk.Frame(root)
button_frame.pack(pady=10, fill="both", expand=True)

ttk.Button(button_frame, text="🔄 Generate Password", command=generate_password).pack(pady=5, fill="x")
ttk.Button(button_frame, text="💾 Save Password", command=save_password).pack(pady=5, fill="x")
ttk.Button(button_frame, text="🔍 Retrieve Password", command=retrieve_password).pack(pady=5, fill="x")

# Run the Tkinter main loop
root.mainloop()



