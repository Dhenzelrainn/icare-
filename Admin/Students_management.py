import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ─── Color constants ───────────────────────────────────────────────────────────
SIDEBAR_TOP    = "#1a3a6b"
SIDEBAR_MID    = "#1e4d8c"
SIDEBAR_BOT    = "#1565c0"
SIDEBAR_ACTIVE = "#2979c8"
SIDEBAR_HOVER  = "#2563a8"
SIDEBAR_TEXT   = "#ffffff"
YELLOW         = "#f5c518"
BG             = "#f4f6f9"
WHITE          = "#ffffff"
BORDER         = "#d0d7e3"
TEXT_DARK      = "#1a1a2e"
TEXT_GRAY      = "#6b7280"
BTN_CYAN       = "#00b4d8"
BTN_CYAN_HO    = "#0096b7"
BTN_GRAY       = "#9ca3af"
BTN_GRAY_HO    = "#6b7280"
BTN_GREEN      = "#22c55e"
BTN_GREEN_HO   = "#16a34a"
BTN_RED        = "#ef4444"
BTN_RED_HO     = "#dc2626"
BADGE_GREEN_BG = "#dcfce7"
BADGE_GREEN_FG = "#166534"
BADGE_GRAY_BG  = "#e5e7eb"
BADGE_GRAY_FG  = "#374151"
TAB_ACTIVE_BG  = "#1e4d8c"
TAB_ACTIVE_FG  = "#ffffff"
TAB_INACT_FG   = "#6b7280"

# ─── Initial data ──────────────────────────────────────────────────────────────
ENROLLED_STUDENTS = [
    {"id": 2, "name": "Dennielle Cruz", "section": "B", "status": "Active",
     "enrolled": "Oct 29, 2025", "graduated": "—"},
]

ARCHIVED_STUDENTS = [
    {"id": 1, "name": "Dhenzel rain Cruz", "section": "A", "email": "—",
     "status": "Archived", "archived_at": "—"},
]

STUDENT_PROFILE = {
    "full_name": "Dennielle Pilapil Cruz",
    "nickname": "denden",
    "birthday": "2006-07-23",
    "age": "19",
    "gender": "Male",
    "section": "B",
    "mother_name": "Dennielle Pilapil Cruz",
    "mother_occupation": "ofw",
    "mother_contact": "09276426345",
    "mother_education": "Vocational",
    "mother_school": "ACTS COMPUTER COLLEGE",
    "mother_graduated": "2000",
    "father_name": "Dennielle Pilapil Cruz",
    "father_occupation": "ofw",
    "father_contact": "09276426345",
    "father_education": "College",
    "father_school": "LSPU",
    "father_graduated": "2000",
    "guardian_name": "Dennielle Pilapil Cruz",
    "guardian_occupation": "Deceased",
    "guardian_contact": "09275858837",
}

# ═══════════════════════════════════════════════════════════════════════════════
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard – Students Management")
        self.geometry("1200x720")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._enrolled  = list(ENROLLED_STUDENTS)
        self._archived  = list(ARCHIVED_STUDENTS)
        self._profile   = STUDENT_PROFILE
        self._view_student = None  # student being viewed in profile page

        self._build_layout()
        self._show_students()

    # ── Layout skeleton ────────────────────────────────────────────────────────
    def _build_layout(self):
        self._sidebar_frame = tk.Frame(self, bg=SIDEBAR_TOP, width=230)
        self._sidebar_frame.pack(side="left", fill="y")
        self._sidebar_frame.pack_propagate(False)

        self._content_frame = tk.Frame(self, bg=BG)
        self._content_frame.pack(side="left", fill="both", expand=True)

        Sidebar(self._sidebar_frame, self)

    def _clear_content(self):
        for w in self._content_frame.winfo_children():
            w.destroy()

    # ── Page switches ──────────────────────────────────────────────────────────
    def _show_students(self):
        self._clear_content()
        StudentsManagementPage(self._content_frame, self)

    def _show_archived(self):
        self._clear_content()
        ArchivedStudentsPage(self._content_frame, self)

    def _show_profile(self, student=None):
        self._clear_content()
        StudentProfilePage(self._content_frame, self, student or self._profile)

    # ── Data operations ────────────────────────────────────────────────────────
    def archive_student(self, student_id):
        match = next((s for s in self._enrolled if s["id"] == student_id), None)
        if not match:
            return
        self._enrolled.remove(match)
        now = datetime.now().strftime("%b %d, %Y")
        self._archived.append({
            "id": match["id"],
            "name": match["name"],
            "section": match["section"],
            "email": "—",
            "status": "Archived",
            "archived_at": now,
        })
        self._show_students()

    def restore_student(self, student_id):
        match = next((s for s in self._archived if s["id"] == student_id), None)
        if not match:
            return
        self._archived.remove(match)
        self._enrolled.append({
            "id": match["id"],
            "name": match["name"],
            "section": match["section"],
            "status": "Active",
            "enrolled": match.get("archived_at", "—"),
            "graduated": "—",
        })
        self._show_archived()

    def delete_student(self, student_id):
        self._archived = [s for s in self._archived if s["id"] != student_id]
        self._show_archived()


# ═══════════════════════════════════════════════════════════════════════════════
class Sidebar(tk.Frame):
    MENU = [
        ("Dashboard",       "⊞"),
        ("Teachers",        "✎"),
        ("Students",        "◎"),
        ("Student Accounts","⊟"),
        ("Activities",      "◈"),
        ("Enrollment",      "⊡"),
        ("Reports",         "⊞"),
        ("Logout",          "⊘"),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=SIDEBAR_TOP)
        self.app = app
        self.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        # ── Header ─────────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=SIDEBAR_TOP, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="☰  Admin Panel", font=("Helvetica", 13, "bold"),
                 bg=SIDEBAR_TOP, fg=SIDEBAR_TEXT, anchor="w",
                 padx=18).pack(fill="x")

        # ── Divider ────────────────────────────────────────────────────────────
        tk.Frame(self, bg="#2a5298", height=1).pack(fill="x", padx=14)

        # ── Profile ────────────────────────────────────────────────────────────
        prof = tk.Frame(self, bg=SIDEBAR_TOP, pady=18)
        prof.pack(fill="x")

        # circular avatar via canvas
        cv = tk.Canvas(prof, width=70, height=70, bg=SIDEBAR_TOP,
                       highlightthickness=0)
        cv.pack()
        cv.create_oval(4, 4, 66, 66, outline=WHITE, width=2, fill=SIDEBAR_TOP)

        tk.Label(prof, text="Christian Joseph Aquino",
                 font=("Helvetica", 9, "bold"), bg=SIDEBAR_TOP,
                 fg=SIDEBAR_TEXT, wraplength=190, justify="center").pack()
        tk.Label(prof, text="Administrator", font=("Helvetica", 8),
                 bg=SIDEBAR_TOP, fg="#a8c4e0").pack(pady=(1, 4))
        vp = tk.Label(prof, text="View Profile →", font=("Helvetica", 8, "underline"),
                      bg=SIDEBAR_TOP, fg=YELLOW, cursor="hand2")
        vp.pack()

        # ── Divider ────────────────────────────────────────────────────────────
        tk.Frame(self, bg="#2a5298", height=1).pack(fill="x", padx=14, pady=(4, 0))

        # ── Menu items ─────────────────────────────────────────────────────────
        menu_frame = tk.Frame(self, bg=SIDEBAR_TOP)
        menu_frame.pack(fill="both", expand=True, pady=(6, 0))

        for label, icon in self.MENU:
            is_active = (label == "Students")
            self._create_menu_item(menu_frame, icon, label, is_active)

    def _create_menu_item(self, parent, icon, label, active=False):
        bg = SIDEBAR_ACTIVE if active else SIDEBAR_TOP
        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill="x")

        inner = tk.Frame(row, bg=bg, padx=16, pady=9)
        inner.pack(fill="x")

        tk.Label(inner, text=f"{icon}  {label}", font=("Helvetica", 9),
                 bg=bg, fg=SIDEBAR_TEXT, anchor="w").pack(fill="x")

        if not active:
            def on_enter(e, r=row, i=inner, lbl=inner.winfo_children()):
                r.configure(bg=SIDEBAR_HOVER)
                i.configure(bg=SIDEBAR_HOVER)
                for ch in i.winfo_children():
                    ch.configure(bg=SIDEBAR_HOVER)

            def on_leave(e, r=row, i=inner):
                r.configure(bg=SIDEBAR_TOP)
                i.configure(bg=SIDEBAR_TOP)
                for ch in i.winfo_children():
                    ch.configure(bg=SIDEBAR_TOP)

            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)
            inner.bind("<Enter>", on_enter)
            inner.bind("<Leave>", on_leave)
            for ch in inner.winfo_children():
                ch.bind("<Enter>", on_enter)
                ch.bind("<Leave>", on_leave)


# ═══════════════════════════════════════════════════════════════════════════════
class StudentsManagementPage(tk.Frame):
    COL_WIDTHS = [50, 200, 80, 90, 120, 120, 220]
    COL_HEADS  = ["ID", "Student Name", "Section", "Status", "Enrolled", "Graduated", "Actions"]

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.pack(fill="both", expand=True)
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_rows())
        self._build()

    def _build(self):
        # ── Top bar ────────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=BG, pady=20, padx=28)
        top.pack(fill="x")

        tk.Label(top, text="Students Management",
                 font=("Helvetica", 18, "bold"), bg=BG,
                 fg=TEXT_DARK).pack(side="left")

        _btn(top, "Archived Students", "#6b7280", "#4b5563",
             lambda: self.app._show_archived()).pack(side="right")

        # ── Tabs ───────────────────────────────────────────────────────────────
        tab_bar = tk.Frame(self, bg=BG, padx=28)
        tab_bar.pack(fill="x")

        enrolled_tab = tk.Label(tab_bar, text="ENROLLED STUDENTS",
                                font=("Helvetica", 9, "bold"),
                                bg=BG, fg=TEXT_DARK, padx=12, pady=6,
                                cursor="hand2", relief="flat", bd=0)
        enrolled_tab.pack(side="left")
        # active underline
        tk.Frame(tab_bar, bg=TEXT_DARK, height=2, width=140).place(
            in_=enrolled_tab, relx=0, rely=1.0, anchor="nw")

        grad_tab = tk.Label(tab_bar, text="GRADUATED STUDENTS",
                            font=("Helvetica", 9), bg=BG, fg=TEXT_GRAY,
                            padx=12, pady=6, cursor="hand2")
        grad_tab.pack(side="left")

        # ── White card ─────────────────────────────────────────────────────────
        card = tk.Frame(self, bg=WHITE, bd=1, relief="solid",
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=28, pady=(8, 28))

        # search
        search_frame = tk.Frame(card, bg=WHITE, pady=12, padx=16)
        search_frame.pack(fill="x")
        search_entry = tk.Entry(search_frame, textvariable=self._search_var,
                                font=("Helvetica", 10), bg="#f9fafb",
                                relief="solid", bd=1,
                                highlightbackground=BORDER,
                                fg=TEXT_GRAY)
        search_entry.insert(0, "Search student...")
        search_entry.pack(fill="x")

        def on_focus_in(e):
            if search_entry.get() == "Search student...":
                search_entry.delete(0, "end")
                search_entry.configure(fg=TEXT_DARK)
        def on_focus_out(e):
            if not search_entry.get():
                search_entry.insert(0, "Search student...")
                search_entry.configure(fg=TEXT_GRAY)
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        # divider
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

        # table header
        hdr_frame = tk.Frame(card, bg="#f9fafb", pady=8)
        hdr_frame.pack(fill="x", padx=16)
        for i, (head, w) in enumerate(zip(self.COL_HEADS, self.COL_WIDTHS)):
            anchor = "w" if i < 6 else "e"
            tk.Label(hdr_frame, text=head, font=("Helvetica", 9, "bold"),
                     bg="#f9fafb", fg=TEXT_DARK, width=w//7,
                     anchor=anchor).grid(row=0, column=i, sticky="w",
                                         padx=(0, 8))

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

        # rows container
        self._rows_frame = tk.Frame(card, bg=WHITE)
        self._rows_frame.pack(fill="both", expand=True, padx=0)

        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        query = self._search_var.get().lower().strip()
        students = self.app._enrolled

        filtered = [s for s in students if
                    query == "" or
                    query == "search student..." or
                    query in s["name"].lower() or
                    str(s["id"]) == query]

        for idx, stu in enumerate(filtered):
            row_bg = WHITE if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(self._rows_frame, bg=row_bg, pady=6)
            row.pack(fill="x", padx=16)
            tk.Frame(self._rows_frame, bg=BORDER, height=1).pack(fill="x")

            # columns
            cells = [
                str(stu["id"]),
                stu["name"],
                stu["section"],
                None,          # badge
                stu["enrolled"],
                stu["graduated"],
                None,          # buttons
            ]

            for col, (val, w) in enumerate(zip(cells, self.COL_WIDTHS)):
                if col == 3:  # status badge
                    badge = _status_badge(row, stu["status"])
                    badge.grid(row=0, column=col, padx=(0, 8), sticky="w")
                elif col == 6:  # action buttons
                    btn_frame = tk.Frame(row, bg=row_bg)
                    btn_frame.grid(row=0, column=col, sticky="e", padx=(0, 4))

                    sid = stu["id"]
                    _btn(btn_frame, "View", BTN_CYAN, BTN_CYAN_HO,
                         lambda s=stu: self.app._show_profile(s),
                         small=True).pack(side="left", padx=2)
                    _btn(btn_frame, "Archive", BTN_GRAY, BTN_GRAY_HO,
                         lambda s=sid: self.app.archive_student(s),
                         small=True).pack(side="left", padx=2)
                    _btn(btn_frame, "Graduate", BTN_GREEN, BTN_GREEN_HO,
                         lambda: None, small=True).pack(side="left", padx=2)
                else:
                    anchor = "w"
                    tk.Label(row, text=val, font=("Helvetica", 9),
                             bg=row_bg, fg=TEXT_DARK, anchor=anchor,
                             width=w//7).grid(row=0, column=col, sticky="w",
                                               padx=(0, 8))


# ═══════════════════════════════════════════════════════════════════════════════
class ArchivedStudentsPage(tk.Frame):
    COL_HEADS  = ["ID", "Student Name", "Section", "Email", "Status", "Archived At", "Actions"]
    COL_WIDTHS = [50, 180, 70, 100, 90, 120, 160]

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        # top bar
        top = tk.Frame(self, bg=BG, pady=20, padx=28)
        top.pack(fill="x")
        tk.Label(top, text="Archived Students",
                 font=("Helvetica", 18, "bold"), bg=BG,
                 fg=TEXT_DARK).pack(side="left")
        _btn(top, "← Back to Students", "#6b7280", "#4b5563",
             lambda: self.app._show_students()).pack(side="right")

        # card
        card = tk.Frame(self, bg=WHITE, bd=1, relief="solid",
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=28, pady=(8, 28))

        # header
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x")
        hdr_frame = tk.Frame(card, bg="#f9fafb", pady=8)
        hdr_frame.pack(fill="x", padx=16)
        for i, (head, w) in enumerate(zip(self.COL_HEADS, self.COL_WIDTHS)):
            tk.Label(hdr_frame, text=head, font=("Helvetica", 9, "bold"),
                     bg="#f9fafb", fg=TEXT_DARK, width=w//7,
                     anchor="w").grid(row=0, column=i, sticky="w", padx=(0, 8))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

        self._rows_frame = tk.Frame(card, bg=WHITE)
        self._rows_frame.pack(fill="both", expand=True)
        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        for idx, stu in enumerate(self.app._archived):
            row_bg = WHITE if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(self._rows_frame, bg=row_bg, pady=6)
            row.pack(fill="x", padx=16)
            tk.Frame(self._rows_frame, bg=BORDER, height=1).pack(fill="x")

            cells = [str(stu["id"]), stu["name"], stu["section"],
                     stu["email"], None, stu["archived_at"], None]

            for col, (val, w) in enumerate(zip(cells, self.COL_WIDTHS)):
                if col == 4:  # status badge
                    badge = _status_badge(row, stu["status"])
                    badge.grid(row=0, column=col, padx=(0, 8), sticky="w")
                elif col == 6:  # action buttons
                    btn_frame = tk.Frame(row, bg=row_bg)
                    btn_frame.grid(row=0, column=col, sticky="e", padx=(0, 4))
                    sid = stu["id"]
                    _btn(btn_frame, "Restore", BTN_GREEN, BTN_GREEN_HO,
                         lambda s=sid: self._restore(s),
                         small=True).pack(side="left", padx=2)
                    _btn(btn_frame, "Delete", BTN_RED, BTN_RED_HO,
                         lambda s=sid: self._delete(s),
                         small=True).pack(side="left", padx=2)
                else:
                    tk.Label(row, text=val, font=("Helvetica", 9),
                             bg=row_bg, fg=TEXT_DARK, anchor="w",
                             width=w//7).grid(row=0, column=col, sticky="w",
                                               padx=(0, 8))

    def _restore(self, sid):
        self.app.restore_student(sid)

    def _delete(self, sid):
        if messagebox.askyesno("Confirm", "Delete this student permanently?"):
            self.app.delete_student(sid)
            self._refresh_rows()


# ═══════════════════════════════════════════════════════════════════════════════
class StudentProfilePage(tk.Frame):
    def __init__(self, parent, app, student_data):
        super().__init__(parent, bg=BG)
        self.app = app
        self.data = student_data
        self.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        # top bar
        top = tk.Frame(self, bg=BG, pady=20, padx=28)
        top.pack(fill="x")
        tk.Label(top, text="Student Profile",
                 font=("Helvetica", 18, "bold"), bg=BG,
                 fg=TEXT_DARK).pack(side="left")
        _btn(top, "← Back to Students", "#6b7280", "#4b5563",
             lambda: self.app._show_students()).pack(side="right")

        # card
        card = tk.Frame(self, bg=WHITE, bd=1, relief="solid",
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=28, pady=(8, 28))

        inner = tk.Frame(card, bg=WHITE, padx=24, pady=20)
        inner.pack(fill="both", expand=True)

        p = self.data

        # ── Child Information ──────────────────────────────────────────────────
        self._section_header(inner, "Child Information")
        self._detail_row(inner, [
            ("Full Name", p.get("full_name", "—")),
            ("Nickname",  p.get("nickname",  "—")),
            ("Birthday",  p.get("birthday",  "—")),
        ])
        self._detail_row(inner, [
            ("Age",     p.get("age",    "—")),
            ("Gender",  p.get("gender", "—")),
            ("Section", p.get("section","—")),
        ])

        # ── Mother's Information ───────────────────────────────────────────────
        self._section_header(inner, "Mother's Information")
        self._detail_row(inner, [
            ("Name",       p.get("mother_name",       "—")),
            ("Occupation", p.get("mother_occupation", "—")),
            ("Contact",    p.get("mother_contact",    "—")),
        ])
        self._detail_row(inner, [
            ("Education",    p.get("mother_education", "—")),
            ("School",       p.get("mother_school",    "—")),
            ("Year Graduated", p.get("mother_graduated","—")),
        ])

        # ── Father's Information ───────────────────────────────────────────────
        self._section_header(inner, "Father's Information")
        self._detail_row(inner, [
            ("Name",       p.get("father_name",       "—")),
            ("Occupation", p.get("father_occupation", "—")),
            ("Contact",    p.get("father_contact",    "—")),
        ])
        self._detail_row(inner, [
            ("Education",    p.get("father_education", "—")),
            ("School",       p.get("father_school",    "—")),
            ("Year Graduated", p.get("father_graduated","—")),
        ])

        # ── Guardian Information ───────────────────────────────────────────────
        self._section_header(inner, "Guardian Information (Optional)")
        self._detail_row(inner, [
            ("Name",       p.get("guardian_name",       "—")),
            ("Occupation", p.get("guardian_occupation", "—")),
            ("Contact",    p.get("guardian_contact",    "—")),
        ])

    def _section_header(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 11, "bold"),
                 bg=WHITE, fg=TEXT_DARK, anchor="w",
                 pady=10).pack(fill="x")
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=(0, 6))

    def _detail_row(self, parent, fields):
        row = tk.Frame(parent, bg=WHITE, pady=4)
        row.pack(fill="x")
        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)
        row.columnconfigure(2, weight=1)

        for col, (label, value) in enumerate(fields):
            cell = tk.Frame(row, bg=WHITE)
            cell.grid(row=0, column=col, sticky="w")

            tk.Label(cell, text=f"{label}: ", font=("Helvetica", 9, "bold"),
                     bg=WHITE, fg=TEXT_DARK).pack(side="left")
            tk.Label(cell, text=value, font=("Helvetica", 9),
                     bg=WHITE, fg=TEXT_DARK).pack(side="left")


# ═══════════════════════════════════════════════════════════════════════════════
# Helper widgets
# ═══════════════════════════════════════════════════════════════════════════════

def _btn(parent, text, bg, hover_bg, command, small=False):
    font_size = 8 if small else 9
    pad_x = 10 if small else 14
    pad_y = 4 if small else 6
    btn = tk.Label(parent, text=text, font=("Helvetica", font_size),
                   bg=bg, fg=WHITE, padx=pad_x, pady=pad_y,
                   cursor="hand2", relief="flat")
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn


def _status_badge(parent, status):
    if status == "Active":
        bg, fg = BTN_GREEN, WHITE
    elif status == "Archived":
        bg, fg = BADGE_GRAY_BG, BADGE_GRAY_FG
    else:
        bg, fg = "#e0e7ff", "#3730a3"

    badge = tk.Label(parent, text=status, font=("Helvetica", 8, "bold"),
                     bg=bg, fg=fg, padx=8, pady=3, relief="flat")
    return badge


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()