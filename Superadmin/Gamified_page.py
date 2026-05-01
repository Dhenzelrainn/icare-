import tkinter as tk


BG_MAIN = "#f4f6f9"
WHITE = "#ffffff"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6b7280"
BORDER = "#d1d5db"


def make_card(parent):
    return tk.Frame(
        parent,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER,
        bd=0
    )


def table_header(parent, headers, weights):
    for col, weight in enumerate(weights):
        parent.grid_columnconfigure(
            col,
            weight=weight,
            uniform="gamified_columns"
        )

    for col, title in enumerate(headers):
        cell = tk.Frame(parent, bg=WHITE, height=42)
        cell.grid(row=0, column=col, sticky="nsew")
        cell.grid_propagate(False)

        tk.Label(
            cell,
            text=title,
            bg=WHITE,
            fg=TEXT_DARK,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill="both", expand=True, padx=14)


def table_line(parent, row, column_count):
    line = tk.Frame(parent, bg="#e5e7eb", height=1)
    line.grid(row=row, column=0, columnspan=column_count, sticky="ew")


def empty_table_row(parent, column_count):
    for col in range(column_count):
        cell = tk.Frame(parent, bg=WHITE, height=40)
        cell.grid(row=2, column=col, sticky="nsew")
        cell.grid_propagate(False)

        if col == 0:
            tk.Label(
                cell,
                text="No activities",
                bg=WHITE,
                fg=TEXT_DARK,
                font=("Segoe UI", 10),
                anchor="w"
            ).pack(fill="both", expand=True, padx=14)

    table_line(parent, 3, column_count)


class GamifiedPage:
    def __init__(self, page_frame):
        self.page_frame = page_frame

    def show(self):
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        root = tk.Frame(self.page_frame, bg=BG_MAIN)
        root.grid(row=0, column=0, sticky="nsew")

        self.page_frame.columnconfigure(0, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        outer = tk.Frame(root, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=58, pady=(34, 0))

        tk.Label(
            outer,
            text="Gamified Activities",
            bg=BG_MAIN,
            fg=TEXT_DARK,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w", pady=(0, 10))

        card = make_card(outer)
        card.pack(fill="x")

        table = tk.Frame(card, bg=WHITE)
        table.pack(fill="x", padx=18, pady=(16, 20))

        headers = ["#", "Student ID", "Activity", "Progress", "Score", "Action"]

        # Higher number = wider column
        column_weights = [1, 3, 5, 4, 3, 4]

        table_header(table, headers, column_weights)
        table_line(table, 1, len(headers))
        empty_table_row(table, len(headers))