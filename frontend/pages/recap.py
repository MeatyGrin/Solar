import tkinter as tk
from pages.base_page import BasePage
from styles import *

_LEFT_ITEMS  = ["Simulation", "Système", "Pertes du système",
                 "Auto-consommation", "Stockage"]
_RIGHT_ITEMS = ["Horizon", "Entrées précises", "Placement du module",
                 "Gestion d'énergie", "Évaluation économique", "Simulation détaillée"]


class RecapPage(BasePage):

    NAV_ITEMS = [
        {"text": "Accueil",      "page": "dashboard"},
        {"text": "Nouveau Proj", "checkbox": True, "checked": True,
         "page": "nouveau_projet"},
        {"text": "Enregistrer",  "page": "save_project"},
    ]

    def build_ui(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        main = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        main.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        tk.Label(main, text="Récapitulatif du projet",
                  font=F_TITLE, bg=BG_PANEL, fg=NAVY, pady=12).grid(
            row=0, column=0, sticky="w", padx=16)
        tk.Frame(main, bg=BORDER, height=1).grid(
            row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        body = tk.Frame(main, bg=BG_PANEL)
        body.grid(row=2, column=0, sticky="nsew", padx=16, pady=4)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, weight=0)

        tk.Label(body, text="Ensemble / sous-projet :", font=("Arial", 9, "bold"),
                  bg=BG_PANEL, fg=NAVY, anchor="w").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.cb_vars: dict = {}

        left_frame = tk.Frame(body, bg=BG_PANEL)
        left_frame.grid(row=1, column=0, sticky="nw", padx=(0, 10))
        for item in _LEFT_ITEMS:
            var = tk.BooleanVar(value=True)
            self.cb_vars[item] = var
            tk.Checkbutton(left_frame, text=item, variable=var, font=F_BODY,
                            bg=BG_PANEL, fg=TEXT_DARK, activebackground=BG_PANEL,
                            selectcolor=WHITE, anchor="w", pady=4).pack(fill="x")

        right_frame = tk.Frame(body, bg=BG_PANEL)
        right_frame.grid(row=1, column=1, sticky="nw", padx=(10, 0))
        for item in _RIGHT_ITEMS:
            var = tk.BooleanVar(value=True)
            self.cb_vars[item] = var
            tk.Checkbutton(right_frame, text=item, variable=var, font=F_BODY,
                            bg=BG_PANEL, fg=TEXT_DARK, activebackground=BG_PANEL,
                            selectcolor=WHITE, anchor="w", pady=4).pack(fill="x")

        # Bouton simulation (colonne droite)
        action_col = tk.Frame(body, bg=BG_PANEL, width=170)
        action_col.grid(row=1, column=2, sticky="ne", padx=(20, 0))
        action_col.pack_propagate(False)

        tk.Label(action_col, text="Lancer la\nsimulation",
                  font=F_SUB, bg=BG_PANEL, fg=NAVY, justify="center", pady=10).pack()
        self._orange_btn(action_col, "▶   Simuler",
                          command=self._run_simulation, width=16).pack(pady=4)
        tk.Frame(action_col, bg=BORDER, height=1).pack(fill="x", pady=10)
        self._outline_btn(action_col, "Simulation avancée",
                           command=self._run_advanced_simulation, width=18).pack()

        # Navigation bottom
        nav_bar = tk.Frame(main, bg=BG_PANEL)
        nav_bar.grid(row=3, column=0, sticky="ew", pady=6, padx=12)

        if "orientation":
            self._outline_btn(
                nav_bar, "◀  Précédent", width=14,
                command=lambda: self.controller.show_page("orientation"),
            ).pack(side="left", padx=4)

        if "simulation_params":
            self._orange_btn(
                nav_bar, "Suivant  ▶", width=14,
                command=lambda: self.controller.show_page("simulation_params"),
            ).pack(side="right", padx=4)

    def _run_simulation(self):
        params = {k: v.get() for k, v in self.cb_vars.items()}
        self.controller.backend.run_simulation(params)
        self.controller.show_page("simulation_params")

    def _run_advanced_simulation(self):
        self.controller.backend.run_advanced_simulation()