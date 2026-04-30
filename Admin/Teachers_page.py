import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ─────────────────────────────────────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────────────────────────────────────
SIDEBAR_BG = "#0f4f9c"
SIDEBAR_BG_2 = "#1d4fb8"
SIDEBAR_ACTIVE = "#0d6efd"
SIDEBAR_HOVER = "#2563eb"
SIDEBAR_TEXT = "#ffffff"
SIDEBAR_MUTED = "#cfe3ff"
YELLOW = "#facc15"

BG = "#f4f6f9"
WHITE = "#ffffff"
CARD_BORDER = "#d0d7e3"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6b7280"

BLUE = "#0d6efd"
BLUE_H = "#0b5ed7"
CYAN = "#00b4d8"
CYAN_H = "#0096b7"
ORANGE = "#f59e0b"
ORANGE_H = "#d97706"
GRAY = "#6b7280"
GRAY_H = "#4b5563"
GREEN = "#198754"
GREEN_H = "#157347"
RED = "#dc3545"
RED_H = "#bb2d3b"


# ─────────────────────────────────────────────────────────────────────────────
# Mock data
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_TEACHERS = [
    {
        "id": 5,
        "first_name": "Shaeena",
        "middle_name": "Rosales",
        "last_name": "Cordova",
        "position": "Teacher",
        "status": "Active",
        "age": "19",
        "birthday": "05/08/2006",
        "birthday_long": "May 08, 2006",
        "gender": "Female",
        "mobile": "09969119641",
        "email": "shaeenarosales08@gmail.com",
        "username": "teacher1",
        "password": "teacher123",
        "barangay": "Bulilan Sur",
        "street": "Street 2 House 2",
    }
]

DEFAULT_ARCHIVED = [
    {
        "id": 1,
        "first_name": "Rose Ann Mae",
        "middle_name": "",
        "last_name": "Flores",
        "position": "Teacher",
        "status": "Archived",
        "age": "",
        "birthday": "",
        "birthday_long": "",
        "gender": "",
        "mobile": "",
        "email": "",
        "username": "",
        "password": "",
        "barangay": "",
        "street": "",
    }
]


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────
def teacher_full_name(t):
    parts = [t.get("first_name", ""), t.get("middle_name", ""), t.get("last_name", "")]
    return " ".join(p for p in parts if p).strip()


def teacher_display_name(t):
    return f"{t.get('first_name', '')} {t.get('last_name', '')}".strip()


def make_button(parent, text, color, hover, command, width=110, height=34, font_size=12):
    return ctk.CTkButton(
        parent,
        text=text,
        width=width,
        height=height,
        corner_radius=6,
        fg_color=color,
        hover_color=hover,
        text_color=WHITE,
        font=ctk.CTkFont(family="Segoe UI", size=font_size, weight="bold"),
        command=command,
    )


def make_outline_button(parent, text, command, width=150):
    return ctk.CTkButton(
        parent,
        text=text,
        width=width,
        height=38,
        corner_radius=6,
        fg_color=WHITE,
        hover_color="#eef4ff",
        border_color=BLUE,
        border_width=1,
        text_color=BLUE,
        font=ctk.CTkFont(family="Segoe UI", size=13),
        command=command,
    )


def make_back_button(parent, command, text="← Back to Teachers"):
    """Highly visible back button for sub-pages."""
    return ctk.CTkButton(
        parent,
        text=text,
        width=175,
        height=38,
        corner_radius=7,
        fg_color=BLUE,
        hover_color=BLUE_H,
        text_color=WHITE,
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        command=command,
    )


def make_card(parent, height=None):
    card = ctk.CTkFrame(
        parent,
        fg_color=WHITE,
        border_color=CARD_BORDER,
        border_width=1,
        corner_radius=6,
    )
    if height:
        card.configure(height=height)
        card.pack_propagate(False)
    return card


def make_status_badge(parent, status):
    if status == "Active":
        bg, fg = GREEN, WHITE
    else:
        bg, fg = "#e5e7eb", "#374151"

    return ctk.CTkLabel(
        parent,
        text=status,
        width=70,
        height=24,
        corner_radius=5,
        fg_color=bg,
        text_color=fg,
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
    )


def make_entry(parent, value="", placeholder=""):
    entry = ctk.CTkEntry(
        parent,
        height=38,
        corner_radius=5,
        border_color="#d6dce6",
        fg_color=WHITE,
        text_color=TEXT_DARK,
        placeholder_text=placeholder,
        font=ctk.CTkFont(family="Segoe UI", size=13),
    )
    if value:
        entry.insert(0, value)
    return entry


def make_labeled_entry(parent, label, value="", placeholder=""):
    wrap = ctk.CTkFrame(parent, fg_color=WHITE)
    ctk.CTkLabel(
        wrap,
        text=label,
        text_color=TEXT_DARK,
        fg_color=WHITE,
        anchor="w",
        font=ctk.CTkFont(family="Segoe UI", size=13),
    ).pack(fill="x", pady=(0, 6))
    entry = make_entry(wrap, value=value, placeholder=placeholder)
    entry.pack(fill="x")
    wrap.entry = entry
    return wrap


def make_search_bar(parent, variable, placeholder="Search teacher..."):
    box = ctk.CTkFrame(
        parent,
        fg_color=WHITE,
        border_color="#d6dce6",
        border_width=1,
        corner_radius=5,
        height=42,
    )
    box.grid_columnconfigure(1, weight=1)
    box.grid_propagate(False)

    ctk.CTkLabel(
        box,
        text="🔍",
        width=36,
        text_color=TEXT_GRAY,
        fg_color=WHITE,
        font=ctk.CTkFont(family="Segoe UI Emoji", size=14),
    ).grid(row=0, column=0, sticky="nsw", padx=(10, 0))

    entry = ctk.CTkEntry(
        box,
        textvariable=variable,
        placeholder_text=placeholder,
        fg_color=WHITE,
        border_width=0,
        height=36,
        text_color=TEXT_DARK,
        placeholder_text_color=TEXT_GRAY,
        font=ctk.CTkFont(family="Segoe UI", size=13),
    )
    entry.grid(row=0, column=1, sticky="ew", pady=2)

    clear_btn = ctk.CTkButton(
        box,
        text="✕",
        width=28,
        height=28,
        corner_radius=14,
        fg_color="#e5e7eb",
        hover_color="#d1d5db",
        text_color=TEXT_GRAY,
        font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        command=lambda: variable.set(""),
    )
    clear_btn.grid(row=0, column=2, sticky="e", padx=(0, 10))
    clear_btn.grid_remove()

    def toggle_clear(*_):
        if variable.get().strip():
            clear_btn.grid()
        else:
            clear_btn.grid_remove()

    variable.trace_add("write", toggle_clear)
    toggle_clear()
    return box


def configure_columns(frame, widths):
    for i, w in enumerate(widths):
        frame.grid_columnconfigure(i, weight=w, uniform="table")


def section_title(parent, title):
    ctk.CTkLabel(
        parent,
        text=title,
        text_color=BLUE,
        fg_color=WHITE,
        anchor="w",
        font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
    ).pack(fill="x", pady=(0, 18))


# ─────────────────────────────────────────────────────────────────────────────
# Main app
# ─────────────────────────────────────────────────────────────────────────────
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Admin Dashboard")
        self.geometry("1500x820")
        self.minsize(1100, 700)
        self.configure(fg_color=BG)

        self.teachers = [dict(t) for t in DEFAULT_TEACHERS]
        self.archived_teachers = [dict(t) for t in DEFAULT_ARCHIVED]
        self.active_menu = "Teachers"

        self.grid_columnconfigure(0, weight=0, minsize=230)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.show_teachers()

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def switch_menu(self, menu):
        self.active_menu = menu
        self.sidebar.refresh()
        if menu == "Teachers":
            self.show_teachers()
        else:
            self.show_placeholder(menu)

    def show_placeholder(self, title):
        self.clear_content()
        page = ctk.CTkFrame(self.content, fg_color=BG, corner_radius=0)
        page.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(
            page,
            text=title,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
        ).pack(anchor="w", padx=32, pady=(32, 12))
        card = make_card(page, height=220)
        card.pack(fill="x", padx=32)
        ctk.CTkLabel(
            card,
            text=f"{title} page is under construction.",
            text_color=TEXT_GRAY,
            fg_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=16),
        ).pack(expand=True)

    def show_teachers(self):
        self.active_menu = "Teachers"
        self.sidebar.refresh()
        self.clear_content()
        TeachersManagementPage(self.content, self).grid(row=0, column=0, sticky="nsew")

    def show_profile(self, teacher):
        self.clear_content()
        TeacherProfilePage(self.content, self, teacher).grid(row=0, column=0, sticky="nsew")

    def show_edit_teacher(self, teacher):
        self.clear_content()
        EditTeacherPage(self.content, self, teacher).grid(row=0, column=0, sticky="nsew")

    def show_add_teacher(self):
        self.clear_content()
        AddTeacherPage(self.content, self).grid(row=0, column=0, sticky="nsew")

    def show_archived_teachers(self):
        self.clear_content()
        ArchivedTeachersPage(self.content, self).grid(row=0, column=0, sticky="nsew")

    def archive_teacher(self, teacher_id):
        teacher = next((t for t in self.teachers if t["id"] == teacher_id), None)
        if not teacher:
            return
        self.teachers = [t for t in self.teachers if t["id"] != teacher_id]
        archived = dict(teacher)
        archived["status"] = "Archived"
        archived["archived_at"] = datetime.now().strftime("%b %d, %Y")
        self.archived_teachers.append(archived)
        self.show_teachers()

    def restore_teacher(self, teacher_id):
        teacher = next((t for t in self.archived_teachers if t["id"] == teacher_id), None)
        if not teacher:
            return
        self.archived_teachers = [t for t in self.archived_teachers if t["id"] != teacher_id]
        restored = dict(teacher)
        restored["status"] = "Active"
        self.teachers.append(restored)
        self.show_archived_teachers()

    def delete_teacher(self, teacher_id):
        if messagebox.askyesno("Delete Teacher", "Delete this teacher?", parent=self):
            self.teachers = [t for t in self.teachers if t["id"] != teacher_id]
            self.show_teachers()

    def delete_archived_teacher(self, teacher_id):
        if messagebox.askyesno("Delete Permanently", "Delete this archived teacher permanently?", parent=self):
            self.archived_teachers = [t for t in self.archived_teachers if t["id"] != teacher_id]
            self.show_archived_teachers()

    def add_teacher(self, data):
        next_id = max([t["id"] for t in self.teachers + self.archived_teachers] + [0]) + 1
        data["id"] = next_id
        data["position"] = "Teacher"
        data["status"] = "Active"
        self.teachers.append(data)
        self.show_teachers()

    def save_teacher(self, teacher_id, data):
        for teacher in self.teachers:
            if teacher["id"] == teacher_id:
                teacher.update(data)
                break
        self.show_teachers()


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
class Sidebar(ctk.CTkFrame):
    MENU = [
        ("Dashboard", "▧"),
        ("Teachers", "👥"),
        ("Students", "🎓"),
        ("Student Accounts", "▣"),
        ("Activities", "▤"),
        ("Enrollment", "▱"),
        ("Reports", "▥"),
        ("Logout", "↩"),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=SIDEBAR_BG, width=230, corner_radius=0)
        self.app = app
        self.grid_propagate(False)
        self.nav_buttons = {}
        self.build()

    def build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        header = ctk.CTkFrame(self, fg_color=SIDEBAR_BG, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(18, 12))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="☰",
            text_color=WHITE,
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Admin Panel",
            text_color=WHITE,
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        ).grid(row=0, column=1, sticky="w", padx=(12, 0))

        profile = ctk.CTkFrame(self, fg_color=SIDEBAR_BG, corner_radius=0)
        profile.grid(row=1, column=0, sticky="ew", pady=(14, 24))
        profile.grid_columnconfigure(0, weight=1)

        avatar = ctk.CTkFrame(
            profile,
            width=78,
            height=78,
            fg_color=SIDEBAR_BG,
            border_color=WHITE,
            border_width=2,
            corner_radius=39,
        )
        avatar.grid(row=0, column=0, pady=(0, 12))
        avatar.grid_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="",
            fg_color=SIDEBAR_BG,
            text_color=WHITE,
        ).pack(expand=True)

        ctk.CTkLabel(
            profile,
            text="Christian Joseph Aquino",
            text_color=WHITE,
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        ).grid(row=1, column=0)

        ctk.CTkLabel(
            profile,
            text="Administrator",
            text_color=SIDEBAR_MUTED,
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=12),
        ).grid(row=2, column=0, pady=(2, 4))

        ctk.CTkLabel(
            profile,
            text="View Profile →",
            text_color=YELLOW,
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=12),
        ).grid(row=3, column=0)

        nav = ctk.CTkFrame(self, fg_color=SIDEBAR_BG, corner_radius=0)
        nav.grid(row=2, column=0, sticky="ew")

        for i, (label, icon) in enumerate(self.MENU):
            btn = ctk.CTkButton(
                nav,
                text=f"{icon}  {label}",
                height=44,
                corner_radius=0,
                fg_color=SIDEBAR_BG,
                hover_color=SIDEBAR_HOVER,
                text_color=WHITE if label != "Logout" else "#fecaca",
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                command=lambda name=label: self.on_click(name),
            )
            btn.grid(row=i, column=0, sticky="ew")
            self.nav_buttons[label] = btn

    def on_click(self, name):
        if name == "Logout":
            messagebox.showinfo("Logout", "Logout clicked.", parent=self.app)
        else:
            self.app.switch_menu(name)

    def refresh(self):
        for label, btn in self.nav_buttons.items():
            if label == "Logout":
                btn.configure(fg_color=SIDEBAR_BG)
            else:
                btn.configure(fg_color=SIDEBAR_ACTIVE if self.app.active_menu == label else SIDEBAR_BG)


# ─────────────────────────────────────────────────────────────────────────────
# Teachers Management
# ─────────────────────────────────────────────────────────────────────────────
class TeachersManagementPage(ctk.CTkFrame):
    HEADS = ["ID", "Teacher Name", "Position", "Status", "Actions"]
    WIDTHS = [8, 34, 24, 18, 30]

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_rows())
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.build()

    def build(self):
        top = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        top.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 18))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text="Teachers Management",
            text_color=TEXT_DARK,
            fg_color=BG,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        btns = ctk.CTkFrame(top, fg_color=BG)
        btns.grid(row=0, column=1, sticky="e")
        make_button(btns, "Archived Teachers", WHITE, "#eef2f7", self.app.show_archived_teachers, width=150, height=38, font_size=12).pack(side="left", padx=(0, 8))
        btns.winfo_children()[0].configure(text_color=GRAY, border_width=1, border_color=GRAY)
        make_button(btns, "+ Add Teacher", BLUE, BLUE_H, self.app.show_add_teacher, width=130, height=38, font_size=12).pack(side="left")

        card = make_card(self)
        card.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 28))
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        search_wrap = ctk.CTkFrame(card, fg_color=WHITE)
        search_wrap.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
        search_wrap.grid_columnconfigure(0, weight=1)
        make_search_bar(search_wrap, self.search_var, "Search teacher...").grid(row=0, column=0, sticky="ew")

        self.table = ctk.CTkFrame(card, fg_color=WHITE, corner_radius=0)
        self.table.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 18))
        self.table.grid_columnconfigure(0, weight=1)
        self.refresh_rows()

    def refresh_rows(self):
        for w in self.table.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.table, fg_color="#f9fafb", corner_radius=0)
        header.pack(fill="x")
        configure_columns(header, self.WIDTHS)

        for i, head in enumerate(self.HEADS):
            ctk.CTkLabel(
                header,
                text=head,
                text_color=TEXT_DARK,
                fg_color="#f9fafb",
                anchor="e" if head == "Actions" else "w",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            ).grid(row=0, column=i, sticky="ew", padx=(8, 8), pady=10)

        ctk.CTkFrame(self.table, fg_color="#e5e7eb", height=1, corner_radius=0).pack(fill="x")

        query = self.search_var.get().strip().lower()
        teachers = self.app.teachers
        if query:
            teachers = [
                t for t in teachers
                if query in teacher_display_name(t).lower()
                or query in teacher_full_name(t).lower()
                or query == str(t["id"])
            ]

        for t in teachers:
            self.create_row(t)

    def create_row(self, teacher):
        row = ctk.CTkFrame(self.table, fg_color=WHITE, corner_radius=0)
        row.pack(fill="x")
        configure_columns(row, self.WIDTHS)

        values = [
            str(teacher["id"]),
            teacher_display_name(teacher),
            teacher.get("position", "Teacher"),
        ]

        for i, val in enumerate(values):
            ctk.CTkLabel(
                row,
                text=val,
                text_color=TEXT_DARK,
                fg_color=WHITE,
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=13),
            ).grid(row=0, column=i, sticky="ew", padx=(8, 8), pady=11)

        make_status_badge(row, teacher.get("status", "Active")).grid(row=0, column=3, sticky="w", padx=(8, 8))

        actions = ctk.CTkFrame(row, fg_color=WHITE)
        actions.grid(row=0, column=4, sticky="e", padx=(8, 8))

        make_button(actions, "View", CYAN, CYAN_H, lambda t=teacher: self.app.show_profile(t), width=50, height=30, font_size=11).pack(side="left", padx=2)
        make_button(actions, "Edit", ORANGE, ORANGE_H, lambda t=teacher: self.app.show_edit_teacher(t), width=48, height=30, font_size=11).pack(side="left", padx=2)
        make_button(actions, "Archive", GRAY, GRAY_H, lambda tid=teacher["id"]: self.app.archive_teacher(tid), width=70, height=30, font_size=11).pack(side="left", padx=2)
        make_button(actions, "Delete", RED, RED_H, lambda tid=teacher["id"]: self.app.delete_teacher(tid), width=60, height=30, font_size=11).pack(side="left", padx=2)

        ctk.CTkFrame(self.table, fg_color="#e5e7eb", height=1, corner_radius=0).pack(fill="x")


# ─────────────────────────────────────────────────────────────────────────────
# Teacher Profile
# ─────────────────────────────────────────────────────────────────────────────
class TeacherProfilePage(ctk.CTkFrame):
    def __init__(self, parent, app, teacher):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self.teacher = teacher
        self.build()

    def build(self):
        ctk.CTkLabel(
            self,
            text="Teacher Profile",
            text_color=TEXT_DARK,
            fg_color=BG,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).pack(anchor="w", padx=150, pady=(50, 8))

        make_back_button(self, self.app.show_teachers).pack(anchor="w", padx=150, pady=(0, 16))

        card = make_card(self, height=270)
        card.pack(fill="x", padx=150)
        card.pack_propagate(False)

        body = ctk.CTkFrame(card, fg_color=WHITE)
        body.pack(fill="both", expand=True, padx=24, pady=24)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, weight=1)

        left = ctk.CTkFrame(body, fg_color=WHITE)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Profile Photo", fg_color=WHITE, text_color=TEXT_GRAY).pack(pady=(0, 8))
        ctk.CTkLabel(
            left,
            text=teacher_display_name(self.teacher),
            fg_color=WHITE,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        ).pack()
        ctk.CTkLabel(
            left,
            text=f"({self.teacher.get('middle_name', '')})",
            fg_color=WHITE,
            text_color=TEXT_GRAY,
            font=ctk.CTkFont(family="Segoe UI", size=13),
        ).pack()

        badge_row = ctk.CTkFrame(left, fg_color=WHITE)
        badge_row.pack(pady=(8, 14))
        ctk.CTkLabel(badge_row, text="Teacher", fg_color=BLUE, text_color=WHITE, corner_radius=5, width=70, height=22).pack(side="left", padx=3)
        ctk.CTkLabel(badge_row, text="Active", fg_color=GREEN, text_color=WHITE, corner_radius=5, width=60, height=22).pack(side="left", padx=3)

        ctk.CTkFrame(left, fg_color="#d1d5db", height=1).pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(left, text=f"Username: {self.teacher.get('username', '')}", fg_color=WHITE, text_color=TEXT_DARK, font=ctk.CTkFont(weight="bold")).pack()
        ctk.CTkLabel(left, text=f"Password: {self.teacher.get('password', '')}", fg_color=WHITE, text_color=TEXT_DARK, font=ctk.CTkFont(weight="bold")).pack(pady=(6, 0))

        middle = ctk.CTkFrame(body, fg_color=WHITE)
        middle.grid(row=0, column=1, sticky="nsew", padx=20)
        self.profile_section(middle, "Personal Info", [
            ("Full Name", teacher_full_name(self.teacher)),
            ("Age", self.teacher.get("age", "")),
            ("Birthday", self.teacher.get("birthday_long", "")),
            ("Gender", self.teacher.get("gender", "")),
        ])

        right = ctk.CTkFrame(body, fg_color=WHITE)
        right.grid(row=0, column=2, sticky="nsew", padx=(20, 0))
        self.profile_section(right, "Contact Info", [
            ("Mobile", self.teacher.get("mobile", "")),
            ("Email", self.teacher.get("email", "")),
        ])
        ctk.CTkLabel(right, text="Address", fg_color=WHITE, text_color=BLUE, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(16, 6))
        self.info_line(right, "Barangay", self.teacher.get("barangay", ""))
        self.info_line(right, "Street", self.teacher.get("street", ""))

        make_button(right, "↩ Back", BLUE, BLUE_H, self.app.show_teachers, width=90, height=40).pack(anchor="e", pady=(28, 0))

    def profile_section(self, parent, title, fields):
        ctk.CTkLabel(parent, text=title, fg_color=WHITE, text_color=BLUE, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(0, 8))
        for label, value in fields:
            self.info_line(parent, label, value)

    def info_line(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(anchor="w", pady=3)
        ctk.CTkLabel(row, text=f"{label}: ", fg_color=WHITE, text_color=TEXT_DARK, font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(row, text=value, fg_color=WHITE, text_color=TEXT_DARK).pack(side="left")


# ─────────────────────────────────────────────────────────────────────────────
# Edit Teacher
# ─────────────────────────────────────────────────────────────────────────────
class EditTeacherPage(ctk.CTkFrame):
    def __init__(self, parent, app, teacher):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self.teacher = teacher
        self.entries = {}
        self.build()

    def build(self):
        ctk.CTkLabel(
            self,
            text="Edit Teacher",
            text_color=TEXT_DARK,
            fg_color=BG,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).pack(anchor="w", padx=150, pady=(50, 8))

        make_back_button(self, self.app.show_teachers).pack(anchor="w", padx=150, pady=(0, 16))

        card = make_card(self)
        card.pack(fill="x", padx=150)

        inner = ctk.CTkFrame(card, fg_color=WHITE)
        inner.pack(fill="x", padx=24, pady=24)

        section_title(inner, "Profile Photo")
        photo_row = ctk.CTkFrame(inner, fg_color=WHITE)
        photo_row.pack(fill="x", pady=(0, 22))
        photo = ctk.CTkFrame(photo_row, fg_color=WHITE, border_color="#d1d5db", border_width=1, width=110, height=110, corner_radius=55)
        photo.pack(side="left", padx=(0, 24))
        photo.pack_propagate(False)

        upload = ctk.CTkFrame(photo_row, fg_color=WHITE)
        upload.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(upload, text="Upload New Photo", fg_color=WHITE, text_color=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        make_entry(upload, value="Choose File    No file chosen").pack(fill="x")
        ctk.CTkLabel(upload, text="Leave empty to keep the current photo.", fg_color=WHITE, text_color=TEXT_GRAY, font=ctk.CTkFont(size=11)).pack(anchor="w", pady=(6, 0))

        section_title(inner, "Personal Details")
        self.form_grid(inner, [
            [("first_name", "First Name", self.teacher["first_name"]), ("middle_name", "Middle Name", self.teacher["middle_name"]), ("last_name", "Surname", self.teacher["last_name"])],
            [("age", "Age", self.teacher["age"]), ("birthday", "Birthday", self.teacher["birthday"]), ("gender", "Gender", self.teacher["gender"]), ("mobile", "Mobile Number", self.teacher["mobile"])],
            [("email", "Email Address", self.teacher["email"]), ("username", "Username", self.teacher["username"])],
        ])

        section_title(inner, "Address")
        self.form_grid(inner, [
            [("barangay", "Barangay", self.teacher["barangay"]), ("street", "Street Address", self.teacher["street"])]
        ])

        btns = ctk.CTkFrame(inner, fg_color=WHITE)
        btns.pack(fill="x", pady=(24, 0))
        make_button(btns, "Save Changes", GREEN, GREEN_H, self.save, width=130).pack(side="right", padx=(8, 0))
        make_button(btns, "Cancel", GRAY, GRAY_H, self.app.show_teachers, width=90).pack(side="right")

    def form_grid(self, parent, rows):
        for row_data in rows:
            row = ctk.CTkFrame(parent, fg_color=WHITE)
            row.pack(fill="x", pady=(0, 18))
            for i in range(len(row_data)):
                row.grid_columnconfigure(i, weight=1, uniform="form")
            for i, (key, label, value) in enumerate(row_data):
                field = make_labeled_entry(row, label, value=value)
                field.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0))
                self.entries[key] = field.entry

    def save(self):
        data = {k: entry.get() for k, entry in self.entries.items()}
        data["birthday_long"] = "May 08, 2006" if data.get("birthday") == "05/08/2006" else data.get("birthday", "")
        data["position"] = "Teacher"
        data["status"] = "Active"
        data["password"] = self.teacher.get("password", "teacher123")
        self.app.save_teacher(self.teacher["id"], data)


# ─────────────────────────────────────────────────────────────────────────────
# Add Teacher
# ─────────────────────────────────────────────────────────────────────────────
class AddTeacherPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self.entries = {}
        self.build()

    def build(self):
        ctk.CTkLabel(
            self,
            text="Add Teacher",
            text_color=TEXT_DARK,
            fg_color=BG,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).pack(anchor="w", padx=150, pady=(50, 8))

        make_back_button(self, self.app.show_teachers).pack(anchor="w", padx=150, pady=(0, 16))

        card = make_card(self)
        card.pack(fill="x", padx=150)
        inner = ctk.CTkFrame(card, fg_color=WHITE)
        inner.pack(fill="x", padx=24, pady=24)

        section_title(inner, "Personal Details")

        first = ctk.CTkFrame(inner, fg_color=WHITE)
        first.pack(fill="x", pady=(0, 22))
        first.grid_columnconfigure(0, weight=1)
        first.grid_columnconfigure(1, weight=1)
        first.grid_columnconfigure(2, weight=1)
        first.grid_columnconfigure(3, weight=1)

        upload = ctk.CTkFrame(first, fg_color=WHITE)
        upload.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        ctk.CTkLabel(upload, text="Upload Photo", fg_color=WHITE, text_color=TEXT_DARK, font=ctk.CTkFont(weight="bold")).pack(anchor="center", pady=(0, 8))
        preview = ctk.CTkFrame(upload, fg_color="#f8fafc", border_color="#d1d5db", border_width=1, width=110, height=110, corner_radius=5)
        preview.pack(anchor="center", pady=(0, 8))
        preview.pack_propagate(False)
        ctk.CTkLabel(preview, text="Preview", fg_color="#f8fafc", text_color=TEXT_GRAY).pack(expand=True)
        make_entry(upload, value="Choose File    No file chosen").pack(fill="x")

        fields = [
            ("first_name", "First Name"),
            ("middle_name", "Middle Name"),
            ("last_name", "Surname / Last Name"),
        ]
        for i, (key, label) in enumerate(fields, start=1):
            field = make_labeled_entry(first, label)
            field.grid(row=0, column=i, sticky="new", padx=(0, 14 if i < 3 else 0))
            self.entries[key] = field.entry

        self.form_grid(inner, [
            [("birthday", "Birthday", ""), ("age", "Age", ""), ("gender", "Gender", ""), ("mobile", "Mobile Number", "e.g. 09123456789")],
            [("email", "Email Address", ""), ("username", "Username", ""), ("password", "Password", ""), ("confirm_password", "Confirm Password", "")],
        ])

        section_title(inner, "Address")
        self.form_grid(inner, [
            [("barangay", "Barangay", "Select Barangay"), ("street", "Street Address", "")]
        ])

        btns = ctk.CTkFrame(inner, fg_color=WHITE)
        btns.pack(fill="x", pady=(24, 0))
        make_button(btns, "Save", GREEN, GREEN_H, self.save, width=80).pack(side="right", padx=(8, 0))
        make_button(btns, "Cancel", GRAY, GRAY_H, self.app.show_teachers, width=90).pack(side="right")

    def form_grid(self, parent, rows):
        for row_data in rows:
            row = ctk.CTkFrame(parent, fg_color=WHITE)
            row.pack(fill="x", pady=(0, 18))
            for i in range(len(row_data)):
                row.grid_columnconfigure(i, weight=1, uniform="form")
            for i, (key, label, placeholder) in enumerate(row_data):
                field = make_labeled_entry(row, label, placeholder=placeholder)
                field.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0))
                self.entries[key] = field.entry

    def save(self):
        data = {k: entry.get() for k, entry in self.entries.items()}
        if not data.get("first_name") and not data.get("last_name"):
            data["first_name"] = "New"
            data["last_name"] = "Teacher"
        data.setdefault("middle_name", "")
        data["birthday_long"] = data.get("birthday", "")
        data["position"] = "Teacher"
        data["status"] = "Active"
        self.app.add_teacher(data)


# ─────────────────────────────────────────────────────────────────────────────
# Archived Teachers
# ─────────────────────────────────────────────────────────────────────────────
class ArchivedTeachersPage(ctk.CTkFrame):
    HEADS = ["ID", "Teacher Name", "Position", "Actions"]
    WIDTHS = [8, 42, 28, 30]

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.build()

    def build(self):
        ctk.CTkLabel(
            self,
            text="Archived Teachers",
            text_color=TEXT_DARK,
            fg_color=BG,
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        ).pack(anchor="w", padx=28, pady=(28, 8))

        make_back_button(self, self.app.show_teachers).pack(anchor="w", padx=28, pady=(0, 18))

        card = make_card(self)
        card.pack(fill="x", padx=28)

        table = ctk.CTkFrame(card, fg_color=WHITE)
        table.pack(fill="x", padx=16, pady=16)

        header = ctk.CTkFrame(table, fg_color="#f9fafb", corner_radius=0)
        header.pack(fill="x")
        configure_columns(header, self.WIDTHS)

        for i, head in enumerate(self.HEADS):
            ctk.CTkLabel(
                header,
                text=head,
                text_color=TEXT_DARK,
                fg_color="#f9fafb",
                anchor="e" if head == "Actions" else "w",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            ).grid(row=0, column=i, sticky="ew", padx=8, pady=10)

        ctk.CTkFrame(table, fg_color="#e5e7eb", height=1).pack(fill="x")

        for teacher in self.app.archived_teachers:
            self.row(table, teacher)

    def row(self, table, teacher):
        row = ctk.CTkFrame(table, fg_color=WHITE, corner_radius=0)
        row.pack(fill="x")
        configure_columns(row, self.WIDTHS)

        vals = [str(teacher["id"]), teacher_display_name(teacher), teacher.get("position", "Teacher")]
        for i, val in enumerate(vals):
            ctk.CTkLabel(
                row,
                text=val,
                text_color=TEXT_DARK,
                fg_color=WHITE,
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=13),
            ).grid(row=0, column=i, sticky="ew", padx=8, pady=12)

        actions = ctk.CTkFrame(row, fg_color=WHITE)
        actions.grid(row=0, column=3, sticky="e", padx=8)
        make_button(actions, "Restore", GREEN, GREEN_H, lambda tid=teacher["id"]: self.app.restore_teacher(tid), width=80, height=32, font_size=11).pack(side="left", padx=3)
        make_button(actions, "Delete Permanently", RED, RED_H, lambda tid=teacher["id"]: self.app.delete_archived_teacher(tid), width=145, height=32, font_size=11).pack(side="left", padx=3)

        ctk.CTkFrame(table, fg_color="#e5e7eb", height=1).pack(fill="x")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
