from __future__ import annotations

from datetime import datetime
import customtkinter as ctk

# This file is intentionally separate from the main admin dashboard.
# The Admin Dashboard imports these page classes and passes `app` into them.
# Required app attributes/methods:
#   app._enrollments
#   app._enrollment_filter
#   app.show_page("Enrollment")
#   app.show_open_enrollment_page()
#   app.show_enrollment_details_page(id)
#   app.approve_enrollment(id, details=False)
#   app.reject_enrollment(id, details=False)
#   app.delete_enrollment(id)
#   app.save_enrollment(data)

DASH_BG = "#f4f6f9"
WHITE = "#ffffff"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6b7280"
S_BORDER = "#d9dee8"

SIDEBAR_ACT = "#0d6efd"
SIDEBAR_HOV = "#2563eb"

BTN_GREEN = "#198754"
BTN_GREEN_H = "#157347"
BTN_RED = "#dc3545"
BTN_RED_H = "#bb2d3b"
BTN_DARK = "#4b5563"
BTN_DARK_H = "#374151"
BTN_GRAY = "#9ca3af"
BTN_GRAY_H = "#6b7280"
BTN_CYAN = "#06b6d4"
BTN_CYAN_H = "#0891b2"

DEFAULT_ENROLLMENTS = [
    {"id": 2, "name": "Dennielle Pilapil Cruz", "date_applied": "2025-10-29 00:00", "status": "Approved",
     "child_first": "Dennielle", "child_middle": "Pilapil", "child_last": "Cruz", "nickname": "denden",
     "birthday": "2006-07-23", "age": "19", "gender": "Male", "street": "Street 2 House 2", "barangay": "Bulilan Sur",
     "mother_name": "Dennielle Pilapil Cruz", "mother_occupation": "ofw", "mother_contact": "09276426345",
     "mother_education": "Vocational", "mother_school": "ACTS COMPUTER COLLEGE", "mother_graduated": "2000",
     "father_name": "Dennielle Pilapil Cruz", "father_occupation": "ofw", "father_contact": "09276426345",
     "father_education": "College", "father_school": "LSPU", "father_graduated": "2000",
     "guardian_name": "Dennielle Pilapil Cruz", "guardian_occupation": "Deceased", "guardian_contact": "09275858837"},
    {"id": 1, "name": "Dhenzel rain Pilapil Cruz", "date_applied": "2025-10-29 00:00", "status": "Approved",
     "child_first": "Dhenzel rain", "child_middle": "Pilapil", "child_last": "Cruz", "nickname": "",
     "birthday": "2006-07-23", "age": "19", "gender": "Male", "street": "", "barangay": "",
     "mother_name": "Dennielle Pilapil Cruz", "mother_occupation": "ofw", "mother_contact": "09276426345",
     "mother_education": "Vocational", "mother_school": "ACTS COMPUTER COLLEGE", "mother_graduated": "2000",
     "father_name": "Dennielle Pilapil Cruz", "father_occupation": "ofw", "father_contact": "09276426345",
     "father_education": "College", "father_school": "LSPU", "father_graduated": "2000",
     "guardian_name": "Dennielle Pilapil Cruz", "guardian_occupation": "Deceased", "guardian_contact": "09275858837"},
]


class EnrollmentBasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=DASH_BG, corner_radius=0)

    def create_card(self, parent, height=None):
        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            border_color=S_BORDER,
            border_width=1,
            corner_radius=8,
        )
        if height:
            card.configure(height=height)
            card.pack_propagate(False)
        return card


def _enroll_button(parent, text, bg, hover_bg, command, width=80, small=False):
    return ctk.CTkButton(
        parent,
        text=text,
        height=26 if small else 34,
        width=width,
        corner_radius=7,
        fg_color=bg,
        hover_color=hover_bg,
        text_color=WHITE,
        font=ctk.CTkFont(family="Segoe UI", size=10 if small else 12, weight="bold"),
        command=command,
    )


def _separator(parent):
    ctk.CTkFrame(parent, fg_color=S_BORDER, height=1, corner_radius=0).pack(fill="x")


def _configure_table_columns(frame, widths):
    for i, weight in enumerate(widths):
        frame.grid_columnconfigure(i, weight=weight, uniform="table")


def _make_search_bar(parent, textvariable, placeholder="Search student..."):
    box = ctk.CTkFrame(
        parent,
        fg_color=WHITE,
        border_color=S_BORDER,
        border_width=1,
        corner_radius=8,
        height=40,
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
        textvariable=textvariable,
        placeholder_text=placeholder,
        fg_color=WHITE,
        border_width=0,
        text_color=TEXT_DARK,
        placeholder_text_color=TEXT_GRAY,
        height=34,
        corner_radius=0,
        font=ctk.CTkFont(family="Segoe UI", size=12),
    )
    entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=2)

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
        command=lambda: textvariable.set(""),
    )
    clear_btn.grid(row=0, column=2, sticky="e", padx=(0, 10))
    clear_btn.grid_remove()

    def toggle_clear(*_):
        if textvariable.get().strip():
            clear_btn.grid()
        else:
            clear_btn.grid_remove()

    textvariable.trace_add("write", toggle_clear)
    toggle_clear()
    return box


def _enroll_status_badge(parent, status):
    cfg = {"Approved": (BTN_GREEN, WHITE), "Pending": ("#f59e0b", WHITE), "Rejected": (BTN_RED, WHITE)}
    bg, fg = cfg.get(status, (BTN_DARK, WHITE))
    return ctk.CTkLabel(parent, text=status, fg_color=bg, text_color=fg, corner_radius=6,
                        width=78, height=22,
                        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"))


def _enroll_title(parent, text, color=SIDEBAR_ACT):
    ctk.CTkLabel(parent, text=text, fg_color=WHITE, text_color=color,
                 font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
                 anchor="w").pack(fill="x", pady=(8, 8))
    ctk.CTkFrame(parent, fg_color=S_BORDER, height=1, corner_radius=0).pack(fill="x", pady=(0, 14))


def _detail_cell(parent, label, value):
    row = ctk.CTkFrame(parent, fg_color=WHITE)
    row.pack(anchor="w", pady=3)
    ctk.CTkLabel(row, text=f"{label}: ", fg_color=WHITE, text_color=TEXT_DARK,
                 font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")).pack(side="left")
    ctk.CTkLabel(row, text=value or "—", fg_color=WHITE, text_color=TEXT_DARK,
                 font=ctk.CTkFont(family="Segoe UI", size=12)).pack(side="left")


class EnrollmentManagementPage(EnrollmentBasePage):
    HEADS = ["ID", "Name", "Date Applied", "Status", "Actions"]
    WIDTHS = [6, 34, 24, 16, 24]

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_rows())
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=DASH_BG)
        top.pack(fill="x", padx=32, pady=(28, 12))
        top.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(top, text="Enrollment Management", fg_color=DASH_BG, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")
        _enroll_button(top, "+ Open Enrollment", SIDEBAR_ACT, SIDEBAR_HOV,
                        self.app.show_open_enrollment_page, width=160).grid(row=0, column=1, sticky="e")

        card = self.create_card(self)
        card.pack(fill="both", expand=False, padx=32, pady=(0, 28))

        tools = ctk.CTkFrame(card, fg_color=WHITE)
        tools.pack(fill="x", padx=16, pady=14)
        tools.grid_columnconfigure(0, weight=1)

        self._search_entry = _make_search_bar(tools, self._search_var, "Search student...")
        self._search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.filter_menu = ctk.CTkOptionMenu(
            tools, values=["All", "Approved", "Pending", "Rejected"], width=170, height=40,
            fg_color=WHITE, button_color=WHITE, button_hover_color="#eef2f7",
            text_color=TEXT_DARK, dropdown_fg_color=WHITE, dropdown_text_color=TEXT_DARK,
            dropdown_hover_color="#eef2f7", font=ctk.CTkFont(family="Segoe UI", size=12),
            command=self._set_filter)
        self.filter_menu.set(self.app._enrollment_filter if self.app._enrollment_filter != "All" else "Filter Status")
        self.filter_menu.grid(row=0, column=1, sticky="e")

        _separator(card)
        self._rows_frame = ctk.CTkFrame(card, fg_color=WHITE, corner_radius=0)
        self._rows_frame.pack(fill="x", padx=16, pady=(0, 16))
        self._refresh_rows()

    def _set_filter(self, value):
        self.app._enrollment_filter = "All" if value == "Filter Status" else value
        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        hdr = ctk.CTkFrame(self._rows_frame, fg_color="#f9fafb", corner_radius=0)
        hdr.pack(fill="x")
        _configure_table_columns(hdr, self.WIDTHS)
        for i, h in enumerate(self.HEADS):
            ctk.CTkLabel(hdr, text=h, fg_color="#f9fafb", text_color=TEXT_DARK,
                         font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                         anchor="e" if h == "Actions" else "w").grid(row=0, column=i, sticky="ew", padx=(8, 6), pady=10)

        rows = list(self.app._enrollments)
        if self.app._enrollment_filter != "All":
            rows = [e for e in rows if e["status"] == self.app._enrollment_filter]

        q = self._search_var.get().lower().strip()
        if q:
            rows = [e for e in rows if q in e["name"].lower() or q == str(e["id"])]

        for e in rows:
            self._row(e)

    def _row(self, e):
        row = ctk.CTkFrame(self._rows_frame, fg_color=WHITE, corner_radius=0)
        row.pack(fill="x")
        _configure_table_columns(row, self.WIDTHS)

        vals = [str(e["id"]), e["name"], e["date_applied"]]
        for col, val in enumerate(vals):
            ctk.CTkLabel(row, text=val, fg_color=WHITE, text_color=TEXT_DARK,
                         font=ctk.CTkFont(family="Segoe UI", size=12),
                         anchor="w").grid(row=0, column=col, sticky="ew", padx=(8, 6), pady=10)

        status_cell = ctk.CTkFrame(row, fg_color=WHITE)
        status_cell.grid(row=0, column=3, sticky="ew", padx=(8, 6), pady=8)
        _enroll_status_badge(status_cell, e["status"]).pack(anchor="w")

        act = ctk.CTkFrame(row, fg_color=WHITE)
        act.grid(row=0, column=4, sticky="e", padx=(8, 6), pady=7)
        eid = e["id"]
        _enroll_button(act, "View", BTN_CYAN, BTN_CYAN_H, lambda i=eid: self.app.show_enrollment_details_page(i), width=54, small=True).pack(side="left", padx=2)
        _enroll_button(act, "Approve", BTN_GRAY if e["status"] == "Approved" else BTN_GREEN,
                        BTN_GRAY_H if e["status"] == "Approved" else BTN_GREEN_H,
                        lambda i=eid: self.app.approve_enrollment(i), width=70, small=True).pack(side="left", padx=2)
        _enroll_button(act, "Reject", BTN_GRAY, BTN_GRAY_H, lambda i=eid: self.app.reject_enrollment(i), width=62, small=True).pack(side="left", padx=2)
        _enroll_button(act, "Delete", BTN_RED, BTN_RED_H, lambda i=eid: self.app.delete_enrollment(i), width=62, small=True).pack(side="left", padx=2)
        ctk.CTkFrame(self._rows_frame, fg_color=S_BORDER, height=1, corner_radius=0).pack(fill="x")


class EnrollmentDetailsPage(EnrollmentBasePage):
    def __init__(self, parent, app, enrollment: dict):
        super().__init__(parent)
        self.app = app
        self.enrollment = enrollment
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=DASH_BG)
        header.pack(fill="x", padx=80, pady=(28, 12))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Enrollment Details", fg_color=DASH_BG, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")
        _enroll_button(header, "← Back to Enrollment List", BTN_DARK, BTN_DARK_H,
                        lambda: self.app.show_page("Enrollment"), width=200).grid(row=0, column=1, sticky="e")

        scroll = ctk.CTkScrollableFrame(self, fg_color=DASH_BG, corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=80, pady=(0, 28))

        self._info_card(scroll, "Child Information", [
            [("First Name", self.enrollment.get("child_first", "")), ("Middle Name", self.enrollment.get("child_middle", "")), ("Last Name", self.enrollment.get("child_last", ""))],
            [("Nickname", self.enrollment.get("nickname", "")), ("Birthday", self.enrollment.get("birthday", "")), ("Age", self.enrollment.get("age", "")), ("Gender", self.enrollment.get("gender", ""))]
        ])

        self._info_card(scroll, "Mother's Information", [
            [("Name", self.enrollment.get("mother_name", "")), ("Occupation", self.enrollment.get("mother_occupation", "")), ("Contact", self.enrollment.get("mother_contact", ""))],
            [("Highest Education", self.enrollment.get("mother_education", "")), ("School", self.enrollment.get("mother_school", "")), ("Year Graduated", self.enrollment.get("mother_graduated", ""))]
        ], education=True)

        self._info_card(scroll, "Father's Information", [
            [("Name", self.enrollment.get("father_name", "")), ("Occupation", self.enrollment.get("father_occupation", "")), ("Contact", self.enrollment.get("father_contact", ""))],
            [("Highest Education", self.enrollment.get("father_education", "")), ("School", self.enrollment.get("father_school", "")), ("Year Graduated", self.enrollment.get("father_graduated", ""))]
        ], education=True)

        self._info_card(scroll, "Guardian Information (Optional)", [
            [("Name", self.enrollment.get("guardian_name", "")), ("Occupation", self.enrollment.get("guardian_occupation", "")), ("Contact", self.enrollment.get("guardian_contact", ""))]
        ])

        card = self.create_card(scroll)
        card.pack(fill="x", pady=(0, 16))
        inner = ctk.CTkFrame(card, fg_color=WHITE)
        inner.pack(fill="x", padx=20, pady=18)
        _enroll_title(inner, "Application Status")
        row = ctk.CTkFrame(inner, fg_color=WHITE)
        row.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(row, text="Status:", fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")).pack(side="left")
        _enroll_status_badge(row, self.enrollment.get("status", "Pending")).pack(side="left", padx=(8, 0))

        btns = ctk.CTkFrame(inner, fg_color=WHITE)
        btns.pack(anchor="w")
        _enroll_button(btns, "Approve", BTN_GREEN, BTN_GREEN_H,
                        lambda: self.app.approve_enrollment(self.enrollment["id"], details=True), width=85).pack(side="left", padx=(0, 8))
        _enroll_button(btns, "Reject", BTN_RED, BTN_RED_H,
                        lambda: self.app.reject_enrollment(self.enrollment["id"], details=True), width=85).pack(side="left")

    def _info_card(self, parent, title, rows, education=False):
        card = self.create_card(parent)
        card.pack(fill="x", pady=(0, 16))
        inner = ctk.CTkFrame(card, fg_color=WHITE)
        inner.pack(fill="x", padx=20, pady=18)
        _enroll_title(inner, title)
        for i, fields in enumerate(rows):
            if education and i == 1:
                ctk.CTkLabel(inner, text="Educational Background", fg_color=WHITE, text_color=TEXT_GRAY,
                             font=ctk.CTkFont(family="Segoe UI", size=12), anchor="w").pack(fill="x", pady=(6, 2))
            self._detail_row(inner, fields)

    def _detail_row(self, parent, fields):
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(fill="x", pady=4)
        for i in range(len(fields)):
            row.grid_columnconfigure(i, weight=1, uniform="details")
        for i, (label, value) in enumerate(fields):
            cell = ctk.CTkFrame(row, fg_color=WHITE)
            cell.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))
            _detail_cell(cell, label, value)


class OpenEnrollmentPage(EnrollmentBasePage):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.entries = {}
        self.dropdowns = {}
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=DASH_BG)
        header.pack(fill="x", padx=80, pady=(38, 16))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Open Enrollment", fg_color=DASH_BG, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")
        _enroll_button(header, "← Back to Enrollment List", BTN_DARK, BTN_DARK_H,
                        lambda: self.app.show_page("Enrollment"), width=200).grid(row=0, column=1, sticky="e")

        card = self.create_card(self)
        card.pack(fill="both", expand=True, padx=80, pady=(0, 28))
        scroll = ctk.CTkScrollableFrame(card, fg_color=WHITE, corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=18, pady=18)

        self._child(scroll)
        self._parent(scroll, "Mother's Information", BTN_GREEN, "mother")
        self._parent(scroll, "Father's Information", BTN_CYAN, "father")
        self._guardian(scroll)

        btns = ctk.CTkFrame(scroll, fg_color=WHITE)
        btns.pack(fill="x", pady=(18, 0))
        _enroll_button(btns, "Save", BTN_GREEN, BTN_GREEN_H, self._save, width=80).pack(side="right", padx=(8, 0))
        _enroll_button(btns, "Cancel", BTN_DARK, BTN_DARK_H, lambda: self.app.show_page("Enrollment"), width=90).pack(side="right")

    def _field(self, parent, key, label, r, c, span=1):
        wrap = ctk.CTkFrame(parent, fg_color=WHITE)
        wrap.grid(row=r, column=c, columnspan=span, sticky="ew", padx=(0 if c == 0 else 10, 0), pady=(0, 12))
        ctk.CTkLabel(wrap, text=label, fg_color=WHITE, text_color=TEXT_DARK, anchor="w",
                     font=ctk.CTkFont(family="Segoe UI", size=12)).pack(fill="x", pady=(0, 5))
        e = ctk.CTkEntry(wrap, height=34, corner_radius=6, border_color=S_BORDER, fg_color=WHITE, text_color=TEXT_DARK)
        e.pack(fill="x")
        self.entries[key] = e

    def _dropdown(self, parent, key, label, values, default, r, c, span=1):
        wrap = ctk.CTkFrame(parent, fg_color=WHITE)
        wrap.grid(row=r, column=c, columnspan=span, sticky="ew", padx=(0 if c == 0 else 10, 0), pady=(0, 12))
        ctk.CTkLabel(wrap, text=label, fg_color=WHITE, text_color=TEXT_DARK, anchor="w",
                     font=ctk.CTkFont(family="Segoe UI", size=12)).pack(fill="x", pady=(0, 5))
        d = ctk.CTkOptionMenu(wrap, values=values, height=34, fg_color=WHITE, button_color=WHITE,
                              button_hover_color="#eef2f7", text_color=TEXT_DARK,
                              dropdown_fg_color=WHITE, dropdown_text_color=TEXT_DARK)
        d.set(default)
        d.pack(fill="x")
        self.dropdowns[key] = d

    def _child(self, parent):
        _enroll_title(parent, "Child Information", SIDEBAR_ACT)
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(fill="x", pady=(0, 22))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=3)

        photo = ctk.CTkFrame(row, fg_color=WHITE)
        photo.grid(row=0, column=0, sticky="new", padx=(0, 20))
        preview = ctk.CTkFrame(photo, fg_color="#f8fafc", border_color=S_BORDER, border_width=1, width=130, height=130, corner_radius=6)
        preview.pack(anchor="center", pady=(0, 10))
        preview.pack_propagate(False)
        ctk.CTkLabel(photo, text="Upload Photo", fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")).pack(anchor="center", pady=(0, 6))
        fake = ctk.CTkFrame(photo, fg_color=WHITE, border_color=S_BORDER, border_width=1, corner_radius=6)
        fake.pack(fill="x")
        ctk.CTkLabel(fake, text="Choose File", fg_color="#f8fafc", text_color=TEXT_DARK, width=90, height=32).pack(side="left")
        ctk.CTkLabel(fake, text="No file chosen", fg_color=WHITE, text_color=TEXT_DARK, width=120, height=32).pack(side="left")

        grid = ctk.CTkFrame(row, fg_color=WHITE)
        grid.grid(row=0, column=1, sticky="nsew")
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1, uniform="child")
        self._field(grid, "child_first", "First Name *", 0, 0)
        self._field(grid, "child_middle", "Middle Name", 0, 1)
        self._field(grid, "child_last", "Last Name *", 0, 2)
        self._field(grid, "nickname", "Nickname", 1, 0)
        self._field(grid, "birthday", "Birthday *", 1, 1)
        self._field(grid, "age", "Age", 1, 2)
        self._dropdown(grid, "gender", "Gender *", ["Select", "Male", "Female"], "Select", 2, 0)
        self._field(grid, "street", "Street *", 2, 1, span=2)
        self._dropdown(grid, "barangay", "Barangay *", ["Select Barangay", "Bulilan Sur", "Bulilan Norte"], "Select Barangay", 3, 0, span=2)

    def _parent(self, parent, title, color, p):
        _enroll_title(parent, title, color)
        g = ctk.CTkFrame(parent, fg_color=WHITE)
        g.pack(fill="x", pady=(0, 22))
        for i in range(3):
            g.grid_columnconfigure(i, weight=1, uniform=p)
        self._field(g, f"{p}_first", "First Name *", 0, 0)
        self._field(g, f"{p}_middle", "Middle Name", 0, 1)
        self._field(g, f"{p}_last", "Last Name *", 0, 2)
        self._field(g, f"{p}_occupation", "Occupation *", 1, 0, span=2)
        self._field(g, f"{p}_contact", "Contact No. *", 1, 2)
        self._field(g, f"{p}_street", "Street", 2, 0, span=2)
        self._dropdown(g, f"{p}_barangay", "Barangay", ["Select Barangay", "Bulilan Sur", "Bulilan Norte"], "Select Barangay", 2, 2)
        ctk.CTkLabel(g, text="Educational Background", fg_color=WHITE, text_color=TEXT_GRAY,
                     font=ctk.CTkFont(family="Segoe UI", size=12), anchor="w").grid(row=3, column=0, sticky="w", pady=(10, 4))
        self._field(g, f"{p}_education", "Highest Education", 4, 0)
        self._field(g, f"{p}_school", "School", 4, 1)
        self._field(g, f"{p}_graduated", "Year Graduated", 4, 2)

    def _guardian(self, parent):
        _enroll_title(parent, "Guardian Information (Optional)", "#facc15")
        g = ctk.CTkFrame(parent, fg_color=WHITE)
        g.pack(fill="x")
        for i in range(3):
            g.grid_columnconfigure(i, weight=1, uniform="guardian")
        self._field(g, "guardian_first", "First Name", 0, 0)
        self._field(g, "guardian_middle", "Middle Name", 0, 1)
        self._field(g, "guardian_last", "Last Name", 0, 2)
        self._field(g, "guardian_occupation", "Occupation", 1, 0, span=2)
        self._field(g, "guardian_contact", "Contact No.", 1, 2)
        self._field(g, "guardian_street", "Street", 2, 0, span=2)
        self._dropdown(g, "guardian_barangay", "Barangay", ["Select Barangay", "Bulilan Sur", "Bulilan Norte"], "Select Barangay", 2, 2)

    def _save(self):
        data = {k: e.get() for k, e in self.entries.items()}
        for k, d in self.dropdowns.items():
            data[k] = d.get()
        data["mother_name"] = " ".join(p for p in [data.get("mother_first", ""), data.get("mother_middle", ""), data.get("mother_last", "")] if p).strip()
        data["father_name"] = " ".join(p for p in [data.get("father_first", ""), data.get("father_middle", ""), data.get("father_last", "")] if p).strip()
        data["guardian_name"] = " ".join(p for p in [data.get("guardian_first", ""), data.get("guardian_middle", ""), data.get("guardian_last", "")] if p).strip()
        data["mother_education"] = data.get("mother_education", "")
        data["mother_school"] = data.get("mother_school", "")
        data["mother_graduated"] = data.get("mother_graduated", "")
        data["father_education"] = data.get("father_education", "")
        data["father_school"] = data.get("father_school", "")
        data["father_graduated"] = data.get("father_graduated", "")
        data["mother_occupation"] = data.get("mother_occupation", "")
        data["mother_contact"] = data.get("mother_contact", "")
        data["father_occupation"] = data.get("father_occupation", "")
        data["father_contact"] = data.get("father_contact", "")
        self.app.save_enrollment(data)

