# utils.py — Colors, Fonts, and Helper Functions

# ══════════════════════════════════════════════════════════════
#  COLORS
# ══════════════════════════════════════════════════════════════
WHITE       = "#FFFFFF"
ACCENT      = "#1E8FFF"
ACCENT_DARK = "#0c6fd4"
TEXT_DARK   = "#1A1A2E"
TEXT_MED    = "#555555"
TEXT_GRAY   = "#999999"
ERROR_RED   = "#E53E3E"
SUCCESS_GRN = "#2ECC71"
BORDER_CLR  = "#E0E0E0"
INPUT_BG    = "#F7FBFF"

BLOCK_COLORS = ["#E05555", "#4CAF50", "#7B68EE", "#F5A623", "#9B59B6"]

# Dashboard colors
DASH_SIDEBAR_TOP = "#1a2a4a"
DASH_BG          = "#f0f4f8"

# Stat card colors
STAT_BLUE   = "#2196F3"
STAT_GREEN  = "#2E7D32"
STAT_CYAN   = "#00BCD4"
STAT_YELLOW = "#F9A825"

# ══════════════════════════════════════════════════════════════
#  FONTS
# ══════════════════════════════════════════════════════════════
F_LABEL = ("Arial", 10, "bold")
F_INPUT = ("Arial", 12)
F_BTN   = ("Arial", 13, "bold")
F_ERR   = ("Arial", 9)
F_HINT  = ("Arial", 8)


# ══════════════════════════════════════════════════════════════
#  COLOR HELPERS
# ══════════════════════════════════════════════════════════════
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

def darken(hex_color, amt=40):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(max(r-amt, 0), max(g-amt, 0), max(b-amt, 0))

def lighten(hex_color, amt=40):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(min(r+amt, 255), min(g+amt, 255), min(b+amt, 255))


# ══════════════════════════════════════════════════════════════
#  CANVAS HELPERS
# ══════════════════════════════════════════════════════════════
def draw_gradient(canvas, w, h, top, bottom):
    r1, g1, b1 = hex_to_rgb(top)
    r2, g2, b2 = hex_to_rgb(bottom)
    for i in range(h):
        t = i / max(h, 1)
        color = rgb_to_hex(r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t)
        canvas.create_line(0, i, w, i, fill=color)

def rounded_rect(canvas, x1, y1, x2, y2, r=15, **kw):
    pts = [x1+r, y1,  x2-r, y1,  x2, y1,  x2, y1+r,
           x2, y2-r,  x2, y2,  x2-r, y2,  x1+r, y2,
           x1, y2,  x1, y2-r,  x1, y1+r,  x1, y1]
    return canvas.create_polygon(pts, smooth=True, **kw)

def draw_background_circles(canvas, w, h):
    circles = [
        (0.12, 0.18, 0.22, "#8ED8F0"),
        (0.38, 0.08, 0.12, "#9ADAF5"),
        (0.05, 0.72, 0.18, "#4DAAA0"),
        (0.25, 0.85, 0.10, "#6ECFB8"),
        (0.55, 0.80, 0.22, "#5BB8A0"),
        (0.82, 0.88, 0.14, "#4DAAA0"),
        (0.90, 0.12, 0.17, "#5BB8A0"),
        (0.95, 0.55, 0.09, "#8ED8F0"),
        (0.06, 0.45, 0.07, "#7DD8F0"),
        (0.70, 0.04, 0.06, "#9ADAF5"),
        (0.48, 0.55, 0.06, "#6ECFB8"),
    ]
    for cx_p, cy_p, r_p, color in circles:
        r_ = int(min(w, h) * r_p)
        cx_ = int(w * cx_p)
        cy_ = int(h * cy_p)
        canvas.create_oval(cx_-r_, cy_-r_, cx_+r_, cy_+r_,
                           fill=color, outline="", stipple="gray50")


# ══════════════════════════════════════════════════════════════
#  REUSABLE STYLED INPUT FIELD
# ══════════════════════════════════════════════════════════════
def make_field(parent, icon_text, show_char="", clear_error_cb=None):
    import tkinter as tk

    outer = tk.Frame(parent, bg=BORDER_CLR, bd=0)
    inner_f = tk.Frame(outer, bg=INPUT_BG, bd=0)
    inner_f.pack(padx=1, pady=1, fill="both", expand=True)

    icon_lbl = tk.Label(inner_f, text=icon_text, font=("Arial", 13),
                        fg=TEXT_GRAY, bg=INPUT_BG, width=2)
    icon_lbl.pack(side="left", padx=(8, 0))

    entry = tk.Entry(inner_f, show=show_char, font=("Arial", 12),
                     bd=0, relief="flat", bg=INPUT_BG, fg=TEXT_DARK,
                     insertbackground=ACCENT, highlightthickness=0)
    entry.pack(side="left", fill="both", expand=True, padx=(4, 8), pady=10)

    if show_char:
        shown = [False]
        def toggle_eye():
            shown[0] = not shown[0]
            entry.config(show="" if shown[0] else show_char)
            eye_lbl.config(text="🙈" if shown[0] else "👁")
        eye_lbl = tk.Label(inner_f, text="👁", font=("Arial", 11),
                           fg=TEXT_GRAY, bg=INPUT_BG, cursor="hand2")
        eye_lbl.pack(side="right", padx=(0, 10))
        eye_lbl.bind("<Button-1>", lambda e: toggle_eye())

    def on_focus_in(_=None):
        outer.config(bg=ACCENT)
        icon_lbl.config(fg=ACCENT)

    def on_focus_out(_=None):
        outer.config(bg=BORDER_CLR)
        icon_lbl.config(fg=TEXT_GRAY)
        if clear_error_cb:
            clear_error_cb()

    entry.bind("<FocusIn>",  on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return outer, entry


# ══════════════════════════════════════════════════════════════
#  ANIMATED iCARE LOGO BLOCKS
# ══════════════════════════════════════════════════════════════
import math

def draw_logo_blocks(canvas, logo_offsets, w, h, area_pct=0.55):
    LETTERS = ["i", "C", "A", "R", "E"]
    canvas.delete("logo")
    if w < 2: return
    logo_area_w = int(w * area_pct)
    bsize = max(50, min(100, (logo_area_w - 60) // 6))
    gap   = max(8, bsize // 10)
    total = len(LETTERS) * bsize + (len(LETTERS)-1) * gap
    start_x = (logo_area_w - total) // 2
    y_base  = h // 2 - bsize // 2

    for i, (letter, color) in enumerate(zip(LETTERS, BLOCK_COLORS)):
        x1 = start_x + i * (bsize + gap)
        y1 = y_base + logo_offsets[i]
        x2 = x1 + bsize
        y2 = y1 + bsize
        fs = max(16, bsize // 2 - 4)
        rounded_rect(canvas, x1+4, y1+6, x2+4, y2+4, r=14,
                     fill=darken(color, 50), outline="", tags="logo")
        rounded_rect(canvas, x1, y1, x2, y2, r=14,
                     fill=color, outline="", tags="logo")
        rounded_rect(canvas, x1+6, y1+5, x1+bsize//2+4, y1+bsize//2-2, r=8,
                     fill=lighten(color, 45), outline="", tags="logo")
        canvas.create_text(x1+bsize//2, y1+bsize//2,
                           text=letter,
                           font=("Arial Rounded MT Bold", fs, "bold"),
                           fill=WHITE, tags="logo")


def draw_card_shadow(card_cv, inner_frame):
    w = card_cv.winfo_width()
    h = card_cv.winfo_height()
    if w < 4: return
    card_cv.delete("all")
    for s in [10, 7, 4, 2]:
        shadow_color = rgb_to_hex(
            max(int(0x40 - s*2), 0x20),
            max(int(0x90 - s*2), 0x60),
            max(int(0xB0 - s*2), 0x80))
        rounded_rect(card_cv, s, s+2, w-2, h-2+s, r=22,
                     fill=shadow_color, outline="")
    rounded_rect(card_cv, 0, 0, w-4, h-4, r=22, fill=WHITE, outline=WHITE)
    card_cv.create_window(5, 5, window=inner_frame,
                          width=w-18, height=h-18, anchor="nw")
