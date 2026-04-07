import tkinter as tk
from styles import *


class BasePage(tk.Frame):
    NAV_ITEMS: list = []

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.build_ui()

    # ── Construction UI ──────────────────────────────────────────────────────

    def build_ui(self):
        pass

    # ── Barre de navigation ──────────────────────────────────────────────────

    def refresh_navbar(self, nav_frame: tk.Frame):
        for w in nav_frame.winfo_children():
            w.destroy()

        home = tk.Label(
            nav_frame, text="⌂", font=("Arial", 17),
            bg=NAV_BG, fg=NAVY, cursor="hand2", padx=10,
        )
        home.pack(side="left", pady=6)
        home.bind("<Button-1>", lambda e: self.controller.show_page("dashboard"))

        tk.Frame(nav_frame, bg=GRAY_LT, width=1, height=24).pack(
            side="left", padx=4, pady=10
        )

        for item in self.NAV_ITEMS:
            self._nav_item(nav_frame, item)

        save = tk.Label(
            nav_frame, text="💾  Enregistrer",
            font=F_NAV, bg=NAV_BG, fg=NAVY, cursor="hand2", padx=12,
        )
        save.pack(side="right", pady=6)
        save.bind("<Button-1>", lambda e: self.controller.show_page("save_project"))

    def _nav_item(self, nav_frame: tk.Frame, item: dict):
        frame = tk.Frame(nav_frame, bg=NAV_BG)
        frame.pack(side="left", padx=2, pady=6)

        if item.get("checkbox"):
            var = tk.BooleanVar(value=item.get("checked", False))
            tk.Checkbutton(
                frame, variable=var, bg=NAV_BG,
                activebackground=NAV_BG, selectcolor=NAV_BG,
                relief="flat", state="disabled",
            ).pack(side="left")

        color = ORANGE if item.get("active") else NAVY
        lbl = tk.Label(
            frame, text=item["text"],
            font=F_NAV, bg=NAV_BG, fg=color,
            cursor="hand2" if item.get("page") else "arrow", padx=3,
        )
        lbl.pack(side="left")
        if item.get("page"):
            lbl.bind(
                "<Button-1>",
                lambda e, p=item["page"]: self.controller.show_page(p),
            )

    # ── Widgets réutilisables ────────────────────────────────────────────────

    def _orange_btn(self, parent, text: str, command=None, width=18) -> tk.Button:
        btn = tk.Button(
            parent, text=text, font=F_BTN,
            bg=ORANGE, fg=WHITE,
            activebackground=ORANGE_HVR, activeforeground=WHITE,
            relief="flat", padx=12, pady=6,
            cursor="hand2", width=width,
            command=command or (lambda: None),
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=ORANGE_HVR))
        btn.bind("<Leave>", lambda e: btn.configure(bg=ORANGE))
        return btn

    def _outline_btn(self, parent, text: str, command=None, width=12) -> tk.Button:
        return tk.Button(
            parent, text=text, font=F_BTN,
            bg=BG_PANEL, fg=NAVY,
            relief="solid", bd=1,
            padx=8, pady=4, cursor="hand2",
            width=width,
            command=command or (lambda: None),
        )

    def _field(self, parent, label: str, row: int,
               var: tk.Variable = None, col_offset: int = 0) -> tk.Entry:
        tk.Label(
            parent, text=label, font=F_BODY,
            bg=BG_PANEL, fg=TEXT_DARK, anchor="w",
        ).grid(row=row, column=col_offset, sticky="w", pady=(6, 1), padx=(0, 8))
        if var is None:
            var = tk.StringVar()
        entry = tk.Entry(
            parent, textvariable=var, font=F_BODY,
            bg=WHITE, relief="solid", bd=1, width=30,
        )
        entry.grid(
            row=row, column=col_offset + 1, sticky="ew",
            pady=(6, 1), padx=(0, 4),
        )
        return entry

    def _nav_bottom(self, parent, prev_page: str = None, next_page: str = None):
        bar = tk.Frame(parent, bg=BG_PANEL)
        bar.pack(fill="x", side="bottom", pady=6, padx=12)

        if prev_page:
            self._outline_btn(
                bar, "◀  Précédent", width=14,
                command=lambda: self.controller.show_page(prev_page),
            ).pack(side="left", padx=4)

        if next_page:
            self._orange_btn(
                bar, "Suivant  ▶", width=14,
                command=lambda: self.controller.show_page(next_page),
            ).pack(side="right", padx=4)

    # ── Cycle de vie ─────────────────────────────────────────────────────────

    def on_show(self, **kwargs):
        pass