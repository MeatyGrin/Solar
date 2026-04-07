"""
plan_3d.py
==========
Page de pose des panneaux solaires sur le toit.
Intègre le backend ModeleToitL + OptimiseurPanneaux + GestionnaireTemplates.

Disposition :
  ┌─────────────────────────────────┬───────────────────────────┐
  │  Onglets : Toit | Panneaux | Angles              [nav]      │
  ├──────────────────────┬──────────┴─────────────┬─────────────┤
  │  Contrôles gauche    │   Aperçu 2D Canvas      │  Stats      │
  │  (dims / panneaux /  │   (plan de toit +        │  + actions  │
  │   angles)            │    panneaux en vue de    │  rapides    │
  │                      │    dessus)               │             │
  └──────────────────────┴──────────────────────────┴─────────────┘

Navigation : Nouveau Projet → Plan3D → Recap
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import sys
import os

from pages.base_page import BasePage
from styles import *

# ── Import backend ────────────────────────────────────────────────────────────
# solar_roof_designer.py (original avec ModeleToitL/Panneau/DimensionsToit)
# doit être dans backend/
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_BACKEND = os.path.join(_ROOT, "backend")
for p in (_BACKEND, _ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.solar_roof_designer import ModeleToitL, DimensionsToit, Panneau
from backend.advanced_features   import OptimiseurPanneaux, GestionnaireTemplates, ExporteurRapport


# ── Constantes dessin 2D ──────────────────────────────────────────────────────
CANVAS_BG      = "#DDE8FF"
TOIT_FILL      = "#E8DDB5"
TOIT_OUTLINE   = "#A09060"
MUR_FILL       = "#D5C8A0"
PANNEAU_FILL   = "#2A4A8A"
PANNEAU_BORDER = "#5A7ABF"
PANNEAU_SEL    = "#FF6B35"    # couleur sélection


class Plan3DPage(BasePage):
    """
    Page principale de pose et configuration des panneaux solaires.
    Remplace orientation.py dans le flow : absorbe dimensions, pose et angles.
    """

    NAV_ITEMS = [
        {"text": "Accueil",      "page": "dashboard"},
        {"text": "Nouveau Proj", "checkbox": True, "checked": True,
         "page": "nouveau_projet"},
        {"text": "Enregistrer",  "page": "save_project"},
    ]

    # ── Init ─────────────────────────────────────────────────────────────────

    def build_ui(self):
        # Modèle backend
        self.modele      = ModeleToitL(DimensionsToit())
        self.optimiseur  = OptimiseurPanneaux(self.modele)
        self.templates   = GestionnaireTemplates.get_templates()

        # État interne
        self._scale      = 18.0    # px / mètre pour le canvas 2D
        self._pan_x      = 20.0    # décalage X canvas
        self._pan_y      = 20.0    # décalage Y canvas
        self._selected   = None    # index panneau sélectionné
        self._drag_start = None

        # Variables Tkinter (orientation)
        self.v_azimuth   = tk.DoubleVar(value=180.0)
        self.v_tilt      = tk.DoubleVar(value=30.0)
        self.v_anneau    = tk.DoubleVar(value=0.0)

        # Layout racine
        self.columnconfigure(0, weight=0)   # contrôles gauche
        self.columnconfigure(1, weight=1)   # canvas centre
        self.columnconfigure(2, weight=0)   # stats droite
        self.rowconfigure(1, weight=1)

        # ── Barre d'onglets ──────────────────────────────────────────────
        tab_bar = tk.Frame(self, bg=BG_PANEL)
        tab_bar.grid(row=0, column=0, columnspan=3, sticky="ew",
                     padx=12, pady=(10, 0))

        self._tab_btns   = {}
        self._tab_panels = {}
        for label, key in [("Toit", "toit"), ("Panneaux", "panneaux"),
                            ("Angles", "angles")]:
            btn = tk.Button(
                tab_bar, text=label, font=F_NAV,
                bg=BG_CARD, fg=NAVY,
                relief="flat", padx=18, pady=6, cursor="hand2",
                command=lambda k=key: self._switch_tab(k),
            )
            btn.pack(side="left", padx=2)
            self._tab_btns[key] = btn

        tk.Frame(tab_bar, bg=BORDER, height=1).pack(
            side="bottom", fill="x")

        # ── Panneau gauche (contrôles) ───────────────────────────────────
        self._ctrl_frame = tk.Frame(self, bg=BG_PANEL, width=230,
                                     bd=1, relief="solid")
        self._ctrl_frame.grid(row=1, column=0, sticky="nsew",
                               padx=(12, 4), pady=(4, 0))
        self._ctrl_frame.pack_propagate(False)

        self._build_tab_toit()
        self._build_tab_panneaux()
        self._build_tab_angles()
        self._switch_tab("toit")

        # ── Canvas aperçu 2D (centre) ────────────────────────────────────
        canvas_wrap = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        canvas_wrap.grid(row=1, column=1, sticky="nsew",
                          padx=4, pady=(4, 0))
        canvas_wrap.rowconfigure(0, weight=1)
        canvas_wrap.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_wrap, bg=CANVAS_BG,
                                 highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Légende
        legend = tk.Frame(canvas_wrap, bg=BG_PANEL)
        legend.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        for color, label in [(TOIT_FILL, "Toit"), (PANNEAU_FILL, "Panneau"),
                              (PANNEAU_SEL, "Sélectionné")]:
            tk.Frame(legend, bg=color, width=14, height=14,
                      relief="solid", bd=1).pack(side="left", padx=(6, 2))
            tk.Label(legend, text=label, font=F_SMALL,
                      bg=BG_PANEL, fg=TEXT_MED).pack(side="left", padx=(0, 8))

        tk.Label(legend, text="Molette : zoom  •  Clic droit : déplacer vue",
                  font=("Arial", 8), bg=BG_PANEL, fg=GRAY).pack(side="right")

        # Bindings canvas
        self.canvas.bind("<Configure>",     lambda e: self._redraw_canvas())
        self.canvas.bind("<ButtonPress-1>", self._on_canvas_click)
        self.canvas.bind("<ButtonPress-3>", self._on_pan_start)
        self.canvas.bind("<B3-Motion>",     self._on_pan_move)
        self.canvas.bind("<MouseWheel>",    self._on_zoom)
        self.canvas.bind("<Button-4>",      self._on_zoom)   # Linux
        self.canvas.bind("<Button-5>",      self._on_zoom)   # Linux

        # ── Panneau droite (stats + actions) ────────────────────────────
        right = tk.Frame(self, bg=BG_PANEL, width=200,
                          bd=1, relief="solid")
        right.grid(row=1, column=2, sticky="nsew",
                    padx=(4, 12), pady=(4, 0))
        right.pack_propagate(False)

        tk.Label(right, text="Statistiques", font=F_SUB,
                  bg=BG_PANEL, fg=NAVY, pady=8).pack(anchor="w", padx=10)
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=8)

        self._stats_labels = {}
        for key, label in [
            ("aire_toit",       "Surface toit"),
            ("aire_panneaux",   "Surface panneaux"),
            ("taux_couverture", "Taux couverture"),
            ("nb_panneaux",     "Nb panneaux"),
            ("puissance_kw",    "Puissance (kWc)"),
            ("production_kwh",  "Production (kWh/an)"),
            ("economies",       "Économies (€/an)"),
        ]:
            row = tk.Frame(right, bg=BG_PANEL)
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=label + " :", font=("Arial", 8, "bold"),
                      bg=BG_PANEL, fg=NAVY, anchor="w").pack(fill="x")
            lbl = tk.Label(row, text="—", font=F_SMALL,
                            bg=BG_CARD, fg=TEXT_MED,
                            anchor="w", padx=6, pady=2, relief="solid", bd=1)
            lbl.pack(fill="x")
            self._stats_labels[key] = lbl

        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=8, pady=8)

        # Boutons actions rapides
        for label, cmd in [
            ("📊  Visualiser 3D",  self._open_pyvista),
            ("📄  Rapport texte",  self._export_rapport),
            ("📋  Exporter CSV",   self._export_csv),
            ("💾  Sauvegarder",    self._save_config),
            ("📂  Charger",        self._load_config),
        ]:
            tk.Button(
                right, text=label, font=F_SMALL,
                bg=BG_PANEL, fg=NAVY, relief="solid", bd=1,
                padx=8, pady=5, cursor="hand2", anchor="w",
                command=cmd,
            ).pack(fill="x", padx=10, pady=2)

        # ── Navigation bas ───────────────────────────────────────────────
        nav_bar = tk.Frame(self, bg=BG_PANEL)
        nav_bar.grid(row=2, column=0, columnspan=3,
                      sticky="ew", padx=12, pady=8)
        self._outline_btn(
            nav_bar, "◀  Précédent", width=14,
            command=lambda: self.controller.show_page("nouveau_projet"),
        ).pack(side="left", padx=4)
        self._orange_btn(
            nav_bar, "Suivant  ▶", width=14,
            command=lambda: self.controller.show_page("recap"),
        ).pack(side="right", padx=4)

    # ═══════════════════════════════════════════════════════════════════════
    # ONGLETS CONTRÔLES
    # ═══════════════════════════════════════════════════════════════════════

    def _build_tab_toit(self):
        """Onglet dimensions du toit + templates."""
        frame = tk.Frame(self._ctrl_frame, bg=BG_PANEL)
        self._tab_panels["toit"] = frame

        # Templates
        tk.Label(frame, text="Template", font=("Arial", 9, "bold"),
                  bg=BG_PANEL, fg=NAVY).pack(anchor="w", padx=8, pady=(10, 2))
        self.v_template = tk.StringVar(value=list(self.templates.keys())[1])
        tmpl_combo = ttk.Combobox(frame, textvariable=self.v_template,
                                   values=list(self.templates.keys()),
                                   state="readonly", width=22)
        tmpl_combo.pack(padx=8, pady=(0, 4))
        self._outline_btn(frame, "Appliquer template", width=22,
                           command=self._apply_template).pack(padx=8, pady=(0, 8))

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=4)

        # Dimensions manuelles
        tk.Label(frame, text="Dimensions (m)", font=("Arial", 9, "bold"),
                  bg=BG_PANEL, fg=NAVY).pack(anchor="w", padx=8, pady=(6, 2))

        dim_grid = tk.Frame(frame, bg=BG_PANEL)
        dim_grid.pack(fill="x", padx=8)
        dim_grid.columnconfigure(1, weight=1)

        self._dim_vars = {}
        dim_fields = [
            ("longueur_bras_x", "Long. bras X"),
            ("largeur_bras_x",  "Larg. bras X"),
            ("longueur_bras_y", "Long. bras Y"),
            ("largeur_bras_y",  "Larg. bras Y"),
            ("hauteur_mur",     "Haut. murs"),
            ("hauteur_toit",    "Haut. toit"),
            ("retrait_faitage", "Retrait faîtage"),
        ]
        for row, (attr, label) in enumerate(dim_fields):
            tk.Label(dim_grid, text=label + " :", font=F_SMALL,
                      bg=BG_PANEL, fg=TEXT_DARK, anchor="w").grid(
                row=row, column=0, sticky="w", pady=2)
            var = tk.DoubleVar(value=getattr(self.modele.dim, attr))
            self._dim_vars[attr] = var
            tk.Entry(dim_grid, textvariable=var, font=F_SMALL,
                      bg=WHITE, relief="solid", bd=1, width=7).grid(
                row=row, column=1, sticky="e", pady=2, padx=(4, 0))

        self._orange_btn(frame, "Appliquer dimensions", width=22,
                          command=self._apply_dimensions).pack(padx=8, pady=10)

    def _build_tab_panneaux(self):
        """Onglet ajout manuel + placement automatique."""
        frame = tk.Frame(self._ctrl_frame, bg=BG_PANEL)
        self._tab_panels["panneaux"] = frame

        # ── Placement auto ───────────────────────────────────────────────
        tk.Label(frame, text="Placement automatique", font=("Arial", 9, "bold"),
                  bg=BG_PANEL, fg=NAVY).pack(anchor="w", padx=8, pady=(10, 2))

        auto_grid = tk.Frame(frame, bg=BG_PANEL)
        auto_grid.pack(fill="x", padx=8)
        auto_grid.columnconfigure(1, weight=1)

        tk.Label(auto_grid, text="Zone :", font=F_SMALL,
                  bg=BG_PANEL, fg=TEXT_DARK).grid(
            row=0, column=0, sticky="w", pady=2)
        self.v_zone = tk.StringVar(value="sud")
        ttk.Combobox(auto_grid, textvariable=self.v_zone,
                      values=["sud", "noue_est", "noue_nord", "ouest", "toutes"],
                      state="readonly", width=10).grid(
            row=0, column=1, sticky="e", pady=2)

        tk.Label(auto_grid, text="Orientation :", font=F_SMALL,
                  bg=BG_PANEL, fg=TEXT_DARK).grid(
            row=1, column=0, sticky="w", pady=2)
        self.v_orient = tk.StringVar(value="paysage")
        ttk.Combobox(auto_grid, textvariable=self.v_orient,
                      values=["paysage", "portrait"],
                      state="readonly", width=10).grid(
            row=1, column=1, sticky="e", pady=2)

        tk.Label(auto_grid, text="Espacement (m) :", font=F_SMALL,
                  bg=BG_PANEL, fg=TEXT_DARK).grid(
            row=2, column=0, sticky="w", pady=2)
        self.v_espacement = tk.DoubleVar(value=0.1)
        tk.Entry(auto_grid, textvariable=self.v_espacement, font=F_SMALL,
                  bg=WHITE, relief="solid", bd=1, width=7).grid(
            row=2, column=1, sticky="e", pady=2)

        self._orange_btn(frame, "▶  Placer automatiquement", width=22,
                          command=self._auto_place).pack(padx=8, pady=(6, 2))
        self._outline_btn(frame, "Tout effacer", width=22,
                           command=self._clear_all).pack(padx=8, pady=(2, 8))

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=4)

        # ── Ajout manuel ─────────────────────────────────────────────────
        tk.Label(frame, text="Ajout manuel", font=("Arial", 9, "bold"),
                  bg=BG_PANEL, fg=NAVY).pack(anchor="w", padx=8, pady=(6, 2))

        man_grid = tk.Frame(frame, bg=BG_PANEL)
        man_grid.pack(fill="x", padx=8)
        man_grid.columnconfigure(1, weight=1)

        self.v_px    = tk.DoubleVar(value=4.5)
        self.v_py    = tk.DoubleVar(value=0.5)
        self.v_pw    = tk.DoubleVar(value=1.65)
        self.v_ph    = tk.DoubleVar(value=1.0)
        self.v_pzone = tk.StringVar(value="sud")

        for row, (label, var, vals) in enumerate([
            ("Pos X (m)",  self.v_px,    None),
            ("Pos Y (m)",  self.v_py,    None),
            ("Largeur",    self.v_pw,    None),
            ("Hauteur",    self.v_ph,    None),
        ]):
            tk.Label(man_grid, text=label + " :", font=F_SMALL,
                      bg=BG_PANEL, fg=TEXT_DARK).grid(
                row=row, column=0, sticky="w", pady=2)
            tk.Entry(man_grid, textvariable=var, font=F_SMALL,
                      bg=WHITE, relief="solid", bd=1, width=7).grid(
                row=row, column=1, sticky="e", pady=2)

        tk.Label(man_grid, text="Zone :", font=F_SMALL,
                  bg=BG_PANEL, fg=TEXT_DARK).grid(
            row=4, column=0, sticky="w", pady=2)
        ttk.Combobox(man_grid, textvariable=self.v_pzone,
                      values=["sud", "noue_est", "noue_nord", "ouest"],
                      state="readonly", width=10).grid(
            row=4, column=1, sticky="e", pady=2)

        self._orange_btn(frame, "➕  Ajouter panneau", width=22,
                          command=self._add_panel_manual).pack(padx=8, pady=(8, 2))
        self._outline_btn(frame, "🗑  Supprimer sélectionné", width=22,
                           command=self._delete_selected).pack(padx=8, pady=2)

        # Liste des panneaux
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=(8, 4))
        tk.Label(frame, text="Panneaux posés", font=("Arial", 9, "bold"),
                  bg=BG_PANEL, fg=NAVY).pack(anchor="w", padx=8)

        list_wrap = tk.Frame(frame, bg=BG_PANEL)
        list_wrap.pack(fill="both", expand=True, padx=8, pady=4)
        sb = ttk.Scrollbar(list_wrap)
        sb.pack(side="right", fill="y")
        self._listbox = tk.Listbox(list_wrap, font=("Arial", 8),
                                    yscrollcommand=sb.set,
                                    bg=WHITE, selectbackground=ORANGE_LT,
                                    selectforeground=NAVY, height=6,
                                    relief="solid", bd=1)
        self._listbox.pack(fill="both", expand=True)
        sb.config(command=self._listbox.yview)
        self._listbox.bind("<<ListboxSelect>>", self._on_list_select)

    def _build_tab_angles(self):
        """Onglet orientation : azimut, tilt, rotation (ex-page orientation)."""
        frame = tk.Frame(self._ctrl_frame, bg=BG_PANEL)
        self._tab_panels["angles"] = frame

        tk.Label(frame, text="Orientation des panneaux",
                  font=("Arial", 9, "bold"), bg=BG_PANEL, fg=NAVY).pack(
            anchor="w", padx=8, pady=(10, 6))
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=(0, 8))

        ctrl_grid = tk.Frame(frame, bg=BG_PANEL)
        ctrl_grid.pack(fill="x", padx=8)
        ctrl_grid.columnconfigure(1, weight=1)

        for row, (label, var, from_, to) in enumerate([
            ("Azimut (°)",          self.v_azimuth, 0,    360),
            ("Inclinaison (°)",     self.v_tilt,    0,    90),
            ("Rotation anneau (°)", self.v_anneau, -180,  180),
        ]):
            tk.Label(ctrl_grid, text=label, font=F_SMALL,
                      bg=BG_PANEL, fg=TEXT_DARK).grid(
                row=row*2, column=0, columnspan=2, sticky="w", pady=(8, 0))
            scale_row = tk.Frame(ctrl_grid, bg=BG_PANEL)
            scale_row.grid(row=row*2+1, column=0, columnspan=2, sticky="ew")
            tk.Scale(scale_row, variable=var, from_=from_, to=to,
                      orient="horizontal", bg=BG_PANEL, fg=NAVY,
                      troughcolor=ORANGE_LT, activebackground=ORANGE,
                      sliderrelief="flat", highlightthickness=0,
                      showvalue=False,
                      command=lambda v: self._update_angle_diagram()).pack(
                side="left", fill="x", expand=True)
            tk.Label(scale_row, textvariable=var, font=F_SMALL,
                      bg=BG_PANEL, fg=NAVY, width=5).pack(side="left")

        # Schéma angulaire intégré
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=(12, 6))
        tk.Label(frame, text="Schéma Tilt / Azimut", font=("Arial", 8, "bold"),
                  bg=BG_PANEL, fg=NAVY).pack(anchor="w", padx=8)

        self._angle_canvas = tk.Canvas(frame, width=200, height=110,
                                        bg=BG_THUMB, highlightthickness=1,
                                        highlightbackground=BORDER)
        self._angle_canvas.pack(padx=8, pady=6)
        self._update_angle_diagram()

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=(4, 8))

        self._orange_btn(frame, "Calculer orientation", width=22,
                          command=self._calculate_orientation).pack(padx=8, pady=4)
        self._outline_btn(frame, "Optimiser auto", width=22,
                           command=self._optimize_orientation).pack(padx=8, pady=2)

    # ═══════════════════════════════════════════════════════════════════════
    # ONGLET SWITCH
    # ═══════════════════════════════════════════════════════════════════════

    def _switch_tab(self, key: str):
        for k, panel in self._tab_panels.items():
            panel.pack_forget()
        self._tab_panels[key].pack(fill="both", expand=True)
        for k, btn in self._tab_btns.items():
            btn.configure(bg=ORANGE if k == key else BG_CARD,
                           fg=WHITE  if k == key else NAVY)

    # ═══════════════════════════════════════════════════════════════════════
    # DESSIN CANVAS 2D (vue de dessus)
    # ═══════════════════════════════════════════════════════════════════════

    def _redraw_canvas(self):
        self.canvas.delete("all")
        self._draw_toit()
        self._draw_panneaux()
        self._draw_zones_labels()

    def _w2c(self, x: float, y: float):
        """Monde → Canvas (vue de dessus, Y inversé)."""
        return (self._pan_x + x * self._scale,
                self._pan_y + y * self._scale)

    def _draw_toit(self):
        """Dessine le toit en L en vue de dessus."""
        d = self.modele.dim
        # Forme en L : union de deux rectangles
        pts_L = [
            (0,                  0),
            (d.longueur_bras_x,  0),
            (d.longueur_bras_x,  d.largeur_bras_x),
            (d.largeur_bras_y,   d.largeur_bras_x),
            (d.largeur_bras_y,   d.longueur_bras_y),
            (0,                  d.longueur_bras_y),
        ]
        flat = []
        for wx, wy in pts_L:
            cx, cy = self._w2c(wx, wy)
            flat += [cx, cy]

        self.canvas.create_polygon(flat, fill=TOIT_FILL,
                                    outline=TOIT_OUTLINE, width=2)

        # Lignes faîtage (retrait)
        r = self.modele.dim.retrait_faitage
        faitage_pts = [
            (r, r),
            (d.longueur_bras_x - r, r),
        ]
        for i in range(len(faitage_pts) - 1):
            x0, y0 = self._w2c(*faitage_pts[i])
            x1, y1 = self._w2c(*faitage_pts[i+1])
            self.canvas.create_line(x0, y0, x1, y1,
                                     fill=TOIT_OUTLINE, width=1,
                                     dash=(6, 4))

        # Axe Nord indicateur
        ax, ay = self._w2c(d.longueur_bras_x + 0.5, 0.5)
        self.canvas.create_text(ax, ay, text="N↑", font=F_SMALL,
                                 fill=NAVY, anchor="w")

    def _draw_panneaux(self):
        """Dessine les panneaux en vue de dessus."""
        for i, p in enumerate(self.modele.panneaux):
            x0, y0 = self._w2c(p.x, p.y)
            x1, y1 = self._w2c(p.x + p.width, p.y + p.height)
            fill    = PANNEAU_SEL if i == self._selected else PANNEAU_FILL
            outline = PANNEAU_SEL if i == self._selected else PANNEAU_BORDER

            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=fill, outline=outline, width=2,
                tags=f"panneau_{i}",
            )
            # Numéro
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            if abs(x1 - x0) > 14:
                self.canvas.create_text(mx, my, text=str(i + 1),
                                         font=("Arial", 7, "bold"),
                                         fill=WHITE)

    def _draw_zones_labels(self):
        """Étiquettes de zones sur le canvas."""
        d = self.modele.dim
        zones = {
            "SUD":      (d.longueur_bras_x / 2,        d.largeur_bras_x / 2),
            "OUEST":    (d.largeur_bras_y / 2,          (d.largeur_bras_x + d.longueur_bras_y) / 2),
            "NOUE EST": ((d.largeur_bras_y + d.longueur_bras_x) / 2,
                          (d.largeur_bras_x + d.largeur_bras_x) / 2),
        }
        for label, (wx, wy) in zones.items():
            cx, cy = self._w2c(wx, wy)
            self.canvas.create_text(cx, cy, text=label,
                                     font=("Arial", 8, "italic"),
                                     fill=TOIT_OUTLINE, anchor="center")

    # ═══════════════════════════════════════════════════════════════════════
    # INTERACTIONS CANVAS
    # ═══════════════════════════════════════════════════════════════════════

    def _on_canvas_click(self, event):
        """Sélectionne un panneau au clic, ou désélectionne."""
        # Coordonnées monde
        wx = (event.x - self._pan_x) / self._scale
        wy = (event.y - self._pan_y) / self._scale

        hit = None
        for i, p in enumerate(self.modele.panneaux):
            if p.x <= wx <= p.x + p.width and p.y <= wy <= p.y + p.height:
                hit = i
                break

        self._selected = hit
        self._listbox.selection_clear(0, "end")
        if hit is not None:
            self._listbox.selection_set(hit)
            self._listbox.see(hit)
        self._redraw_canvas()

    def _on_list_select(self, event):
        sel = self._listbox.curselection()
        if sel:
            self._selected = sel[0]
            self._redraw_canvas()

    def _on_pan_start(self, event):
        self._drag_start = (event.x, event.y)

    def _on_pan_move(self, event):
        if self._drag_start:
            dx = event.x - self._drag_start[0]
            dy = event.y - self._drag_start[1]
            self._pan_x += dx
            self._pan_y += dy
            self._drag_start = (event.x, event.y)
            self._redraw_canvas()

    def _on_zoom(self, event):
        factor = 1.1
        if hasattr(event, "delta"):
            if event.delta < 0:
                factor = 1 / factor
        elif event.num == 5:
            factor = 1 / factor

        # Zoom centré sur la souris
        cx = (event.x - self._pan_x) / self._scale
        cy = (event.y - self._pan_y) / self._scale
        self._scale *= factor
        self._pan_x  = event.x - cx * self._scale
        self._pan_y  = event.y - cy * self._scale
        self._redraw_canvas()

    # ═══════════════════════════════════════════════════════════════════════
    # SCHÉMA ANGLE (onglet Angles)
    # ═══════════════════════════════════════════════════════════════════════

    def _update_angle_diagram(self):
        c = self._angle_canvas
        c.delete("all")
        w, h = 200, 110
        cx, cy = 100, 85

        # Sol
        c.create_line(10, cy, 190, cy, fill=GRAY, width=2)
        # Verticale
        c.create_line(cx, cy, cx, 10, fill=GRAY_LT, width=1, dash=(4, 4))

        tilt = self.v_tilt.get()
        ang  = math.radians(90 - tilt)
        ex   = cx + 65 * math.cos(ang)
        ey   = cy - 65 * math.sin(ang)
        c.create_line(cx, cy, ex, ey, fill=ORANGE, width=3,
                       arrow="last", arrowshape=(9, 11, 4))

        # Arc tilt
        c.create_arc(cx-35, cy-35, cx+35, cy+35,
                      start=0, extent=90 - tilt,
                      style="arc", outline=NAVY, width=1)
        c.create_text(cx + 20, cy - 12,
                       text=f"{int(tilt)}°", font=("Arial", 8), fill=NAVY)

        # Azimut
        az = int(self.v_azimuth.get())
        c.create_text(100, 104,
                       text=f"Azimut : {az}°  •  Tilt : {int(tilt)}°",
                       font=("Arial", 7), fill=GRAY)

    # ═══════════════════════════════════════════════════════════════════════
    # ACTIONS – TOIT
    # ═══════════════════════════════════════════════════════════════════════

    def _apply_template(self):
        name = self.v_template.get()
        if name in self.templates:
            dims = self.templates[name]
            self.modele.update_dimensions(dims)
            # Sync variables UI
            for attr, var in self._dim_vars.items():
                var.set(getattr(dims, attr))
            self._after_model_update()

    def _apply_dimensions(self):
        try:
            dims = DimensionsToit(
                **{attr: var.get() for attr, var in self._dim_vars.items()}
            )
            self.modele.update_dimensions(dims)
            self._after_model_update()
        except Exception as exc:
            messagebox.showerror("Erreur dimensions", str(exc))

    # ═══════════════════════════════════════════════════════════════════════
    # ACTIONS – PANNEAUX
    # ═══════════════════════════════════════════════════════════════════════

    def _auto_place(self):
        zone     = self.v_zone.get()
        orient   = self.v_orient.get()
        espacem  = self.v_espacement.get()

        try:
            if zone == "toutes":
                panneaux = self.optimiseur.placement_automatique_complet(
                    orientation=orient)
            else:
                panneaux = self.optimiseur.placement_automatique_zone(
                    zone, orient, espacem)

            if not panneaux:
                messagebox.showwarning(
                    "Placement auto",
                    "Aucun panneau placé. Vérifiez les dimensions du toit.")
                return

            for p in panneaux:
                self.modele.ajouter_panneau(p)
            self._after_model_update()
        except Exception as exc:
            messagebox.showerror("Erreur placement", str(exc))

    def _add_panel_manual(self):
        try:
            p = Panneau(
                x=self.v_px.get(), y=self.v_py.get(),
                width=self.v_pw.get(), height=self.v_ph.get(),
                zone=self.v_pzone.get(),
            )
            self.modele.ajouter_panneau(p)
            self._after_model_update()
        except Exception as exc:
            messagebox.showerror("Erreur ajout", str(exc))

    def _delete_selected(self):
        if self._selected is not None:
            self.modele.supprimer_panneau(self._selected)
            self._selected = None
            self._after_model_update()

    def _clear_all(self):
        if messagebox.askyesno("Confirmation", "Supprimer tous les panneaux ?"):
            self.modele.clear_panneaux()
            self._selected = None
            self._after_model_update()

    # ═══════════════════════════════════════════════════════════════════════
    # ACTIONS – ANGLES
    # ═══════════════════════════════════════════════════════════════════════

    def _calculate_orientation(self):
        self.controller.backend.calculate_orientation(
            azimuth=self.v_azimuth.get(),
            tilt=self.v_tilt.get(),
            angle_extra=self.v_anneau.get(),
        )

    def _optimize_orientation(self):
        self.controller.backend.optimize_orientation()

    # ═══════════════════════════════════════════════════════════════════════
    # ACTIONS – EXPORT / VISUALISATION
    # ═══════════════════════════════════════════════════════════════════════

    def _open_pyvista(self):
        """Ouvre la fenêtre PyVista 3D (séparée, non-bloquante)."""
        try:
            import pyvista as pv

            plotter = pv.Plotter(title="Solar Roof – Vue 3D")

            mesh_murs = self.modele.get_mesh_murs()
            mesh_toit = self.modele.get_mesh_toit()
            plotter.add_mesh(mesh_murs, color="white",
                              show_edges=True, line_width=2)
            plotter.add_mesh(mesh_toit, color="#C2B280",
                              show_edges=True, line_width=1,
                              pbr=True, metallic=0.1, roughness=0.7)

            mesh_pan = self.modele.get_mesh_panneaux()
            if mesh_pan:
                plotter.add_mesh(mesh_pan, color="#2c3e50",
                                  show_edges=True,
                                  edge_color="red", line_width=2)

            stats = self.modele.calculer_statistiques()
            prod  = self.optimiseur.calculer_production_estimee()
            info  = (
                f"Surface toit : {stats['aire_toit']:.1f} m²\n"
                f"Panneaux : {stats['nb_panneaux']}  "
                f"({stats['taux_couverture']:.1f}%)\n"
                f"Puissance : {prod['puissance_kw']:.2f} kWc\n"
                f"Production : {prod['production_kwh_an']:.0f} kWh/an\n"
                f"Économies : {prod['economies_euros_an']:.0f} €/an"
            )
            plotter.add_text(info, position="upper_left",
                              color="black", font_size=11)
            plotter.camera_position = [(-15, -15, 12), (5, 5, 3), (0, 0, 1)]
            plotter.set_background("#FFFBE6")
            plotter.show()

        except ImportError:
            messagebox.showerror(
                "PyVista manquant",
                "Installez PyVista : pip install pyvista\n"
                "(et vtk si nécessaire)")
        except Exception as exc:
            messagebox.showerror("Erreur 3D", str(exc))

    def _export_rapport(self):
        path = filedialog.asksaveasfilename(
            title="Sauvegarder le rapport",
            defaultextension=".txt",
            filetypes=[("Texte", "*.txt"), ("Tous", "*.*")],
        )
        if path:
            try:
                exp = ExporteurRapport(self.modele)
                exp.generer_rapport_texte(path)
                messagebox.showinfo("Rapport", f"Rapport sauvegardé :\n{path}")
            except Exception as exc:
                messagebox.showerror("Erreur rapport", str(exc))

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Exporter CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Tous", "*.*")],
        )
        if path:
            try:
                exp = ExporteurRapport(self.modele)
                exp.generer_rapport_csv(path)
                messagebox.showinfo("Export CSV", f"CSV sauvegardé :\n{path}")
            except Exception as exc:
                messagebox.showerror("Erreur CSV", str(exc))

    def _save_config(self):
        path = filedialog.asksaveasfilename(
            title="Sauvegarder configuration",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Tous", "*.*")],
        )
        if path:
            try:
                self.modele.sauvegarder(path)
                messagebox.showinfo("Sauvegarde", f"Configuration sauvegardée :\n{path}")
            except Exception as exc:
                messagebox.showerror("Erreur sauvegarde", str(exc))

    def _load_config(self):
        path = filedialog.askopenfilename(
            title="Charger configuration",
            filetypes=[("JSON", "*.json"), ("Tous", "*.*")],
        )
        if path:
            try:
                self.modele.charger(path)
                # Sync variables UI → dimensions
                for attr, var in self._dim_vars.items():
                    var.set(getattr(self.modele.dim, attr))
                self._selected = None
                self._after_model_update()
                messagebox.showinfo("Chargement", "Configuration chargée !")
            except Exception as exc:
                messagebox.showerror("Erreur chargement", str(exc))

    # ═══════════════════════════════════════════════════════════════════════
    # MISE À JOUR GLOBALE
    # ═══════════════════════════════════════════════════════════════════════

    def _after_model_update(self):
        """Appelé après toute modification du modèle."""
        self._update_listbox()
        self._update_stats()
        self._redraw_canvas()
        self._sync_to_controller()

    def _update_listbox(self):
        self._listbox.delete(0, "end")
        for i, p in enumerate(self.modele.panneaux):
            self._listbox.insert(
                "end",
                f"#{i+1:02d}  {p.zone:10s}  ({p.x:.1f},{p.y:.1f})  "
                f"{p.width:.2f}×{p.height:.2f}m",
            )

    def _update_stats(self):
        stats = self.modele.calculer_statistiques()
        prod  = self.optimiseur.calculer_production_estimee()

        values = {
            "aire_toit":       f"{stats['aire_toit']:.2f} m²",
            "aire_panneaux":   f"{stats['aire_panneaux']:.2f} m²",
            "taux_couverture": f"{stats['taux_couverture']:.1f} %",
            "nb_panneaux":     str(stats["nb_panneaux"]),
            "puissance_kw":    f"{prod['puissance_kw']:.2f} kWc",
            "production_kwh":  f"{prod['production_kwh_an']:.0f} kWh",
            "economies":       f"{prod['economies_euros_an']:.0f} €",
        }
        for key, lbl in self._stats_labels.items():
            lbl.configure(text=values.get(key, "—"))

    def _sync_to_controller(self):
        """Synchronise les données du modèle vers le projet courant."""
        import dataclasses
        proj = self.controller.current_project
        proj["roof_dimensions"] = dataclasses.asdict(self.modele.dim)
        proj["panneaux"]        = [p.to_dict() for p in self.modele.panneaux]
        proj["orientation"]     = {
            "azimuth":     self.v_azimuth.get(),
            "tilt":        self.v_tilt.get(),
            "angle_extra": self.v_anneau.get(),
        }

    # ═══════════════════════════════════════════════════════════════════════
    # CYCLE DE VIE
    # ═══════════════════════════════════════════════════════════════════════

    def on_show(self, **kwargs):
        # Recalcul initial après affichage (le canvas a sa taille réelle)
        self.after(80, self._after_model_update)