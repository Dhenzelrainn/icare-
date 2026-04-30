# login.py — Login Page

import math
import tkinter as tk
from tkinter import messagebox

from utils import (
    WHITE, ACCENT, ACCENT_DARK, TEXT_DARK, TEXT_GRAY,
    ERROR_RED, SUCCESS_GRN, BORDER_CLR,
    F_LABEL, F_ERR, F_HINT,
    draw_gradient, rounded_rect, rgb_to_hex,
    draw_background_circles, draw_logo_blocks, draw_card_shadow,
    make_field
)


class LoginPage:
    def __init__(self, auth_manager):
        self.auth = auth_manager

        self.root = tk.Tk()
        self.root.title("iCare Daycare | Login")
        self.root.geometry("1000x620")
        self.root.minsize(600, 480)
        self.root.resizable(True, True)

        self._build_ui()

    # ══════════════════════════════════════════════════════════
    #  BUILD UI
    # ══════════════════════════════════════════════════════════
    def _build_ui(self):
        self._logo_offsets = [0.0] * 5
        self._logo_phases  = [i * 0.4 for i in range(5)]
        self._logo_t       = 0.0
        self._bg_size      = [0, 0]
        self._loading      = False

        self.bg = tk.Canvas(self.root, bd=0, highlightthickness=0)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.card_host = tk.Frame(self.bg, bg="#5ABCD8", bd=0)
        self.card_cv   = tk.Canvas(self.card_host, bd=0,
                                   highlightthickness=0, bg="#5ABCD8")
        self.card_cv.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.card_cv, bg=WHITE)

        self.card_cv.bind("<Configure>",
                          lambda e: draw_card_shadow(self.card_cv, self.inner))

        self._build_card_content()

        self.bg.bind("<Configure>", self._redraw_bg)
        self.bg.after(100, self._animate_logo)

        fs = [False]
        def toggle_fs(e=None):
            fs[0] = not fs[0]
            self.root.attributes("-fullscreen", fs[0])
        self.root.bind("<F11>", toggle_fs)
        self.root.bind("<Escape>",
                       lambda e: self.root.attributes("-fullscreen", False))

    def _build_card_content(self):
        inner = self.inner

        # Mini iCARE logo
        header = tk.Frame(inner, bg=WHITE)
        header.pack(fill="x", pady=(26, 0))
        icon_row = tk.Frame(header, bg=WHITE)
        icon_row.pack()
        for letter, color in zip(["i", "C"], ["#E05555", "#4CAF50"]):
            tk.Label(icon_row, text=letter,
                     font=("Arial Rounded MT Bold", 14, "bold"),
                     fg=WHITE, bg=color, width=2).pack(side="left", padx=1)
        tk.Label(icon_row, text="CARE",
                 font=("Arial Rounded MT Bold", 14, "bold"),
                 fg=ACCENT, bg=WHITE).pack(side="left", padx=(4, 0))

        tk.Label(inner, text="Welcome Back!",
                 font=("Arial", 18, "bold"), fg=TEXT_DARK,
                 bg=WHITE).pack(pady=(6, 2))
        tk.Label(inner, text="Sign in to your account",
                 font=("Arial", 10), fg=TEXT_GRAY,
                 bg=WHITE).pack(pady=(0, 10))

        div = tk.Canvas(inner, height=1, bd=0, highlightthickness=0, bg=WHITE)
        div.pack(fill="x", padx=28, pady=(0, 14))
        div.bind("<Configure>", lambda e: (
            div.delete("all"),
            div.create_line(0, 0, div.winfo_width(), 0, fill=BORDER_CLR)
        ))

        # Error banner
        self.err_var    = tk.StringVar()
        self._err_frame = tk.Frame(inner, bg="#FFF0F0")
        tk.Label(self._err_frame, text="⚠", font=("Arial", 11),
                 fg="#E53E3E", bg="#FFF0F0").pack(side="left", padx=(10, 4), pady=5)
        tk.Label(self._err_frame, textvariable=self.err_var, font=F_ERR,
                 fg="#E53E3E", bg="#FFF0F0", anchor="w",
                 wraplength=280).pack(side="left", pady=5, padx=(0, 10))

        # Username
        tk.Label(inner, text="Username", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").pack(
                 fill="x", padx=28, pady=(0, 4))
        u_f, self.u_entry = make_field(inner, "👤",
                                        clear_error_cb=self._clear_error)
        u_f.pack(fill="x", padx=28, pady=(0, 14))

        # Password row
        p_row = tk.Frame(inner, bg=WHITE)
        p_row.pack(fill="x", padx=28, pady=(0, 4))
        tk.Label(p_row, text="Password", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE).pack(side="left")
        forgot = tk.Label(p_row, text="Forgot password?",
                          font=("Arial", 9), fg=ACCENT,
                          bg=WHITE, cursor="hand2")
        forgot.pack(side="right")
        forgot.bind("<Enter>", lambda e: forgot.config(
            fg=ACCENT_DARK, font=("Arial", 9, "underline")))
        forgot.bind("<Leave>", lambda e: forgot.config(
            fg=ACCENT, font=("Arial", 9)))
        forgot.bind("<Button-1>", lambda e: messagebox.showinfo(
            "Forgot Password",
            "Please contact your system administrator\nto reset your password.",
            parent=self.root))

        p_f, self.p_entry = make_field(inner, "🔒", show_char="•",
                                        clear_error_cb=self._clear_error)
        p_f.pack(fill="x", padx=28, pady=(0, 6))

        # Demo hint
        tk.Label(inner, text="Demo: admin/admin123  •  superadmin/superadmin123",
                 font=F_HINT, fg=TEXT_GRAY, bg=WHITE).pack(pady=(0, 12))

        # Login button
        self.btn_cv = tk.Canvas(inner, height=46, bd=0,
                                highlightthickness=0, bg=WHITE)
        self.btn_cv.pack(fill="x", padx=28)
        self.btn_cv.bind("<Configure>", lambda e: self._draw_btn("normal"))
        self.btn_cv.bind("<Enter>",
                         lambda e: not self._loading and self._draw_btn("hover"))
        self.btn_cv.bind("<Leave>",
                         lambda e: not self._loading and self._draw_btn("normal"))
        self.btn_cv.bind("<Button-1>", self._do_login)
        self.root.bind("<Return>", self._do_login)

        # OR divider
        or_frame = tk.Frame(inner, bg=WHITE)
        or_frame.pack(fill="x", padx=28, pady=(14, 10))
        tk.Frame(or_frame, bg=BORDER_CLR, height=1).pack(
            side="left", fill="x", expand=True, pady=8)
        tk.Label(or_frame, text="  or continue with  ",
                 font=("Arial", 9), fg=TEXT_GRAY, bg=WHITE).pack(side="left")
        tk.Frame(or_frame, bg=BORDER_CLR, height=1).pack(
            side="left", fill="x", expand=True, pady=8)

        # Google button (cosmetic)
        g_btn   = tk.Frame(inner, bg=WHITE, cursor="hand2")
        g_btn.pack(pady=(0, 4))
        g_inner = tk.Frame(g_btn, bg=WHITE, relief="flat", bd=0,
                           highlightthickness=1,
                           highlightbackground=BORDER_CLR)
        g_inner.pack(ipadx=18, ipady=8)
        g_icon  = tk.Canvas(g_inner, width=22, height=22,
                            bd=0, highlightthickness=0, bg=WHITE)
        g_icon.pack(side="left", padx=(0, 8))
        g_icon.create_text(11, 11, text="G",
                           font=("Arial", 12, "bold"), fill="#4285F4")
        tk.Label(g_inner, text="Sign in with Google",
                 font=("Arial", 10), fg=TEXT_DARK, bg=WHITE).pack(side="left")
        for w in [g_btn, g_inner]:
            w.bind("<Enter>",
                   lambda e: g_inner.config(highlightbackground=ACCENT))
            w.bind("<Leave>",
                   lambda e: g_inner.config(highlightbackground=BORDER_CLR))

        # Sign up link
        su_frame = tk.Frame(inner, bg=WHITE)
        su_frame.pack(pady=(10, 18))
        tk.Label(su_frame, text="Don't have an account?  ",
                 font=("Arial", 10), fg=TEXT_GRAY, bg=WHITE).pack(side="left")
        su_lbl = tk.Label(su_frame, text="Sign up",
                          font=("Arial", 10, "bold"), fg=ACCENT,
                          bg=WHITE, cursor="hand2")
        su_lbl.pack(side="left")
        su_lbl.bind("<Enter>", lambda e: su_lbl.config(
            fg=ACCENT_DARK, font=("Arial", 10, "bold", "underline")))
        su_lbl.bind("<Leave>", lambda e: su_lbl.config(
            fg=ACCENT, font=("Arial", 10, "bold")))
        su_lbl.bind("<Button-1>", lambda e: self._open_signup())

    # ══════════════════════════════════════════════════════════
    #  LOGIN LOGIC
    # ══════════════════════════════════════════════════════════
    def _do_login(self, _=None):
        if self._loading:
            return
        uname = self.u_entry.get().strip()
        pwd   = self.p_entry.get()

        success, role, msg = self.auth.login(uname, pwd)

        if not success:
            self._show_error(msg)
            self._draw_btn("error")
            self.root.after(1500, lambda: self._draw_btn("normal"))
            return

        self._loading = True
        self._draw_btn("loading")
        self.root.update()

        def open_dash():
            self._loading = False
            self._draw_btn("success")
            self.root.update()
            self.root.after(600, lambda: self._open_dashboard(role))

        self.root.after(700, open_dash)

    def _open_dashboard(self, role):
        if role == "Super Admin":
            from Superadmin.Superadmin_Dashboard import SuperAdminDashboard
            self.root.withdraw()
            SuperAdminDashboard(
                auth_manager=self.auth,
                on_logout=self._on_logout
            )
        elif role == "Admin":
            self.root.withdraw()
            self._open_admin_dashboard()
        else:
            messagebox.showinfo(
                "Access Restricted",
                f"Role '{role}' does not have Admin access.\n\n"
                "Please log in with an Admin account.\n\n"
                "Demo: admin / admin123",
                parent=self.root
            )
            self._draw_btn("normal")
            self.auth.logout()

    def _open_admin_dashboard(self):
        from Admin.admin_dashboard import MainApp
        dash = MainApp(
            auth_manager=self.auth,
            on_logout=self._on_logout
        )
        dash.protocol("WM_DELETE_WINDOW", lambda: self._on_admin_close(dash))
        dash.mainloop()

    def _on_admin_close(self, dash):
        self.auth.logout()
        dash.destroy()
        self._on_logout()

    def _on_logout(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.u_entry.delete(0, "end")
        self.p_entry.delete(0, "end")
        self._draw_btn("normal")

    def _open_signup(self):
        from signup import SignupPage
        self.root.withdraw()
        SignupPage(
            parent_win=self.root,
            auth_manager=self.auth,
            on_back=lambda: self.root.deiconify()
        )

    # ══════════════════════════════════════════════════════════
    #  ERROR HELPERS
    # ══════════════════════════════════════════════════════════
    def _show_error(self, msg):
        self.err_var.set(msg)
        self._err_frame.pack(fill="x", padx=28, pady=(0, 8))

    def _clear_error(self):
        self.err_var.set("")
        self._err_frame.pack_forget()

    # ══════════════════════════════════════════════════════════
    #  LOGIN BUTTON DRAW
    # ══════════════════════════════════════════════════════════
    def _draw_btn(self, state="normal"):
        self.btn_cv.delete("all")
        bw = self.btn_cv.winfo_width() or 320
        if state == "normal":
            rounded_rect(self.btn_cv, 0, 0, bw, 46, r=10,
                         fill=ACCENT, outline="")
            rounded_rect(self.btn_cv, 0, 0, bw, 24, r=10,
                         fill="#2E9FFF", outline="")
            self.btn_cv.create_text(bw//2, 23, text="Login  ➜",
                                    font=("Arial", 12, "bold"), fill=WHITE)
        elif state == "hover":
            rounded_rect(self.btn_cv, 0, 0, bw, 46, r=10,
                         fill=ACCENT_DARK, outline="")
            self.btn_cv.create_text(bw//2, 23, text="Login  ➜",
                                    font=("Arial", 12, "bold"), fill=WHITE)
        elif state == "loading":
            rounded_rect(self.btn_cv, 0, 0, bw, 46, r=10,
                         fill="#7FBFFF", outline="")
            self.btn_cv.create_text(bw//2, 23, text="⏳  Logging in…",
                                    font=("Arial", 12, "bold"), fill=WHITE)
        elif state == "success":
            rounded_rect(self.btn_cv, 0, 0, bw, 46, r=10,
                         fill=SUCCESS_GRN, outline="")
            self.btn_cv.create_text(bw//2, 23, text="✔  Welcome!",
                                    font=("Arial", 12, "bold"), fill=WHITE)
        elif state == "error":
            rounded_rect(self.btn_cv, 0, 0, bw, 46, r=10,
                         fill=ERROR_RED, outline="")
            self.btn_cv.create_text(bw//2, 23, text="✘  Invalid Credentials",
                                    font=("Arial", 12, "bold"), fill=WHITE)

    # ══════════════════════════════════════════════════════════
    #  BACKGROUND + LOGO ANIMATION
    # ══════════════════════════════════════════════════════════
    def _redraw_bg(self, event=None):
        w = self.bg.winfo_width()
        h = self.bg.winfo_height()
        if w < 2: return
        if w != self._bg_size[0] or h != self._bg_size[1]:
            self._bg_size[0], self._bg_size[1] = w, h
            self.bg.delete("all")
            draw_gradient(self.bg, w, h, "#6EC8EE", "#3AAAD4")
            draw_background_circles(self.bg, w, h)
            CW = 400
            card_x = int(w * 0.57) + (int(w * 0.43) - CW) // 2
            card_y = h // 2
            self.bg.create_window(card_x, card_y, window=self.card_host,
                                  width=min(CW+12, int(w*0.43)-20),
                                  height=min(530, h-30),
                                  tags="card_win")
        draw_logo_blocks(self.bg, self._logo_offsets, w, h)

    def _animate_logo(self):
        self._logo_t += 0.05
        for i in range(5):
            self._logo_offsets[i] = math.sin(
                self._logo_t + self._logo_phases[i]) * 8
        try:
            w = self.bg.winfo_width()
            h = self.bg.winfo_height()
            draw_logo_blocks(self.bg, self._logo_offsets, w, h)
            self.root.after(30, self._animate_logo)
        except:
            pass

    def run(self):
        self.root.mainloop()