
import tkinter as tk
from tkinter import messagebox

BG = "#f4f6f9"
WHITE = "#ffffff"
SIDEBAR_BG = "#0f4f9c"
SIDEBAR_ACTIVE = "#0d6efd"
SIDEBAR_HOVER = "#2563eb"
SIDEBAR_MUTED = "#cfe3ff"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6b7280"
BORDER = "#d9dee8"

BLUE = "#0d6efd"
BLUE_HOVER = "#0b5ed7"
GREEN = "#198754"
GREEN_HOVER = "#157347"
GRAY = "#6c757d"
GRAY_HOVER = "#5c636a"
YELLOW = "#ffc107"
YELLOW_HOVER = "#e0a800"
RED = "#dc3545"
RED_HOVER = "#bb2d3b"


DEFAULT_ACCOUNTS = [
    {
        "id": 4,
        "full_name": "Dennielle Cruz",
        "status": "Active",
        "username": "dennielle13",
        "password": "",
        "date_created": "Oct 29, 2025",
    },
    {
        "id": 3,
        "full_name": "Dhenzel rain Cruz",
        "status": "Active",
        "username": "dhenzelrain",
        "password": "",
        "date_created": "Oct 29, 2025",
    },
]


def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()


def set_button_hover(button, normal, hover):
    button.configure(bg=normal, activebackground=hover)

    def on_enter(_):
        button.configure(bg=hover)

    def on_leave(_):
        button.configure(bg=normal)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


def create_button(parent, text, color, hover, command, width=None, fg=WHITE, font_size=10):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", font_size, "bold"),
        padx=10,
        pady=7,
    )
    if width is not None:
        btn.configure(width=width)
    set_button_hover(btn, color, hover)
    return btn


def create_card(parent):
    outer = tk.Frame(parent, bg=BORDER)
    inner = tk.Frame(outer, bg=WHITE)
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    return outer, inner


def create_input(parent, textvariable=None, placeholder="", show=None):
    entry = tk.Entry(
        parent,
        textvariable=textvariable,
        relief="solid",
        bd=1,
        highlightthickness=0,
        bg=WHITE,
        fg=TEXT_DARK,
        insertbackground=TEXT_DARK,
        font=("Segoe UI", 11),
        show=show or "",
    )
    entry.placeholder = placeholder
    entry.real_show = show or ""

    def add_placeholder():
        if not entry.get() and placeholder:
            entry.insert(0, placeholder)
            entry.configure(fg=TEXT_GRAY, show="")

    def remove_placeholder(_=None):
        if placeholder and entry.get() == placeholder and entry.cget("fg") == TEXT_GRAY:
            entry.delete(0, "end")
            entry.configure(fg=TEXT_DARK, show=entry.real_show)

    def restore_placeholder(_=None):
        if placeholder and not entry.get():
            add_placeholder()

    if placeholder:
        add_placeholder()
        entry.bind("<FocusIn>", remove_placeholder)
        entry.bind("<FocusOut>", restore_placeholder)

    return entry


def entry_value(entry):
    if getattr(entry, "placeholder", "") and entry.get() == entry.placeholder and entry.cget("fg") == TEXT_GRAY:
        return ""
    return entry.get()


def create_status_badge(parent, status):
    bg = GREEN if status == "Active" else GRAY
    return tk.Label(
        parent,
        text=status,
        bg=bg,
        fg=WHITE,
        font=("Segoe UI", 9, "bold"),
        padx=10,
        pady=3,
    )


class Sidebar(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=SIDEBAR_BG, width=230)
        self.app = app
        self.pack_propagate(False)
        self.build()

    def build(self):
        header = tk.Frame(self, bg=SIDEBAR_BG)
        header.pack(fill="x", padx=18, pady=(18, 20))

        tk.Label(header, text="☰", bg=SIDEBAR_BG, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left")
        tk.Label(header, text="Admin Panel", bg=SIDEBAR_BG, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left", padx=(14, 0))

        profile = tk.Frame(self, bg=SIDEBAR_BG)
        profile.pack(fill="x", pady=(6, 26))

        avatar = tk.Canvas(profile, width=78, height=78, bg=SIDEBAR_BG, highlightthickness=0)
        avatar.create_oval(4, 4, 74, 74, outline=WHITE, width=2)
        avatar.pack(pady=(0, 12))

        tk.Label(profile, text="Christian Joseph Aquino", bg=SIDEBAR_BG, fg=WHITE, font=("Segoe UI", 11, "bold")).pack()
        tk.Label(profile, text="Administrator", bg=SIDEBAR_BG, fg=SIDEBAR_MUTED, font=("Segoe UI", 10)).pack(pady=(3, 4))
        tk.Label(profile, text="View Profile →", bg=SIDEBAR_BG, fg="#fde047", font=("Segoe UI", 10)).pack()

        nav = tk.Frame(self, bg=SIDEBAR_BG)
        nav.pack(fill="x", pady=(2, 0))

        menu = [
            ("Dashboard", "▧"),
            ("Teachers", "👥"),
            ("Students", "🎓"),
            ("Student Accounts", "▣"),
            ("Activities", "▤"),
            ("Enrollment", "▱"),
            ("Reports", "▥"),
        ]

        for label, icon in menu:
            self.create_sidebar_item(nav, label, icon)

        spacer = tk.Frame(self, bg=SIDEBAR_BG)
        spacer.pack(fill="both", expand=True)

        tk.Label(
            self,
            text="↩  Logout",
            bg=SIDEBAR_BG,
            fg="#fecaca",
            font=("Segoe UI", 11),
            anchor="w",
            padx=14,
            pady=14,
            cursor="hand2",
        ).pack(fill="x", side="bottom")

    def create_sidebar_item(self, parent, label, icon):
        active = label == "Student Accounts"
        row = tk.Label(
            parent,
            text=f"{icon}  {label}",
            bg=SIDEBAR_ACTIVE if active else SIDEBAR_BG,
            fg=WHITE,
            font=("Segoe UI", 11, "bold" if active else "normal"),
            anchor="w",
            padx=14,
            pady=13,
            cursor="hand2",
        )
        row.pack(fill="x")

        if not active:
            row.bind("<Enter>", lambda _: row.configure(bg=SIDEBAR_HOVER))
            row.bind("<Leave>", lambda _: row.configure(bg=SIDEBAR_BG))


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1500x820")
        self.minsize(1100, 700)
        self.configure(bg=BG)

        self.accounts = [dict(a) for a in DEFAULT_ACCOUNTS]
        self.show_all = False

        self.grid_columnconfigure(0, minsize=230, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = tk.Frame(self, bg=BG)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)

        self.show_student_accounts()

    def clear_main(self):
        clear_frame(self.main)

    def show_student_accounts(self):
        self.clear_main()
        StudentAccountsPage(self.main, self).grid(row=0, column=0, sticky="nsew")

    def show_edit_student_account(self, account_id):
        account = self.find_account(account_id)
        if account:
            self.clear_main()
            EditStudentAccountPage(self.main, self, account).grid(row=0, column=0, sticky="nsew")

    def find_account(self, account_id):
        return next((a for a in self.accounts if a["id"] == account_id), None)

    def edit_account(self, account_id):
        self.show_edit_student_account(account_id)

    def deactivate_account(self, account_id):
        account = self.find_account(account_id)
        if account:
            account["status"] = "Inactive"
        self.show_student_accounts()

    def activate_account(self, account_id):
        account = self.find_account(account_id)
        if account:
            account["status"] = "Active"
        self.show_student_accounts()

    def delete_account(self, account_id):
        if messagebox.askyesno("Delete Account", "Delete this student account?", parent=self):
            self.accounts = [a for a in self.accounts if a["id"] != account_id]
            self.show_student_accounts()

    def toggle_show_all(self):
        self.show_all = not self.show_all
        self.show_student_accounts()

    def save_account(self, account_id, username, password):
        account = self.find_account(account_id)
        if account:
            account["username"] = username
            account["password"] = password
        self.show_student_accounts()


class StudentAccountsPage(tk.Frame):
    HEADERS = ["ID", "Full Name", "Status", "Username", "Date Created", "Actions"]
    COL_WIDTHS = [75, 330, 175, 245, 260, 230]

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_table())

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.build()

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 18))
        top.grid_columnconfigure(0, weight=1)

        tk.Label(top, text="Student Accounts", bg=BG, fg=TEXT_DARK, font=("Segoe UI", 28, "bold")).grid(row=0, column=0, sticky="w")

        text = "Show Active Only" if self.app.show_all else "Show All"
        color = GRAY if self.app.show_all else BLUE
        hover = GRAY_HOVER if self.app.show_all else BLUE_HOVER
        create_button(top, text, color, hover, self.app.toggle_show_all, width=16, font_size=11).grid(row=0, column=1, sticky="e")

        outer, card = create_card(self)
        outer.grid(row=1, column=0, sticky="new", padx=28, pady=(0, 28))
        card.grid_columnconfigure(0, weight=1)

        search_wrap = tk.Frame(card, bg=WHITE)
        search_wrap.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 10))
        search_wrap.grid_columnconfigure(0, weight=1)

        self.search_entry = create_input(search_wrap, textvariable=self.search_var, placeholder="Search student...")
        self.search_entry.grid(row=0, column=0, sticky="ew", ipady=8)

        self.table = tk.Frame(card, bg=WHITE)
        self.table.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        self.refresh_table()

    def create_table_header(self):
        header = tk.Frame(self.table, bg="#f9fafb")
        header.grid(row=0, column=0, sticky="ew")
        for i, width in enumerate(self.COL_WIDTHS):
            header.grid_columnconfigure(i, minsize=width, weight=0, uniform="accounts_table")

        for col, title in enumerate(self.HEADERS):
            tk.Label(
                header,
                text=title,
                bg="#f9fafb",
                fg=TEXT_DARK,
                font=("Segoe UI", 11, "bold"),
                anchor="e" if title == "Actions" else "w",
                padx=8,
                pady=10,
            ).grid(row=0, column=col, sticky="ew")

    def refresh_table(self):
        clear_frame(self.table)
        self.create_table_header()

        query = self.search_var.get().strip().lower()
        if query == "search student...":
            query = ""

        rows = self.app.accounts
        if not self.app.show_all:
            rows = [a for a in rows if a["status"] == "Active"]

        if query:
            rows = [
                a for a in rows
                if query in a["full_name"].lower()
                or query in a["username"].lower()
                or query == str(a["id"])
            ]

        for index, account in enumerate(rows, start=1):
            self.create_table_row(index, account)

    def create_table_row(self, row_index, account):
        row = tk.Frame(self.table, bg=WHITE)
        row.grid(row=row_index, column=0, sticky="ew")

        for i, width in enumerate(self.COL_WIDTHS):
            row.grid_columnconfigure(i, minsize=width, weight=0, uniform="accounts_table")

        values = [
            str(account["id"]),
            account["full_name"],
            "",
            account["username"],
            account["date_created"],
        ]

        for col, value in enumerate(values):
            if col == 2:
                badge_cell = tk.Frame(row, bg=WHITE)
                badge_cell.grid(row=0, column=col, sticky="ew", padx=8, pady=8)
                create_status_badge(badge_cell, account["status"]).pack(anchor="w")
            else:
                tk.Label(
                    row,
                    text=value,
                    bg=WHITE,
                    fg=TEXT_DARK,
                    font=("Segoe UI", 11),
                    anchor="w",
                    padx=8,
                    pady=12,
                ).grid(row=0, column=col, sticky="ew")

        actions = tk.Frame(row, bg=WHITE)
        actions.grid(row=0, column=5, sticky="e", padx=8, pady=7)

        create_button(actions, "Edit", YELLOW, YELLOW_HOVER, lambda account_id=account["id"]: self.app.edit_account(account_id), width=5, fg=TEXT_DARK, font_size=10).pack(side="left", padx=3)

        if account["status"] == "Active":
            create_button(actions, "Deactivate", GRAY, GRAY_HOVER, lambda account_id=account["id"]: self.app.deactivate_account(account_id), width=10, font_size=10).pack(side="left", padx=3)
        else:
            create_button(actions, "Activate", GREEN, GREEN_HOVER, lambda account_id=account["id"]: self.app.activate_account(account_id), width=8, font_size=10).pack(side="left", padx=3)

        create_button(actions, "Delete", RED, RED_HOVER, lambda account_id=account["id"]: self.app.delete_account(account_id), width=6, font_size=10).pack(side="left", padx=3)

        tk.Frame(self.table, bg="#e5e7eb", height=1).grid(row=row_index + 1000, column=0, sticky="ew")


class EditStudentAccountPage(tk.Frame):
    def __init__(self, parent, app, account):
        super().__init__(parent, bg=BG)
        self.app = app
        self.account = account
        self.grid_columnconfigure(0, weight=1)
        self.build()

    def build(self):
        wrapper = tk.Frame(self, bg=BG)
        wrapper.grid(row=0, column=0, sticky="n", pady=(48, 0))

        tk.Label(
            wrapper,
            text="Edit Student Account",
            bg=BG,
            fg=TEXT_DARK,
            font=("Segoe UI", 28, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 18))

        outer, card = create_card(wrapper)
        outer.grid(row=1, column=0, sticky="ew")
        outer.configure(width=1040)
        outer.grid_propagate(False)

        card.configure(width=1038)
        card.grid_columnconfigure(0, weight=1)

        form = tk.Frame(card, bg=WHITE)
        form.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        form.grid_columnconfigure(0, weight=1)

        tk.Label(form, text="Username", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.username_entry = create_input(form)
        self.username_entry.insert(0, self.account["username"])
        self.username_entry.grid(row=1, column=0, sticky="ew", ipady=8, pady=(0, 16))

        tk.Label(form, text="New Password (Required)", bg=WHITE, fg=TEXT_DARK, font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=(0, 8))
        self.password_entry = create_input(form, show="*")
        self.password_entry.grid(row=3, column=0, sticky="ew", ipady=8, pady=(0, 16))

        create_button(form, "Save Changes", BLUE, BLUE_HOVER, self.save, font_size=11).grid(row=4, column=0, sticky="ew", ipady=3, pady=(0, 2))
        create_button(form, "Cancel", GRAY, GRAY_HOVER, self.app.show_student_accounts, font_size=11).grid(row=5, column=0, sticky="ew", ipady=3)

    def save(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:
            messagebox.showwarning("Missing Username", "Username is required.", parent=self.app)
            return

        self.app.save_account(self.account["id"], username, password)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
