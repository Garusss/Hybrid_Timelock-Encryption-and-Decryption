# Hybrid_Timelock-Encryption-and-Decryption
Hybrid time-locked file encryption system built in Python using AES-256-GCM, PBKDF2, trusted online time verification, and a lightweight RSW time-lock puzzle. Prevents early decryption even if system time is modified. Designed for secure, real-world time-based access control.

🚀 Features

🔐 AES-256-GCM for authenticated file encryption

🔑 PBKDF2-HMAC-SHA256 for secure password-based key derivation

⏳ Lightweight RSW time-lock puzzle (calibrated computational delay)

🌍 Trusted time verification via HTTPS (timeapi.io)

🇳🇵 Nepal-time (Asia/Kathmandu) user input with internal UTC conversion

🛡 SHA-256 integrity verification

🖥 Modern GUI built with CustomTkinter

🔒 Resistant to system clock manipulation attacks

🧠 System Architecture
🔹 Encryption Phase

➜ User selects a file

➜ User enters a password

➜ User selects unlock date & time (Nepal Time)

➜ System converts Nepal time → UTC internally

➜ File is encrypted using AES-256-GCM

➜ Metadata (salt, nonce, unlock time, RSW puzzle) is stored separately

➜ A small calibrated RSW puzzle is generated for additional cryptographic delay

🔹 Decryption Phase

➜ User selects encrypted file

➜ Password is required again

➜ Current UTC time is fetched securely from a trusted time API

➜ System verifies:

Trusted UTC >= Stored Unlock UTC


If unlocked:

➜ RSW puzzle is solved (small computational delay)

➜ AES key is recovered

➜ File is decrypted

➜ SHA-256 integrity is verified

🔐 Security Design

This hybrid model protects against:

❌ System clock manipulation

❌ Immediate decryption upon unlock

❌ Unauthorized access without password

❌ File integrity tampering

The system balances usability and cryptographic enforcement by combining real-world time validation with computational delay.

🛠 Technologies Used

Python 3.10+

cryptography

customtkinter

sympy

requests

tzdata

zoneinfo

📦 Installation
Clone the repository
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

Install dependencies
pip install -r requirements.txt

Run the application
python main.py

⚠ Requirements

🌐 Internet connection required for trusted time verification

🪟 Windows users must install tzdata (included in requirements.txt)

🎓 Academic Context

This project was developed for an intermediate-level cryptography module to demonstrate:

➜ Symmetric encryption (AES-256)

➜ Authenticated encryption (GCM mode)

➜ Key derivation functions (PBKDF2-HMAC-SHA256)

➜ Time-lock cryptographic concepts (RSW algorithm)

➜ Secure time validation models

➜ Hybrid cryptographic system design

📌 Limitations

➜ RSW delay duration depends on CPU performance

➜ Unlock precision depends on trusted time API availability

➜ Designed for academic and educational purposes
