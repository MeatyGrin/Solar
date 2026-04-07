"""
simulation_params.py
====================
Page "Paramètres de simulation" (Frame 24 dans la maquette).
Affiche les paramètres du projet, les résultats de simulation mockés
et les graphiques de production/pertes.
"""

import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from styles import *


# ── Données de démonstration ──────────────────────────────────────────────
_MONTHLY_PRODUCTION = [
    ("Jan", 320), ("Fév", 380), ("Mar", 520), ("Avr", 610),
    ("Mai", 680), ("Jui", 720), ("Jul", 740), ("Aoû", 700),
    ("Sep", 590), ("Oct", 450), ("Nov", 330), ("Déc", 290),
]
_MONTHLY_LOSSES = [
    ("Jan", 12), ("Fév", 10), ("Mar",  8), ("Avr",  7),
    ("Mai",  6), ("Jui",  5), ("Jul",  5), ("Aoû",  6),
    ("Sep",  7), ("Oct",  9), ("Nov", 11), ("Déc", 13),
]


class SimulationParamsPage(BasePage):

    NAV_ITEMS = [
        {"text": "Accueil",      "page": "dashboard"},
        {"text": "Nouveau Proj", "checkbox": True, "checked": True,
         "page": "nouveau_projet"},
        {"text": "Enregistrer",  "page": "save_project"},
    ]

    # ── Construction UI ───────────────────────────────────────────────────

    def build_ui(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        main = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        main.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=0)  # titre
        main.rowconfigure(1, weight=0)  # séparateur
        main.rowconfigure(2, weight=0)  # infos projet
        main.rowconfigure(3, weight=0)  # séparateur
        main.rowconfigure(4, weight=0)  # bandeaux résultats
        main.rowconfigure(5, weight=1)  # graphiques (flex)
        main.rowconfigure(6, weight=0)  # boutons action
        main.rowconfigure(7, weight=0)  # nav bas

        # ── En-tête ──────────────────────────────────────────────────────
        header = tk.Frame(main, bg=BG_PANEL)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 0))
        tk.Label(
            header, text="Paramètres de simulation",
            font=F_TITLE, bg=BG_PANEL, fg=NAVY,
        ).pack(side="left")

        tk.Frame(main, bg=BORDER, height=1).grid(
            row=1, column=0, sticky="ew", padx=12, pady=(6, 0)
        )

        # ── Bloc informations (2 colonnes) ────────────────────────────────
        info_frame = tk.Frame(main, bg=BG_PANEL)
        info_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=8)
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Colonne gauche – informations projet
        left_col = tk.LabelFrame(
            info_frame, text="Projet", font=("Arial", 9, "bold"),
            bg=BG_PANEL, fg=NAVY, bd=1, relief="groove",
        )
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=2)

        self._lbl_project_name = self._info_row(left_col, "Projet", "—")
        self._lbl_site         = self._info_row(left_col, "Site",   "—")
        self._info_row(left_col, "Type de système", "Raccordé au réseau")
        self._info_row(left_col, "Simulation",      "01/01 au 31/12")

        # Colonne droite – champ PV
        right_col = tk.LabelFrame(
            info_frame, text="Champ PV", font=("Arial", 9, "bold"),
            bg=BG_PANEL, fg=NAVY, bd=1, relief="groove",
        )
        right_col.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=2)

        self._info_row(right_col, "Module PV",        "—")
        self._info_row(right_col, "Onduleur",         "—")
        self._info_row(right_col, "Puiss. nominale",  "—  kWc")
        self._info_row(right_col, "Puls. nom. ond.",  "—  kW")
        self._info_row(right_col, "Tension MPP",      "—  V")
        self._info_row(right_col, "Courant MPP",      "—  A")
        self._info_row(right_col, "Nbr. d'onduleurs", "—")

        # ── Séparateur + titre résultats ──────────────────────────────────
        tk.Frame(main, bg=BORDER, height=1).grid(
            row=3, column=0, sticky="ew", padx=12, pady=(0, 4)
        )

        res_header = tk.Frame(main, bg=BG_PANEL)
        res_header.grid(row=3, column=0, sticky="ew", padx=16, pady=(8, 0))
        tk.Label(
            res_header, text="Nouvelles productions",
            font=("Arial", 10, "bold"), bg=BG_PANEL, fg=NAVY,
        ).pack(side="left")

        # ── Bandeaux KPI ──────────────────────────────────────────────────
        kpi_frame = tk.Frame(main, bg=BG_CARD, bd=1, relief="solid")
        kpi_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=4)

        kpi_items = [
            ("Production\ndu système",  "—",   "kWh/an"),
            ("Prod.\nnormalisée",       "—",   "kWh/kWc"),
            ("Productible",             "—",   "kWh"),
            ("Indice de\nperformance",  "—",   ""),
            ("Pertes\nchamp",           "—",   "%"),
            ("Pertes\nsystème",         "—",   "%"),
        ]
        for i, (label, val, unit) in enumerate(kpi_items):
            col_frame = tk.Frame(kpi_frame, bg=BG_CARD)
            col_frame.pack(side="left", expand=True, fill="both")

            if i > 0:
                tk.Frame(col_frame, bg=BORDER, width=1).pack(
                    side="left", fill="y", pady=6
                )

            inner = tk.Frame(col_frame, bg=BG_CARD)
            inner.pack(side="left", expand=True, fill="both",
                       padx=10, pady=8)

            tk.Label(
                inner, text=label,
                font=F_SMALL, bg=BG_CARD, fg=TEXT_MED,
                wraplength=90, justify="center",
            ).pack()

            value_lbl = tk.Label(
                inner, text=val,
                font=("Arial", 13, "bold"), bg=BG_CARD, fg=NAVY,
            )
            value_lbl.pack()

            if unit:
                tk.Label(
                    inner, text=unit,
                    font=F_SMALL, bg=BG_CARD, fg=GRAY,
                ).pack()

        # ── Graphiques ────────────────────────────────────────────────────
        charts_frame = tk.Frame(main, bg=BG_PANEL)
        charts_frame.grid(row=5, column=0, sticky="nsew", padx=12, pady=4)
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)
        charts_frame.rowconfigure(0, weight=1)

        # Graphique 1 – Production mensuelle
        left_chart = tk.LabelFrame(
            charts_frame,
            text="Production mensuelle (kWh)",
            font=("Arial", 9, "bold"),
            bg=BG_CARD, fg=NAVY, bd=1, relief="groove",
        )
        left_chart.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=2)
        left_chart.rowconfigure(0, weight=1)
        left_chart.columnconfigure(0, weight=1)

        self.canvas_prod = tk.Canvas(
            left_chart, bg=BG_CARD, highlightthickness=0
        )
        self.canvas_prod.grid(row=0, column=0, sticky="nsew",
                               padx=6, pady=(4, 6))
        self.canvas_prod.bind(
            "<Configure>",
            lambda e: self._draw_bar_chart(
                self.canvas_prod, _MONTHLY_PRODUCTION,
                bar_color=ORANGE, bg=BG_CARD, unit="kWh",
            ),
        )

        # Graphique 2 – Pertes système
        right_chart = tk.LabelFrame(
            charts_frame,
            text="Pertes système (%)",
            font=("Arial", 9, "bold"),
            bg=BG_CARD, fg=NAVY, bd=1, relief="groove",
        )
        right_chart.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=2)
        right_chart.rowconfigure(0, weight=1)
        right_chart.columnconfigure(0, weight=1)

        self.canvas_loss = tk.Canvas(
            right_chart, bg=BG_CARD, highlightthickness=0
        )
        self.canvas_loss.grid(row=0, column=0, sticky="nsew",
                               padx=6, pady=(4, 6))
        self.canvas_loss.bind(
            "<Configure>",
            lambda e: self._draw_bar_chart(
                self.canvas_loss, _MONTHLY_LOSSES,
                bar_color="#5A7ABF", bg=BG_CARD, unit="%",
            ),
        )

        # ── Barre de boutons ──────────────────────────────────────────────
        tk.Frame(main, bg=BORDER, height=1).grid(
            row=6, column=0, sticky="ew", padx=12, pady=(4, 0)
        )

        btn_bar = tk.Frame(main, bg=BG_PANEL)
        btn_bar.grid(row=6, column=0, sticky="ew", padx=12, pady=6)

        for label, cmd in [
            ("Rapport",    self._rapport),
            ("Tableaux",   self._tableaux),
            ("Évaluation", self._evaluation),
            ("Sauvegarder", lambda: self.controller.show_page("save_project")),
            ("Annuler",     lambda: self.controller.show_page("dashboard")),
        ]:
            is_orange = (label == "Sauvegarder")
            btn = tk.Button(
                btn_bar, text=label, font=F_BTN,
                bg=ORANGE if is_orange else BG_PANEL,
                fg=WHITE  if is_orange else NAVY,
                relief="solid", bd=1,
                padx=12, pady=5, cursor="hand2",
                command=cmd,
            )
            btn.pack(side="left", padx=4)
            if is_orange:
                btn.configure(relief="flat")
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=ORANGE_HVR))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=ORANGE))

        # Navigation bottom
        nav_bar = tk.Frame(main, bg=BG_PANEL)
        nav_bar.grid(row=7, column=0, sticky="ew", pady=6, padx=12)

        if "recap":
            self._outline_btn(
                nav_bar, "◀  Précédent", width=14,
                command=lambda: self.controller.show_page("recap"),
            ).pack(side="left", padx=4)

    # ── Helpers UI ───────────────────────────────────────────────────────

    def _info_row(self, parent, label: str, default_value: str) -> tk.Label:
        """Crée une ligne label / valeur dans un LabelFrame. Retourne le Label valeur."""
        row = tk.Frame(parent, bg=BG_PANEL)
        row.pack(fill="x", padx=8, pady=2)
        tk.Label(
            row, text=label + " :",
            font=("Arial", 9, "bold"),
            bg=BG_PANEL, fg=NAVY,
            width=18, anchor="w",
        ).pack(side="left")
        val_lbl = tk.Label(
            row, text=default_value,
            font=F_SMALL, bg=BG_PANEL, fg=TEXT_MED, anchor="w",
        )
        val_lbl.pack(side="left", fill="x", expand=True)
        return val_lbl

    # ── Dessin de graphiques ──────────────────────────────────────────────

    def _draw_bar_chart(
        self,
        canvas: tk.Canvas,
        data: list,
        bar_color: str,
        bg: str,
        unit: str = "",
    ):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 10 or h < 10:
            return

        pad_left   = 36
        pad_right  = 10
        pad_top    = 10
        pad_bottom = 28

        chart_w = w - pad_left - pad_right
        chart_h = h - pad_top  - pad_bottom

        max_val = max(v for _, v in data) or 1
        n       = len(data)
        bar_gap = chart_w / n
        bar_w   = bar_gap * 0.55

        # Axes
        canvas.create_line(
            pad_left, pad_top,
            pad_left, pad_top + chart_h,
            fill=GRAY, width=1,
        )
        canvas.create_line(
            pad_left, pad_top + chart_h,
            w - pad_right, pad_top + chart_h,
            fill=GRAY, width=1,
        )

        # Graduations Y (4 niveaux)
        for level in range(1, 5):
            y = pad_top + chart_h - (chart_h * level / 4)
            val = int(max_val * level / 4)
            canvas.create_line(
                pad_left - 3, y, pad_left, y,
                fill=GRAY, width=1,
            )
            canvas.create_text(
                pad_left - 5, y,
                text=str(val), font=("Arial", 7),
                fill=GRAY, anchor="e",
            )
            canvas.create_line(
                pad_left, y, w - pad_right, y,
                fill=GRAY_LT, width=1, dash=(4, 4),
            )

        # Barres
        for i, (label, val) in enumerate(data):
            x_center = pad_left + bar_gap * (i + 0.5)
            bar_h    = (val / max_val) * chart_h
            x0 = x_center - bar_w / 2
            x1 = x_center + bar_w / 2
            y0 = pad_top + chart_h - bar_h
            y1 = pad_top + chart_h

            canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=bar_color, outline="",
            )
            # Valeur au-dessus
            canvas.create_text(
                x_center, y0 - 3,
                text=str(val),
                font=("Arial", 6), fill=TEXT_MED, anchor="s",
            )
            # Étiquette mois
            canvas.create_text(
                x_center, pad_top + chart_h + 10,
                text=label,
                font=("Arial", 7), fill=TEXT_MED, anchor="n",
            )

        # Unité
        canvas.create_text(
            pad_left + 4, pad_top,
            text=unit, font=("Arial", 7), fill=GRAY, anchor="sw",
        )

    # ── Cycle de vie ─────────────────────────────────────────────────────

    def on_show(self, **kwargs):
        """Met à jour les champs avec les données du projet courant."""
        proj = self.controller.current_project
        name = proj.get("name", "—")
        site = proj.get("meteo_file", "—")
        if hasattr(self, "_lbl_project_name"):
            self._lbl_project_name.configure(text=name)
        if hasattr(self, "_lbl_site"):
            self._lbl_site.configure(text=site)

        # Forcer le redessin des graphiques après affichage
        self.after(80, lambda: self._draw_bar_chart(
            self.canvas_prod, _MONTHLY_PRODUCTION,
            bar_color=ORANGE, bg=BG_CARD, unit="kWh",
        ))
        self.after(80, lambda: self._draw_bar_chart(
            self.canvas_loss, _MONTHLY_LOSSES,
            bar_color="#5A7ABF", bg=BG_CARD, unit="%",
        ))

    # ── Actions backend ───────────────────────────────────────────────────

    def _rapport(self):
        self.controller.backend.generate_report("rapport", "")

    def _tableaux(self):
        self.controller.backend.generate_report("tableaux", "")

    def _evaluation(self):
        self.controller.backend.generate_report("evaluation", "")