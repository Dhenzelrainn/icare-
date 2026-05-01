import tkinter as tk
from tkinter import ttk


BG_MAIN = "#f4f6f9"
WHITE = "#ffffff"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6b7280"
BORDER = "#d1d5db"

BTN_BLUE = "#0d6efd"
BTN_CYAN = "#17c1dc"
BTN_GRAY = "#6c757d"
BTN_DARK = "#4b5563"
BTN_RED = "#dc3545"

STATUS_GREEN = "#198754"
STATUS_GRAY = "#6c757d"
STATUS_DARK = "#212529"


ACTIVE_STUDENTS = [
    {
        "id": "2",
        "name": "Dennielle Cruz",
        "first_name": "Dennielle",
        "last_name": "Cruz",
        "gender": "Male",
        "age": "19",
        "section": "B",
        "status": "Active",
        "enrolled": "2025",
        "graduated": "—",
    },
    {
        "id": "1",
        "name": "Dhenzel rain Cruz",
        "first_name": "Dhenzel rain",
        "last_name": "Cruz",
        "gender": "Male",
        "age": "19",
        "section": "A",
        "status": "Graduated",
        "enrolled": "2025",
        "graduated": "2025-11-02",
    },
]


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


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


def make_card(parent):
    return tk.Frame(
        parent,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER,
        bd=0
    )


def status_badge(parent, text):
    color = STATUS_GREEN

    if text == "Graduated":
        color = STATUS_GRAY
    elif text == "Archived":
        color = STATUS_DARK

    return tk.Label(
        parent,
        text=text,
        bg=color,
        fg="white",
        font=("Segoe UI", 8, "bold"),
        padx=12,
        pady=3
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


def table_header(parent, headers, weights, uniform_name):
    for index, weight in enumerate(weights):
        parent.grid_columnconfigure(
            index,
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


def year_controls(parent, first_button_text, first_button_command):
    make_button(
        parent,
        first_button_text,
        BTN_GRAY,
        command=first_button_command,
        padx=14,
        pady=7
    ).pack(side="left", padx=(0, 8))

    combo = ttk.Combobox(
        parent,
        values=["All years", "2023", "2024", "2025"],
        state="readonly",
        width=10,
        font=("Segoe UI", 9)
    )
    combo.set("All years")
    combo.pack(side="left", padx=(0, 8), ipady=4)

    make_button(
        parent,
        "Filter",
        BTN_GRAY,
        command=lambda: None,
        padx=12,
        pady=7
    ).pack(side="left")


class StudentsPage:
    headers = ["ID", "Name", "Section", "Status", "Enrolled", "Graduated", "Actions"]

    # Higher number = mas malapad na column
    column_weights = [1, 4, 2, 2, 2, 2, 3]

    def __init__(self, page_frame, archived_students):
        self.page_frame = page_frame
        self.archived_students = archived_students

    def show(self):
        clear_frame(self.page_frame)

        root = tk.Frame(self.page_frame, bg=BG_MAIN)
        root.grid(row=0, column=0, sticky="nsew")

        self.page_frame.columnconfigure(0, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        outer = tk.Frame(root, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=58, pady=(34, 0))

        header = tk.Frame(outer, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 22))

        tk.Label(
            header,
            text="Students",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 21, "bold")
        ).pack(side="left")

        controls = tk.Frame(header, bg=BG_MAIN)
        controls.pack(side="right")

        year_controls(
            controls,
            "Archived Students",
            lambda: ArchivedStudentsPage(self.page_frame, self.archived_students).show()
        )

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
        search.insert(0, "Search student...")
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
            "student_columns"
        )

        if not ACTIVE_STUDENTS:
            empty = tk.Frame(table, bg=WHITE, height=44)
            empty.grid(row=1, column=0, columnspan=7, sticky="ew")
            empty.grid_propagate(False)

            tk.Label(
                empty,
                text="No students found.",
                bg=WHITE,
                fg=TEXT_GRAY,
                font=("Segoe UI", 10)
            ).pack(expand=True)
            return

        for row, student in enumerate(ACTIVE_STUDENTS, start=1):
            table.grid_rowconfigure(row, weight=0)
            self.student_row(table, row, student)

    def student_row(self, table, row, student):
        bg = WHITE

        values = [
            student["id"],
            student["name"],
            student["section"],
            student["status"],
            student["enrolled"],
            student["graduated"],
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

            if col == 3:
                wrap = tk.Frame(cell, bg=bg)
                wrap.pack(anchor="w", padx=10, pady=9)
                status_badge(wrap, student["status"]).pack()

            elif col == 6:
                actions = tk.Frame(cell, bg=bg)
                actions.pack(anchor="w", padx=8, pady=5)

                action_button(
                    actions,
                    "View",
                    BTN_CYAN,
                    command=lambda s=student: StudentDetailsPage(
                        self.page_frame,
                        self.archived_students,
                        s,
                        previous_page="students"
                    ).show(),
                    width=8
                ).pack(side="left", padx=(0, 6))

                action_button(
                    actions,
                    "Archive",
                    BTN_DARK,
                    command=lambda s=student: self.archive_student(s),
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

    def archive_student(self, student):
        if student in ACTIVE_STUDENTS:
            ACTIVE_STUDENTS.remove(student)

            archived_copy = dict(student)
            archived_copy["status"] = "Archived"

            if archived_copy not in self.archived_students:
                self.archived_students.append(archived_copy)

            self.show()


class ArchivedStudentsPage:
    headers = ["ID", "Name", "Section", "Status", "Enrolled", "Graduated", "Actions"]

    # Same responsive sizing para consistent sa active students table
    column_weights = [1, 4, 2, 2, 2, 2, 3]

    def __init__(self, page_frame, archived_students):
        self.page_frame = page_frame
        self.archived_students = archived_students

        if not self.archived_students:
            self.archived_students.append({
                "id": "1",
                "name": "Dhenzel rain Cruz",
                "first_name": "Dhenzel rain",
                "last_name": "Cruz",
                "gender": "Male",
                "age": "19",
                "section": "A",
                "status": "Archived",
                "enrolled": "2025",
                "graduated": "2025-11-02",
            })

    def show(self):
        clear_frame(self.page_frame)

        root = tk.Frame(self.page_frame, bg=BG_MAIN)
        root.grid(row=0, column=0, sticky="nsew")

        self.page_frame.columnconfigure(0, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        outer = tk.Frame(root, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=58, pady=(34, 0))

        header = tk.Frame(outer, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 22))

        tk.Label(
            header,
            text="Archived Students",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 21, "bold")
        ).pack(side="left")

        controls = tk.Frame(header, bg=BG_MAIN)
        controls.pack(side="right")

        year_controls(
            controls,
            "Back to Students",
            lambda: StudentsPage(self.page_frame, self.archived_students).show()
        )

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
        search.insert(0, "Search archived student...")
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
            "archived_student_columns"
        )

        if not self.archived_students:
            empty = tk.Frame(table, bg=WHITE, height=44)
            empty.grid(row=1, column=0, columnspan=7, sticky="ew")
            empty.grid_propagate(False)

            tk.Label(
                empty,
                text="No archived students.",
                bg=WHITE,
                fg=TEXT_GRAY,
                font=("Segoe UI", 10)
            ).pack(expand=True)
            return

        for row, student in enumerate(self.archived_students, start=1):
            table.grid_rowconfigure(row, weight=0)
            self.archived_row(table, row, student)

    def archived_row(self, table, row, student):
        bg = WHITE

        values = [
            student["id"],
            student["name"],
            student["section"],
            student["status"],
            student["enrolled"],
            student["graduated"],
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

            if col == 3:
                wrap = tk.Frame(cell, bg=bg)
                wrap.pack(anchor="w", padx=10, pady=9)
                status_badge(wrap, "Archived").pack()

            elif col == 6:
                actions = tk.Frame(cell, bg=bg)
                actions.pack(anchor="w", padx=8, pady=5)

                action_button(
                    actions,
                    "View",
                    BTN_CYAN,
                    command=lambda s=student: StudentDetailsPage(
                        self.page_frame,
                        self.archived_students,
                        s,
                        previous_page="archived_students"
                    ).show(),
                    width=8
                ).pack(side="left", padx=(0, 6))

                action_button(
                    actions,
                    "Delete",
                    BTN_RED,
                    command=lambda s=student: self.delete_student(s),
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

    def delete_student(self, student):
        if student in self.archived_students:
            self.archived_students.remove(student)
            self.show()


class StudentDetailsPage:
    def __init__(self, page_frame, archived_students, student, previous_page="students"):
        self.page_frame = page_frame
        self.archived_students = archived_students
        self.student = student
        self.previous_page = previous_page

    def show(self):
        clear_frame(self.page_frame)

        root = tk.Frame(self.page_frame, bg=BG_MAIN)
        root.grid(row=0, column=0, sticky="nsew")

        self.page_frame.columnconfigure(0, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        outer = tk.Frame(root, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=150, pady=(58, 0))

        header = tk.Frame(outer, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 24))

        tk.Label(
            header,
            text="Student Details",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 24, "bold")
        ).pack(side="left")

        make_button(
            header,
            "Back to Students",
            BTN_GRAY,
            command=self.go_back,
            padx=18,
            pady=9
        ).pack(side="right")

        card = tk.Frame(
            outer,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#e5e7eb",
            bd=0
        )
        card.pack(fill="x")

        content = tk.Frame(card, bg=WHITE)
        content.pack(fill="x", padx=20, pady=22)

        tk.Label(
            content,
            text="Basic Information",
            bg=WHITE,
            fg=BTN_BLUE,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        tk.Frame(content, bg="#e5e7eb", height=1).pack(fill="x", pady=(8, 24))

        body = tk.Frame(content, bg=WHITE)
        body.pack(fill="x")

        image_area = tk.Frame(body, bg=WHITE, width=260, height=150)
        image_area.pack(side="left", padx=(70, 70))
        image_area.pack_propagate(False)

        tk.Label(
            image_area,
            text="Profile Image",
            bg=WHITE,
            fg=TEXT_DARK,
            font=("Segoe UI", 11)
        ).pack(expand=True)

        details = tk.Frame(body, bg=WHITE)
        details.pack(side="left", fill="x", expand=True)

        for c in range(3):
            details.grid_columnconfigure(c, weight=1, uniform="detail")

        fields = [
            ("First Name", self.student["first_name"]),
            ("Last Name", self.student["last_name"]),
            ("Gender", self.student["gender"]),
            ("Age", self.student["age"]),
            ("Section", self.student["section"]),
            ("Status", self.student["status"]),
        ]

        for index, (label, value) in enumerate(fields):
            r = index // 3
            c = index % 3

            box = tk.Frame(details, bg=WHITE)
            box.grid(row=r, column=c, sticky="w", pady=(0, 28))

            tk.Label(
                box,
                text=label,
                bg=WHITE,
                fg=TEXT_DARK,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w")

            if label == "Status":
                status_badge(box, value).pack(anchor="w", pady=(8, 0))
            else:
                tk.Label(
                    box,
                    text=value,
                    bg=WHITE,
                    fg=TEXT_DARK,
                    font=("Segoe UI", 10)
                ).pack(anchor="w", pady=(8, 0))

    def go_back(self):
        if self.previous_page == "archived_students":
            ArchivedStudentsPage(self.page_frame, self.archived_students).show()
        else:
            StudentsPage(self.page_frame, self.archived_students).show()