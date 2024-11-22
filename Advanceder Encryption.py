import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import os

class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Goat's Better Encryption Method")
        self.root.geometry("500x500")
        self.root.config(bg="#2c2f33")
        self.label = tk.Label(root, text="Enter Text To Encrypt or Decrypt:", 
                              font=("Helvetica", 12), bg="#2c2f33", fg="#ffffff")
        self.label.pack(pady=10)
        self.textbox = tk.Text(root, height=6, width=60, font=("Courier", 12), 
                                bd=2, relief="solid", wrap="word", 
                                bg="#23272a", fg="#ffffff")
        self.textbox.pack(pady=15)
        self.passphrase_label = tk.Label(root, text="Enter Passphrase:", 
                                         font=("Helvetica", 12), bg="#2c2f33", fg="#ffffff")
        self.passphrase_label.pack(pady=5)
        self.passphrase_entry = tk.Entry(root, font=("Courier", 12), 
                                          bd=2, relief="solid", show="*", 
                                          bg="#23272a", fg="#ffffff")
        self.passphrase_entry.pack(pady=10)
        self.encryptbutton = tk.Button(root, text="Encrypt & Save as .jonsnow", 
                                        font=("Helvetica", 12, "bold"), 
                                        bg="#7289da", fg="white", 
                                        command=self.encryptandsave, 
                                        relief="raised", bd=2)
        self.encryptbutton.pack(pady=10, ipadx=10, ipady=5)

        self.decryptbutton = tk.Button(root, text="Decrypt .jonsnow", 
                                        font=("Helvetica", 12, "bold"), 
                                        bg="#99aab5", fg="black", 
                                        relief="raised", bd=2, command=self.decryptfile)
        self.decryptbutton.pack(pady=10, ipadx=10, ipady=5)

    def derivekey(self, passphrase):
        salt = b"salt"  # hopefully use a unique salt for each encryption
        kdf = PBKDF2HMAC(  # this kdf just makes your passkey into the most absurdly radical hash kinda (summarized)
            algorithm=hashes.SHA256(), 
            length=32,  # length of the generated key
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(passphrase.encode())
        return base64.urlsafe_b64encode(key)

    def encryptandsave(self):
        text = self.textbox.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Enter something you idiot")
            return

        passphrase = self.passphrase_entry.get()
        if not passphrase:
            messagebox.showwarning("Warning", "No passphrase?!")
            return

        # derive the key from the passphrase
        key = self.derivekey(passphrase)
        fernet = Fernet(key)
        encrypted_text = fernet.encrypt(text.encode())

        # save the encrypted text to file
        filepath = filedialog.asksaveasfilename(defaultextension=".jonsnow", 
                                                filetypes=[("JONSNOW Files", "*.jonsnow")])
        if filepath:
            with open(filepath, 'wb') as file:
                file.write(encrypted_text)
            messagebox.showinfo("Success", "File encrypted and saved successfully!")

        self.textbox.delete("1.0", tk.END)
        # self.passphrase_entry.delete("1.0", tk.END) #this doesnt work fors oem reason

    def decryptfile(self):
        filepath = filedialog.askopenfilename(defaultextension=".jonsnow", 
                                              filetypes=[("JONSNOW Files", "*.jonsnow")])
        if not filepath:
            messagebox.showwarning("Warning", "No file selected!")
            return

        # the box to ask foer password aftrer
        while True:
            passphrase = simpledialog.askstring("Passphrase", "Enter your passphrase:", show="*")
            if not passphrase:
                messagebox.showwarning("Warning", "Passphrase is required for decryption!")
                return

            success = self.openanddecrypt(filepath, passphrase)
            if success:
                break
            else:
                retry = messagebox.askretrycancel("Invalid Passphrase", "The passphrase is incorrect. Try again?")
                if not retry:
                    break

    def openanddecrypt(self, filepath, passphrase):
        try:
            with open(filepath, 'rb') as file:
                encrypted_text = file.read()

            key = self.derivekey(passphrase)
            fernet = Fernet(key)

            decrypted_text = fernet.decrypt(encrypted_text).decode()

            self.textbox.delete("1.0", tk.END)
            self.textbox.insert(tk.END, decrypted_text)
            messagebox.showinfo("Decryption", "File decrypted")
            return True
        except Exception as e:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEncryptionApp(root)
    root.mainloop()
