import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Goat's Encryption Method")
        self.root.geometry("500x500")
        self.root.config(bg="#2c2f33")

        # Add GUI components
        self.label = tk.Label(root, text="Enter Text To Encrypt or Decrypt:", 
                              font=("Helvetica", 12), bg="#2c2f33", fg="#ffffff")
        self.label.pack(pady=10)

        self.textbox = tk.Text(root, height=6, width=60, font=("Courier", 12), 
                                bd=2, relief="solid", wrap="word", 
                                bg="#23272a", fg="#ffffff")
        self.textbox.pack(pady=15)

        self.encryptbutton = tk.Button(root, text="Encrypt & Save as .jonsnow", 
                                        font=("Helvetica", 12, "bold"), 
                                        bg="#7289da", fg="white", 
                                        command=self.encryptandsave, 
                                        relief="raised", bd=2)
        self.encryptbutton.pack(pady=10, ipadx=10, ipady=5)

        self.decryptbutton = tk.Button(root, text="Open & Decrypt .jonsnow", 
                                        font=("Helvetica", 12, "bold"), 
                                        bg="#99aab5", fg="black", 
                                        command=self.openanddecrypt, 
                                        relief="raised", bd=2)
        self.decryptbutton.pack(pady=10, ipadx=10, ipady=5)

        self.decryptedtext = ""  # store decrypted text temporarily

    # Generate a random key using the cryptography library
    def generate_key(self):
        return Fernet.generate_key()

    # Save key to a file securely (not recommended to hard-code, but for demo)
    def save_key(self, key, filepath):
        with open(filepath, 'wb') as file:
            file.write(key)

    # Load the encryption key
    def load_key(self, filepath):
        with open(filepath, 'rb') as file:
            return file.read()

    def encryptandsave(self):
        text = self.textbox.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to encrypt!")
            return

        # Generate a new encryption key and encrypt the text
        key = self.generate_key()
        fernet = Fernet(key)
        encrypted_text = fernet.encrypt(text.encode())

        # Save the encrypted text and the key
        filepath = filedialog.asksaveasfilename(defaultextension=".jonsnow", 
                                                filetypes=[("JONSNOW Files", "*.jonsnow")])
        if filepath:
            with open(filepath, 'wb') as file:
                file.write(encrypted_text)

            # Also save the key to a separate file
            key_filepath = os.path.splitext(filepath)[0] + ".key"
            self.save_key(key, key_filepath)

            messagebox.showinfo("Success", "File encrypted and saved successfully!")

        self.textbox.delete("1.0", tk.END)

    def openanddecrypt(self):
        # Let user select the encrypted file
        filepath = filedialog.askopenfilename(filetypes=[("JONSNOW Files", "*.jonsnow")])
        if not filepath:
            return
        
        try:
            # Open the encrypted file
            with open(filepath, 'rb') as file:
                encrypted_text = file.read()

            # Ask user to provide the key file
            key_filepath = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
            if not key_filepath:
                raise FileNotFoundError("Key file not found!")

            # Load the key
            key = self.load_key(key_filepath)
            fernet = Fernet(key)

            # Decrypt the text
            decrypted_text = fernet.decrypt(encrypted_text).decode()

            # Display the decrypted text
            self.textbox.delete("1.0", tk.END)
            self.textbox.insert(tk.END, decrypted_text)
            messagebox.showinfo("Decryption", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEncryptionApp(root)
    root.mainloop()
