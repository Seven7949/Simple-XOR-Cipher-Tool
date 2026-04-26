#!/usr/bin/env python3
"""
Simple XOR Cipher Tool

This tool provides basic XOR encryption/decryption for educational purposes.
WARNING: XOR cipher is NOT secure for protecting sensitive data.
Use proper encryption libraries like 'cryptography' for real security.
"""

import argparse
import sys
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

def xor_encrypt_decrypt(text: str, key: str) -> str:
    """
    Encrypt or decrypt text using XOR cipher with the given key.

    Args:
        text (str): The text to encrypt/decrypt.
        key (str): The secret key.

    Returns:
        str: The encrypted/decrypted text.

    Raises:
        ValueError: If key is empty.
    """
    if not key:
        raise ValueError("Key cannot be empty.")
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("Both text and key must be strings.")
    result = ''.join([chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text)])
    return result

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a key from password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def aes_encrypt(text: str, password: str) -> str:
    """Encrypt text using AES with password-derived key."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_text = text.encode() + b'\0' * (16 - len(text.encode()) % 16)
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    return base64.b64encode(salt + iv + ciphertext).decode()

def aes_decrypt(encrypted_text: str, password: str) -> str:
    """Decrypt text using AES with password-derived key."""
    data = base64.b64decode(encrypted_text)
    salt, iv, ciphertext = data[:16], data[16:32], data[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    return padded_text.rstrip(b'\0').decode()

class CipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XOR Cipher Tool")
        self.root.geometry("500x400")

        self.mode = tk.StringVar(value="xor")
        self.operation = tk.StringVar(value="encrypt")

        # Mode selection
        tk.Label(root, text="Encryption Mode:").pack()
        tk.Radiobutton(root, text="XOR (Educational)", variable=self.mode, value="xor").pack()
        tk.Radiobutton(root, text="AES (Secure)", variable=self.mode, value="aes").pack()

        # Operation
        tk.Label(root, text="Operation:").pack()
        tk.Radiobutton(root, text="Encrypt", variable=self.operation, value="encrypt").pack()
        tk.Radiobutton(root, text="Decrypt", variable=self.operation, value="decrypt").pack()

        # Key
        tk.Label(root, text="Password/Key:").pack()
        self.key_entry = tk.Entry(root, show="*")
        self.key_entry.pack()

        # Input
        tk.Label(root, text="Input Text:").pack()
        self.input_text = tk.Text(root, height=5)
        self.input_text.pack()

        # Buttons
        tk.Button(root, text="Process", command=self.process).pack()
        tk.Button(root, text="Load File", command=self.load_file).pack()
        tk.Button(root, text="Save Output", command=self.save_output).pack()

        # Output
        tk.Label(root, text="Output:").pack()
        self.output_text = tk.Text(root, height=5)
        self.output_text.pack()

    def process(self):
        try:
            key = self.key_entry.get()
            text = self.input_text.get("1.0", tk.END).strip()
            mode = self.mode.get()
            op = self.operation.get()

            if mode == "xor":
                result = xor_encrypt_decrypt(text, key)
            else:
                if op == "encrypt":
                    result = aes_encrypt(text, key)
                else:
                    result = aes_decrypt(text, key)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, f.read())

    def save_output(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.output_text.get("1.0", tk.END).strip())

def main():
    parser = argparse.ArgumentParser(description="Simple XOR Cipher Tool")
    parser.add_argument('-m', '--message', type=str, help='The message to encrypt/decrypt')
    parser.add_argument('-k', '--key', type=str, required=True, help='The secret key or password')
    parser.add_argument('-f', '--file', type=str, help='File to encrypt/decrypt (instead of message)')
    parser.add_argument('-o', '--output', type=str, help='Output file for result')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode (default is encrypt)')
    parser.add_argument('--secure', action='store_true', help='Use secure AES encryption instead of XOR')
    parser.add_argument('--gui', action='store_true', help='Launch GUI mode')

    args = parser.parse_args()

    if args.gui:
        if not TKINTER_AVAILABLE:
            print("❌ Tkinter not available. Install tkinter or use CLI mode.")
            sys.exit(1)
        root = tk.Tk()
        CipherGUI(root)
        root.mainloop()
        return

    print("🔐 XOR Cipher Tool")
    if not args.secure:
        print("⚠️  WARNING: Using XOR (educational only). XOR is not secure!")
    else:
        print("🔒 Using secure AES encryption.")

    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        elif args.message:
            text = args.message
        else:
            text = input("Enter your message: ")

        if args.secure:
            if args.decrypt:
                output = aes_decrypt(text, args.key)
            else:
                output = aes_encrypt(text, args.key)
        else:
            output = xor_encrypt_decrypt(text, args.key)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Result saved to {args.output}")
        else:
            print("\n💬 Result:")
            print(output)

    except FileNotFoundError:
        print("❌ File not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
