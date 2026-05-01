# superadmin_dashboard.py — Super Admin Dashboard shell

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Superadmin.Constants import (
    WHITE, ACCENT, ACCENT_DARK, TEXT_DARK, TEXT_MED, TEXT_GRAY,
    ERROR_RED, SUCCESS_GRN, BORDER_CLR, DASH_BG,
    STAT_BLUE, STAT_GREEN, STAT_CYAN, STAT_YELLOW,
    SIDEBAR_BG, SIDEBAR_ACT, SIDEBAR_HOV, SIDEBAR_SEP,
)

from Admins_page import AdminPage, ArchivedPage, AdminInformationPage, INITIAL_ADMINS
from Teachers_page import TeachersPage, ArchivedTeachersPage, TeacherInformationPage
from Students_page import StudentsPage
from Gamified_page import GamifiedPage

TODAY = date.today().strftime("%Y-%m-%d")


class SuperAdminDashboard:
    def __init__(self, auth_manager, on_logout):
        self.auth = auth_manager
        self.on_logout = on_logout

        self.admins = [dict(a) for a in INITIAL_ADMINS]
        self.archived_admins = []
        self.archived_students = []

        self.win = tk.Toplevel()
        self.win.title("Super Admin Dashboard")
        self.win.geometry("1400x800")
        self.win.minsize(1100, 650)
        self.win.resizable(True, True)
        self.win.protocol("WM_DELETE_WINDOW", self._logout)

        self._active_page = "Dashboard"
        self._sidebar_collapsed = False

        self._build_ui()
        self.win.grab_set()

    # ==========================================================
    # MAIN BUILD
    # ==========================================================
    def _build_ui(self):
        self.win.columnconfigure(1, weight=1)
        self.win.rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()

    # ==========================================================
    # SIDEBAR
    # ==========================================================
    def _build_sidebar(self):
        self.sb = tk.Frame(self.win, bg=SIDEBAR_BG, width=200)
        self.sb.grid(row=0, column=0, sticky="ns")
        self.sb.grid_propagate(False)

        top = tk.Frame(self.sb, bg=SIDEBAR_BG)
        top.pack(fill="x", pady=(14, 0), padx=10)

        tk.Button(
            top,
            text="☰",
            font=("Segoe UI", 14),
            fg=WHITE,
            bg=SIDEBAR_BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=SIDEBAR_HOV,
            activeforeground=WHITE,
            command=self._toggle_sidebar
        ).pack(side="left")

        self.brand_lbl = tk.Label(
            top,
            text="Super Admin",
            font=("Segoe UI", 11, "bold"),
            fg=WHITE,
            bg=SIDEBAR_BG
        )
        self.brand_lbl.pack(side="left", padx=(8, 0))

        tk.Frame(self.sb, bg=SIDEBAR_SEP, height=1).pack(fill="x", pady=(12, 4))

        self._nav_rows = {}
        self._nav_labels = {}

        for label, icon in [
            ("Dashboard", "⊞"),
            ("Admins", "👥"),
            ("Teachers", "🎓"),
            ("Students", "🧑‍🎓"),
            ("Gamified", "🎮"),
        ]:
            self._make_nav_row(label, icon)

        tk.Frame(self.sb, bg=SIDEBAR_BG).pack(fill="both", expand=True)
        tk.Frame(self.sb, bg=SIDEBAR_SEP, height=1).pack(fill="x")

        logout_row = tk.Frame(self.sb, bg=SIDEBAR_BG, cursor="hand2")
        logout_row.pack(fill="x")

        logout_icon = tk.Label(
            logout_row,
            text="🚪",
            font=("Segoe UI", 11),
            fg="#f87171",
            bg=SIDEBAR_BG
        )
        logout_icon.pack(side="left", padx=(16, 6), pady=12)

        self.logout_text = tk.Label(
            logout_row,
            text="Logout",
            font=("Segoe UI", 10),
            fg="#f87171",
            bg=SIDEBAR_BG
        )
        self.logout_text.pack(side="left")

        for w in [logout_row, logout_icon, self.logout_text]:
            w.bind("<Enter>", lambda e, r=logout_row: self._set_row_bg(r, SIDEBAR_HOV))
            w.bind("<Leave>", lambda e, r=logout_row: self._set_row_bg(r, SIDEBAR_BG))
            w.bind("<Button-1>", lambda e: self._logout())

    def _make_nav_row(self, label, icon):
        is_active = self._active_page == label
        bg = SIDEBAR_ACT if is_active else SIDEBAR_BG

        row = tk.Frame(self.sb, bg=bg, cursor="hand2")
        row.pack(fill="x")

        icon_lbl = tk.Label(row, text=icon, font=("Segoe UI", 12), fg=WHITE, bg=bg)
        icon_lbl.pack(side="left", padx=(16, 6), pady=10)

        text_lbl = tk.Label(
            row,
            text=label,
            font=("Segoe UI", 10, "bold" if is_active else "normal"),
            fg=WHITE,
            bg=bg
        )
        text_lbl.pack(side="left")

        self._nav_rows[label] = row
        self._nav_labels[label] = text_lbl

        def click_page(event=None, page_name=label):
            self._active_page = page_name
            self._refresh_nav()
            self._show_page(page_name)

        for w in (row, icon_lbl, text_lbl):
            w.bind("<Button-1>", click_page)
            w.bind(
                "<Enter>",
                lambda e, r=row, lbl=label: self._set_row_bg(r, SIDEBAR_HOV)
                if self._active_page != lbl else None
            )
            w.bind(
                "<Leave>",
                lambda e, r=row, lbl=label: self._set_row_bg(r, SIDEBAR_BG)
                if self._active_page != lbl else None
            )

    def _set_row_bg(self, row, color):
        row.config(bg=color)
        for child in row.winfo_children():
            child.config(bg=color)

    def _refresh_nav(self):
        for label, row in self._nav_rows.items():
            is_active = self._active_page == label
            bg = SIDEBAR_ACT if is_active else SIDEBAR_BG
            self._set_row_bg(row, bg)
            self._nav_labels[label].config(
                font=("Segoe UI", 10, "bold" if is_active else "normal")
            )

    def _toggle_sidebar(self):
        if self._sidebar_collapsed:
            self.sb.config(width=200)
            self.brand_lbl.pack(side="left", padx=(8, 0))
            for lbl in self._nav_labels.values():
                lbl.pack(side="left")
            self.logout_text.pack(side="left")
            self._sidebar_collapsed = False
        else:
            self.brand_lbl.pack_forget()
            for lbl in self._nav_labels.values():
                lbl.pack_forget()
            self.logout_text.pack_forget()
            self.sb.config(width=56)
            self._sidebar_collapsed = True

    # ==========================================================
    # PAGE ROUTING
    # ==========================================================
    def _build_main(self):
        self.main = tk.Frame(self.win, bg="#f5f8ff")
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(0, weight=1)

        self.page_frame = tk.Frame(self.main, bg="#f5f8ff")
        self.page_frame.grid(row=0, column=0, sticky="nsew")
        self.page_frame.columnconfigure(0, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

        self._show_page("Dashboard")

    def _clear_page(self):
        for widget in self.page_frame.winfo_children():
            widget.destroy()

    def _show_page(self, name):
        self._clear_page()

        if name == "Dashboard":
            self._page_dashboard()
        elif name == "Admins":
            self._page_admins()
        elif name == "Teachers":
            self._page_teachers()
        elif name == "Students":
            self._page_students()
        elif name == "Gamified":
            self._page_gamified()
        else:
            self._page_dashboard()
    
    def _page_admins(self):
        def nav(page, admin=None, previous="admins"):
            self._clear_page()

            if page == "archived":
                ArchivedPage(
                    self.page_frame,
                    nav,
                    archived_admins=self.archived_admins,
                    admins=self.admins
                ).grid(row=0, column=0, sticky="nsew")

            elif page == "admin_info":
                AdminInformationPage(
                    self.page_frame,
                    nav,
                    admin,
                    previous
            ).grid(row=0, column=0, sticky="nsew")

            else:
                AdminPage(
                     self.page_frame,
                     nav,
                     admins=self.admins,
                     archived_admins=self.archived_admins
            ).grid(row=0, column=0, sticky="nsew")

        nav("admins")

    def _page_teachers(self):
        def nav(page, teacher=None, previous="teachers"):
            self._clear_page()

            if page == "archived_teachers":
                ArchivedTeachersPage(
                    self.page_frame,
                    nav
                ).grid(row=0, column=0, sticky="nsew")

            elif page == "teacher_info":
                TeacherInformationPage(
                     self.page_frame,
                     nav,
                     teacher,
                     previous
                ).grid(row=0, column=0, sticky="nsew")

            else:
                 TeachersPage(
                    self.page_frame,
                    nav
                ).grid(row=0, column=0, sticky="nsew")

        nav("teachers")

    def _page_students(self):
        StudentsPage(self.page_frame, self.archived_students).show()

    def _page_gamified(self):
        GamifiedPage(self.page_frame).show()

    # ==========================================================
    # DASHBOARD PAGE
    # ==========================================================
    def _page_dashboard(self):
        canvas = tk.Canvas(self.page_frame, bg="#f5f8ff", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.page_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas, bg="#f5f8ff")
        window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        def resize_canvas(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", resize_canvas)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        frame.columnconfigure(0, weight=1)

        content = tk.Frame(frame, bg="#f5f8ff")
        content.grid(row=0, column=0, sticky="ew", padx=32, pady=(20, 28))
        content.columnconfigure(0, weight=1)

        tk.Label(
            content,
            text="Super Admin Dashboard",
            font=("Segoe UI", 22, "bold"),
            fg="#1f2937",
            bg="#f5f8ff"
        ).grid(row=0, column=0, sticky="w", pady=(0, 18))

        self._build_stat_cards(content)
        self._build_register_card(content)

    def _build_stat_cards(self, parent):
        cards_row = tk.Frame(parent, bg="#f5f8ff")
        cards_row.grid(row=1, column=0, sticky="ew", pady=(0, 40))

        for i in range(4):
            cards_row.columnconfigure(i, weight=1)

        try:
            admins_count, teachers_count, _ = self.auth.get_counts()
        except Exception:
            admins_count, teachers_count = 1, 1

        cards = [
            (str(admins_count), "Admins", "👥", "#0d6efd"),
            (str(teachers_count), "Teachers", "🎓", "#198754"),
            ("1", "Enrolled Students", "📋", "#0dcaf0"),
            ("0", "Activities", "🎮", "#ffc107"),
        ]

        for i, (num, label, icon, color) in enumerate(cards):
            shadow = tk.Frame(cards_row, bg="#d9dee8")
            shadow.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0), ipady=1)

            card = tk.Frame(shadow, bg=color, height=76)
            card.pack(fill="x", padx=(0, 2), pady=(0, 2))
            card.pack_propagate(False)

            left = tk.Frame(card, bg=color)
            left.pack(side="left", padx=16, pady=12)

            tk.Label(
                left,
                text=num,
                bg=color,
                fg="white",
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w")

            tk.Label(
                left,
                text=label,
                bg=color,
                fg="white",
                font=("Segoe UI", 9)
            ).pack(anchor="w")

            tk.Label(
                card,
                text=icon,
                bg=color,
                fg="#e8f2ff",
                font=("Segoe UI", 23)
            ).pack(side="right", padx=18)

    def _build_register_card(self, parent):
        shadow = tk.Frame(parent, bg="#e2e8f0")
        shadow.grid(row=2, column=0, sticky="ew")
        shadow.columnconfigure(0, weight=1)

        card = tk.Frame(shadow, bg="white")
        card.grid(row=0, column=0, sticky="ew", padx=(0, 2), pady=(0, 2))
        card.columnconfigure(0, weight=1)

        header = tk.Frame(card, bg="white")
        header.grid(row=0, column=0, sticky="ew", padx=22, pady=(22, 16))
        header.columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="Register New Admin",
            bg="white",
            fg="#0d6efd",
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            header,
            text="Add a new admin account below",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 9)
        ).grid(row=0, column=1, sticky="e")

        body = tk.Frame(card, bg="white")
        body.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 22))
        body.columnconfigure(0, weight=1)

        top = tk.Frame(body, bg="white")
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(0, minsize=300)
        top.columnconfigure(1, weight=1)

        # PROFILE PHOTO
        photo = tk.Frame(top, bg="white")
        photo.grid(row=0, column=0, sticky="nw", padx=(0, 28))

        tk.Label(
            photo,
            text="Profile Photo",
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="center")

        preview = tk.Canvas(photo, width=130, height=130, bg="white", highlightthickness=0)
        preview.pack(pady=(8, 10))
        preview.create_oval(12, 12, 118, 118, fill="white", outline="#e5e7eb", width=1)
        preview.create_text(65, 65, text="👤", font=("Segoe UI", 34), fill="#cbd5e1")

        file_row = tk.Frame(photo, bg="white", highlightthickness=1, highlightbackground="#d1d5db")
        file_row.pack(fill="x")

        tk.Button(
            file_row,
            text="Choose File",
            relief="flat",
            bg="#f8f9fa",
            fg="#111827",
            font=("Segoe UI", 9),
            padx=10,
            pady=5
        ).pack(side="left")

        tk.Label(
            file_row,
            text="No file chosen",
            bg="white",
            fg="#374151",
            font=("Segoe UI", 9),
            padx=10
        ).pack(side="left")

        # RIGHT FORM AREA
        form = tk.Frame(top, bg="white")
        form.grid(row=0, column=1, sticky="ew")
        for c in range(12):
            form.columnconfigure(c, weight=1)

        e_fn = self._field(form, "First Name", 0, 0, 4)
        e_mn = self._field(form, "Middle Name", 0, 4, 4)
        e_ln = self._field(form, "Surname", 0, 8, 4)

        e_bd = self._field(form, "Birth Date", 2, 0, 4, placeholder="mm/dd/yyyy")
        e_age = self._field(form, "Age", 2, 4, 2, disabled=True)

        gender_var = tk.StringVar(value="Select Gender")
        self._combo(form, "Gender", 2, 6, 3, gender_var, ["Select Gender", "Male", "Female", "Other"])

        e_mobile = self._field(form, "Mobile Number", 2, 9, 3, placeholder="09171234567")

        # LOWER ROWS
        lower = tk.Frame(body, bg="white")
        lower.grid(row=1, column=0, sticky="ew", pady=(16, 0))
        for c in range(12):
            lower.columnconfigure(c, weight=1)

        e_email = self._field(lower, "Email Address", 0, 0, 4)
        e_user = self._field(lower, "Username", 0, 4, 4, placeholder="Leave blank to auto-generate")
        e_pw = self._field(lower, "Password", 0, 8, 4, show="•")

        e_cpw = self._field(lower, "Confirm Password", 2, 0, 4, show="•")

        tk.Frame(body, bg="#d1d5db", height=1).grid(row=2, column=0, sticky="ew", pady=22)

        address = tk.Frame(body, bg="white")
        address.grid(row=3, column=0, sticky="ew")
        for c in range(12):
            address.columnconfigure(c, weight=1)

        barangay_var = tk.StringVar(value="Select Barangay")
        barangays = [
            "Select Barangay", "Bagumbayan", "Bambang", "Calzada", "Cembo",
            "Comembo", "East Rembo", "Guadalupe Nuevo", "Guadalupe Viejo",
            "Hagonoy", "Lower Bicutan", "Napindan", "Pembo", "Pinagsama",
            "Rizal", "San Miguel", "Tanyag", "Ususan", "Wawa", "Western Bicutan"
        ]
        self._combo(address, "Barangay", 0, 0, 6, barangay_var, barangays)

        e_addr = self._field(address, "Street Address / Building / House No.", 2, 0, 12)

        msg_var = tk.StringVar()
        msg_lbl = tk.Label(body, textvariable=msg_var, bg="white", font=("Segoe UI", 10))
        msg_lbl.grid(row=4, column=0, sticky="w", pady=(12, 0))

        btns = tk.Frame(body, bg="white")
        btns.grid(row=5, column=0, sticky="w", pady=(12, 0))

        def calc_age(event=None):
            raw = e_bd.get().strip()
            try:
                bday = datetime.strptime(raw, "%m/%d/%Y")
                today = datetime.today()
                age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
                e_age.config(state="normal")
                e_age.delete(0, "end")
                e_age.insert(0, str(age))
                e_age.config(state="disabled")
            except Exception:
                pass

        e_bd.bind("<FocusOut>", calc_age)

        def mobile_digits(event=None):
            value = "".join(ch for ch in e_mobile.get() if ch.isdigit())[:11]
            e_mobile.delete(0, "end")
            e_mobile.insert(0, value)

        e_mobile.bind("<KeyRelease>", mobile_digits)

        def register_admin():
            username = e_user.get().strip()
            mobile = e_mobile.get().strip()

            if username == "Leave blank to auto-generate":
                username = ""
            if mobile == "09171234567":
                mobile = ""

            try:
                ok, msg = self.auth.register_admin(
                    e_fn.get().strip(),
                    e_ln.get().strip(),
                    username,
                    e_pw.get(),
                    e_cpw.get(),
                    middle_name=e_mn.get().strip(),
                    birth_date=e_bd.get().strip(),
                    age=e_age.get().strip(),
                    gender="" if gender_var.get() == "Select Gender" else gender_var.get(),
                    mobile=mobile,
                    email=e_email.get().strip(),
                    barangay="" if barangay_var.get() == "Select Barangay" else barangay_var.get(),
                    address=e_addr.get().strip()
                )
            except Exception as exc:
                ok, msg = False, str(exc)

            msg_lbl.config(fg=SUCCESS_GRN if ok else ERROR_RED)
            msg_var.set(("✔  " if ok else "✘  ") + msg)

        def reset_form():
            for entry in [e_fn, e_mn, e_ln, e_bd, e_email, e_pw, e_cpw, e_addr]:
                entry.delete(0, "end")

            e_age.config(state="normal")
            e_age.delete(0, "end")
            e_age.config(state="disabled")

            e_user.delete(0, "end")
            e_user.insert(0, "Leave blank to auto-generate")
            e_user.config(fg=TEXT_GRAY)

            e_mobile.delete(0, "end")
            e_mobile.insert(0, "09171234567")
            e_mobile.config(fg=TEXT_GRAY)

            gender_var.set("Select Gender")
            barangay_var.set("Select Barangay")
            msg_var.set("")

        tk.Button(
            btns,
            text="Register Admin",
            command=register_admin,
            bg="#0d6efd",
            fg="white",
            activebackground="#0b5ed7",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=22,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btns,
            text="Reset",
            command=reset_form,
            bg="white",
            fg="#6b7280",
            activebackground="#f3f4f6",
            relief="solid",
            bd=1,
            padx=22,
            pady=7,
            cursor="hand2",
            font=("Segoe UI", 9)
        ).pack(side="left")

    def _field(self, parent, label, row, col, span, placeholder="", show="", disabled=False):
        tk.Label(
            parent,
            text=label,
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 9),
            anchor="w"
        ).grid(row=row, column=col, columnspan=span, sticky="ew", padx=(0, 14), pady=(0, 6))

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg="#e9ecef" if disabled else "white",
            fg=TEXT_GRAY if placeholder else "#111827",
            relief="solid",
            bd=1,
            show=show,
            disabledbackground="#e9ecef",
            disabledforeground="#6b7280"
        )
        entry.grid(row=row + 1, column=col, columnspan=span, sticky="ew", padx=(0, 14), pady=(0, 16), ipady=7)

        if placeholder:
            entry.insert(0, placeholder)

            def focus_in(event, e=entry, p=placeholder):
                if e.get() == p:
                    e.delete(0, "end")
                    e.config(fg="#111827")

            def focus_out(event, e=entry, p=placeholder):
                if not e.get():
                    e.insert(0, p)
                    e.config(fg=TEXT_GRAY)

            entry.bind("<FocusIn>", focus_in)
            entry.bind("<FocusOut>", focus_out)

        if disabled:
            entry.config(state="disabled")

        return entry

    def _combo(self, parent, label, row, col, span, variable, values):
        tk.Label(
            parent,
            text=label,
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 9),
            anchor="w"
        ).grid(row=row, column=col, columnspan=span, sticky="ew", padx=(0, 14), pady=(0, 6))

        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo.grid(row=row + 1, column=col, columnspan=span, sticky="ew", padx=(0, 14), pady=(0, 16), ipady=5)
        return combo

    # ==========================================================
    # LOGOUT
    # ==========================================================
    def _logout(self):
        try:
            self.auth.logout()
        except Exception:
            pass

        try:
            self.win.grab_release()
        except Exception:
            pass

        self.win.destroy()

        if self.on_logout:
            self.on_logout()