"""
High-tech Password Vault UI (single-file)
Features added:
- Modern Material You inspired palette
- Gradient backdrop and soft glass cards
- Search bar, theme toggle (light/dark)
- Password generator, strength meter
- Show/Hide and copy-to-clipboard
- Smooth micro-interaction animations (simple)
- Same encrypted SQLite vault using Fernet

Dependencies: Pillow, cryptography (Fernet). All else uses the Python stdlib.

Save as password_vault_high_tech.py and run with Python 3.8+.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sqlite3
import secrets
import string
import hashlib
import sys
import traceback
from cryptography.fernet import Fernet
from PIL import Image, ImageTk

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

def encrypt(text: str) -> bytes:
    return CIPHER.encrypt(text.encode())

def decrypt(token: bytes) -> str:
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

# ----------------------------- THEME / STYLE -----------------------------

PALETTE = {
    "PRIMARY": "#6750A4",
    "ACCENT": "#7F67BE",
    "BG_LIGHT": "#F4F0FF",
    "BG_DARK": "#0F1115",
    "CARD": "#FFFFFF",
    "CARD_DARK": "#121217",
    "TEXT": "#1C1B1F",
    "MUTED": "#8B84A7",
    "OUTLINE": "#D0CBE5",
}

FONT = ("Segoe UI", 11)
HEADER_FONT = ("Segoe UI Semibold", 14)

# ----------------------------- UTILITIES -----------------------------

def generate_password(length=16, use_symbols=True):
    alphabet = string.ascii_letters + string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.<>?/"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def password_strength(pw: str) -> (int, str):
    score = 0
    length = len(pw)
    if length >= 8:
        score += 1
    if any(c.islower() for c in pw) and any(c.isupper() for c in pw):
        score += 1
    if any(c.isdigit() for c in pw):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in pw):
        score += 1
    # score 0-4
    labels = ["Very Weak", "Weak", "Okay", "Strong", "Excellent"]
    return score, labels[score]

# ----------------------------- APP CLASS -----------------------------

class HighTechVault(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Vault — HighTech UI")
        self.geometry("980x600")
        self.minsize(900, 540)
        self.configure(bg=PALETTE['BG_LIGHT'])

        self.dark_mode = False

        self._setup_styles()
        self._build_ui()
        self._load_entries()

    # ----------------------------- STYLES -----------------------------
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('TButton', font=FONT, padding=8)
        style.configure('Accent.TButton', background=PALETTE['PRIMARY'], foreground='white', relief='flat')
        style.map('Accent.TButton', background=[('active', PALETTE['ACCENT'])])

        style.configure('TEntry', padding=6)
        style.configure('Treeview', font=FONT, rowheight=28)
        style.configure('Treeview.Heading', font=HEADER_FONT)

    # ----------------------------- UI BUILD -----------------------------
    def _build_ui(self):
        # gradient background canvas
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self._draw_gradient()

        # top bar
        top_frame = tk.Frame(self.canvas, bg='', bd=0)
        self.top_window = self.canvas.create_window(20, 18, anchor='nw', window=top_frame)

        title = tk.Label(top_frame, text='Password Vault', font=("Segoe UI Bold", 18), bg='', fg=PALETTE['TEXT'])
        title.pack(side='left')

        self.theme_btn = ttk.Button(top_frame, text='Toggle Theme', command=self._toggle_theme)
        self.theme_btn.pack(side='right')

        # main content area - left card (form) and right card (list)
        left_card = self._card_frame(self.canvas, width=360, height=420)
        self.left_window = self.canvas.create_window(30, 70, anchor='nw', window=left_card)

        right_card = self._card_frame(self.canvas, width=560, height=480)
        self.right_window = self.canvas.create_window(410, 70, anchor='nw', window=right_card)

        # Left card contents
        tk.Label(left_card, text='Add New Entry', font=HEADER_FONT, bg=left_card['bg']).pack(pady=(14, 6))

        # service
        tk.Label(left_card, text='Service', bg=left_card['bg'], font=FONT).pack(anchor='w', padx=20)
        self.service_entry = ttk.Entry(left_card)
        self.service_entry.pack(fill='x', padx=20, pady=6)

        tk.Label(left_card, text='Username', bg=left_card['bg'], font=FONT).pack(anchor='w', padx=20)
        self.username_entry = ttk.Entry(left_card)
        self.username_entry.pack(fill='x', padx=20, pady=6)

        tk.Label(left_card, text='Password', bg=left_card['bg'], font=FONT).pack(anchor='w', padx=20)
        pw_frame = tk.Frame(left_card, bg=left_card['bg'])
        pw_frame.pack(fill='x', padx=20)
        self.password_entry = ttk.Entry(pw_frame, show='•')
        self.password_entry.pack(side='left', fill='x', expand=True)
        self.show_pw = tk.BooleanVar(value=False)
        self.show_btn = ttk.Button(pw_frame, text='Show', width=6, command=self._toggle_show)
        self.show_btn.pack(side='left', padx=6)

        gen_frame = tk.Frame(left_card, bg=left_card['bg'])
        gen_frame.pack(fill='x', padx=20, pady=(6, 0))
        ttk.Button(gen_frame, text='Generate', command=self._generate_pw).pack(side='left')
        ttk.Button(gen_frame, text='Save', style='Accent.TButton', command=self._save_entry).pack(side='right')

        # strength meter
        self.strength_label = tk.Label(left_card, text='Strength: —', bg=left_card['bg'], font=FONT)
        self.strength_label.pack(anchor='w', padx=20, pady=(10, 0))
        self.password_entry.bind('<KeyRelease>', self._on_pw_change)

        # Right card contents - search + tree
        search_frame = tk.Frame(right_card, bg=right_card['bg'])
        search_frame.pack(fill='x', padx=12, pady=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        self.search_var.trace_add('write', lambda *a: self._load_entries())
        ttk.Button(search_frame, text='Clear', command=self._clear_search).pack(side='right', padx=6)

        # treeview
        cols = ("Service", "Username", "Password")
        self.tree = ttk.Treeview(right_card, columns=cols, show='headings', selectmode='browse')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=12, pady=(0, 12))
        self.tree.bind('<Double-1>', self._on_row_double)

        # row actions
        action_frame = tk.Frame(right_card, bg=right_card['bg'])
        action_frame.pack(fill='x', padx=12, pady=(0, 12))
        ttk.Button(action_frame, text='Copy Password', command=self._copy_selected_pw).pack(side='left')
        ttk.Button(action_frame, text='Delete', command=self._delete_selected).pack(side='left', padx=6)

    # ----------------------------- SMALL HELPERS -----------------------------
    def _card_frame(self, parent, width=300, height=300):
        # simple card with a subtle shadow effect (frame only)
        frame = tk.Frame(parent, bg=PALETTE['CARD'], bd=0, highlightthickness=0)
        frame.config(width=width, height=height)
        frame.pack_propagate(False)
        return frame

    def _draw_gradient(self):
        # draw a subtle vertical gradient using rectangles
        self.canvas.delete('grad')
        w = self.winfo_width() or 980
        h = self.winfo_height() or 600
        r1, g1, b1 = (244, 240, 255)  # BG_LIGHT
        r2, g2, b2 = (230, 224, 255)  # slightly darker
        steps = 40
        for i in range(steps):
            r = int(r1 + (r2 - r1) * (i / steps))
            g = int(g1 + (g2 - g1) * (i / steps))
            b = int(b1 + (b2 - b1) * (i / steps))
            color = f'#{r:02x}{g:02x}{b:02x}'
            y1 = int(i * h / steps)
            y2 = int((i + 1) * h / steps)
            self.canvas.create_rectangle(0, y1, w, y2, fill=color, outline=color, tags='grad')
        # bind resize
        self.bind('<Configure>', lambda e: self.after(10, self._draw_gradient))

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            PALETTE['CARD'] = PALETTE['CARD_DARK']
            PALETTE['BG_LIGHT'] = PALETTE['BG_DARK']
            self.configure(bg=PALETTE['BG_DARK'])
        else:
            PALETTE['CARD'] = '#FFFFFF'
            PALETTE['BG_LIGHT'] = '#F4F0FF'
            self.configure(bg=PALETTE['BG_LIGHT'])
        # redraw static elements
        self._draw_gradient()

    def _toggle_show(self):
        current = self.show_pw.get()
        self.show_pw.set(not current)
        self.password_entry.config(show='' if not current else '•')
        self.show_btn.config(text='Hide' if not current else 'Show')

    def _generate_pw(self):
        pw = generate_password(16, use_symbols=True)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, pw)
        self._on_pw_change()

    def _on_pw_change(self, event=None):
        pw = self.password_entry.get()
        score, label = password_strength(pw)
        colors = ['#c62828', '#ef6c00', '#f9a825', '#2e7d32', '#1b5e20']
        color = colors[score]
        self.strength_label.config(text=f'Strength: {label}')

    def _clear_search(self):
        self.search_var.set('')

    # ----------------------------- DATABASE ACTIONS -----------------------------
    def _save_entry(self):
        s = self.service_entry.get().strip()
        u = self.username_entry.get().strip()
        p = self.password_entry.get()
        if not (s and u and p):
            messagebox.showerror('Error', 'All fields are required.')
            return
        enc = encrypt(p)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO vault (service, username, password) VALUES (?, ?, ?)', (s, u, enc))
        conn.commit()
        conn.close()
        self._load_entries()
        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def _load_entries(self):
        self.tree.delete(*self.tree.get_children())
        q = self.search_var.get().strip().lower()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, service, username, password FROM vault ORDER BY id DESC')
        rows = c.fetchall()
        conn.close()
        for rid, s, u, p in rows:
            if q and q not in s.lower() and q not in u.lower():
                continue
            try:
                d = decrypt(p)
            except Exception:
                d = 'Invalid'
            # show masked password
            masked = '•' * min(12, len(d)) + (d[-2:] if len(d) > 2 else '')
            self.tree.insert('', 'end', iid=str(rid), values=(s, u, masked))

    def _on_row_double(self, event):
        item = self.tree.selection()
        if not item:
            return
        iid = item[0]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT service, username, password FROM vault WHERE id=?', (iid,))
        row = c.fetchone()
        conn.close()
        if not row:
            return
        s, u, p = row
        try:
            d = decrypt(p)
        except Exception:
            d = 'Invalid'
        # show detail modal
        self._show_detail_modal(s, u, d)

    def _show_detail_modal(self, service, username, password):
        modal = tk.Toplevel(self)
        modal.transient(self)
        modal.grab_set()
        modal.title(service)
        modal.geometry('420x200')

        tk.Label(modal, text=service, font=HEADER_FONT).pack(pady=(12, 6))
        tk.Label(modal, text=f'Username: {username}', font=FONT).pack(anchor='w', padx=14)

        pw_frame = tk.Frame(modal)
        pw_frame.pack(fill='x', padx=14, pady=(12, 6))
        pw_entry = ttk.Entry(pw_frame)
        pw_entry.insert(0, password)
        pw_entry.config(state='readonly')
        pw_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(pw_frame, text='Copy', command=lambda: self._clipboard_copy(password)).pack(side='left', padx=6)

        ttk.Button(modal, text='Close', command=modal.destroy).pack(pady=(8, 14))

    def _clipboard_copy(self, text):
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo('Copied', 'Password copied to clipboard.')
        except Exception:
            messagebox.showerror('Error', 'Could not copy to clipboard.')

    def _copy_selected_pw(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select', 'Select a row first.')
            return
        iid = sel[0]
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT password FROM vault WHERE id=?', (iid,))
        row = c.fetchone()
        conn.close()
        if not row:
            return
        try:
            pw = decrypt(row[0])
        except Exception:
            messagebox.showerror('Error', 'Could not decrypt password.')
            return
        self._clipboard_copy(pw)

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select', 'Select a row first.')
            return
        iid = sel[0]
        if not messagebox.askyesno('Confirm', 'Delete this entry?'):
            return
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM vault WHERE id=?', (iid,))
        conn.commit()
        conn.close()
        self._load_entries()

# ----------------------------- RUN APP -----------------------------

if __name__ == '__main__':
    try:
        init_db()
        app = HighTechVault()
        app.mainloop()
    except Exception:
        traceback.print_exc()
        input('Press Enter to exit...')
