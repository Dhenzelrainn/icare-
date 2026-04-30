# signup.py — Sign Up Page

import math
import tkinter as tk
from tkinter import messagebox

from utils import (
    WHITE, ACCENT, ACCENT_DARK, TEXT_DARK, TEXT_GRAY,
    ERROR_RED, BORDER_CLR,
    F_LABEL, F_ERR,
    draw_gradient, rounded_rect, rgb_to_hex,
    draw_background_circles, draw_logo_blocks, draw_card_shadow,
    make_field
)


class SignupPage:
    def __init__(self, parent_win, auth_manager, on_back):
        self.auth    = auth_manager
        self.on_back = on_back

        self.win = tk.Toplevel(parent_win)
        self.win.title("iCare Daycare | Sign Up")
        self.win.geometry("1000x640")
        self.win.minsize(600, 500)
        self.win.resizable(True, True)
        self.win.grab_set()
        self.win.protocol("WM_DELETE_WINDOW", self._go_back)

        self._logo_offsets = [0.0] * 5
        self._logo_phases  = [i * 0.4 for i in range(5)]
        self._logo_t       = 0.0
        self._bg_size      = [0, 0]

        self._build_ui()

    def _build_ui(self):
        self.bg = tk.Canvas(self.win, bd=0, highlightthickness=0)
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

    def _build_card_content(self):
        inner = self.inner

        header = tk.Frame(inner, bg=WHITE)
        header.pack(fill="x", pady=(20, 0))
        icon_row = tk.Frame(header, bg=WHITE)
        icon_row.pack()
        for letter, color in zip(["i", "C"], ["#E05555", "#4CAF50"]):
            tk.Label(icon_row, text=letter,
                     font=("Arial Rounded MT Bold", 14, "bold"),
                     fg=WHITE, bg=color, width=2).pack(side="left", padx=1)
        tk.Label(icon_row, text="CARE",
                 font=("Arial Rounded MT Bold", 14, "bold"),
                 fg=ACCENT, bg=WHITE).pack(side="left", padx=(4, 0))

        tk.Label(inner, text="Create Account",
                 font=("Arial", 17, "bold"), fg=TEXT_DARK,
                 bg=WHITE).pack(pady=(6, 1))
        tk.Label(inner, text="Join iCare Daycare today",
                 font=("Arial", 10), fg=TEXT_GRAY,
                 bg=WHITE).pack(pady=(0, 8))

        tk.Frame(inner, bg=BORDER_CLR, height=1).pack(
            fill="x", padx=28, pady=(0, 10))

        self.err_var    = tk.StringVar()
        self._err_frame = tk.Frame(inner, bg="#FFF0F0")
        tk.Label(self._err_frame, text="⚠", font=("Arial", 11),
                 fg=ERROR_RED, bg="#FFF0F0").pack(
                 side="left", padx=(10, 4), pady=5)
        tk.Label(self._err_frame, textvariable=self.err_var, font=F_ERR,
                 fg=ERROR_RED, bg="#FFF0F0", anchor="w",
                 wraplength=280).pack(side="left", pady=5, padx=(0, 10))

        name_row = tk.Frame(inner, bg=WHITE)
        name_row.pack(fill="x", padx=28, pady=(0, 4))
        name_row.columnconfigure(0, weight=1)
        name_row.columnconfigure(1, weight=1)

        tk.Label(name_row, text="First Name", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").grid(
                 row=0, column=0, sticky="w", padx=(0, 6))
        tk.Label(name_row, text="Last Name", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").grid(
                 row=0, column=1, sticky="w")

        fn_f, self.fn_entry = make_field(name_row, "👤",
                                          clear_error_cb=self._clear_error)
        fn_f.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(0, 10))

        ln_f, self.ln_entry = make_field(name_row, "👤",
                                          clear_error_cb=self._clear_error)
        ln_f.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        tk.Label(inner, text="Username", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").pack(fill="x", padx=28)
        u_f, self.u_entry = make_field(inner, "🪪",
                                        clear_error_cb=self._clear_error)
        u_f.pack(fill="x", padx=28, pady=(0, 8))

        tk.Label(inner, text="Password", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").pack(fill="x", padx=28)
        p_f, self.p_entry = make_field(inner, "🔒", show_char="•",
                                        clear_error_cb=self._clear_error)
        p_f.pack(fill="x", padx=28, pady=(0, 8))

        tk.Label(inner, text="Confirm Password", font=F_LABEL,
                 fg=TEXT_DARK, bg=WHITE, anchor="w").pack(fill="x", padx=28)
        cp_f, self.cp_entry = make_field(inner, "🔒", show_char="•",
                                          clear_error_cb=self._clear_error)
        cp_f.pack(fill="x", padx=28, pady=(0, 8))

        reg_cv = tk.Canvas(inner, height=46, bd=0,
                           highlightthickness=0, bg=WHITE)
        reg_cv.pack(fill="x", padx=28, pady=(4, 0))

        def draw_reg_btn(hover=False):
            reg_cv.delete("all")
            bw = reg_cv.winfo_width() or 320
            c = ACCENT_DARK if hover else ACCENT
            rounded_rect(reg_cv, 0, 0, bw, 46, r=10, fill=c, outline="")
            if not hover:
                rounded_rect(reg_cv, 0, 0, bw, 24, r=10,
                             fill="#2E9FFF", outline="")
            reg_cv.create_text(bw//2, 23, text="Create Account",
                                font=("Arial", 12, "bold"), fill=WHITE)

        reg_cv.bind("<Configure>", lambda e: draw_reg_btn())
        reg_cv.bind("<Enter>",     lambda e: draw_reg_btn(True))
        reg_cv.bind("<Leave>",     lambda e: draw_reg_btn(False))
        reg_cv.bind("<Button-1>",  lambda e: self._do_signup())
        self.win.bind("<Return>",  lambda e: self._do_signup())

        back_frame = tk.Frame(inner, bg=WHITE)
        back_frame.pack(pady=(10, 16))
        tk.Label(back_frame, text="Already have an account?  ",
                 font=("Arial", 10), fg=TEXT_GRAY, bg=WHITE).pack(side="left")
        back_lbl = tk.Label(back_frame, text="Log in",
                             font=("Arial", 10, "bold"), fg=ACCENT,
                             bg=WHITE, cursor="hand2")
        back_lbl.pack(side="left")
        back_lbl.bind("<Enter>", lambda e: back_lbl.config(
            fg=ACCENT_DARK, font=("Arial", 10, "bold", "underline")))
        back_lbl.bind("<Leave>", lambda e: back_lbl.config(
            fg=ACCENT, font=("Arial", 10, "bold")))
        back_lbl.bind("<Button-1>", lambda e: self._go_back())

    def _do_signup(self):
        fn = self.fn_entry.get().strip()
        ln = self.ln_entry.get().strip()
        u  = self.u_entry.get().strip()
        p  = self.p_entry.get()
        cp = self.cp_entry.get()

        success, msg = self.auth.register(fn, ln, u, p, cp)

        if not success:
            self._show_error(msg)
            return

        messagebox.showinfo(
            "Success",
            f"Account created!\nYou can now log in as '{u}'.",
            parent=self.win
        )
        self._go_back()

    def _go_back(self):
        self.win.grab_release()
        self.win.destroy()
        self.on_back()

    def _show_error(self, msg):
        self.err_var.set(msg)
        self._err_frame.pack(fill="x", padx=28, pady=(0, 6))

    def _clear_error(self):
        self.err_var.set("")
        self._err_frame.pack_forget()

    def _redraw_bg(self, event=None):
        w = self.bg.winfo_width()
        h = self.bg.winfo_height()
        if w < 2: return
        CW = 400
        if w != self._bg_size[0] or h != self._bg_size[1]:
            self._bg_size[0], self._bg_size[1] = w, h
            self.bg.delete("all")
            draw_gradient(self.bg, w, h, "#6EC8EE", "#3AAAD4")
            draw_background_circles(self.bg, w, h)
            card_x = int(w * 0.57) + (int(w * 0.43) - CW) // 2
            card_y = h // 2
            self.bg.create_window(card_x, card_y, window=self.card_host,
                                  width=min(CW+12, int(w*0.43)-20),
                                  height=min(570, h-30),
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
            self.win.after(30, self._animate_logo)
        except:
            pass
