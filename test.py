import tkinter as tk
from tkinter import filedialog, messagebox
import os
import datetime
import base64
from cryptography.fernet import Fernet

def generate_proximity_key():
    # Get current date and time
    now = datetime.datetime.now()
    # Target date is December 14 of the current year
    target_date = datetime.datetime(now.year, 12, 14)
    
    # Calculate seconds difference between now and December 14
    delta_seconds = abs((target_date - now).total_seconds())
    
    # Generate a key based on the difference
    key_base = str(delta_seconds).encode('utf-8')
    # Ensure key is 32 bytes (Fernet requirement)
    proximity_key = base64.urlsafe_b64encode(key_base[:32].ljust(32, b'0'))
    
    return proximity_key

def encrypt_message(message):
    # Generate proximity-based encryption key
    key = generate_proximity_key()
    fernet = Fernet(key)
    
    # Encrypt the message
    encrypted_message = fernet.encrypt(message.encode())
    
    return encrypted_message

def decrypt_message(encrypted_message):
    # Generate proximity-based encryption key
    key = generate_proximity_key()
    fernet = Fernet(key)
    
    # Decrypt the message
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    
    return decrypted_message

def save_encrypted_file(message, file_name):
    encrypted_message = encrypt_message(message)
    
    # Save the encrypted message to a .jonsnow file
    with open(f"{file_name}.jonsnow", "wb") as file:
        file.write(encrypted_message)
    
    # Ask if user wants a .txt version of the encrypted data
    if input("Do you want a .txt file to show the encryption? (yes/no): ").strip().lower() == 'yes':
        with open(f"{file_name}.txt", "wb") as txt_file:
            txt_file.write(encrypted_message)
    
    print(f"Encrypted data saved as {file_name}.jonsnow")

def load_encrypted_file(file_name):
    # Read the encrypted message from a .jonsnow file
    with open(f"{file_name}.jonsnow", "rb") as file:
        encrypted_message = file.read()
    
    # Decrypt the message
    decrypted_message = decrypt_message(encrypted_message)
    
    print("Decrypted message:", decrypted_message)

# Example usage
message = "This is a secret message"
file_name = "encrypted_output"

# Save encrypted message
save_encrypted_file(message, file_name)

# Load and decrypt the message
load_encrypted_file(file_name)


class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sigma's Encryption")
        self.root.geometry("500x500")
        self.root.config(bg="#2E2E2E")  # Dark grey background for tech vibe

        # Header Label
        self.label = tk.Label(
            root, text="Enter Text To Encrypt or Decrypt:", 
            font=("Helvetica", 14, "bold"), bg="#2E2E2E", fg="#B0B0B0"
        )
        self.label.pack(pady=15)

        # Text Box
        self.text_box = tk.Text(
            root, height=6, width=60, font=("Helvetica", 12), 
            bd=0, relief="solid", wrap="word", bg="#3E3E3E", fg="#D3D3D3", 
            insertbackground="#D3D3D3"  # Cursor color
        )
        self.text_box.pack(pady=15)

        # Encrypt & Save Button
        self.encrypt_button = tk.Button(
            root, text="Encrypt & Save", font=("Helvetica", 12), 
            bg="#4A4A4A", fg="#A0A0A0", activebackground="#5A5A5A",
            command=self.encrypt_and_save, relief="flat"
        )
        self.encrypt_button.pack(pady=10, ipadx=10, ipady=5)

        # Decrypt Button
        self.decrypt_button = tk.Button(
            root, text="Open & Decrypt", font=("Helvetica", 12),
            bg="#4A4A4A", fg="#A0A0A0", activebackground="#5A5A5A",
            command=self.open_and_decrypt, relief="flat"
        )
        self.decrypt_button.pack(pady=10, ipadx=10, ipady=5)

    def encrypt_and_save(self):
        text = self.text_box.get("1.0", tk.END).strip()
        encrypted_text = encrypt_text(text)

        # Save the encrypted file as .jonsnow
        jonsnow_path = filedialog.asksaveasfilename(defaultextension=".jonsnow", filetypes=[("JONSNOW Files", "*.jonsnow")])
        if jonsnow_path:
            with open(jonsnow_path, 'w', encoding='utf-8') as file:
                file.write(encrypted_text)

            # Ask if the user wants to save a .txt file as well
            save_txt = messagebox.askyesno("Save as .txt?", "Would you like to save the encrypted text as a .txt file as well?")
            if save_txt:
                txt_path = os.path.splitext(jonsnow_path)[0] + ".txt"
                with open(txt_path, 'w', encoding='utf-8') as file:
                    file.write(encrypted_text)

            messagebox.showinfo("Success", "Files saved successfully.")

    def open_and_decrypt(self):
        filepath = filedialog.askopenfilename(filetypes=[("JONSNOW Files", "*.jonsnow")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                encrypted_text = file.read()

            try:
                decrypted_text = decrypt_text(encrypted_text)
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, decrypted_text)
                messagebox.showinfo("Decryption", "File decrypted successfully.")
            except Exception as e:
                messagebox.showerror("Error", "Decryption failed. Possible date/key mismatch.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEncryptionApp(root)
    root.mainloop()
