# Simple-XOR-Cipher-Tool
# 🔐 XOR Cipher Tool (Symmetric Encryption)

A beginner-friendly XOR cipher tool that lets you encrypt and decrypt text using a shared secret key.

---

## ⚠️ Security Warning

**This tool is for educational purposes only!** XOR cipher is fundamentally insecure and should never be used to protect sensitive or confidential data. It is vulnerable to:
- Known-plaintext attacks
- Frequency analysis
- Brute-force attacks on short keys

For real-world encryption, use established libraries like Python's `cryptography` module with AES.

---

## ⚡ How XOR Works

Every character in the message is XOR'd with the corresponding character in the key.
This makes a simple reversible encryption — apply XOR again with the same key and you get the original text.

---

## 🚀 Features

- Encrypt any text message using XOR and a key
- Decrypt back using the same key
- Command-line interface with options
- Support for file encryption/decryption
- Basic input validation and error handling

---

## 🛠️ Technologies Used

- Python 3
- Basic bitwise operations

---

## 🧪 Usage

### Installation

```bash
git clone https://github.com/Seven7949/Simple-XOR-Cipher-Tool.git
cd Simple-XOR-Cipher-Tool
pip install -r requirements.txt
```

### Basic Usage

Encrypt a message with XOR:
```bash
python xor_cipher.py -m "hello world" -k "mysecretkey"
```

Encrypt securely with AES:
```bash
python xor_cipher.py -m "hello world" -k "mypassword" --secure
```

Decrypt a message:
```bash
python xor_cipher.py -m "encrypted_text" -k "mysecretkey" -d
```

Decrypt securely:
```bash
python xor_cipher.py -m "encrypted_text" -k "mypassword" -d --secure
```

### File Encryption

Encrypt a file:
```bash
python xor_cipher.py -f input.txt -k "mysecretkey" -o encrypted.txt
```

Decrypt a file:
```bash
python xor_cipher.py -f encrypted.txt -k "mysecretkey" -o decrypted.txt -d
```

### GUI Mode

Launch the graphical user interface:
```bash
python xor_cipher.py --gui
```

The GUI allows selecting XOR or AES mode, encrypting/decrypting text, and loading/saving files.

---

## 🧪 Testing

Run the unit tests:
```bash
python -m pytest test_xor_cipher.py
```

Or run directly:
```bash
python test_xor_cipher.py
```

---

## 📈 Future Improvements for Industrial Readiness

To make this project production-ready:
- Integrate secure encryption (AES with `cryptography` library)
- Add key derivation functions (PBKDF2)
- Implement proper key management and storage
- Add GUI interface
- Support for binary files
- Database integration for storing encrypted data
- Logging and auditing
- Automated testing and CI/CD pipelines
- Security audits and compliance checks

---

## 📄 License

This project is open-source. See LICENSE file for details.
