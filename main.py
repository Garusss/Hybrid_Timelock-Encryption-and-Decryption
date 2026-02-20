import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json
import os

from crypto_utils import *
from rsw import *
from time_verifier import get_trusted_time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Hybrid Time-Locked Encryption")
        self.geometry("500x600")
        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(self, text="Password").pack(pady=10)
        self.password = ctk.CTkEntry(self, show="*", width=300)
        self.password.pack()

        ctk.CTkLabel(self, text="Unlock Date (YYYY-MM-DD) - Nepal Time").pack(pady=10)
        self.date_entry = ctk.CTkEntry(self, width=300)
        self.date_entry.pack()

        ctk.CTkLabel(self, text="Unlock Time (HH:MM) - Nepal Time").pack(pady=10)
        self.time_entry = ctk.CTkEntry(self, width=300)
        self.time_entry.pack()

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=20)
        self.progress.set(0)

        ctk.CTkButton(self, text="Encrypt", command=self.encrypt).pack(pady=10)
        ctk.CTkButton(self, text="Decrypt", command=self.decrypt).pack(pady=10)

    # =========================
    # ENCRYPT FUNCTION
    # =========================
    def encrypt(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        password = self.password.get()
        if not password:
            messagebox.showerror("Error", "Password required!")
            return

        try:
            local_time = datetime.strptime(
                self.date_entry.get() + " " + self.time_entry.get(),
                "%Y-%m-%d %H:%M"
            )
        except:
            messagebox.showerror("Error", "Invalid date/time format!")
            return

        # Attach Nepal timezone
        nepal_time = local_time.replace(tzinfo=ZoneInfo("Asia/Kathmandu"))

        # Convert to UTC
        unlock_time = nepal_time.astimezone(timezone.utc)

        # Generate salt & derive key
        salt = os.urandom(16)
        key = derive_key(password, salt)

        output_file = file_path + ".enc"
        nonce = encrypt_file(file_path, output_file, key)

        # Create RSW puzzle using derived key
        puzzle = create_small_delay_puzzle(key, delay_seconds=5)

        metadata = {
            "salt": salt.hex(),
            "nonce": nonce.hex(),
            "unlock_time": unlock_time.isoformat(),
            "file_hash": sha256_hash(file_path),
            "puzzle": puzzle
        }

        with open(output_file + ".meta", "w") as f:
            json.dump(metadata, f)

        messagebox.showinfo("Success", "File encrypted successfully!")

    # =========================
    # DECRYPT FUNCTION
    # =========================
    def decrypt(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        meta_path = file_path + ".meta"
        if not os.path.exists(meta_path):
            messagebox.showerror("Error", "Metadata file missing!")
            return

        password_dialog = ctk.CTkInputDialog(
            text="Enter password:",
            title="Password Required"
        )
        password = password_dialog.get_input()

        if not password:
            return

        with open(meta_path, "r") as f:
            metadata = json.load(f)

        # ================= TIME VALIDATION =================
        server_time = get_trusted_time()
        if server_time is None:
            messagebox.showerror("Error", "Cannot verify trusted time!")
            return

        unlock_time = datetime.fromisoformat(metadata["unlock_time"])

        if server_time < unlock_time:
            messagebox.showerror(
                "Locked",
                f"File locked until {unlock_time} (UTC)"
            )
            return

        # ================= SOLVE RSW PUZZLE =================
        def update_progress(value):
            self.progress.set(value)
            self.update_idletasks()

        recovered_key = solve_puzzle(metadata["puzzle"], update_progress)

        # ================= PASSWORD VALIDATION FIX =================
        salt = bytes.fromhex(metadata["salt"])
        derived_key = derive_key(password, salt)

        if derived_key != recovered_key:
            messagebox.showerror("Error", "Incorrect password!")
            return

        # ================= FILE DECRYPTION =================
        nonce = bytes.fromhex(metadata["nonce"])
        output_file = file_path.replace(".enc", ".decrypted")

        try:
            decrypt_file(file_path, output_file, recovered_key, nonce)
        except:
            messagebox.showerror("Error", "Decryption failed!")
            return

        # ================= INTEGRITY CHECK =================
        if sha256_hash(output_file) == metadata["file_hash"]:
            messagebox.showinfo("Success", "Decryption successful!")
        else:
            messagebox.showerror("Error", "Integrity check failed!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
