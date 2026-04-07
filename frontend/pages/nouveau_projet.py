import tkinter as tk
from tkinter import filedialog, messagebox
from pages.base_page import BasePage
from styles import *


class NouveauProjetPage(BasePage):

    NAV_ITEMS = [
        {"text": "Accueil",        "page": "dashboard"},
        {"text": "Nouveau Projet", "checkbox": True, "checked": True, "active": True},
    ]

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # ── Formulaire (gauche) ──────────────────────────────────────────────
        left = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        left.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)

        tk.Label(
            left, text="Nouveau Projet",
            font=F_TITLE, bg=BG_PANEL, fg=NAVY, pady=12,
        ).pack(anchor="w", padx=16)
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12, pady=(0, 10))

        form = tk.Frame(left, bg=BG_PANEL)
        form.pack(padx=20, pady=8, fill="x", anchor="n")
        form.columnconfigure(1, weight=1)

        self.v_name   = tk.StringVar()
        self.v_folder = tk.StringVar()
        self.v_meteo  = tk.StringVar()
        self.v_area   = tk.StringVar()
        self.v_loc    = tk.StringVar()

        self._field(form, "Nom du projet",     row=0, var=self.v_name)
        self._field(form, "Dossier associé",   row=1, var=self.v_folder)

        # Fichier météo avec bouton Parcourir
        tk.Label(form, text="Fichier météo", font=F_BODY,
                  bg=BG_PANEL, fg=TEXT_DARK, anchor="w").grid(
            row=2, column=0, sticky="w", pady=(6, 1), padx=(0, 8))

        meteo_row = tk.Frame(form, bg=BG_PANEL)
        meteo_row.grid(row=2, column=1, sticky="ew", pady=(6, 1))
        tk.Entry(meteo_row, textvariable=self.v_meteo, font=F_BODY,
                  bg=WHITE, relief="solid", bd=1, width=22).pack(side="left")
        tk.Button(
            meteo_row, text=" … ", font=F_BODY,
            bg=GRAY_LT, relief="solid", bd=1,
            cursor="hand2", command=self._browse_meteo,
        ).pack(side="left", padx=4)

        # Lien Site File
        lnk = tk.Label(
            form,
            text="📍  Choisir depuis la liste de sites météo",
            font=("Arial", 9, "underline"), bg=BG_PANEL, fg=ORANGE, cursor="hand2",
        )
        lnk.grid(row=3, column=1, sticky="w", pady=(2, 10))
        lnk.bind("<Button-1>", lambda e: self.controller.show_page("site_file"))

        self._field(form, "Toiture totale (m²)", row=4, var=self.v_area)
        self._field(form, "Localisation",         row=5, var=self.v_loc)

        # Boutons
        btn_frame = tk.Frame(left, bg=BG_PANEL)
        btn_frame.pack(padx=20, pady=16, anchor="w")

        self._orange_btn(
            btn_frame, "Créer le projet",
            command=self._create_project, width=18,
        ).pack(side="left", padx=(0, 10))

        self._outline_btn(
            btn_frame, "Annuler",
            command=lambda: self.controller.show_page("dashboard"), width=10,
        ).pack(side="left")

        self._nav_bottom(left, prev_page="dashboard", next_page="plan")

        # ── Miniatures droite ────────────────────────────────────────────────
        right = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", width=210)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        right.pack_propagate(False)

        for title in ("Projet Thomson", "Projet Lino Olivie"):
            tk.Label(
                right, text=title, font=("Arial", 9, "bold"),
                bg=BG_PANEL, fg=NAVY, pady=6, padx=10, anchor="w",
            ).pack(fill="x")
            thumb = tk.Canvas(right, width=185, height=80, bg="#E8EEFF",
                               highlightthickness=1, highlightbackground=BORDER)
            thumb.pack(padx=10, pady=(0, 8))
            self._draw_mini_thumb(thumb)

    def _draw_mini_thumb(self, canvas):
        cx, cy, s = 92, 40, 0.45
        canvas.create_polygon(
            [cx-70*s, cy+18*s, cx+70*s, cy+18*s, cx+70*s, cy+55*s, cx-70*s, cy+55*s],
            fill="#D5C8A0", outline="#B0A070")
        canvas.create_polygon(
            [cx+70*s, cy+18*s, cx+100*s, cy+3*s, cx+100*s, cy+40*s, cx+70*s, cy+55*s],
            fill="#C0B085", outline="#B0A070")
        canvas.create_polygon(
            [cx-70*s, cy+18*s, cx+70*s, cy+18*s, cx+100*s, cy+3*s, cx-40*s, cy+3*s],
            fill="#E8DDB0", outline="#B0A070")
        for col in range(2):
            for row in range(2):
                px = cx + (-55 + col*50)*s
                py = cy + (14 - row*12)*s
                panel = [px, py, px+44*s, py, px+54*s, py-10*s, px+10*s, py-10*s]
                canvas.create_polygon(panel, fill=BLUE_PANEL, outline=BLUE_LT)

    def _browse_meteo(self):
        path = filedialog.askopenfilename(
            title="Sélectionner un fichier météo",
            filetypes=[("EPW files", "*.epw"), ("All files", "*.*")],
        )
        if path:
            self.v_meteo.set(path)

    def _create_project(self):
        name = self.v_name.get().strip()
        if not name:
            messagebox.showwarning("Champ requis", "Veuillez saisir un nom de projet.")
            return
        project = self.controller.backend.create_new_project(
            name=name,
            associated_folder=self.v_folder.get().strip(),
            meteo_file=self.v_meteo.get().strip(),
        )
        self.controller.current_project.update(project)
        self.controller.show_page("plan")