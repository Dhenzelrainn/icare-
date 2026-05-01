import tkinter as tk

INITIAL_ADMINS = [
    {
        "id": "7",
        "username": "admin1",
        "name": "Christian Joseph Aquino",
        "status": "Active",
        "created": "",
        "first_name": "Christian Joseph",
        "middle_name": "Perez",
        "surname": "Aquino",
        "birth_date": "—",
        "age": "—",
        "gender": "—",
        "mobile": "—",
        "email": "christianjosephpaquino@gmail.com",
        "barangay": "—",
        "street": "—",
    },
    {
        "id": "2",
        "username": "dennielle",
        "name": "Dennielle Cruz",
        "status": "Active",
        "created": "2025-10-29",
        "first_name": "Dennielle",
        "middle_name": "—",
        "surname": "Cruz",
        "birth_date": "—",
        "age": "—",
        "gender": "—",
        "mobile": "—",
        "email": "—",
        "barangay": "—",
        "street": "—",
    },
]


class AdminPage(tk.Frame):
    def __init__(self, parent, navigate, admins=None, archived_admins=None):
        super().__init__(parent, bg="#f4f6fb")
        self.navigate = navigate
        self.admins = admins if admins is not None else [dict(a) for a in INITIAL_ADMINS]
        self.archived_admins = archived_admins if archived_admins is not None else []
        self.build()

    def build(self):
        header = tk.Frame(self, bg="#f4f6fb")
        header.pack(fill="x", padx=34, pady=(30, 18))

        tk.Label(
            header,
            text="Admin Accounts",
            bg="#f4f6fb",
            fg="#111827",
            font=("Segoe UI", 23, "bold")
        ).pack(side="left")

        tk.Button(
            header,
            text="Archived Admins",
            command=lambda: self.navigate("archived"),
            bg="#6c757d",
            fg="white",
            activebackground="#6c757d",
            activeforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            width=16,
            height=2,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(side="right")

        card = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d1d5db",
            highlightthickness=1,
            bd=0
        )
        card.pack(fill="both", expand=True, padx=34, pady=(0, 30))

        search = tk.Entry(
            card,
            font=("Segoe UI", 10),
            fg="#6b7280",
            bg="white",
            relief="solid",
            bd=1
        )
        search.insert(0, "Search admin...")
        search.pack(fill="x", padx=18, pady=(20, 14), ipady=9)

        table_wrapper = tk.Frame(card, bg="white")
        table_wrapper.pack(fill="x", expand=False, padx=18, pady=(0, 12))
        table_wrapper.grid_columnconfigure(0, weight=1)

        self.table = tk.Frame(table_wrapper, bg="white")
        self.table.grid(row=0, column=0, sticky="ew")

        self.render_table()

    def render_table(self):
        for w in self.table.winfo_children():
            w.destroy()

        headers = ["ID", "Username", "Name", "Status", "Created", "Actions"]

        col_config = [
            {"weight": 1},
            {"weight": 2},
            {"weight": 4},
            {"weight": 2},
            {"weight": 2},
            {"weight": 4},
        ]

        for i, cfg in enumerate(col_config):
            self.table.grid_columnconfigure(
                i,
                weight=cfg["weight"],
                uniform="admin_columns"
            )

        for col, text in enumerate(headers):
            tk.Label(
                self.table,
                text=text,
                bg="white",
                fg="#111827",
                font=("Segoe UI", 9, "bold"),
                anchor="w"
            ).grid(row=0, column=col, sticky="ew", padx=(8, 4), pady=(0, 8))

        if not self.admins:
            empty = tk.Frame(self.table, bg="#f3f4f6", height=42)
            empty.grid(row=1, column=0, columnspan=6, sticky="ew")
            empty.grid_propagate(False)

            tk.Label(
                empty,
                text="No admin accounts.",
                bg="#f3f4f6",
                fg="#6b7280",
                font=("Segoe UI", 10)
            ).pack(expand=True)
            return

        for idx, admin in enumerate(self.admins, start=1):
            self.table.grid_rowconfigure(idx, weight=0)
            self.build_row(idx, admin, selected=(idx == 1))

    def build_row(self, row, admin, selected=False):
        bg = "#f1f3f5" if selected else "white"

        values = [
            admin["id"],
            admin["username"],
            admin["name"],
            admin["status"],
            admin["created"]
        ]

        for col in range(6):
            cell = tk.Frame(
                self.table,
                bg=bg,
                height=44,
                bd=0,
                highlightthickness=0
            )
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)

            if col == 3:
                badge_wrap = tk.Frame(cell, bg=bg)
                badge_wrap.pack(anchor="w", padx=8, pady=8)

                tk.Label(
                    badge_wrap,
                    text=admin["status"],
                    bg="#16a34a",
                    fg="white",
                    font=("Segoe UI", 8, "bold"),
                    padx=12,
                    pady=4,
                    bd=0
                ).pack()

            elif col == 5:
                actions = tk.Frame(cell, bg=bg, bd=0, highlightthickness=0)
                actions.pack(anchor="w", padx=6, pady=5)

                self.action_btn(
                    actions,
                    "View",
                    "#0dcaf0",
                    width=7,
                    command=lambda a=admin: self.navigate("admin_info", admin=a, previous="admins")
                ).pack(side="left", padx=(0, 4))

                self.action_btn(
                    actions,
                    "Edit",
                    "#ffc107",
                    width=7,
                    fg="#111827"
                ).pack(side="left", padx=(0, 4))

                self.action_btn(
                    actions,
                    "Archive",
                    "#6c757d",
                    width=8,
                    command=lambda a=admin: self.archive_admin(a)
                ).pack(side="left", padx=(0, 4))

                self.action_btn(
                    actions,
                    "Reset PW",
                    "#0d6efd",
                    width=9
                ).pack(side="left")

            else:
                tk.Label(
                    cell,
                    text=values[col],
                    bg=bg,
                    fg="#111827",
                    font=("Segoe UI", 9),
                    anchor="w",
                    bd=0
                ).pack(fill="both", expand=True, padx=8)

    def action_btn(self, parent, text, color, width, fg="white", command=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=color,
            activeforeground=fg,
            relief="flat",
            bd=0,
            highlightthickness=0,
            width=width,
            height=2,
            cursor="hand2",
            font=("Segoe UI", 8, "bold")
        )

    def archive_admin(self, admin):
        if admin in self.admins:
            self.admins.remove(admin)
            self.archived_admins.append(admin)
            self.render_table()


class ArchivedPage(tk.Frame):
    def __init__(self, parent, navigate, archived_admins=None, admins=None):
        super().__init__(parent, bg="#f4f6fb")
        self.navigate = navigate
        self.archived_admins = archived_admins if archived_admins is not None else []
        self.admins = admins if admins is not None else []
        self.build()

    def build(self):
        header = tk.Frame(self, bg="#f4f6fb")
        header.pack(fill="x", padx=34, pady=(30, 18))

        tk.Label(
            header,
            text="Archived Admin Accounts",
            bg="#f4f6fb",
            fg="#111827",
            font=("Segoe UI", 22, "bold")
        ).pack(side="left")

        tk.Button(
            header,
            text="Back to Admin Accounts",
            command=lambda: self.navigate("admins"),
            bg="#0d6efd",
            fg="white",
            activebackground="#0d6efd",
            activeforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=16,
            height=2,
            cursor="hand2",
            font=("Segoe UI", 9)
        ).pack(side="right")

        card = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d1d5db",
            highlightthickness=1,
            bd=0
        )
        card.pack(fill="both", expand=True, padx=34, pady=(0, 30))

        table_wrapper = tk.Frame(card, bg="white")
        table_wrapper.pack(fill="x", expand=False, padx=18, pady=18)
        table_wrapper.grid_columnconfigure(0, weight=1)

        self.archived_table = tk.Frame(table_wrapper, bg="white")
        self.archived_table.grid(row=0, column=0, sticky="ew")

        self.render_table()

    def render_table(self):
        for w in self.archived_table.winfo_children():
            w.destroy()

        headers = ["ID", "Username", "Name", "Date Created", "Actions"]

        col_config = [
            {"weight": 1},
            {"weight": 2},
            {"weight": 4},
            {"weight": 2},
            {"weight": 3},
        ]

        for i, cfg in enumerate(col_config):
            self.archived_table.grid_columnconfigure(
                i,
                weight=cfg["weight"],
                uniform="archived_columns"
            )

        for col, text in enumerate(headers):
            tk.Label(
                self.archived_table,
                text=text,
                bg="white",
                fg="#111827",
                font=("Segoe UI", 10, "bold"),
                anchor="w"
            ).grid(row=0, column=col, sticky="ew", padx=(8, 4), pady=(0, 10))

        if not self.archived_admins:
            msg = tk.Frame(
                self.archived_table,
                bg="#eeeeee",
                height=42,
                bd=0,
                highlightthickness=0
            )
            msg.grid(row=1, column=0, columnspan=5, sticky="ew")
            msg.grid_propagate(False)

            tk.Label(
                msg,
                text="No archived admins.",
                bg="#eeeeee",
                fg="#111827",
                font=("Segoe UI", 10)
            ).pack(expand=True)
            return

        for row_index, admin in enumerate(self.archived_admins, start=1):
            self.archived_table.grid_rowconfigure(row_index, weight=0)
            self.build_archived_row(row_index, admin)

    def build_archived_row(self, row, admin):
        bg = "#eeeeee"

        values = [
            admin["id"],
            admin["username"],
            admin["name"],
            admin["created"]
        ]

        for col in range(5):
            cell = tk.Frame(
                self.archived_table,
                bg=bg,
                height=42,
                bd=0,
                highlightthickness=0
            )
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)

            if col == 4:
                actions = tk.Frame(cell, bg=bg, bd=0, highlightthickness=0)
                actions.pack(anchor="w", padx=8, pady=5)

                self.action_btn(
                    actions,
                    "View",
                    "#0dcaf0",
                    width=7,
                    command=lambda a=admin: self.navigate("admin_info", admin=a, previous="archived")
                ).pack(side="left", padx=(0, 4))

                self.action_btn(
                    actions,
                    "Restore",
                    "#16a34a",
                    width=8,
                    command=lambda a=admin: self.restore_admin(a)
                ).pack(side="left", padx=(0, 4))

                self.action_btn(
                    actions,
                    "Delete",
                    "#dc3545",
                    width=7,
                    command=lambda a=admin: self.delete_admin(a)
                ).pack(side="left")

            else:
                tk.Label(
                    cell,
                    text=values[col],
                    bg=bg,
                    fg="#111827",
                    font=("Segoe UI", 10),
                    anchor="w",
                    bd=0
                ).pack(fill="both", expand=True, padx=8)

    def action_btn(self, parent, text, color, width, fg="white", command=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=color,
            activeforeground=fg,
            relief="flat",
            bd=0,
            highlightthickness=0,
            width=width,
            height=2,
            cursor="hand2",
            font=("Segoe UI", 8, "bold")
        )

    def restore_admin(self, admin):
        if admin in self.archived_admins:
            self.archived_admins.remove(admin)
            self.admins.append(admin)
            self.render_table()

    def delete_admin(self, admin):
        if admin in self.archived_admins:
            self.archived_admins.remove(admin)
            self.render_table()


class AdminInformationPage(tk.Frame):
    def __init__(self, parent, navigate, admin, previous_page="admins"):
        super().__init__(parent, bg="#f4f6fb")
        self.navigate = navigate
        self.admin = admin
        self.previous_page = previous_page
        self.build()

    def get_value(self, key, default="—"):
        value = self.admin.get(key, default)

        if value is None or value == "":
            return default

        return value

    def split_name(self):
        full_name = self.get_value("name", "")
        parts = full_name.split()

        first_name = self.admin.get("first_name", "")
        middle_name = self.admin.get("middle_name", "")
        surname = self.admin.get("surname", "")

        if not first_name:
            first_name = parts[0] if len(parts) >= 1 else "—"

        if not surname:
            surname = parts[-1] if len(parts) >= 2 else "—"

        if not middle_name:
            middle_name = " ".join(parts[1:-1]) if len(parts) > 2 else "—"

        return first_name or "—", middle_name or "—", surname or "—"

    def build(self):
        outer = tk.Frame(self, bg="#f4f6fb")
        outer.pack(fill="both", expand=True, padx=58, pady=(30, 0))

        header = tk.Frame(outer, bg="#f4f6fb")
        header.pack(fill="x", pady=(0, 22))

        tk.Label(
            header,
            text="Admin Information",
            bg="#f4f6fb",
            fg="#111827",
            font=("Segoe UI", 22, "bold")
        ).pack(side="left", expand=True, anchor="center")

        tk.Button(
            header,
            text="Back",
            command=lambda: self.navigate(self.previous_page),
            bg="#0d6efd",
            fg="white",
            activebackground="#0d6efd",
            activeforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            width=10,
            height=2,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

        shadow = tk.Frame(outer, bg="#e5e7eb")
        shadow.pack(anchor="center")

        card = tk.Frame(
            shadow,
            bg="white",
            width=780,
            height=560,
            bd=0
        )
        card.pack(padx=(0, 2), pady=(0, 2))
        card.pack_propagate(False)

        profile = tk.Canvas(
            card,
            width=120,
            height=120,
            bg="white",
            highlightthickness=0
        )
        profile.pack(anchor="center", pady=(28, 4))

        profile.create_oval(
            18,
            18,
            105,
            105,
            fill="#ffffff",
            outline="#e5e7eb",
            width=2
        )

        profile.create_oval(
            22,
            22,
            109,
            109,
            outline="#f3f4f6",
            width=3
        )

        tk.Label(
            card,
            text=self.get_value("name"),
            bg="white",
            fg="#111827",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="center")

        tk.Label(
            card,
            text="Admin Account",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 9)
        ).pack(anchor="center", pady=(0, 22))

        content = tk.Frame(card, bg="white")
        content.pack(fill="x", padx=44)

        first_name, middle_name, surname = self.split_name()

        self.section_heading(content, "Personal Details", 0)

        self.detail_grid(
            content,
            1,
            [
                ("First Name", first_name),
                ("Middle Name", middle_name),
                ("Surname", surname),
                ("Birth Date", self.get_value("birth_date")),
                ("Age", self.get_value("age")),
                ("Gender", self.get_value("gender")),
            ],
            columns=3
        )

        self.section_heading(content, "Contact Details", 3)

        self.detail_grid(
            content,
            4,
            [
                ("Mobile Number", self.get_value("mobile")),
                ("Email", self.get_value("email")),
            ],
            columns=3
        )

        self.section_heading(content, "Address", 6)

        self.detail_grid(
            content,
            7,
            [
                ("Barangay", self.get_value("barangay")),
                ("Street", self.get_value("street")),
            ],
            columns=3
        )

    def section_heading(self, parent, title, row):
        wrap = tk.Frame(parent, bg="white")
        wrap.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0 if row == 0 else 16, 10)
        )

        tk.Frame(
            wrap,
            bg="#0d6efd",
            width=4,
            height=24
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            wrap,
            text=title,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

    def detail_grid(self, parent, start_row, items, columns=3):
        for c in range(columns):
            parent.grid_columnconfigure(c, weight=1, uniform="admin_detail")

        for index, (label, value) in enumerate(items):
            r = start_row + (index // columns)
            c = index % columns

            box = tk.Frame(parent, bg="white")
            box.grid(
                row=r,
                column=c,
                sticky="w",
                padx=(0, 28),
                pady=(0, 16)
            )

            tk.Label(
                box,
                text=label,
                bg="white",
                fg="#111827",
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")

            tk.Label(
                box,
                text=value,
                bg="white",
                fg="#111827",
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(3, 0))