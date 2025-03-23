# cloud_user.py
from tkinter import *
from tkinter import filedialog, messagebox
import os, pickle
from hashlib import sha1
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt

# Global variables for keys and filename
filename = ""
public_key = None
private_key = None

def generateKeys():
    global public_key, private_key
    try:
        # Check if keys already exist
        if os.path.exists('public.pckl') and os.path.exists('private.pckl'):
            with open('public.pckl', 'rb') as f:
                public_key = pickle.load(f)
            with open('private.pckl', 'rb') as f:
                private_key = pickle.load(f)
            messagebox.showinfo("Key Generation", "Keys loaded successfully.")
        else:
            # Generate new keys using eciespy's generate_eth_key
            secret_key = generate_eth_key()
            private_key = secret_key.to_hex()  # hex string
            public_key = secret_key.public_key.to_hex()
            with open('public.pckl', 'wb') as f:
                pickle.dump(public_key, f)
            with open('private.pckl', 'wb') as f:
                pickle.dump(private_key, f)
            messagebox.showinfo("Key Generation", "Keys generated and stored successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating keys: {e}")

def selectFile():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file")
    if filename:
        messagebox.showinfo("File Selected", f"Selected file: {filename}")

def encryptAndUpload():
    global public_key  # Ensure we use the global public_key
    if public_key is None:
        messagebox.showerror("Error", "Please generate keys first!")
        return
    if not filename:
        messagebox.showerror("Error", "No file selected!")
        return
    try:
        with open(filename, "rb") as f:
            file_data = f.read()
        # Encrypt the file data using the public key
        cipher_text = encrypt(public_key, file_data)
        # Compute master hash (using SHA-1 here for simulation)
        master_hash = sha1(cipher_text).hexdigest()
        # Save the encrypted file locally (simulate upload)
        upload_path = os.path.join(os.getcwd(), "CloudUser", "upload")
        os.makedirs(upload_path, exist_ok=True)
        encrypted_filename = os.path.join(upload_path, os.path.basename(filename) + ".enc")
        with open(encrypted_filename, "wb") as f:
            f.write(cipher_text)
        messagebox.showinfo("Upload Success", f"File encrypted and uploaded.\nMaster Hash: {master_hash}")
    except Exception as e:
        messagebox.showerror("Encryption Error", f"Error during encryption: {e}")

def downloadAndDecrypt():
    global private_key
    if private_key is None:
        messagebox.showerror("Error", "Private key not found. Generate keys first!")
        return
    if not filename:
        messagebox.showerror("Error", "No file selected!")
        return
    try:
        upload_path = os.path.join(os.getcwd(), "CloudUser", "upload")
        encrypted_filename = os.path.join(upload_path, os.path.basename(filename) + ".enc")
        if not os.path.exists(encrypted_filename):
            messagebox.showerror("Error", "Encrypted file not found!")
            return
        with open(encrypted_filename, "rb") as f:
            cipher_text = f.read()
        plain_text = decrypt(private_key, cipher_text)
        download_path = os.path.join(os.getcwd(), "CloudUser", "download")
        os.makedirs(download_path, exist_ok=True)
        decrypted_filename = os.path.join(download_path, os.path.basename(filename))
        with open(decrypted_filename, "wb") as f:
            f.write(plain_text)
        messagebox.showinfo("Download Success", f"File downloaded and decrypted at:\n{decrypted_filename}")
    except Exception as e:
        messagebox.showerror("Decryption Error", f"Error during decryption: {e}")

# Create the main GUI window
main = Tk()
main.title("Cloud Security Project - Cloud User Interface")
main.geometry("1300x800")

# Create buttons
Button(main, text="Generate Keys", command=generateKeys, width=25).pack(pady=10)
Button(main, text="Select File", command=selectFile, width=25).pack(pady=10)
Button(main, text="Encrypt & Upload", command=encryptAndUpload, width=25).pack(pady=10)
Button(main, text="Download & Decrypt", command=downloadAndDecrypt, width=25).pack(pady=10)

main.mainloop()
