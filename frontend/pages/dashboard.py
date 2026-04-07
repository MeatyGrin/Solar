import tkinter as tk
from pages.base_page import BasePage
from styles import *

DEMO_PROJECTS = [
    {"name": "Projet Thomson",     "area": "48 m²", "power": "8.2 kWc"},
    {"name": "Projet Lino Olivie", "area": "32 m²", "power": "5.4 kWc"},
]


class DashboardPage(BasePage):

    NAV_ITEMS = [
        {"text": "Accueil",      "active": True},
        {"text": "Nouveau Proj", "checkbox": True, "checked": False,
         "page": "nouveau_projet"},
    ]

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # ── Panneau principal (gauche) ───────────────────────────────────────
        left = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        left.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)

        center = tk.Frame(left, bg=BG_PANEL)
        center.place(relx=0.5, rely=0.44, anchor="center")

        # Icône soleil
        icon_outer = tk.Frame(center, bg=ORANGE, width=76, height=76)
        icon_outer.pack()
        icon_outer.pack_propagate(False)
        tk.Label(
            icon_outer, text="☀", font=("Arial", 38),
            bg=ORANGE, fg=WHITE,
        ).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center, text="Bienvenue sur Solar System",
            font=("Arial", 17, "bold"), bg=BG_PANEL, fg=NAVY, pady=14,
        ).pack()

        tk.Label(
            center,
            text="Créez, configurez et simulez votre installation solaire\n"
                 "de manière simple et efficace.",
            font=F_BODY, bg=BG_PANEL, fg=TEXT_MED, justify="center",
        ).pack()

        self._orange_btn(
            center, "▶   Démarrer Votre Système",
            command=lambda: self.controller.show_page("nouveau_projet"),
            width=28,
        ).pack(pady=18)

        self._nav_bottom(left, next_page="nouveau_projet")

        # ── Panneau droit – Projets récents ──────────────────────────────────
        right = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", width=210)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        right.pack_propagate(False)

        tk.Label(
            right, text="Projets récents",
            font=F_SUB, bg=BG_PANEL, fg=NAVY, pady=10,
        ).pack(anchor="w", padx=12)
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=10)

        for proj in DEMO_PROJECTS:
            self._project_card(right, proj)

    def _project_card(self, parent, proj: dict):
        card = tk.Frame(parent, bg=BG_THUMB, bd=1, relief="solid", cursor="hand2")
        card.pack(fill="x", padx=10, pady=8)
        card.bind("<Button-1>", lambda e, p=proj: self._open_project(p))

        tk.Label(
            card, text=proj["name"],
            font=("Arial", 9, "bold"), bg=BG_THUMB, fg=NAVY,
            padx=10, pady=5, anchor="w",
        ).pack(fill="x")

        mini = tk.Canvas(card, width=180, height=70, bg="#E8EEFF",
                          highlightthickness=0)
        mini.pack(padx=6, pady=(0, 4))
        self._draw_mini_building(mini)

        tk.Label(
            card,
            text=f"Surface : {proj['area']}   •   Puissance : {proj['power']}",
            font=F_SMALL, bg=BG_THUMB, fg=TEXT_MED,
            padx=10, pady=4, anchor="w",
        ).pack(fill="x")

    def _draw_mini_building(self, canvas):
        cx, cy, s = 90, 35, 0.42
        canvas.create_polygon(
            [cx-70*s, cy+18*s, cx+70*s, cy+18*s,
             cx+70*s, cy+55*s, cx-70*s, cy+55*s],
            fill="#D5C8A0", outline="#B0A070")
        canvas.create_polygon(
            [cx+70*s, cy+18*s, cx+100*s, cy+3*s,
             cx+100*s, cy+40*s, cx+70*s, cy+55*s],
            fill="#C0B085", outline="#B0A070")
        canvas.create_polygon(
            [cx-70*s, cy+18*s, cx+70*s, cy+18*s,
             cx+100*s, cy+3*s, cx-40*s, cy+3*s],
            fill="#E8DDB0", outline="#B0A070")
        for col in range(2):
            for row in range(2):
                px = cx + (-60 + col*52)*s
                py = cy + (14 - row*12)*s
                panel = [px, py, px+46*s, py, px+56*s, py-10*s, px+10*s, py-10*s]
                canvas.create_polygon(panel, fill=BLUE_PANEL, outline=BLUE_LT)

    def _open_project(self, proj: dict):
        self.controller.current_project.update(proj)
        self.controller.show_page("plan")