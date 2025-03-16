import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import os
import secrets
import json
import time
import platform
import sys

class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Goat's Better Encryption Method")
        
        # Improve window sizing and positioning for macOS
        if platform.system() == 'Darwin':
            # macOS-specific window configuration
            self.root.geometry("500x600")  # Slightly taller for macOS
            self.root.resizable(True, True)  # Allow resizing
            
            # Use system-native look if possible
            try:
                self.root.tk.call('tk', 'windowingsystem')
            except tk.TclError:
                pass
        else:
            self.root.geometry("500x500")
        
        self.root.config(bg="#2c2f33")
        
        # Add menu bar for macOS
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Encrypt", command=self.encryptandsave)
        self.file_menu.add_command(label="Decrypt", command=self.decryptfile)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.secure_exit)
        
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
        
        # Default security parameters
        self.iterations = 310000  # Increased from 100000
        self.algorithm = hashes.SHA256()
        
        # Bind event to clear textbox securely
        self.root.protocol("WM_DELETE_WINDOW", self.secure_exit)

    def derivekey(self, passphrase, salt=None):
        if salt is None:
            salt = secrets.token_bytes(16)  # hopefully use a unique salt for each encryption
        kdf = PBKDF2HMAC(  # this kdf just makes your passkey into the most absurdly radical hash kinda (summarized)
            algorithm=self.algorithm, 
            length=32,  # length of the generated key
            salt=salt,
            iterations=self.iterations,
        )
        key = kdf.derive(passphrase.encode())
        return base64.urlsafe_b64encode(key), salt

    def encryptandsave(self):
        text = self.textbox.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Enter something you idiot")
            return

        passphrase = self.passphrase_entry.get()
        if not passphrase:
            messagebox.showwarning("Warning", "No passphrase?!")
            return

        try:
            # Generate a unique salt for this encryption
            salt = secrets.token_bytes(16)
            
            # derive the key from the passphrase
            key, salt = self.derivekey(passphrase, salt)
            fernet = Fernet(key)
            encrypted_text = fernet.encrypt(text.encode())
            
            # Create metadata for the file
            metadata = {
                "version": "2.0",
                "timestamp": int(time.time()),
                "iterations": self.iterations,
                "algorithm": "SHA256",
                "salt": base64.b64encode(salt).decode('utf-8')
            }
            
            # Prepare final data structure
            file_data = {
                "metadata": metadata,
                "encrypted_data": base64.b64encode(encrypted_text).decode('utf-8')
            }
            
            # JSON serialize the data
            file_content = json.dumps(file_data).encode('utf-8')

            # Improved file dialog for macOS
            filepath = filedialog.asksaveasfilename(
                defaultextension=".jonsnow", 
                filetypes=[("JONSNOW Files", "*.jonsnow")],
                initialdir=os.path.expanduser("~/Desktop")  # Default to Desktop on macOS
            )
            if filepath:
                # Ensure file permissions are secure
                with open(filepath, 'wb') as file:
                    os.chmod(filepath, 0o600)  # Read/write for owner only
                    file.write(file_content)
                messagebox.showinfo("Success", "File encrypted and saved successfully!")

            self.textbox.delete("1.0", tk.END)
            self.passphrase_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt: {str(e)}")

    def decryptfile(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".jonsnow", 
            filetypes=[("JONSNOW Files", "*.jonsnow")],
            initialdir=os.path.expanduser("~/Desktop")  # Default to Desktop on macOS
        )
        if not filepath:
            messagebox.showwarning("Warning", "No file selected!")
            return

        # the box to ask for password after
        while True:
            passphrase = simpledialog.askstring(
                "Passphrase", 
                "Enter your passphrase:", 
                show="*",
                parent=self.root  # Ensure dialog is modal
            )
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
                file_content = file.read()
            
            try:
                # Try new format first
                file_data = json.loads(file_content.decode('utf-8'))
                metadata = file_data.get("metadata", {})
                
                # Get decryption parameters from metadata
                version = metadata.get("version", "1.0")
                salt = base64.b64decode(metadata.get("salt", ""))
                self.iterations = metadata.get("iterations", 310000)
                
                # Get encrypted data
                encrypted_text = base64.b64decode(file_data.get("encrypted_data", ""))
                
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Fall back to old format
                encrypted_text = file_content
                salt = b"salt"  # Old format used fixed salt
                self.iterations = 100000  # Old iteration count
            
            key, _ = self.derivekey(passphrase, salt)
            fernet = Fernet(key)

            decrypted_text = fernet.decrypt(encrypted_text).decode()

            self.textbox.delete("1.0", tk.END)
            self.textbox.insert(tk.END, decrypted_text)
            messagebox.showinfo("Decryption", "File decrypted")
            return True
            
        except Exception as e:
            return False
    
    def secure_exit(self):
        # Securely clear sensitive data
        self.textbox.delete("1.0", tk.END)
        self.passphrase_entry.delete(0, tk.END)
        
        # Overwrite memory with junk data to help prevent memory scraping
        self.textbox.insert(tk.END, "x" * 1000)
        self.textbox.delete("1.0", tk.END)
        
        self.root.destroy()

if __name__ == "__main__":
    # Ensure proper macOS app handling
    if platform.system() == 'Darwin':
        try:
            import AppKit
        except ImportError:
            pass

    root = tk.Tk()
    
    # Center the window on screen
    window_width = 500
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position x and y coordinates
    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    
    app = AdvancedEncryptionApp(root)
    
    # Ensure app is in foreground on macOS
    if platform.system() == 'Darwin':
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
    
    root.mainloop()
