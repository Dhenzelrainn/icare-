# constants.py — Shared colors, fonts, and helper functions

import tkinter as tk
from tkinter import ttk

# ── Try to import from utils; fall back to safe defaults if not found ──
try:
    from utils import (
        WHITE, ACCENT, ACCENT_DARK, TEXT_DARK, TEXT_MED, TEXT_GRAY,
        ERROR_RED, SUCCESS_GRN, BORDER_CLR, DASH_BG,
        STAT_BLUE, STAT_GREEN, STAT_CYAN, STAT_YELLOW,
        F_LABEL,
        rounded_rect, darken
    )
except ImportError:
    WHITE       = "#ffffff"
    ACCENT      = "#2563eb"
    ACCENT_DARK = "#1d4ed8"
    TEXT_DARK   = "#1a1a2e"
    TEXT_MED    = "#4a4a6a"
    TEXT_GRAY   = "#9090a0"
    ERROR_RED   = "#dc2626"
    SUCCESS_GRN = "#16a34a"
    BORDER_CLR  = "#e0e0ec"
    DASH_BG     = "#f0f2f5"
    STAT_BLUE   = "#2563eb"
    STAT_GREEN  = "#16a34a"
    STAT_CYAN   = "#06b6d4"
    STAT_YELLOW = "#f59e0b"
    F_LABEL     = ("Segoe UI", 9)
    def rounded_rect(*a, **kw): pass
    def darken(c, a=20): return c

# ─────────────────────── SIDEBAR COLOURS ────────────────────────────
SIDEBAR_BG  = "#1a2a4a"
SIDEBAR_ACT = "#2563eb"
SIDEBAR_HOV = "#1e3a6e"
SIDEBAR_SEP = "#2a3f5f"

# ─────────────────────── BUTTON COLOURS ─────────────────────────────
BTN_CYAN     = "#06b6d4"
BTN_YELLOW   = "#f59e0b"
BTN_DARKGRAY = "#4b5563"
BTN_GREEN    = "#16a34a"
BTN_RED      = "#dc2626"
STATUS_GREEN = "#16a34a"

# ─────────────────────── FONTS ───────────────────────────────────────
FONT_TITLE   = ("Segoe UI", 18, "bold")
FONT_HEADING = ("Segoe UI", 10, "bold")
FONT_BODY    = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI", 9)
FONT_BTN     = ("Segoe UI", 9, "bold")

# ─────────────────────── HELPERS ────────────────────────────────────

def _darken_hex(hex_color, amount=20):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "#{:02x}{:02x}{:02x}".format(
        max(0, r - amount), max(0, g - amount), max(0, b - amount))


def make_btn(parent, text, color, command, fg=WHITE, width=None):
    kw = dict(font=FONT_BTN, fg=fg, bg=color, relief="flat", bd=0,
              cursor="hand2", padx=8, pady=4,
              activebackground=color, activeforeground=fg,
              command=command)
    if width:
        kw["width"] = width
    b = tk.Button(parent, text=text, **kw)
    b.bind("<Enter>", lambda e, _b=b, _c=color: _b.config(bg=_darken_hex(_c)))
    b.bind("<Leave>", lambda e, _b=b, _c=color: _b.config(bg=_c))
    return b


def separator(parent, bg=BORDER_CLR, height=1, pady=0):
    tk.Frame(parent, bg=bg, height=height).pack(fill="x", pady=pady)