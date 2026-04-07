import tkinter as tk
from styles import *

_ICONS = [
    ("⌂", "dashboard", "Accueil"),
    ("ℹ", "info",      "Informations"),
    ("＋", "add",      "Ajouter"),
    ("－", "remove",   "Retirer"),
    ("↑",  "up",       "Remonter"),
    ("↓",  "down",     "Descendre"),
]


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=SIDEBAR_BG, width=SIDEBAR_W)
        self.controller = controller
        self.pack_propagate(False)
        self._build()

    def _build(self):
        for icon, name, tooltip in _ICONS:
            btn = tk.Label(
                self, text=icon, font=("Arial", 13),
                bg=SIDEBAR_BG, fg=NAVY,
                cursor="hand2", width=2, pady=9,
            )
            btn.pack(side="top", fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=ORANGE_LT, fg=ORANGE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=SIDEBAR_BG, fg=NAVY))
            btn.bind("<Button-1>", lambda e, n=name: self._on_click(n))

    def _on_click(self, name: str):
        if name == "dashboard":
            self.controller.show_page("dashboard")