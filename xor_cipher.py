def xor_encrypt_decrypt(text, key):
    result = ''.join([chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text)])
    return result

if __name__ == "__main__":
    print("🔐 XOR Cipher Tool")
    choice = input("Encrypt or Decrypt? (e/d): ").lower()

    if choice not in ['e', 'd']:
        print("❌ Invalid option.")
        exit()

    message = input("Enter your message: ")
    key = input("Enter your secret key: ")

    output = xor_encrypt_decrypt(message, key)
    print("\n💬 Result:")
    print(output)
