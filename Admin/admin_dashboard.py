import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
try:
    # Kapag admin_dashboard.py is imported as Admin.admin_dashboard from root main.py
    from .Enrollment import EnrollmentManagementPage, EnrollmentDetailsPage, OpenEnrollmentPage, DEFAULT_ENROLLMENTS
except ImportError:
    # Kapag admin_dashboard.py is run directly inside the Admin folder
    from Enrollment import EnrollmentManagementPage, EnrollmentDetailsPage, OpenEnrollmentPage, DEFAULT_ENROLLMENTS

# ── App setup ─────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── Colors ────────────────────────────────────────────────────────────────────
WHITE       = "#ffffff"
SIDEBAR_BG  = "#1d3153"
SIDEBAR_ACT = "#2563eb"
SIDEBAR_HOV = "#27446f"
SIDEBAR_SEP = "#2f4770"
DASH_BG     = "#f5f8ff"

S_BORDER    = "#dbe1ea"
BTN_CYAN    = "#00b4d8"
BTN_CYAN_H  = "#0096b7"
BTN_GRAY    = "#9ca3af"
BTN_GRAY_H  = "#6b7280"
BTN_GREEN   = "#22c55e"
BTN_GREEN_H = "#16a34a"
BTN_RED     = "#ef4444"
BTN_RED_H   = "#dc2626"
BTN_DARK    = "#4b5563"
BTN_DARK_H  = "#374151"
TEXT_DARK   = "#111827"
TEXT_GRAY   = "#6b7280"

# ── Seed data ─────────────────────────────────────────────────────────────────
_DEFAULT_ENROLLED = [
    {"id": 2, "name": "Dennielle Cruz", "section": "B",
     "status": "Active", "enrolled": "Oct 29, 2025", "graduated": "—"},
]

_DEFAULT_ARCHIVED = [
    {"id": 1, "name": "Dhenzel rain Cruz", "section": "A",
     "email": "—", "status": "Archived", "archived_at": "—"},
]

_DEFAULT_PROFILE = {
    "full_name": "Dennielle Pilapil Cruz", "nickname": "denden",
    "birthday": "2006-07-23", "age": "19", "gender": "Male", "section": "B",
    "mother_name": "Dennielle Pilapil Cruz", "mother_occupation": "ofw",
    "mother_contact": "09276426345", "mother_education": "Vocational",
    "mother_school": "ACTS COMPUTER COLLEGE", "mother_graduated": "2000",
    "father_name": "Dennielle Pilapil Cruz", "father_occupation": "ofw",
    "father_contact": "09276426345", "father_education": "College",
    "father_school": "LSPU", "father_graduated": "2000",
    "guardian_name": "Dennielle Pilapil Cruz",
    "guardian_occupation": "Deceased", "guardian_contact": "09275858837",
}

_DEFAULT_TEACHERS = [
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

_DEFAULT_ARCHIVED_TEACHERS = [
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


_DEFAULT_STUDENT_ACCOUNTS = [
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



class MainApp(ctk.CTk):
    def __init__(self, auth_manager=None, on_logout=None):
        super().__init__()

        self.auth = auth_manager
        self.on_logout = on_logout

        current = {}
        if self.auth and getattr(self.auth, "current_user", None):
            current = self.auth.users.get(self.auth.current_user, {})

        self.first_name  = current.get("first_name", "Christian Joseph")
        self.last_name   = current.get("last_name", "Aquino")
        self.role        = current.get("role", "Admin")
        self.full_name   = f"{self.first_name} {self.last_name}"
        self.middle_name = current.get("middle_name", "")
        self.birth_date  = current.get("birth_date", "")
        self.age         = current.get("age", "")
        self.gender      = current.get("gender", "")
        self.mobile      = current.get("mobile", "")
        self.email       = current.get("email", "")
        self.barangay    = current.get("barangay", "")
        self.address     = current.get("address", "")

        self._enrolled = list(_DEFAULT_ENROLLED)
        self._archived = list(_DEFAULT_ARCHIVED)
        self._profile = dict(_DEFAULT_PROFILE)

        # Teachers data connected to the same dashboard state
        self._teachers = [dict(t) for t in _DEFAULT_TEACHERS]
        self._archived_teachers = [dict(t) for t in _DEFAULT_ARCHIVED_TEACHERS]

        # Student accounts data connected to the same dashboard state
        self._student_accounts = [dict(a) for a in _DEFAULT_STUDENT_ACCOUNTS]
        self._student_accounts_show_all = False

        # Enrollment data connected to the same dashboard state
        self._enrollments = [dict(e) for e in DEFAULT_ENROLLMENTS]
        self._enrollment_filter = "All"

        self.title("Admin Dashboard")
        self.geometry("1500x780")
        self.minsize(1100, 650)
        self.configure(fg_color=DASH_BG)

        self._active_page = "Dashboard"
        self._sidebar_collapsed = False

        self._sidebar_width_open = 260
        self._sidebar_width_closed = 66

        self.grid_columnconfigure(0, weight=0, minsize=self._sidebar_width_open)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self.show_page("Dashboard")

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            fg_color=SIDEBAR_BG,
            width=self._sidebar_width_open,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # Use GRID inside the sidebar for a stable full-height rail.
        # Rows:
        # 0 = burger/header
        # 1 = separator
        # 2 = profile box
        # 3 = nav buttons
        # 4 = spacer
        # 5 = separator
        # 6 = logout
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.top_bar = ctk.CTkFrame(self.sidebar, fg_color=SIDEBAR_BG, corner_radius=0)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(14, 0))
        self.top_bar.grid_columnconfigure(1, weight=1)

        self.burger_btn = ctk.CTkButton(
            self.top_bar,
            text="☰",
            width=46,
            height=40,
            corner_radius=8,
            fg_color=SIDEBAR_BG,
            hover_color=SIDEBAR_HOV,
            text_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            command=self.toggle_sidebar
        )
        self.burger_btn.grid(row=0, column=0, sticky="w")

        self.brand_lbl = ctk.CTkLabel(
            self.top_bar,
            text="Admin Panel",
            text_color=WHITE,
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold")
        )
        self.brand_lbl.grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.sidebar_sep_top = ctk.CTkFrame(
            self.sidebar,
            fg_color=SIDEBAR_SEP,
            height=1,
            corner_radius=0
        )
        self.sidebar_sep_top.grid(row=1, column=0, sticky="ew", pady=(12, 4))

        self.profile_box = ctk.CTkFrame(self.sidebar, fg_color=SIDEBAR_BG, corner_radius=0)
        self.profile_box.grid(row=2, column=0, sticky="ew", pady=(18, 20))
        self.profile_box.grid_columnconfigure(0, weight=1)

        self.profile_avatar = ctk.CTkLabel(
            self.profile_box,
            text="👤",
            width=82,
            height=82,
            fg_color=SIDEBAR_BG,
            text_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI Emoji", size=36),
            corner_radius=41
        )
        self.profile_avatar.grid(row=0, column=0, pady=(0, 6))

        self.profile_name = ctk.CTkLabel(
            self.profile_box,
            text=self.full_name,
            text_color=WHITE,
            fg_color=SIDEBAR_BG,
            wraplength=190,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.profile_name.grid(row=1, column=0, pady=(2, 0))

        self.profile_role = ctk.CTkLabel(
            self.profile_box,
            text=self.role,
            text_color="#dbeafe",
            fg_color=SIDEBAR_BG,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.profile_role.grid(row=2, column=0)

        self.profile_link = ctk.CTkButton(
            self.profile_box,
            text="View Profile →",
            width=150,
            height=30,
            fg_color=SIDEBAR_BG,
            hover_color=SIDEBAR_HOV,
            text_color="#fde047",
            command=self.show_profile
        )
        self.profile_link.grid(row=3, column=0, pady=(5, 0))

        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color=SIDEBAR_BG, corner_radius=0)
        self.nav_frame.grid(row=3, column=0, sticky="ew")
        self.nav_frame.grid_columnconfigure(0, weight=1)

        self.nav_rows = {}
        self.nav_texts = {}

        menu = [
            ("Dashboard", "⊞"),
            ("Teachers", "▣"),
            ("Students", "🎓"),
            ("Student Accounts", "👥"),
            ("Activities", "▤"),
            ("Enrollment", "□"),
            ("Reports", "▥"),
        ]
        for label, icon in menu:
            self._make_nav_row(label, icon)

        self.sidebar_spacer = ctk.CTkFrame(self.sidebar, fg_color=SIDEBAR_BG, corner_radius=0)
        self.sidebar_spacer.grid(row=4, column=0, sticky="nsew")

        self.sidebar_sep_bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color=SIDEBAR_SEP,
            height=1,
            corner_radius=0
        )
        self.sidebar_sep_bottom.grid(row=5, column=0, sticky="ew")

        self.logout_row = ctk.CTkButton(
            self.sidebar,
            text="↩  Logout",
            width=self._sidebar_width_open,
            height=54,
            corner_radius=0,
            fg_color=SIDEBAR_BG,
            hover_color=SIDEBAR_HOV,
            text_color="#fca5a5",
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            command=self.logout
        )
        self.logout_row.grid(row=6, column=0, sticky="ew")

    def _make_nav_row(self, label, icon):
        is_active = self._active_page == label
        row = ctk.CTkButton(
            self.nav_frame,
            text=f"{icon}  {label}",
            width=self._sidebar_width_open,
            height=52,
            corner_radius=0,
            fg_color=SIDEBAR_ACT if is_active else SIDEBAR_BG,
            hover_color=SIDEBAR_HOV,
            text_color=WHITE,
            anchor="w",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
                weight="bold" if is_active else "normal"
            ),
            command=lambda page_name=label: self.show_page(page_name)
        )
        row.grid(row=len(self.nav_rows), column=0, sticky="ew")
        self.nav_rows[label] = row
        self.nav_texts[label] = f"{icon}  {label}"

    def refresh_nav(self):
        for label, row in self.nav_rows.items():
            is_active = self._active_page == label

            if self._sidebar_collapsed:
                icon = self.nav_texts[label].split("  ", 1)[0]
                row.configure(
                    text=icon,
                    width=self._sidebar_width_closed,
                    anchor="center",
                    fg_color=SIDEBAR_ACT if is_active else SIDEBAR_BG,
                    font=ctk.CTkFont(
                        family="Segoe UI Symbol",
                        size=20,
                        weight="bold" if is_active else "normal"
                    )
                )
            else:
                row.configure(
                    text=self.nav_texts[label],
                    width=self._sidebar_width_open,
                    anchor="w",
                    fg_color=SIDEBAR_ACT if is_active else SIDEBAR_BG,
                    font=ctk.CTkFont(
                        family="Segoe UI",
                        size=16,
                        weight="bold" if is_active else "normal"
                    )
                )

    def toggle_sidebar(self):
        if self._sidebar_collapsed:
            self._show_full_sidebar()
        else:
            self._show_icon_sidebar()

        self.refresh_nav()
        self.sidebar.update_idletasks()
        self.update_idletasks()

    def _show_icon_sidebar(self):
        self._sidebar_collapsed = True

        self.grid_columnconfigure(0, minsize=self._sidebar_width_closed)
        self.sidebar.configure(width=self._sidebar_width_closed)

        # Header: keep only burger button.
        self.top_bar.grid_configure(padx=8)
        self.brand_lbl.grid_remove()
        self.burger_btn.grid_configure(sticky="ew")

        # Remove profile area completely while hidden.
        self.profile_box.grid_remove()

        # Icon rail layout.
        for row in self.nav_rows.values():
            row.configure(width=self._sidebar_width_closed, anchor="center")

        self.logout_row.configure(
            text="↩",
            width=self._sidebar_width_closed,
            anchor="center",
            font=ctk.CTkFont(family="Segoe UI Symbol", size=20)
        )

    def _show_full_sidebar(self):
        self._sidebar_collapsed = False

        self.grid_columnconfigure(0, minsize=self._sidebar_width_open)
        self.sidebar.configure(width=self._sidebar_width_open)

        # Header: burger + Admin Panel.
        self.top_bar.grid_configure(padx=8)
        self.burger_btn.grid_configure(sticky="w")
        self.brand_lbl.grid()

        # Restore profile area.
        self.profile_box.grid()

        for row in self.nav_rows.values():
            row.configure(width=self._sidebar_width_open, anchor="w")

        self.logout_row.configure(
            text="↩  Logout",
            width=self._sidebar_width_open,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )

    def _build_main(self):
        self.main = ctk.CTkFrame(self, fg_color=DASH_BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)

    def clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    def show_page(self, page_name):
        self._active_page = page_name
        self.refresh_nav()
        self.clear_main()

        if page_name == "Dashboard":
            page = DashboardPage(self.main, self.full_name, self.role, self.show_page)
        elif page_name == "Teachers":
            page = TeachersManagementPage(self.main, self)
        elif page_name == "Students":
            page = StudentsManagementPage(self.main, self)
        elif page_name == "Student Accounts":
            page = StudentAccountsPage(self.main, self)
        elif page_name == "Enrollment":
            page = EnrollmentManagementPage(self.main, self)
        else:
            page = SimplePage(self.main, page_name)
        page.grid(row=0, column=0, sticky="nsew")

    def show_archived_page(self):
        self.clear_main()
        page = ArchivedStudentsPage(self.main, self)
        page.grid(row=0, column=0, sticky="nsew")

    def show_profile_page(self, student_data=None):
        self.clear_main()
        page = StudentProfilePage(self.main, self, student_data or self._profile)
        page.grid(row=0, column=0, sticky="nsew")

    def show_profile(self):
        self._active_page = "Profile"
        self.refresh_nav()
        self.clear_main()
        page = ProfilePage(
            self.main,
            full_name=self.full_name, role=self.role,
            first_name=self.first_name, last_name=self.last_name,
            middle_name=self.middle_name, birth_date=self.birth_date,
            age=self.age, gender=self.gender, mobile=self.mobile,
            email=self.email, barangay=self.barangay, address=self.address)
        page.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self):
            if self.auth:
                self.auth.logout()
            self.destroy()
            if self.on_logout:
                self.on_logout()



    # ── Student Accounts page routing ─────────────────────────────────────────
    def show_edit_student_account_page(self, account_id):
        self._active_page = "Student Accounts"
        self.refresh_nav()
        account = next((a for a in self._student_accounts if a["id"] == account_id), None)
        if not account:
            return
        self.clear_main()
        page = EditStudentAccountPage(self.main, self, account)
        page.grid(row=0, column=0, sticky="nsew")

    # ── Student Accounts data operations ─────────────────────────────────────
    def toggle_student_accounts_show_all(self):
        self._student_accounts_show_all = not self._student_accounts_show_all
        self.show_page("Student Accounts")

    def deactivate_student_account(self, account_id):
        account = next((a for a in self._student_accounts if a["id"] == account_id), None)
        if account:
            account["status"] = "Inactive"
        self.show_page("Student Accounts")

    def activate_student_account(self, account_id):
        account = next((a for a in self._student_accounts if a["id"] == account_id), None)
        if account:
            account["status"] = "Active"
        self.show_page("Student Accounts")

    def delete_student_account(self, account_id):
        if messagebox.askyesno("Delete Account", "Delete this student account?", parent=self):
            self._student_accounts = [a for a in self._student_accounts if a["id"] != account_id]
            self.show_page("Student Accounts")

    def save_student_account(self, account_id, username, password):
        account = next((a for a in self._student_accounts if a["id"] == account_id), None)
        if account:
            account["username"] = username
            account["password"] = password
        self.show_page("Student Accounts")



    # ── Enrollment page routing ───────────────────────────────────────────────
    def show_open_enrollment_page(self):
        self._active_page = "Enrollment"
        self.refresh_nav()
        self.clear_main()
        page = OpenEnrollmentPage(self.main, self)
        page.grid(row=0, column=0, sticky="nsew")

    def show_enrollment_details_page(self, enrollment_id):
        self._active_page = "Enrollment"
        self.refresh_nav()
        enrollment = next((e for e in self._enrollments if e["id"] == enrollment_id), None)
        if not enrollment:
            return
        self.clear_main()
        page = EnrollmentDetailsPage(self.main, self, enrollment)
        page.grid(row=0, column=0, sticky="nsew")

    def approve_enrollment(self, enrollment_id, details=False):
        item = next((e for e in self._enrollments if e["id"] == enrollment_id), None)
        if item:
            item["status"] = "Approved"
        self.show_enrollment_details_page(enrollment_id) if details else self.show_page("Enrollment")

    def reject_enrollment(self, enrollment_id, details=False):
        item = next((e for e in self._enrollments if e["id"] == enrollment_id), None)
        if item:
            item["status"] = "Rejected"
        self.show_enrollment_details_page(enrollment_id) if details else self.show_page("Enrollment")

    def delete_enrollment(self, enrollment_id):
        if messagebox.askyesno("Delete Enrollment", "Delete this enrollment record?", parent=self):
            self._enrollments = [e for e in self._enrollments if e["id"] != enrollment_id]
            self.show_page("Enrollment")

    def save_enrollment(self, data):
        next_id = max([e["id"] for e in self._enrollments] + [0]) + 1
        first = data.get("child_first", "").strip() or "New"
        middle = data.get("child_middle", "").strip()
        last = data.get("child_last", "").strip() or "Student"
        data["id"] = next_id
        data["name"] = " ".join(p for p in [first, middle, last] if p)
        data["date_applied"] = datetime.now().strftime("%Y-%m-%d 00:00")
        data["status"] = "Pending"
        self._enrollments.insert(0, data)
        self.show_page("Enrollment")


    # ── Teachers page routing ─────────────────────────────────────────────────
    def show_archived_teachers_page(self):
        self._active_page = "Teachers"
        self.refresh_nav()
        self.clear_main()
        page = ArchivedTeachersPage(self.main, self)
        page.grid(row=0, column=0, sticky="nsew")

    def show_teacher_profile_page(self, teacher_data):
        self._active_page = "Teachers"
        self.refresh_nav()
        self.clear_main()
        page = TeacherProfilePage(self.main, self, teacher_data)
        page.grid(row=0, column=0, sticky="nsew")

    def show_edit_teacher_page(self, teacher_data):
        self._active_page = "Teachers"
        self.refresh_nav()
        self.clear_main()
        page = EditTeacherPage(self.main, self, teacher_data)
        page.grid(row=0, column=0, sticky="nsew")

    def show_add_teacher_page(self):
        self._active_page = "Teachers"
        self.refresh_nav()
        self.clear_main()
        page = AddTeacherPage(self.main, self)
        page.grid(row=0, column=0, sticky="nsew")

    # ── Teachers data operations ──────────────────────────────────────────────
    def archive_teacher(self, teacher_id):
        match = next((t for t in self._teachers if t["id"] == teacher_id), None)
        if not match:
            return
        self._teachers.remove(match)
        archived = dict(match)
        archived["status"] = "Archived"
        archived["archived_at"] = datetime.now().strftime("%b %d, %Y")
        self._archived_teachers.append(archived)
        self.show_page("Teachers")

    def restore_teacher(self, teacher_id):
        match = next((t for t in self._archived_teachers if t["id"] == teacher_id), None)
        if not match:
            return
        self._archived_teachers.remove(match)
        restored = dict(match)
        restored["status"] = "Active"
        self._teachers.append(restored)
        self.show_archived_teachers_page()

    def delete_teacher(self, teacher_id):
        if messagebox.askyesno("Delete Teacher", "Delete this teacher?", parent=self):
            self._teachers = [t for t in self._teachers if t["id"] != teacher_id]
            self.show_page("Teachers")

    def delete_archived_teacher(self, teacher_id):
        if messagebox.askyesno("Delete Permanently", "Delete this archived teacher permanently?", parent=self):
            self._archived_teachers = [t for t in self._archived_teachers if t["id"] != teacher_id]
            self.show_archived_teachers_page()

    def add_teacher(self, data):
        next_id = max([t["id"] for t in self._teachers + self._archived_teachers] + [0]) + 1
        data["id"] = next_id
        data["position"] = "Teacher"
        data["status"] = "Active"
        data.setdefault("birthday_long", data.get("birthday", ""))
        self._teachers.append(data)
        self.show_page("Teachers")

    def save_teacher(self, teacher_id, data):
        for teacher in self._teachers:
            if teacher["id"] == teacher_id:
                teacher.update(data)
                break
        self.show_page("Teachers")


    def archive_student(self, student_id):
        match = next((s for s in self._enrolled if s["id"] == student_id), None)
        if not match:
            return
        self._enrolled.remove(match)
        now = datetime.now().strftime("%b %d, %Y")
        self._archived.append({
            "id": match["id"], "name": match["name"],
            "section": match["section"], "email": "—",
            "status": "Archived", "archived_at": now,
        })
        self.show_page("Students")

    def restore_student(self, student_id):
        match = next((s for s in self._archived if s["id"] == student_id), None)
        if not match:
            return
        self._archived.remove(match)
        self._enrolled.append({
            "id": match["id"], "name": match["name"],
            "section": match["section"], "status": "Active",
            "enrolled": match.get("archived_at", "—"), "graduated": "—",
        })
        self.show_archived_page()

    def delete_student(self, student_id):
        self._archived = [s for s in self._archived if s["id"] != student_id]
        self.show_archived_page()


class BasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=DASH_BG, corner_radius=0)

    def create_card(self, parent, height=None):
        card = ctk.CTkFrame(
            parent, fg_color=WHITE, border_color=S_BORDER,
            border_width=1, corner_radius=14)
        if height:
            card.configure(height=height)
            card.pack_propagate(False)
        return card

    def page_title(self, text):
        ctk.CTkLabel(
            self, text=text, text_color=TEXT_DARK, fg_color=DASH_BG,
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            anchor="w").pack(fill="x", padx=32, pady=(28, 18))


class DashboardPage(BasePage):
    def __init__(self, parent, full_name, role, page_callback):
        super().__init__(parent)
        self.full_name = full_name
        self.role = role
        self.page_callback = page_callback
        self.build()

    def build(self):
        self.page_title("Admin Dashboard")

        stats = ctk.CTkFrame(self, fg_color=DASH_BG)
        stats.pack(fill="x", padx=32, pady=(0, 22))
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)

        cards = [
            (str(len(getattr(self.page_callback.__self__, "_teachers", []))) if hasattr(self.page_callback, "__self__") else "0", "Teachers", "#0d6efd", "▣"),
            ("2", "Students", "#198754", "🎓"),
            ("0", "Activities", "#ffc107", "▤"),
        ]
        for i, (num, label, color, icon) in enumerate(cards):
            self.stat_card(stats, num, label, color, icon).grid(
                row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))

        self.quick_actions().pack(fill="x", padx=32)

    def stat_card(self, parent, num, label, color, icon):
        card = ctk.CTkFrame(parent, fg_color=color, height=90, corner_radius=14)
        card.pack_propagate(False)
        left = ctk.CTkFrame(card, fg_color=color)
        left.pack(side="left", padx=18, pady=12)
        ctk.CTkLabel(left, text=num, text_color=WHITE, fg_color=color,
                     font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(left, text=label, text_color=WHITE, fg_color=color,
                     font=ctk.CTkFont(family="Segoe UI", size=13)).pack(anchor="w")
        ctk.CTkLabel(card, text=icon, text_color="#e8f2ff", fg_color=color,
                     font=ctk.CTkFont(family="Segoe UI Symbol", size=30, weight="bold")).pack(side="right", padx=20)
        return card

    def quick_actions(self):
        card = self.create_card(self, height=130)
        ctk.CTkLabel(card, text="Quick Actions", text_color=TEXT_DARK, fg_color=WHITE,
                     font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
                     anchor="w").pack(fill="x", padx=22, pady=(18, 10))
        row = ctk.CTkFrame(card, fg_color=WHITE)
        row.pack(anchor="w", padx=22)
        self.action_btn(row, "🎓  Manage Students", "#0d6efd", "Students").pack(side="left", padx=(0, 12))
        self.action_btn(row, "▣  Manage Teachers", "#198754", "Teachers").pack(side="left", padx=(0, 12))
        self.action_btn(row, "▤  View Activities", "#ffc107", "Activities").pack(side="left", padx=(0, 12))
        self.action_btn(row, "□  Enrollment", "#0dcaf0", "Enrollment").pack(side="left")
        return card

    def action_btn(self, parent, text, color, page):
        return ctk.CTkButton(
            parent, text=text, height=34, corner_radius=8,
            fg_color=color, hover_color=color, text_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.page_callback(page))



def _make_search_bar(parent, textvariable, placeholder="Search student..."):
    """Search bar with left icon and visible clear button."""
    box = ctk.CTkFrame(
        parent,
        fg_color="#f9fafb",
        border_color=S_BORDER,
        border_width=1,
        corner_radius=8,
        height=40
    )
    box.grid_columnconfigure(1, weight=1)
    box.grid_propagate(False)

    icon = ctk.CTkLabel(
        box,
        text="🔍",
        width=36,
        text_color=TEXT_GRAY,
        fg_color="#f9fafb",
        font=ctk.CTkFont(family="Segoe UI Emoji", size=15)
    )
    icon.grid(row=0, column=0, sticky="nsw", padx=(10, 0))

    entry = ctk.CTkEntry(
        box,
        textvariable=textvariable,
        placeholder_text=placeholder,
        fg_color="#f9fafb",
        border_width=0,
        text_color=TEXT_DARK,
        placeholder_text_color=TEXT_GRAY,
        height=34,
        corner_radius=0,
        font=ctk.CTkFont(family="Segoe UI", size=12)
    )
    entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=2)

    clear_btn = ctk.CTkButton(
        box,
        text="✕",
        width=30,
        height=28,
        corner_radius=14,
        fg_color="#e5e7eb",
        hover_color="#d1d5db",
        text_color=TEXT_GRAY,
        font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        command=lambda: textvariable.set("")
    )
    clear_btn.grid(row=0, column=2, sticky="e", padx=(0, 10), pady=5)
    clear_btn.grid_remove()

    def _toggle_clear(*_):
        if textvariable.get().strip():
            clear_btn.grid()
        else:
            clear_btn.grid_remove()

    textvariable.trace_add("write", _toggle_clear)
    _toggle_clear()
    return box

def _configure_table_columns(frame, widths):
    """Apply identical column weights to every header/data row."""
    for i, weight in enumerate(widths):
        frame.grid_columnconfigure(i, weight=weight, uniform="table")


def _teacher_full_name(t):
    return " ".join(
        p for p in [t.get("first_name", ""), t.get("middle_name", ""), t.get("last_name", "")]
        if p
    ).strip()


def _teacher_display_name(t):
    return f"{t.get('first_name', '')} {t.get('last_name', '')}".strip()


def _teacher_button(parent, text, bg, hover_bg, command, width=80, small=False):
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
        command=command
    )


def _teacher_back_button(parent, command, text="← Back to Teachers"):
    return ctk.CTkButton(
        parent,
        text=text,
        height=34,
        width=170,
        corner_radius=8,
        fg_color=SIDEBAR_ACT,
        hover_color=SIDEBAR_HOV,
        text_color=WHITE,
        font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        command=command
    )


def _teacher_header_with_back(parent, title, command, padx=80, top_pady=(38, 16), back_text="← Back to Teachers"):
    header = ctk.CTkFrame(parent, fg_color=DASH_BG)
    header.pack(fill="x", padx=padx, pady=top_pady)
    header.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        header,
        text=title,
        fg_color=DASH_BG,
        text_color=TEXT_DARK,
        font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
        anchor="w"
    ).grid(row=0, column=0, sticky="w")

    _teacher_back_button(
        header,
        command,
        text=back_text
    ).grid(row=0, column=1, sticky="e")

    return header


def _teacher_entry(parent, value="", placeholder=""):
    entry = ctk.CTkEntry(
        parent,
        height=36,
        corner_radius=6,
        border_color=S_BORDER,
        fg_color=WHITE,
        text_color=TEXT_DARK,
        placeholder_text=placeholder,
        font=ctk.CTkFont(family="Segoe UI", size=12),
    )
    if value:
        entry.insert(0, value)
    return entry


def _teacher_labeled_entry(parent, label, value="", placeholder=""):
    box = ctk.CTkFrame(parent, fg_color=WHITE)
    ctk.CTkLabel(
        box,
        text=label,
        fg_color=WHITE,
        text_color=TEXT_DARK,
        anchor="w",
        font=ctk.CTkFont(family="Segoe UI", size=12)
    ).pack(fill="x", pady=(0, 5))
    entry = _teacher_entry(box, value, placeholder)
    entry.pack(fill="x")
    box.entry = entry
    return box


class TeachersManagementPage(BasePage):
    HEADS = ["ID", "Teacher Name", "Position", "Status", "Actions"]
    WIDTHS = [7, 34, 24, 16, 30]

    def __init__(self, parent, app: MainApp):
        super().__init__(parent)
        self.app = app
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_rows())
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=DASH_BG)
        top.pack(fill="x", padx=32, pady=(28, 12))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text="Teachers Management",
            fg_color=DASH_BG,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w")

        btns = ctk.CTkFrame(top, fg_color=DASH_BG)
        btns.grid(row=0, column=1, sticky="e")

        _teacher_button(
            btns, "Archived Teachers", BTN_DARK, BTN_DARK_H,
            self.app.show_archived_teachers_page, width=150
        ).pack(side="left", padx=(0, 8))

        _teacher_button(
            btns, "+ Add Teacher", SIDEBAR_ACT, SIDEBAR_HOV,
            self.app.show_add_teacher_page, width=130
        ).pack(side="left")

        card = self.create_card(self)
        card.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        sf = ctk.CTkFrame(card, fg_color=WHITE)
        sf.pack(fill="x", padx=16, pady=14)
        self._search_entry = _make_search_bar(sf, self._search_var, "Search teacher...")
        self._search_entry.pack(fill="x")

        _separator(card)

        self._rows_frame = ctk.CTkScrollableFrame(card, fg_color=WHITE, corner_radius=0)
        self._rows_frame.pack(fill="both", expand=True)
        self._refresh_rows()

    def _table_header(self):
        hdr = ctk.CTkFrame(self._rows_frame, fg_color="#f9fafb", corner_radius=8)
        hdr.pack(fill="x", padx=16, pady=(8, 4))
        _configure_table_columns(hdr, self.WIDTHS)

        for i, h in enumerate(self.HEADS):
            ctk.CTkLabel(
                hdr,
                text=h,
                fg_color="#f9fafb",
                text_color=TEXT_DARK,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                anchor="e" if h == "Actions" else "w"
            ).grid(row=0, column=i, sticky="ew", padx=(0, 6), pady=7)

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        self._table_header()

        query = self._search_var.get().lower().strip()
        teachers = self.app._teachers
        if query:
            teachers = [
                t for t in teachers
                if query in _teacher_display_name(t).lower()
                or query in _teacher_full_name(t).lower()
                or query == str(t["id"])
            ]

        for idx, teacher in enumerate(teachers):
            row_bg = WHITE if idx % 2 == 0 else "#fafbff"
            row = ctk.CTkFrame(self._rows_frame, fg_color=row_bg, corner_radius=8)
            row.pack(fill="x", padx=16, pady=4)
            _configure_table_columns(row, self.WIDTHS)

            values = [str(teacher["id"]), _teacher_display_name(teacher), teacher.get("position", "Teacher")]
            for col, val in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=val,
                    fg_color=row_bg,
                    text_color=TEXT_DARK,
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    anchor="w"
                ).grid(row=0, column=col, sticky="ew", padx=(0, 6), pady=7)

            _status_badge(row, teacher.get("status", "Active")).grid(row=0, column=3, sticky="w", padx=(0, 6), pady=7)

            act = ctk.CTkFrame(row, fg_color=row_bg)
            act.grid(row=0, column=4, sticky="e", pady=5)

            tid = teacher["id"]
            _teacher_button(act, "View", BTN_CYAN, BTN_CYAN_H, lambda t=teacher: self.app.show_teacher_profile_page(t), width=54, small=True).pack(side="left", padx=2)
            _teacher_button(act, "Edit", "#f59e0b", "#d97706", lambda t=teacher: self.app.show_edit_teacher_page(t), width=50, small=True).pack(side="left", padx=2)
            _teacher_button(act, "Archive", BTN_GRAY, BTN_GRAY_H, lambda i=tid: self.app.archive_teacher(i), width=70, small=True).pack(side="left", padx=2)
            _teacher_button(act, "Delete", BTN_RED, BTN_RED_H, lambda i=tid: self.app.delete_teacher(i), width=62, small=True).pack(side="left", padx=2)


class ArchivedTeachersPage(BasePage):
    HEADS = ["ID", "Teacher Name", "Position", "Actions"]
    WIDTHS = [7, 38, 26, 30]

    def __init__(self, parent, app: MainApp):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        _teacher_header_with_back(
            self,
            "Archived Teachers",
            lambda: self.app.show_page("Teachers"),
            padx=32,
            top_pady=(28, 12)
        )

        card = self.create_card(self)
        card.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        self._rows_frame = ctk.CTkScrollableFrame(card, fg_color=WHITE, corner_radius=0)
        self._rows_frame.pack(fill="both", expand=True)
        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        hdr = ctk.CTkFrame(self._rows_frame, fg_color="#f9fafb", corner_radius=8)
        hdr.pack(fill="x", padx=16, pady=(8, 4))
        _configure_table_columns(hdr, self.WIDTHS)

        for i, h in enumerate(self.HEADS):
            ctk.CTkLabel(
                hdr,
                text=h,
                fg_color="#f9fafb",
                text_color=TEXT_DARK,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                anchor="e" if h == "Actions" else "w"
            ).grid(row=0, column=i, sticky="ew", padx=(0, 6), pady=7)

        for idx, teacher in enumerate(self.app._archived_teachers):
            row_bg = WHITE if idx % 2 == 0 else "#fafbff"
            row = ctk.CTkFrame(self._rows_frame, fg_color=row_bg, corner_radius=8)
            row.pack(fill="x", padx=16, pady=4)
            _configure_table_columns(row, self.WIDTHS)

            values = [str(teacher["id"]), _teacher_display_name(teacher), teacher.get("position", "Teacher")]
            for col, val in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=val,
                    fg_color=row_bg,
                    text_color=TEXT_DARK,
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    anchor="w"
                ).grid(row=0, column=col, sticky="ew", padx=(0, 6), pady=7)

            act = ctk.CTkFrame(row, fg_color=row_bg)
            act.grid(row=0, column=3, sticky="e", pady=5)

            tid = teacher["id"]
            _teacher_button(act, "Restore", BTN_GREEN, BTN_GREEN_H, lambda i=tid: self.app.restore_teacher(i), width=80, small=True).pack(side="left", padx=2)
            _teacher_button(act, "Delete Permanently", BTN_RED, BTN_RED_H, lambda i=tid: self.app.delete_archived_teacher(i), width=145, small=True).pack(side="left", padx=2)


class TeacherProfilePage(BasePage):
    def __init__(self, parent, app: MainApp, teacher_data: dict):
        super().__init__(parent)
        self.app = app
        self.teacher = teacher_data
        self._build()

    def _build(self):
        _teacher_header_with_back(
            self,
            "Teacher Profile",
            lambda: self.app.show_page("Teachers"),
            padx=80,
            top_pady=(40, 16)
        )

        card = self.create_card(self, height=290)
        card.pack(fill="x", padx=80)
        card.pack_propagate(False)

        body = ctk.CTkFrame(card, fg_color=WHITE)
        body.pack(fill="both", expand=True, padx=28, pady=24)
        for i in range(3):
            body.grid_columnconfigure(i, weight=1, uniform="profile")

        left = ctk.CTkFrame(body, fg_color=WHITE)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ctk.CTkLabel(left, text="Profile Photo", fg_color=WHITE, text_color=TEXT_GRAY).pack(pady=(0, 8))
        ctk.CTkLabel(left, text=_teacher_display_name(self.teacher), fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold")).pack()
        ctk.CTkLabel(left, text=f"({self.teacher.get('middle_name', '')})", fg_color=WHITE,
                     text_color=TEXT_GRAY).pack()

        badge_row = ctk.CTkFrame(left, fg_color=WHITE)
        badge_row.pack(pady=(8, 12))
        ctk.CTkLabel(badge_row, text="Teacher", fg_color=SIDEBAR_ACT, text_color=WHITE, corner_radius=6, width=70, height=24).pack(side="left", padx=3)
        ctk.CTkLabel(badge_row, text=self.teacher.get("status", "Active"), fg_color=BTN_GREEN, text_color=WHITE, corner_radius=6, width=70, height=24).pack(side="left", padx=3)

        ctk.CTkFrame(left, fg_color=S_BORDER, height=1).pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(left, text=f"Username: {self.teacher.get('username', '')}", fg_color=WHITE,
                     text_color=TEXT_DARK, font=ctk.CTkFont(weight="bold")).pack()
        ctk.CTkLabel(left, text=f"Password: {self.teacher.get('password', '')}", fg_color=WHITE,
                     text_color=TEXT_DARK, font=ctk.CTkFont(weight="bold")).pack(pady=(6, 0))

        middle = ctk.CTkFrame(body, fg_color=WHITE)
        middle.grid(row=0, column=1, sticky="nsew", padx=20)
        self._info_section(middle, "Personal Info", [
            ("Full Name", _teacher_full_name(self.teacher)),
            ("Age", self.teacher.get("age", "")),
            ("Birthday", self.teacher.get("birthday_long", self.teacher.get("birthday", ""))),
            ("Gender", self.teacher.get("gender", "")),
        ])

        right = ctk.CTkFrame(body, fg_color=WHITE)
        right.grid(row=0, column=2, sticky="nsew", padx=(20, 0))
        self._info_section(right, "Contact Info", [
            ("Mobile", self.teacher.get("mobile", "")),
            ("Email", self.teacher.get("email", "")),
        ])
        ctk.CTkLabel(right, text="Address", fg_color=WHITE, text_color=SIDEBAR_ACT,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(14, 6))
        self._info_line(right, "Barangay", self.teacher.get("barangay", ""))
        self._info_line(right, "Street", self.teacher.get("street", ""))


    def _info_section(self, parent, title, fields):
        ctk.CTkLabel(parent, text=title, fg_color=WHITE, text_color=SIDEBAR_ACT,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 8))
        for label, value in fields:
            self._info_line(parent, label, value)

    def _info_line(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(anchor="w", pady=3)
        ctk.CTkLabel(row, text=f"{label}: ", fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(row, text=value, fg_color=WHITE, text_color=TEXT_DARK).pack(side="left")


class EditTeacherPage(BasePage):
    def __init__(self, parent, app: MainApp, teacher_data: dict):
        super().__init__(parent)
        self.app = app
        self.teacher = teacher_data
        self.entries = {}
        self._build()

    def _build(self):
        _teacher_header_with_back(
            self,
            "Edit Teacher",
            lambda: self.app.show_page("Teachers"),
            padx=80,
            top_pady=(38, 16)
        )

        card = self.create_card(self)
        card.pack(fill="x", padx=80)
        inner = ctk.CTkFrame(card, fg_color=WHITE)
        inner.pack(fill="x", padx=26, pady=24)

        ctk.CTkLabel(inner, text="Personal Details", fg_color=WHITE, text_color=SIDEBAR_ACT,
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 16))

        self._form_grid(inner, [
            [("first_name", "First Name", self.teacher.get("first_name", "")), ("middle_name", "Middle Name", self.teacher.get("middle_name", "")), ("last_name", "Surname", self.teacher.get("last_name", ""))],
            [("age", "Age", self.teacher.get("age", "")), ("birthday", "Birthday", self.teacher.get("birthday", "")), ("gender", "Gender", self.teacher.get("gender", "")), ("mobile", "Mobile Number", self.teacher.get("mobile", ""))],
            [("email", "Email Address", self.teacher.get("email", "")), ("username", "Username", self.teacher.get("username", ""))],
        ])

        ctk.CTkLabel(inner, text="Address", fg_color=WHITE, text_color=SIDEBAR_ACT,
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(6, 16))
        self._form_grid(inner, [
            [("barangay", "Barangay", self.teacher.get("barangay", "")), ("street", "Street Address", self.teacher.get("street", ""))]
        ])

        btns = ctk.CTkFrame(inner, fg_color=WHITE)
        btns.pack(fill="x", pady=(18, 0))
        _teacher_button(btns, "Save Changes", BTN_GREEN, BTN_GREEN_H, self._save, width=130).pack(side="right", padx=(8, 0))
        _teacher_button(btns, "Cancel", BTN_DARK, BTN_DARK_H, lambda: self.app.show_page("Teachers"), width=90).pack(side="right")

    def _form_grid(self, parent, rows):
        for row_data in rows:
            row = ctk.CTkFrame(parent, fg_color=WHITE)
            row.pack(fill="x", pady=(0, 16))
            for i in range(len(row_data)):
                row.grid_columnconfigure(i, weight=1, uniform="teacher_form")
            for i, (key, label, value) in enumerate(row_data):
                field = _teacher_labeled_entry(row, label, value=value)
                field.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))
                self.entries[key] = field.entry

    def _save(self):
        data = {k: e.get() for k, e in self.entries.items()}
        data["position"] = "Teacher"
        data["status"] = "Active"
        data["password"] = self.teacher.get("password", "teacher123")
        data["birthday_long"] = "May 08, 2006" if data.get("birthday") == "05/08/2006" else data.get("birthday", "")
        self.app.save_teacher(self.teacher["id"], data)


class AddTeacherPage(BasePage):
    def __init__(self, parent, app: MainApp):
        super().__init__(parent)
        self.app = app
        self.entries = {}
        self._build()

    def _build(self):
        _teacher_header_with_back(
            self,
            "Add Teacher",
            lambda: self.app.show_page("Teachers"),
            padx=80,
            top_pady=(38, 16)
        )

        card = self.create_card(self)
        card.pack(fill="x", padx=80)
        inner = ctk.CTkFrame(card, fg_color=WHITE)
        inner.pack(fill="x", padx=26, pady=24)

        ctk.CTkLabel(inner, text="Personal Details", fg_color=WHITE, text_color=SIDEBAR_ACT,
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 16))

        self._form_grid(inner, [
            [("first_name", "First Name", ""), ("middle_name", "Middle Name", ""), ("last_name", "Surname / Last Name", "")],
            [("birthday", "Birthday", ""), ("age", "Age", ""), ("gender", "Gender", ""), ("mobile", "Mobile Number", "")],
            [("email", "Email Address", ""), ("username", "Username", ""), ("password", "Password", ""), ("confirm_password", "Confirm Password", "")],
        ])

        ctk.CTkLabel(inner, text="Address", fg_color=WHITE, text_color=SIDEBAR_ACT,
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(6, 16))
        self._form_grid(inner, [
            [("barangay", "Barangay", ""), ("street", "Street Address", "")]
        ])

        btns = ctk.CTkFrame(inner, fg_color=WHITE)
        btns.pack(fill="x", pady=(18, 0))
        _teacher_button(btns, "Save", BTN_GREEN, BTN_GREEN_H, self._save, width=80).pack(side="right", padx=(8, 0))
        _teacher_button(btns, "Cancel", BTN_DARK, BTN_DARK_H, lambda: self.app.show_page("Teachers"), width=90).pack(side="right")

    def _form_grid(self, parent, rows):
        for row_data in rows:
            row = ctk.CTkFrame(parent, fg_color=WHITE)
            row.pack(fill="x", pady=(0, 16))
            for i in range(len(row_data)):
                row.grid_columnconfigure(i, weight=1, uniform="teacher_add_form")
            for i, (key, label, value) in enumerate(row_data):
                field = _teacher_labeled_entry(row, label, value=value)
                field.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))
                self.entries[key] = field.entry

    def _save(self):
        data = {k: e.get() for k, e in self.entries.items()}
        if not data.get("first_name") and not data.get("last_name"):
            data["first_name"] = "New"
            data["last_name"] = "Teacher"
        data["birthday_long"] = data.get("birthday", "")
        self.app.add_teacher(data)



class StudentsManagementPage(BasePage):
    HEADS = ["ID", "Student Name", "Section", "Status", "Enrolled", "Graduated", "Actions"]
    WIDTHS = [5, 22, 9, 11, 14, 14, 26]

    def __init__(self, parent, app: MainApp):
        super().__init__(parent)
        self.app = app
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_rows())
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=DASH_BG)
        top.pack(fill="x", padx=32, pady=(28, 6))
        ctk.CTkLabel(top, text="Students Management", fg_color=DASH_BG, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), anchor="w").pack(side="left")
        _pill_btn(top, "Archived Students", BTN_DARK, BTN_DARK_H, self.app.show_archived_page).pack(side="right")

        tab_row = ctk.CTkFrame(self, fg_color=DASH_BG)
        tab_row.pack(fill="x", padx=32, pady=(0, 8))
        _tab_label(tab_row, "ENROLLED STUDENTS", active=True).pack(side="left")
        _tab_label(tab_row, "GRADUATED STUDENTS").pack(side="left", padx=(12, 0))

        card = self.create_card(self)
        card.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        sf = ctk.CTkFrame(card, fg_color=WHITE)
        sf.pack(fill="x", padx=16, pady=12)
        self._search_entry = _make_search_bar(sf, self._search_var, "Search student...")
        self._search_entry.pack(fill="x")

        _separator(card)

        # Put the header and rows inside the SAME scrollable table area.
        # This keeps columns perfectly aligned because they share the same inner width.
        self._rows_frame = ctk.CTkScrollableFrame(card, fg_color=WHITE, corner_radius=0)
        self._rows_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        # Header row uses the same parent, same padx, and same column weights as data rows.
        hdr = ctk.CTkFrame(self._rows_frame, fg_color="#f9fafb", corner_radius=8)
        hdr.pack(fill="x", padx=16, pady=(8, 4))
        _configure_table_columns(hdr, self.WIDTHS)

        for i, h in enumerate(self.HEADS):
            ctk.CTkLabel(
                hdr,
                text=h,
                fg_color="#f9fafb",
                text_color=TEXT_DARK,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                anchor="e" if h == "Actions" else "w"
            ).grid(row=0, column=i, sticky="ew", padx=(0, 6), pady=7)

        query = self._search_var.get().lower().strip()
        students = self.app._enrolled
        if query:
            students = [s for s in students if query in s["name"].lower() or query == str(s["id"])]

        for idx, stu in enumerate(students):
            row_bg = WHITE if idx % 2 == 0 else "#fafbff"
            row = ctk.CTkFrame(self._rows_frame, fg_color=row_bg, corner_radius=8)
            row.pack(fill="x", padx=16, pady=4)
            _configure_table_columns(row, self.WIDTHS)

            values = [str(stu["id"]), stu["name"], stu["section"]]
            for col, val in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=val,
                    fg_color=row_bg,
                    text_color=TEXT_DARK,
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    anchor="w"
                ).grid(row=0, column=col, sticky="ew", padx=(0, 6), pady=7)

            _status_badge(row, stu["status"]).grid(row=0, column=3, sticky="w", padx=(0, 6), pady=7)

            ctk.CTkLabel(
                row,
                text=stu["enrolled"],
                fg_color=row_bg,
                text_color=TEXT_DARK,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                anchor="w"
            ).grid(row=0, column=4, sticky="ew", padx=(0, 6), pady=7)

            ctk.CTkLabel(
                row,
                text=stu["graduated"],
                fg_color=row_bg,
                text_color=TEXT_GRAY,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                anchor="w"
            ).grid(row=0, column=5, sticky="ew", padx=(0, 6), pady=7)

            act = ctk.CTkFrame(row, fg_color=row_bg)
            act.grid(row=0, column=6, sticky="e", padx=(0, 0), pady=5)

            sid = stu["id"]
            _pill_btn(act, "View", BTN_CYAN, BTN_CYAN_H, lambda s=stu: self.app.show_profile_page(s), small=True).pack(side="left", padx=2)
            _pill_btn(act, "Archive", BTN_GRAY, BTN_GRAY_H, lambda s=sid: self.app.archive_student(s), small=True).pack(side="left", padx=2)
            _pill_btn(act, "Graduate", BTN_GREEN, BTN_GREEN_H, lambda: None, small=True).pack(side="left", padx=2)


class ArchivedStudentsPage(BasePage):
    HEADS = ["ID", "Student Name", "Section", "Email", "Status", "Archived At", "Actions"]
    WIDTHS = [5, 20, 8, 12, 10, 14, 16]

    def __init__(self, parent, app: MainApp):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=DASH_BG)
        top.pack(fill="x", padx=32, pady=(28, 6))
        ctk.CTkLabel(top, text="Archived Students", fg_color=DASH_BG, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), anchor="w").pack(side="left")
        _pill_btn(top, "← Back to Students", BTN_DARK, BTN_DARK_H,
                  lambda: self.app.show_page("Students")).pack(side="right")

        card = self.create_card(self)
        card.pack(fill="both", expand=True, padx=32, pady=(8, 28))

        # Header and rows are built inside the same scrollable frame
        # so all columns line up exactly.
        self._rows_frame = ctk.CTkScrollableFrame(card, fg_color=WHITE, corner_radius=0)
        self._rows_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        hdr = ctk.CTkFrame(self._rows_frame, fg_color="#f9fafb", corner_radius=8)
        hdr.pack(fill="x", padx=16, pady=(8, 4))
        _configure_table_columns(hdr, self.WIDTHS)

        for i, h in enumerate(self.HEADS):
            ctk.CTkLabel(
                hdr,
                text=h,
                fg_color="#f9fafb",
                text_color=TEXT_DARK,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                anchor="e" if h == "Actions" else "w"
            ).grid(row=0, column=i, sticky="ew", padx=(0, 6), pady=7)

        for idx, stu in enumerate(self.app._archived):
            row_bg = WHITE if idx % 2 == 0 else "#fafbff"
            row = ctk.CTkFrame(self._rows_frame, fg_color=row_bg, corner_radius=8)
            row.pack(fill="x", padx=16, pady=4)
            _configure_table_columns(row, self.WIDTHS)

            values = [str(stu["id"]), stu["name"], stu["section"], stu["email"]]
            for col, val in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=val,
                    fg_color=row_bg,
                    text_color=TEXT_DARK,
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    anchor="w"
                ).grid(row=0, column=col, sticky="ew", padx=(0, 6), pady=7)

            _status_badge(row, stu["status"]).grid(row=0, column=4, sticky="w", padx=(0, 6), pady=7)

            ctk.CTkLabel(
                row,
                text=stu["archived_at"],
                fg_color=row_bg,
                text_color=TEXT_GRAY,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                anchor="w"
            ).grid(row=0, column=5, sticky="ew", padx=(0, 6), pady=7)

            act = ctk.CTkFrame(row, fg_color=row_bg)
            act.grid(row=0, column=6, sticky="e", padx=(0, 0), pady=5)

            sid = stu["id"]
            _pill_btn(act, "Restore", BTN_GREEN, BTN_GREEN_H, lambda s=sid: self.app.restore_student(s), small=True).pack(side="left", padx=2)
            _pill_btn(act, "Delete", BTN_RED, BTN_RED_H, lambda s=sid: self._confirm_delete(s), small=True).pack(side="left", padx=2)

    def _confirm_delete(self, sid):
        if messagebox.askyesno("Confirm Delete", "Delete this student permanently?", parent=self):
            self.app.delete_student(sid)


class StudentProfilePage(BasePage):
    def __init__(self, parent, app: MainApp, student_data: dict):
        super().__init__(parent)
        self.app = app
        self.data = student_data
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=DASH_BG)
        top.pack(fill="x", padx=32, pady=(28, 6))
        ctk.CTkLabel(top, text="Student Profile", fg_color=DASH_BG, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), anchor="w").pack(side="left")
        _pill_btn(top, "← Back to Students", BTN_DARK, BTN_DARK_H,
                  lambda: self.app.show_page("Students")).pack(side="right")

        card = self.create_card(self)
        card.pack(fill="both", expand=True, padx=32, pady=(8, 28))

        inner = ctk.CTkScrollableFrame(card, fg_color=WHITE, corner_radius=0)
        inner.pack(fill="both", expand=True, padx=20, pady=20)
        p = self.data

        self._section_title(inner, "Child Information")
        self._detail_trio(inner, [("Full Name", p.get("full_name", p.get("name", "—"))), ("Nickname", p.get("nickname", "—")), ("Birthday", p.get("birthday", "—"))])
        self._detail_trio(inner, [("Age", p.get("age", "—")), ("Gender", p.get("gender", "—")), ("Section", p.get("section", "—"))])

        self._section_title(inner, "Mother's Information")
        self._detail_trio(inner, [("Name", p.get("mother_name", "—")), ("Occupation", p.get("mother_occupation", "—")), ("Contact", p.get("mother_contact", "—"))])
        self._detail_trio(inner, [("Education", p.get("mother_education", "—")), ("School", p.get("mother_school", "—")), ("Year Graduated", p.get("mother_graduated", "—"))])

        self._section_title(inner, "Father's Information")
        self._detail_trio(inner, [("Name", p.get("father_name", "—")), ("Occupation", p.get("father_occupation", "—")), ("Contact", p.get("father_contact", "—"))])
        self._detail_trio(inner, [("Education", p.get("father_education", "—")), ("School", p.get("father_school", "—")), ("Year Graduated", p.get("father_graduated", "—"))])

        self._section_title(inner, "Guardian Information (Optional)")
        self._detail_trio(inner, [("Name", p.get("guardian_name", "—")), ("Occupation", p.get("guardian_occupation", "—")), ("Contact", p.get("guardian_contact", "—"))])

    def _section_title(self, parent, text):
        ctk.CTkLabel(parent, text=text, fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                     anchor="w").pack(fill="x", pady=(12, 4))
        _separator(parent)

    def _detail_trio(self, parent, fields):
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(fill="x", pady=4)
        for col in range(3):
            row.grid_columnconfigure(col, weight=1)
        for col, (label, value) in enumerate(fields):
            cell = ctk.CTkFrame(row, fg_color=WHITE)
            cell.grid(row=0, column=col, sticky="ew", padx=(0, 10))
            ctk.CTkLabel(cell, text=f"{label}:", fg_color=WHITE, text_color=TEXT_GRAY,
                         font=ctk.CTkFont(family="Segoe UI", size=11), anchor="w").pack(anchor="w")
            ctk.CTkLabel(cell, text=value, fg_color=WHITE, text_color=TEXT_DARK,
                         font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), anchor="w").pack(anchor="w")



def _account_status_badge(parent, status):
    if status == "Active":
        bg, fg = BTN_GREEN, WHITE
    else:
        bg, fg = BTN_DARK, WHITE

    return ctk.CTkLabel(
        parent,
        text=status,
        fg_color=bg,
        text_color=fg,
        corner_radius=6,
        width=64,
        height=22,
        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold")
    )


class StudentAccountsPage(BasePage):
    HEADS = ["ID", "Full Name", "Status", "Username", "Date Created", "Actions"]
    WIDTHS = [6, 28, 14, 20, 20, 24]

    def __init__(self, parent, app: MainApp):
        super().__init__(parent)
        self.app = app
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_rows())
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=DASH_BG)
        top.pack(fill="x", padx=32, pady=(28, 12))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text="Student Accounts",
            fg_color=DASH_BG,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w")

        toggle_text = "Show Active Only" if self.app._student_accounts_show_all else "Show All"
        toggle_color = BTN_DARK if self.app._student_accounts_show_all else SIDEBAR_ACT
        toggle_hover = BTN_DARK_H if self.app._student_accounts_show_all else SIDEBAR_HOV

        _pill_btn(
            top,
            toggle_text,
            toggle_color,
            toggle_hover,
            self.app.toggle_student_accounts_show_all
        ).grid(row=0, column=1, sticky="e")

        card = self.create_card(self)
        card.pack(fill="both", expand=False, padx=32, pady=(0, 28))

        sf = ctk.CTkFrame(card, fg_color=WHITE)
        sf.pack(fill="x", padx=16, pady=14)
        self._search_entry = _make_search_bar(sf, self._search_var, "Search student...")
        self._search_entry.pack(fill="x")

        _separator(card)

        self._rows_frame = ctk.CTkFrame(card, fg_color=WHITE, corner_radius=0)
        self._rows_frame.pack(fill="x", padx=16, pady=(0, 16))
        self._refresh_rows()

    def _refresh_rows(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        hdr = ctk.CTkFrame(self._rows_frame, fg_color="#f9fafb", corner_radius=0)
        hdr.pack(fill="x")
        _configure_table_columns(hdr, self.WIDTHS)

        for i, h in enumerate(self.HEADS):
            ctk.CTkLabel(
                hdr,
                text=h,
                fg_color="#f9fafb",
                text_color=TEXT_DARK,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                anchor="e" if h == "Actions" else "w"
            ).grid(row=0, column=i, sticky="ew", padx=(8, 6), pady=10)

        query = self._search_var.get().lower().strip()
        accounts = self.app._student_accounts

        if not self.app._student_accounts_show_all:
            accounts = [a for a in accounts if a["status"] == "Active"]

        if query:
            accounts = [
                a for a in accounts
                if query in a["full_name"].lower()
                or query in a["username"].lower()
                or query == str(a["id"])
            ]

        for idx, account in enumerate(accounts):
            row_bg = WHITE
            row = ctk.CTkFrame(self._rows_frame, fg_color=row_bg, corner_radius=0)
            row.pack(fill="x")
            _configure_table_columns(row, self.WIDTHS)

            values = [
                str(account["id"]),
                account["full_name"],
                "",
                account["username"],
                account["date_created"],
            ]

            for col, val in enumerate(values):
                if col == 2:
                    cell = ctk.CTkFrame(row, fg_color=row_bg)
                    cell.grid(row=0, column=col, sticky="ew", padx=(8, 6), pady=8)
                    _account_status_badge(cell, account["status"]).pack(anchor="w")
                else:
                    ctk.CTkLabel(
                        row,
                        text=val,
                        fg_color=row_bg,
                        text_color=TEXT_DARK,
                        font=ctk.CTkFont(family="Segoe UI", size=12),
                        anchor="w"
                    ).grid(row=0, column=col, sticky="ew", padx=(8, 6), pady=10)

            act = ctk.CTkFrame(row, fg_color=row_bg)
            act.grid(row=0, column=5, sticky="e", padx=(8, 6), pady=7)

            aid = account["id"]
            _teacher_button(
                act,
                "Edit",
                "#f59e0b",
                "#d97706",
                lambda i=aid: self.app.show_edit_student_account_page(i),
                width=52,
                small=True
            ).pack(side="left", padx=2)

            if account["status"] == "Active":
                _teacher_button(
                    act,
                    "Deactivate",
                    BTN_DARK,
                    BTN_DARK_H,
                    lambda i=aid: self.app.deactivate_student_account(i),
                    width=86,
                    small=True
                ).pack(side="left", padx=2)
            else:
                _teacher_button(
                    act,
                    "Activate",
                    BTN_GREEN,
                    BTN_GREEN_H,
                    lambda i=aid: self.app.activate_student_account(i),
                    width=78,
                    small=True
                ).pack(side="left", padx=2)

            _teacher_button(
                act,
                "Delete",
                BTN_RED,
                BTN_RED_H,
                lambda i=aid: self.app.delete_student_account(i),
                width=62,
                small=True
            ).pack(side="left", padx=2)

            ctk.CTkFrame(self._rows_frame, fg_color=S_BORDER, height=1, corner_radius=0).pack(fill="x")


class EditStudentAccountPage(BasePage):
    def __init__(self, parent, app: MainApp, account: dict):
        super().__init__(parent)
        self.app = app
        self.account = account
        self._build()

    def _build(self):
        # Page header: title on the left, back button on the right.
        header = ctk.CTkFrame(self, fg_color=DASH_BG)
        header.pack(fill="x", padx=80, pady=(38, 18))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Edit Student Account",
            fg_color=DASH_BG,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="← Back to Student Accounts",
            height=36,
            width=210,
            corner_radius=8,
            fg_color=SIDEBAR_ACT,
            hover_color=SIDEBAR_HOV,
            text_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.app.show_page("Student Accounts")
        ).grid(row=0, column=1, sticky="e")

        # Wider form, aligned like the rest of the admin pages.
        card = self.create_card(self)
        card.pack(fill="x", padx=80, pady=(0, 28))

        form = ctk.CTkFrame(card, fg_color=WHITE)
        form.pack(fill="x", padx=28, pady=28)
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Username",
            fg_color=WHITE,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=7,
            border_color=S_BORDER,
            fg_color=WHITE,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.username_entry.insert(0, self.account["username"])
        self.username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 18))

        ctk.CTkLabel(
            form,
            text="New Password (Required)",
            fg_color=WHITE,
            text_color=TEXT_DARK,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(0, 8))

        self.password_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=7,
            border_color=S_BORDER,
            fg_color=WHITE,
            text_color=TEXT_DARK,
            show="*",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 22))

        ctk.CTkButton(
            form,
            text="Save Changes",
            height=40,
            corner_radius=7,
            fg_color=SIDEBAR_ACT,
            hover_color=SIDEBAR_HOV,
            text_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._save
        ).grid(row=4, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkButton(
            form,
            text="Cancel",
            height=40,
            corner_radius=7,
            fg_color=BTN_DARK,
            hover_color=BTN_DARK_H,
            text_color=WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self.app.show_page("Student Accounts")
        ).grid(row=5, column=0, sticky="ew")

    def _save(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:
            messagebox.showwarning("Missing Username", "Username is required.", parent=self.app)
            return

        self.app.save_student_account(self.account["id"], username, password)




class SimplePage(BasePage):
    def __init__(self, parent, title):
        super().__init__(parent)
        self._title = title
        self.build()

    def build(self):
        self.page_title(self._title)
        card = self.create_card(self, height=280)
        card.pack(fill="x", padx=32)
        icons = {
            "Teachers": "▣", "Student Accounts": "👥",
            "Activities": "▤", "Enrollment": "□", "Reports": "▥",
        }
        ctk.CTkLabel(card, text=icons.get(self._title, "□"), fg_color=WHITE, text_color="#0d6efd",
                     font=ctk.CTkFont(family="Segoe UI Symbol", size=54, weight="bold")).pack(pady=(42, 10))
        ctk.CTkLabel(card, text=f"{self._title} Page", fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack()
        ctk.CTkLabel(card, text="This page is under construction.", fg_color=WHITE, text_color=TEXT_GRAY,
                     font=ctk.CTkFont(family="Segoe UI", size=13)).pack(pady=(8, 0))


class ProfilePage(BasePage):
    def __init__(self, parent, full_name, role, first_name, last_name,
                 middle_name, birth_date, age, gender, mobile,
                 email, barangay, address):
        super().__init__(parent)
        self.full_name = full_name
        self.role = role
        self.info = {
            "First Name": first_name,
            "Middle Name": middle_name or "N/A",
            "Last Name": last_name,
            "Role": role,
            "Birth Date": birth_date or "N/A",
            "Age": age or "N/A",
            "Gender": gender or "N/A",
            "Mobile": mobile or "N/A",
            "Email": email or "N/A",
            "Barangay": barangay or "N/A",
            "Address": address or "N/A",
        }
        self.build()

    def build(self):
        self.page_title("Profile Information")
        card = self.create_card(self, height=450)
        card.pack(fill="x", padx=32)

        top = ctk.CTkFrame(card, fg_color=WHITE)
        top.pack(fill="x", padx=32, pady=(28, 20))

        av = ctk.CTkLabel(top, text="👤", width=86, height=86, fg_color="#f8fafc",
                          text_color="#64748b", corner_radius=43,
                          font=ctk.CTkFont(family="Segoe UI Emoji", size=32))
        av.pack(side="left")

        nb = ctk.CTkFrame(top, fg_color=WHITE)
        nb.pack(side="left", padx=20)
        ctk.CTkLabel(nb, text=self.full_name, fg_color=WHITE, text_color=TEXT_DARK,
                     font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(nb, text=self.role, fg_color=WHITE, text_color=TEXT_GRAY,
                     font=ctk.CTkFont(family="Segoe UI", size=13)).pack(anchor="w", pady=(4, 0))

        details = ctk.CTkFrame(card, fg_color=WHITE)
        details.pack(fill="x", padx=32)
        details.grid_columnconfigure(0, weight=1)
        details.grid_columnconfigure(1, weight=1)

        row = col = 0
        for label, value in self.info.items():
            item = ctk.CTkFrame(details, fg_color=WHITE)
            item.grid(row=row, column=col, sticky="ew", padx=(0, 40), pady=8)
            ctk.CTkLabel(item, text=label, fg_color=WHITE, text_color=TEXT_GRAY,
                         font=ctk.CTkFont(family="Segoe UI", size=11), anchor="w").pack(anchor="w")
            ctk.CTkLabel(item, text=value, fg_color=WHITE, text_color=TEXT_DARK,
                         font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), anchor="w").pack(anchor="w")
            col += 1
            if col == 2:
                col = 0
                row += 1


def _pill_btn(parent, text, bg, hover_bg, command, small=False):
    return ctk.CTkButton(
        parent, text=text, height=26 if small else 34,
        corner_radius=8, fg_color=bg, hover_color=hover_bg,
        text_color=WHITE, width=72 if small else 140,
        font=ctk.CTkFont(family="Segoe UI", size=10 if small else 12),
        command=command)


def _status_badge(parent, status):
    cfg = {
        "Active": ("#22c55e", WHITE),
        "Archived": ("#e5e7eb", "#374151"),
    }
    bg, fg = cfg.get(status, ("#e0e7ff", "#3730a3"))
    return ctk.CTkLabel(parent, text=status, fg_color=bg, text_color=fg,
                        corner_radius=12, width=74, height=24,
                        font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"))


def _tab_label(parent, text, active=False):
    fg = TEXT_DARK if active else TEXT_GRAY
    return ctk.CTkLabel(parent, text=text, fg_color=DASH_BG, text_color=fg,
                        font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold" if active else "normal"))


def _separator(parent):
    ctk.CTkFrame(parent, fg_color=S_BORDER, height=1, corner_radius=0).pack(fill="x")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
