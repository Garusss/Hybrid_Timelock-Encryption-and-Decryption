import os
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

backend = default_backend()

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=backend
    )
    return kdf.derive(password.encode())

def encrypt_file(input_path, output_path, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    with open(input_path, "rb") as f:
        data = f.read()

    ciphertext = aesgcm.encrypt(nonce, data, None)

    with open(output_path, "wb") as f:
        f.write(ciphertext)

    return nonce

def decrypt_file(input_path, output_path, key, nonce):
    aesgcm = AESGCM(key)

    with open(input_path, "rb") as f:
        ciphertext = f.read()

    data = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, "wb") as f:
        f.write(data)

def sha256_hash(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()
