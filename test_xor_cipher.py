#!/usr/bin/env python3
"""
Unit tests for XOR Cipher Tool
"""

import unittest
from xor_cipher import xor_encrypt_decrypt

try:
    from xor_cipher import aes_encrypt, aes_decrypt
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

class TestXORCipher(unittest.TestCase):
    def test_basic_encrypt_decrypt(self):
        key = "key"
        message = "hello"
        encrypted = xor_encrypt_decrypt(message, key)
        decrypted = xor_encrypt_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_empty_key_raises_error(self):
        with self.assertRaises(ValueError):
            xor_encrypt_decrypt("hello", "")

    def test_non_string_inputs(self):
        with self.assertRaises(TypeError):
            xor_encrypt_decrypt(123, "key")
        with self.assertRaises(TypeError):
            xor_encrypt_decrypt("hello", 123)

    def test_unicode_support(self):
        key = "🔑"
        message = "héllo 🌍"
        encrypted = xor_encrypt_decrypt(message, key)
        decrypted = xor_encrypt_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_key_longer_than_message(self):
        key = "verylongkey"
        message = "hi"
        encrypted = xor_encrypt_decrypt(message, key)
        decrypted = xor_encrypt_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

@unittest.skipUnless(CRYPTOGRAPHY_AVAILABLE, "Cryptography library not available")
class TestAESCipher(unittest.TestCase):
    def test_aes_encrypt_decrypt(self):
        password = "password"
        message = "hello world"
        encrypted = aes_encrypt(message, password)
        decrypted = aes_decrypt(encrypted, password)
        self.assertEqual(decrypted, message)

    def test_aes_wrong_password(self):
        password = "password"
        wrong_password = "wrong"
        message = "hello"
        encrypted = aes_encrypt(message, password)
        with self.assertRaises(Exception):  # Should fail with wrong password
            aes_decrypt(encrypted, wrong_password)

if __name__ == "__main__":
    unittest.main()