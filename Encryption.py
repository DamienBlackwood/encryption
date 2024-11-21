import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime as dt

def calculated_date_based_key(base_key=5):
    mybday = dt(dt.now().year, 12, 14)
    today = dt.now()
    day_diff = abs((mybday - today).days)
    datemodify = day_diff % 26 # specifically so its in alphabet shit
    return base_key + datemodify

def encrypt_text(text):
    key = calculated_date_based_key()
    encrypt_text = ''.join(chr((ord(char) + key) % 256) for char in text)
    return encrypt_text

def decrypt_text(encrypted_text):
    key = calculated_date_based_key()
    decrypted_text = ''.join(chr((ord(char) - key) % 256) for char in encrypted_text)
    return decrypted_text

class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sigma's Encryption")
        self.root.geometry("500x500")
        self.root.config(bg="#f0f0f0")

        self.root.attributes("-transparentcolor", "#f0f0f0")

        self.label = tk.Label(root, text="Enter Text To Encrypt or Decrypt:", font = ("Times New Roman", 12, "bold"), bg = "#0f0f0f", fg = "#333")
        self.label.pack(pady= 10)
        self.text_box = tk.Text(root, height =6, width= 60, font = ("Times New Roman", 12), bd = 2, relief = "solid", wrap = "word", bg = "#ffffff", fg = "#333")
        self.text_box.pack(pady= 15)

        self.encrypt_button = tk.Button(root, text="Encrypt & Save as .jonsnow", font = ("Times New Roman", 12, "bold"), bg = "#4CAF50", fg = "white", command = self.encrypt_and_save, relief="raised", bd = 2)
        self.encrypt_button.pack(pady = 10, ipadx = 10, ipady = 5)

        self.decrypt_button = tk.Button(root, text="Open & Decrypt .jonsnow", font = ("Times New Roman", 12, "bold"), bg = "#FF5722", fg= "white", command = self.open_and_decrypt, relief="raised", bd = 2)
        self.decrypt_button.pack(pady = 10, ipadx = 10, ipady = 5)

    def encrypt_and_save(self):
        text = self.text_box.get("1.0", tk.END).strip()
        encrypted_text = encrypt_text(text)

        # so here im trynna save the files
        filepath = filedialog.asksaveasfilename(defaultextension=".jonsnow", filetypes=[("JONSNOW Files", "*.jonsnow")])
        if filepath:
            with open(filepath, 'w') as file:
                file.write(encrypted_text)
            messagebox.showinfo("Success!", "I encrypted your file, stay safe kiddo!")


    def open_and_decrypt(self):
        filepath = filedialog.askopenfilename(filetypes=[("JONSNOW Files", "*.jonsnow")])
        if filepath:
            with open(filepath, 'r') as file:
                encrypted_text = file.read()

            try:
                #just incase
                decrypted_text = decrypt_text(encrypted_text)
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, decrypted_text)
                messagebox.showinfo("Decryption", "File decrypted successfully,")
            except Exception as e:
                messagebox.showerror("Error", "Decryption failed. I think there's a date/key mismatch.")

    
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEncryptionApp(root)
    root.mainloop()
                


