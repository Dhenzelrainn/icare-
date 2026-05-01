import tkinter as tk


BG_MAIN = "#f4f6f9"
WHITE = "#ffffff"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6b7280"
BORDER = "#d1d5db"

BTN_BLUE = "#0d6efd"
BTN_CYAN = "#17c1dc"
BTN_GRAY = "#6c757d"
BTN_GREEN = "#198754"
BTN_RED = "#dc3545"
STATUS_GREEN = "#15965b"


TEACHERS = [
    {
        "id": "5",
        "name": "Shaeena Rosales Cordova",
        "username": "teacher1",
        "email": "shaeenarosales08@gmail.com",
        "mobile": "09969119641",
        "status": "Active",
        "registered": "",
        "first_name": "Shaeena",
        "middle_name": "Rosales",
        "surname": "Cordova",
        "birthday": "2006-05-08",
        "age": "19",
        "gender": "Female",
        "barangay": "Bulilan Sur",
        "street": "Street 2 House 2",
    },
    {
        "id": "1",
        "name": "Rose Ann Mae Bravo Flores",
        "username": "Rose",
        "email": "rose@gmail.com",
        "mobile": "01829123273",
        "status": "Active",
        "registered": "2025-10-29",
        "first_name": "Rose Ann Mae",
        "middle_name": "Bravo",
        "surname": "Flores",
        "birthday": "2005-10-29",
        "age": "20",
        "gender": "Female",
        "barangay": "—",
        "street": "—",
    },
]


ARCHIVED_TEACHERS = [
    {
        "id": "5",
        "name": "Shaeena Rosales Cordova",
        "username": "teacher1",
        "email": "shaeenarosales08@gmail.com",
        "mobile": "09969119641",
        "status": "Active",
        "registered": "",
        "first_name": "Shaeena",
        "middle_name": "Rosales",
        "surname": "Cordova",
        "birthday": "2006-05-08",
        "age": "19",
        "gender": "Female",
        "barangay": "Bulilan Sur",
        "street": "Street 2 House 2",
    }
]


def make_button(parent, text, bg, command=None, fg="white", width=None, padx=14, pady=7):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        font=("Segoe UI", 9, "bold"),
        padx=padx,
        pady=pady,
        width=width
    )


def action_button(parent, text, color, command=None, width=8):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        width=width,
        height=2,
        cursor="hand2",
        font=("Segoe UI", 8, "bold")
    )


def status_badge(parent, text="Active"):
    return tk.Label(
        parent,
        text=text,
        bg=STATUS_GREEN,
        fg="white",
        font=("Segoe UI", 8, "bold"),
        padx=12,
        pady=3
    )


def make_card(parent):
    return tk.Frame(
        parent,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER,
        bd=0
    )


def table_header(parent, headers, weights, uniform_name):
    for i, weight in enumerate(weights):
        parent.grid_columnconfigure(
            i,
            weight=weight,
            uniform=uniform_name
        )

    for col, title in enumerate(headers):
        tk.Label(
            parent,
            text=title,
            bg=WHITE,
            fg=TEXT_DARK,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=col, sticky="ew", padx=(10, 6), pady=(0, 10))


class TeachersPage(tk.Frame):
    headers = ["ID", "Name", "Username", "Email", "Mobile", "Status", "Registered", "Actions"]

    # Higher number = wider column
    column_weights = [1, 4, 2, 4, 2, 2, 2, 3]

    def __init__(self, parent, navigate):
        super().__init__(parent, bg=BG_MAIN)
        self.navigate = navigate
        self.build()

    def build(self):
        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=58, pady=(34, 0))

        header = tk.Frame(outer, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 58))

        tk.Label(
            header,
            text="Teachers",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 21, "bold")
        ).pack(side="left")

        make_button(
            header,
            "Archived Teachers",
            BTN_GRAY,
            command=lambda: self.navigate("archived_teachers"),
            padx=18,
            pady=9
        ).pack(side="right")

        card = make_card(outer)
        card.pack(fill="x")

        search = tk.Entry(
            card,
            font=("Segoe UI", 10),
            fg=TEXT_GRAY,
            bg=WHITE,
            relief="solid",
            bd=1
        )
        search.insert(0, "Search teacher...")
        search.pack(fill="x", padx=14, pady=(14, 20), ipady=8)

        table_wrapper = tk.Frame(card, bg=WHITE)
        table_wrapper.pack(fill="x", padx=14, pady=(0, 18))
        table_wrapper.grid_columnconfigure(0, weight=1)

        table = tk.Frame(table_wrapper, bg=WHITE)
        table.grid(row=0, column=0, sticky="ew")

        table_header(
            table,
            self.headers,
            self.column_weights,
            "teacher_columns"
        )

        for row, teacher in enumerate(TEACHERS, start=1):
            table.grid_rowconfigure(row, weight=0)
            self.table_row(table, row, teacher, selected=(row == 1))

    def table_row(self, table, row, teacher, selected=False):
        bg = "#eeeeee" if selected else WHITE

        values = [
            teacher["id"],
            teacher["name"],
            teacher["username"],
            teacher["email"],
            teacher["mobile"],
            teacher["status"],
            teacher["registered"],
        ]

        for col in range(8):
            cell = tk.Frame(
                table,
                bg=bg,
                height=44,
                bd=0,
                highlightthickness=0
            )
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)

            if col == 5:
                wrap = tk.Frame(cell, bg=bg)
                wrap.pack(anchor="w", padx=10, pady=9)
                status_badge(wrap, teacher["status"]).pack()

            elif col == 7:
                actions = tk.Frame(cell, bg=bg)
                actions.pack(anchor="w", padx=8, pady=5)

                action_button(
                    actions,
                    "View",
                    BTN_CYAN,
                    command=lambda t=teacher: self.navigate(
                        "teacher_info",
                        teacher=t,
                        previous="teachers"
                    ),
                    width=8
                ).pack(side="left", padx=(0, 6))

                action_button(
                    actions,
                    "Archive",
                    BTN_GRAY,
                    command=lambda: None,
                    width=8
                ).pack(side="left")

            else:
                tk.Label(
                    cell,
                    text=values[col],
                    bg=bg,
                    fg=TEXT_DARK,
                    font=("Segoe UI", 10),
                    anchor="w"
                ).pack(fill="both", expand=True, padx=10)


class ArchivedTeachersPage(tk.Frame):
    headers = ["ID", "Name", "Username", "Email", "Mobile", "Date Created", "Actions"]

    # Higher number = wider column
    column_weights = [1, 4, 2, 4, 2, 2, 3]

    def __init__(self, parent, navigate):
        super().__init__(parent, bg=BG_MAIN)
        self.navigate = navigate
        self.build()

    def build(self):
        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=58, pady=(34, 0))

        header = tk.Frame(outer, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 52))

        tk.Label(
            header,
            text="Archived Teachers",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 21, "bold")
        ).pack(side="left")

        make_button(
            header,
            "Back to Teachers",
            BTN_BLUE,
            command=lambda: self.navigate("teachers"),
            padx=18,
            pady=9
        ).pack(side="right")

        card = make_card(outer)
        card.pack(fill="x")

        table_wrapper = tk.Frame(card, bg=WHITE)
        table_wrapper.pack(fill="x", padx=14, pady=20)
        table_wrapper.grid_columnconfigure(0, weight=1)

        table = tk.Frame(table_wrapper, bg=WHITE)
        table.grid(row=0, column=0, sticky="ew")

        table_header(
            table,
            self.headers,
            self.column_weights,
            "archived_teacher_columns"
        )

        if not ARCHIVED_TEACHERS:
            empty = tk.Frame(table, bg="#eeeeee", height=44)
            empty.grid(row=1, column=0, columnspan=7, sticky="ew")
            empty.grid_propagate(False)

            tk.Label(
                empty,
                text="No archived teachers.",
                bg="#eeeeee",
                fg=TEXT_DARK,
                font=("Segoe UI", 10)
            ).pack(expand=True)
            return

        for row, teacher in enumerate(ARCHIVED_TEACHERS, start=1):
            table.grid_rowconfigure(row, weight=0)
            self.table_row(table, row, teacher)

    def table_row(self, table, row, teacher):
        bg = "#eeeeee"

        values = [
            teacher["id"],
            teacher["name"],
            teacher["username"],
            teacher["email"],
            teacher["mobile"],
            teacher["registered"],
        ]

        for col in range(7):
            cell = tk.Frame(
                table,
                bg=bg,
                height=44,
                bd=0,
                highlightthickness=0
            )
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)

            if col == 6:
                actions = tk.Frame(cell, bg=bg)
                actions.pack(anchor="w", padx=8, pady=5)

                action_button(
                    actions,
                    "View",
                    BTN_CYAN,
                    command=lambda t=teacher: self.navigate(
                        "teacher_info",
                        teacher=t,
                        previous="archived_teachers"
                    ),
                    width=6
                ).pack(side="left", padx=(0, 6))

                action_button(
                    actions,
                    "Restore",
                    BTN_GREEN,
                    width=8
                ).pack(side="left", padx=(0, 6))

                action_button(
                    actions,
                    "Delete",
                    BTN_RED,
                    width=7
                ).pack(side="left")

            else:
                tk.Label(
                    cell,
                    text=values[col],
                    bg=bg,
                    fg=TEXT_DARK,
                    font=("Segoe UI", 10),
                    anchor="w"
                ).pack(fill="both", expand=True, padx=10)


class TeacherInformationPage(tk.Frame):
    def __init__(self, parent, navigate, teacher, previous_page):
        super().__init__(parent, bg=BG_MAIN)
        self.navigate = navigate
        self.teacher = teacher
        self.previous_page = previous_page
        self.build()

    def build(self):
        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=58, pady=(34, 0))

        header = tk.Frame(outer, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 18))

        tk.Label(
            header,
            text="Teacher Information",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 22, "bold")
        ).pack(side="left", expand=True)

        make_button(
            header,
            "Back",
            BTN_BLUE,
            command=lambda: self.navigate(self.previous_page),
            width=8,
            padx=12,
            pady=9
        ).pack(side="right")

        shadow = tk.Frame(outer, bg="#e5e7eb")
        shadow.pack(anchor="center")

        card = tk.Frame(
            shadow,
            bg=WHITE,
            width=820,
            height=560,
            bd=0
        )
        card.pack(padx=(0, 2), pady=(0, 2))
        card.pack_propagate(False)

        profile = tk.Canvas(
            card,
            width=110,
            height=110,
            bg=WHITE,
            highlightthickness=0
        )
        profile.pack(anchor="center", pady=(30, 2))

        profile.create_oval(
            14,
            14,
            100,
            100,
            fill="#fefefe",
            outline="#e5e7eb",
            width=1
        )

        profile.create_oval(
            18,
            18,
            104,
            104,
            outline="#f3f4f6",
            width=3
        )

        tk.Label(
            card,
            text=self.teacher["name"],
            bg=WHITE,
            fg=TEXT_DARK,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="center")

        tk.Label(
            card,
            text="Teacher Account",
            bg=WHITE,
            fg=TEXT_GRAY,
            font=("Segoe UI", 9)
        ).pack(anchor="center", pady=(0, 20))

        content = tk.Frame(card, bg=WHITE)
        content.pack(fill="x", padx=36)

        self.section_heading(content, "Personal Details", 0)

        self.detail_grid(
            content,
            1,
            [
                ("First Name", self.teacher["first_name"]),
                ("Middle Name", self.teacher["middle_name"]),
                ("Surname", self.teacher["surname"]),
                ("Birthday", self.teacher["birthday"]),
                ("Age", self.teacher["age"]),
                ("Gender", self.teacher["gender"]),
            ],
            columns=3
        )

        self.section_heading(content, "Contact Details", 3)

        self.detail_grid(
            content,
            4,
            [
                ("Email", self.teacher["email"]),
                ("Username", self.teacher["username"]),
                ("Mobile Number", self.teacher["mobile"]),
            ],
            columns=3
        )

        self.section_heading(content, "Address", 6)

        self.detail_grid(
            content,
            7,
            [
                ("Barangay", self.teacher["barangay"]),
                ("Street", self.teacher["street"]),
            ],
            columns=3
        )

    def section_heading(self, parent, title, row):
        wrap = tk.Frame(parent, bg=WHITE)
        wrap.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0 if row == 0 else 16, 8)
        )

        tk.Frame(
            wrap,
            bg=BTN_BLUE,
            width=4,
            height=23
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            wrap,
            text=title,
            bg=WHITE,
            fg=TEXT_DARK,
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

    def detail_grid(self, parent, start_row, items, columns=3):
        for c in range(columns):
            parent.grid_columnconfigure(c, weight=1, uniform="detail")

        for index, (label, value) in enumerate(items):
            r = start_row + (index // columns)
            c = index % columns

            box = tk.Frame(parent, bg=WHITE)
            box.grid(
                row=r,
                column=c,
                sticky="w",
                padx=(0, 20),
                pady=(0, 18)
            )

            tk.Label(
                box,
                text=label,
                bg=WHITE,
                fg=TEXT_DARK,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")

            tk.Label(
                box,
                text=value,
                bg=WHITE,
                fg=TEXT_DARK,
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(2, 0))