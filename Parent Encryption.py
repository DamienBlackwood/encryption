import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime as dt

# its the base key
def birthdaykey(basekey=5):
    bday = dt(dt.now().year, 12, 14)  # I want to make sure its the 14th of december of the current yaer
    now = dt.now()
    seconds = abs((bday - now).total_seconds())  # difference in seconds
    modkey = int(seconds) % 256  # keep it within byte range
    return basekey + modkey

# i want a constant offset to make sure the time variance isnt code breaking!!!!
def encodekey(key, offset=42):
    return key + offset

def decodekey(encodedkey, offset=42):
    return encodedkey - offset

def encryptedwithkey(text):
    key = birthdaykey()
    encodedkey = encodekey(key)
    ENCRYPTEDTEXT = ''.join(chr((ord(char) + key) % 256) for char in text)
    return ENCRYPTEDTEXT, encodedkey

def decryptedwithkey(encryptedtext, encodedkey):
    key = decodekey(encodedkey)
    decryptedtext = ''.join(chr((ord(char) - key) % 256) for char in encryptedtext)
    return decryptedtext


class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Goat's Encryption Method")
        self.root.geometry("500x500")
        self.root.config(bg="#2c2f33")  # it needs to look swagger

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

    # most important i'd say
    def encryptandsave(self):
        text = self.textbox.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to encrypt!")
            return

        encryptedtext, encodedkey = encryptedwithkey(text)

        # save the encrypted text and encoded key
        filepath = filedialog.asksaveasfilename(defaultextension=".jonsnow", 
                                                filetypes=[("JONSNOW Files", "*.jonsnow")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(f"{encodedkey}\n{encryptedtext}")
            messagebox.showinfo("Success", "File encrypted and saved successfully!")

        if messagebox.askyesno("Save Text File", "Would you like to also save a .txt file of the encryption?"):
            txt_filepath = os.path.splitext(filepath)[0] + ".txt"
            with open(txt_filepath, 'w', encoding='utf-8') as file:
                file.write(encryptedtext)
            messagebox.showinfo("Success", "Encrypted text saved as a .txt file!")

        self.textbox.delete("1.0", tk.END)
    # opening file 😋
    def openanddecrypt(self):
        filepath = filedialog.askopenfilename(filetypes=[("JONSNOW Files", "*.jonsnow")])
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) < 2:
                    raise ValueError("Invalid file format")
                encodedkey = int(lines[0].strip())  # read the key muahhahahahahahha
                encryptedtext = ''.join(lines[1:])  
            
            self.decryptedtext = decryptedwithkey(encryptedtext, encodedkey)

        
            self.textbox.delete("1.0", tk.END)
            self.textbox.insert(tk.END, self.decryptedtext)
            messagebox.showinfo("Decryption", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# rad
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEncryptionApp(root)
    root.mainloop()
