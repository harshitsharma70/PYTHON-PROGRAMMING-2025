import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
import traceback

# ----------------------------- FILE PATHS -----------------------------

HOME_PATH = Path.home() / "password_vault"
HOME_PATH.mkdir(exist_ok=True)

DB_PATH = HOME_PATH / "vault.db"
KEY_PATH = HOME_PATH / "vault.key"


# ----------------------------- ENCRYPTION -----------------------------

def load_or_create_key():
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes()
    else:
        key = Fernet.generate_key()
        KEY_PATH.write_bytes(key)
        return key


FERNET_KEY = load_or_create_key()
CIPHER = Fernet(FERNET_KEY)

def encrypt(text):
    return CIPHER.encrypt(text.encode())

def decrypt(token):
    return CIPHER.decrypt(token).decode()


# ----------------------------- DATABASE SETUP -----------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ----------------------------- MATERIAL YOU STYLE -----------------------------

PRIMARY = "#6750A4"
LIGHT_BG = "#F4F0FF"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1C1B1F"
OUTLINE = "#D0CBE5"
FONT = ("Segoe UI", 11)

# ----------------------------- APP CLASS -----------------------------

class PasswordVault:
    def __init__(self, window):
        self.window = window
        self.window.title("Password Vault")
        self.window.geometry("900x550")
        self.window.configure(bg=LIGHT_BG)

        self._style_widgets()
        self._build_gui()
        self._load_entries()

    # ----------------------------- STYLES -----------------------------

    def _style_widgets(self):
        style = ttk.Style()

        style.theme_use("clam")

        # Buttons
        style.configure(
            "Material.TButton",
            background=PRIMARY,
            foreground="white",
            padding=8,
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            focusthickness=3
        )
        style.map(
            "Material.TButton",
            background=[("active", "#7F67BE")]
        )

        # Entry fields
        style.configure(
            "Material.TEntry",
            padding=6,
            relief="flat",
            foreground=TEXT_DARK,
            fieldbackground="white"
        )

        # Treeview
        style.configure(
            "Material.Treeview",
            background="white",
            fieldbackground="white",
            foreground=TEXT_DARK,
            rowheight=28,
            borderwidth=0
        )
        style.configure(
            "Material.Treeview.Heading",
            font=("Segoe UI", 12, "bold"),
            background="#EADDFF",
            foreground=TEXT_DARK
        )

    # ----------------------------- GUI -----------------------------

    def _build_gui(self):
        # LEFT CARD
        card = tk.Frame(
            self.window,
            bg=CARD_BG,
            bd=0,
            highlightbackground=OUTLINE,
            highlightthickness=2
        )
        card.place(x=30, y=30, width=330, height=260)

        tk.Label(card, text="Add New Entry", font=("Segoe UI", 15, "bold"),
                 bg=CARD_BG, fg=TEXT_DARK).pack(pady=10)

        # Inputs
        tk.Label(card, text="Service", bg=CARD_BG, fg=TEXT_DARK, font=FONT).pack(anchor="w", padx=20)
        self.service_entry = ttk.Entry(card, style="Material.TEntry")
        self.service_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(card, text="Username", bg=CARD_BG, fg=TEXT_DARK, font=FONT).pack(anchor="w", padx=20)
        self.username_entry = ttk.Entry(card, style="Material.TEntry")
        self.username_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(card, text="Password", bg=CARD_BG, fg=TEXT_DARK, font=FONT).pack(anchor="w", padx=20)
        self.password_entry = ttk.Entry(card, style="Material.TEntry", show="●")
        self.password_entry.pack(fill="x", padx=20, pady=5)

        ttk.Button(card, text="Save", style="Material.TButton",
                   command=self._save_entry).pack(pady=15)

        # TABLE CARD
        table_card = tk.Frame(
            self.window, bg=CARD_BG,
            highlightbackground=OUTLINE, highlightthickness=2
        )
        table_card.place(x=380, y=30, width=500, height=480)

        self.tree = ttk.Treeview(
            table_card,
            columns=("Service", "Username", "Password"),
            show="headings",
            style="Material.Treeview"
        )

        for col in ("Service", "Username", "Password"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ----------------------------- SAVE ENTRY -----------------------------

    def _save_entry(self):
        s = self.service_entry.get()
        u = self.username_entry.get()
        p = self.password_entry.get()

        if not (s and u and p):
            messagebox.showerror("Error", "All fields are required.")
            return

        enc = encrypt(p)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO vault (service, username, password) VALUES (?, ?, ?)",
                  (s, u, enc))
        conn.commit()
        conn.close()

        self._load_entries()

        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    # ----------------------------- LOAD ENTRIES -----------------------------

    def _load_entries(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT service, username, password FROM vault")
        rows = c.fetchall()
        conn.close()

        for i in self.tree.get_children():
            self.tree.delete(i)

        for s, u, p in rows:
            try:
                d = decrypt(p)
            except:
                d = "Invalid"

            self.tree.insert("", tk.END, values=(s, u, d))


# ----------------------------- RUN APP -----------------------------

if __name__ == "__main__":
    try:
        init_db()
        root = tk.Tk()
        app = PasswordVault(root)
        root.mainloop()

    except Exception:
        traceback.print_exc()
        input("Press Enter to exit...")
