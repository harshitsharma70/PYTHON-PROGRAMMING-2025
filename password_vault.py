import tkinter as tk

from tkinter import messagebox, ttk

import sqlite3

from pathlib import Path

from cryptography.fernet import Fernet

import random

import string

import hashlib



HOME_PATH = Path.home() / "password_vault"

HOME_PATH.mkdir(exist_ok=True)



DB_PATH = HOME_PATH / "vault.db"

KEY_PATH = HOME_PATH / "key.key"





def load_key():

    if KEY_PATH.exists():

        return KEY_PATH.read_bytes()

    else:

        key = Fernet.generate_key()

        KEY_PATH.write_bytes(key)

        return key





fernet = Fernet(load_key())




def init_db():

    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS vault (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                website TEXT,

                username TEXT,

                password BLOB

                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS master_password (

                id INTEGER PRIMARY KEY,

                hash TEXT

                )""")

    conn.commit()

    conn.close()





init_db()






def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_master_password_hash():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT hash FROM master_password WHERE id = 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def set_master_password_hash(password_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO master_password (id, hash) VALUES (1, ?)",
              (password_hash,))
    conn.commit()
    conn.close()



class PasswordVault:

    def __init__(self, window):

        self.window = window

        self.window.title("Password Vault")

        self.window.geometry("700x550")

        self.window.resizable(True, True)

        

        if get_master_password_hash() is None:

            set_master_password_hash(hash_password("admin"))



        self.master_password_screen()



    def master_password_screen(self):

        self.clear_window()



        tk.Label(self.window, text="Password Vault",

                 font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.window, text="Enter Master Password",

                 font=("Arial", 12)).pack(pady=10)



        self.master_entry = tk.Entry(self.window, show="*", width=30, font=("Arial", 11))

        self.master_entry.pack(pady=5)

        self.master_entry.bind("<Return>", lambda e: self.check_master_password())

        self.master_entry.focus()



        tk.Button(self.window, text="Login", width=15,

                  command=self.check_master_password, font=("Arial", 10)).pack(pady=10)



    def check_master_password(self):

        entered_password = self.master_entry.get()

        stored_hash = get_master_password_hash()

        

        if stored_hash and hash_password(entered_password) == stored_hash:

            self.vault_screen()

        else:

            messagebox.showerror("Error", "Incorrect Master Password!")

            self.master_entry.delete(0, tk.END)



    def vault_screen(self):

        self.clear_window()


        header_frame = tk.Frame(self.window)

        header_frame.pack(fill=tk.X, pady=10)

        

        tk.Label(header_frame, text="Password Vault",

                 font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=10)

        

        tk.Button(header_frame, text="Change Master Password",

                  command=self.change_master_password_window,

                  font=("Arial", 9)).pack(side=tk.RIGHT, padx=10)

        

        tk.Button(header_frame, text="Logout",

                  command=self.master_password_screen,

                  font=("Arial", 9)).pack(side=tk.RIGHT, padx=5)



        search_frame = tk.Frame(self.window)

        search_frame.pack(fill=tk.X, padx=10, pady=5)

        

        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame, font=("Arial", 10))

        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.search_entry.bind("<KeyRelease>", self.filter_data)

        

        tree_frame = tk.Frame(self.window)

        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        

        columns = ("website", "username", "password")

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("website", text="Website")

        self.tree.heading("username", text="Username")

        self.tree.heading("password", text="Password")

        self.tree.column("website", width=200)

        self.tree.column("username", width=200)

        self.tree.column("password", width=200)

        

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)

        self.tree.configure(yscrollcommand=scrollbar.set)

        

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        

        self.load_data()




        button_frame = tk.Frame(self.window)

        button_frame.pack(fill=tk.X, padx=10, pady=10)

        

        tk.Button(button_frame, text="Add New", command=self.add_new_window,

                  font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Edit", command=self.edit_entry,

                  font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Delete", command=self.delete_entry,

                  font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Copy Password", command=self.copy_password_manual,

                  font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)


        self.tree.bind("<Double-1>", self.copy_password)




    def load_data(self, filter_text=""):


        for item in self.tree.get_children():

            self.tree.delete(item)

        

        conn = sqlite3.connect(DB_PATH)

        c = conn.cursor()



        if filter_text:

            c.execute("""SELECT id, website, username, password FROM vault 

                        WHERE website LIKE ? OR username LIKE ?""",

                     (f"%{filter_text}%", f"%{filter_text}%"))

        else:

            c.execute("SELECT id, website, username, password FROM vault")

        rows = c.fetchall()



        for row in rows:

            try:

                decrypted_pw = fernet.decrypt(row[3]).decode()

                self.tree.insert("", "end", iid=row[0],

                                 values=(row[1], row[2], decrypted_pw))

            except Exception as e:

                messagebox.showerror("Error", f"Failed to decrypt password: {str(e)}")



        conn.close()

    

    def filter_data(self, event=None):

        filter_text = self.search_entry.get().lower()

        self.load_data(filter_text)




    def add_new_window(self, entry_id=None):

        win = tk.Toplevel(self.window)

        win.title("Edit Password" if entry_id else "Add Password")

        win.geometry("400x350")

        win.transient(self.window)

        win.grab_set()




        existing_data = None

        if entry_id:

            conn = sqlite3.connect(DB_PATH)

            c = conn.cursor()

            c.execute("SELECT website, username, password FROM vault WHERE id = ?", (entry_id,))

            result = c.fetchone()

            conn.close()

            if result:

                try:

                    existing_data = (result[0], result[1], fernet.decrypt(result[2]).decode())

                except:

                    messagebox.showerror("Error", "Failed to decrypt entry")

                    win.destroy()

                    return



        tk.Label(win, text="Website", font=("Arial", 10)).pack(pady=5)

        website_entry = tk.Entry(win, width=35, font=("Arial", 10))

        website_entry.pack(pady=5)

        if existing_data:

            website_entry.insert(0, existing_data[0])



        tk.Label(win, text="Username", font=("Arial", 10)).pack(pady=5)

        username_entry = tk.Entry(win, width=35, font=("Arial", 10))

        username_entry.pack(pady=5)

        if existing_data:

            username_entry.insert(0, existing_data[1])



        tk.Label(win, text="Password", font=("Arial", 10)).pack(pady=5)

        password_entry = tk.Entry(win, width=35, font=("Arial", 10), show="*")

        password_entry.pack(pady=5)

        if existing_data:

            password_entry.insert(0, existing_data[2])




        show_password_var = tk.BooleanVar()

        def toggle_password():

            if show_password_var.get():

                password_entry.config(show="")

            else:

                password_entry.config(show="*")

        tk.Checkbutton(win, text="Show Password", variable=show_password_var,

                      command=toggle_password, font=("Arial", 9)).pack(pady=5)




        def generate_password():

            chars = string.ascii_letters + string.digits + string.punctuation

            pw = ''.join(random.choice(chars) for _ in range(16))

            password_entry.delete(0, tk.END)

            password_entry.insert(0, pw)

            show_password_var.set(True)

            toggle_password()



        tk.Button(win, text="Generate Strong Password",

                  command=generate_password, font=("Arial", 9)).pack(pady=5)



        def save():

            website = website_entry.get().strip()

            username = username_entry.get().strip()

            password = password_entry.get()



            if not website or not username or not password:

                messagebox.showwarning("Warning", "All fields are required!")

                return



            encrypted_pw = fernet.encrypt(password.encode())



            conn = sqlite3.connect(DB_PATH)

            c = conn.cursor()

            if entry_id:

                c.execute("UPDATE vault SET website = ?, username = ?, password = ? WHERE id = ?",

                          (website, username, encrypted_pw, entry_id))

            else:

                c.execute("INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",

                          (website, username, encrypted_pw))

            conn.commit()

            conn.close()



            win.destroy()

            self.load_data(self.search_entry.get().lower())



        button_frame = tk.Frame(win)

        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save", command=save,

                  font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Cancel", command=win.destroy,

                  font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=5)



    def copy_password(self, event):

        self.copy_password_manual()

    

    def copy_password_manual(self):

        selected = self.tree.selection()

        if selected:

            item = self.tree.item(selected)

            password = item["values"][2]



            self.window.clipboard_clear()

            self.window.clipboard_append(password)



            messagebox.showinfo("Copied", "Password copied to clipboard!")

        else:

            messagebox.showwarning("Warning", "Please select an entry first!")

    

    def edit_entry(self):

        selected = self.tree.selection()

        if selected:

            entry_id = selected[0]

            self.add_new_window(entry_id)

        else:

            messagebox.showwarning("Warning", "Please select an entry to edit!")

    


    def delete_entry(self):

        selected = self.tree.selection()

        if selected:

            entry_id = selected[0]

            item = self.tree.item(selected)

            website = item["values"][0]

            

            confirm = messagebox.askyesno("Confirm Delete",

                                         f"Are you sure you want to delete the entry for '{website}'?")

            if confirm:

                conn = sqlite3.connect(DB_PATH)

                c = conn.cursor()

                c.execute("DELETE FROM vault WHERE id = ?", (entry_id,))

                conn.commit()

                conn.close()

                

                self.load_data(self.search_entry.get().lower())

                messagebox.showinfo("Success", "Entry deleted successfully!")

        else:

            messagebox.showwarning("Warning", "Please select an entry to delete!")

    


    def change_master_password_window(self):

        win = tk.Toplevel(self.window)

        win.title("Change Master Password")

        win.geometry("400x250")

        win.transient(self.window)

        win.grab_set()



        tk.Label(win, text="Change Master Password", font=("Arial", 14, "bold")).pack(pady=10)

        

        tk.Label(win, text="Current Password:", font=("Arial", 10)).pack(pady=5)

        current_entry = tk.Entry(win, show="*", width=30, font=("Arial", 10))

        current_entry.pack(pady=5)

        

        tk.Label(win, text="New Password:", font=("Arial", 10)).pack(pady=5)

        new_entry = tk.Entry(win, show="*", width=30, font=("Arial", 10))

        new_entry.pack(pady=5)

        

        tk.Label(win, text="Confirm New Password:", font=("Arial", 10)).pack(pady=5)

        confirm_entry = tk.Entry(win, show="*", width=30, font=("Arial", 10))

        confirm_entry.pack(pady=5)

        

        def save_new_password():

            current = current_entry.get()

            new_pw = new_entry.get()

            confirm_pw = confirm_entry.get()

            

            stored_hash = get_master_password_hash()

            if not stored_hash or hash_password(current) != stored_hash:

                messagebox.showerror("Error", "Current password is incorrect!")

                return

            

            if not new_pw:

                messagebox.showwarning("Warning", "New password cannot be empty!")

                return

            

            if new_pw != confirm_pw:

                messagebox.showerror("Error", "New passwords do not match!")

                return

            

            if len(new_pw) < 4:

                messagebox.showwarning("Warning", "Password must be at least 4 characters long!")

                return

            

            set_master_password_hash(hash_password(new_pw))

            messagebox.showinfo("Success", "Master password changed successfully!")

            win.destroy()

            self.master_password_screen()

        

        button_frame = tk.Frame(win)

        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Change Password", command=save_new_password,

                  font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Cancel", command=win.destroy,

                  font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)




    def clear_window(self):

        for widget in self.window.winfo_children():

            widget.destroy()




root = tk.Tk()

app = PasswordVault(root)

root.mainloop()