import tkinter as tk
import math
from pages.base_page import BasePage
from styles import *


class OrientationPage(BasePage):

    NAV_ITEMS = [
        {"text": "Accueil",      "page": "dashboard"},
        {"text": "Nouveau Proj", "checkbox": True, "checked": True,
         "page": "nouveau_projet"},
        {"text": "Enregistrer",  "page": "save_project"},
    ]

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        main = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        main.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        # En-tête + sous-onglets
        header = tk.Frame(main, bg=BG_PANEL)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        tk.Label(header, text="Orientation des panneaux",
                  font=F_TITLE, bg=BG_PANEL, fg=NAVY).pack(side="left", padx=4)
        for lbl in ["Angles", "Optimisations", "Anneau", "Tilt"]:
            tk.Label(header, text=lbl, font=F_NAV, bg=BG_PANEL, fg=NAVY,
                      padx=10, cursor="hand2").pack(side="left")

        tk.Frame(main, bg=BORDER, height=1).grid(
            row=1, column=0, sticky="ew", padx=10, pady=4)

        # Corps
        body = tk.Frame(main, bg=BG_PANEL)
        body.grid(row=2, column=0, sticky="nsew", padx=10, pady=4)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(body, bg="#DDE8FF", bd=1, relief="solid",
                                 highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", pady=4)
        self.canvas.bind("<Configure>", lambda e: self._redraw())

        # Contrôles
        ctrl = tk.Frame(body, bg=BG_PANEL, width=190)
        ctrl.grid(row=0, column=1, sticky="ns", padx=(12, 0), pady=4)
        ctrl.pack_propagate(False)

        tk.Label(ctrl, text="Paramètres d'orientation",
                  font=F_SUB, bg=BG_PANEL, fg=NAVY, pady=6).pack(anchor="w")
        tk.Frame(ctrl, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

        self.v_azimuth = tk.DoubleVar(value=180.0)
        self.v_tilt    = tk.DoubleVar(value=30.0)
        self.v_anneau  = tk.DoubleVar(value=0.0)

        self._angle_ctrl(ctrl, "Azimut (°)",          self.v_azimuth, 0,    360)
        self._angle_ctrl(ctrl, "Inclinaison (°)",     self.v_tilt,    0,    90)
        self._angle_ctrl(ctrl, "Rotation anneau (°)", self.v_anneau, -180,  180)

        self._orange_btn(ctrl, "Calculer",
                          command=self._calculate, width=18).pack(pady=10)
        self._outline_btn(ctrl, "Optimiser auto",
                           command=self._optimize, width=18).pack()

        # Navigation bottom
        nav_bar = tk.Frame(main, bg=BG_PANEL)
        nav_bar.grid(row=3, column=0, sticky="ew", pady=6, padx=12)

        if "plan":
            self._outline_btn(
                nav_bar, "◀  Précédent", width=14,
                command=lambda: self.controller.show_page("plan"),
            ).pack(side="left", padx=4)

        if "recap":
            self._orange_btn(
                nav_bar, "Suivant  ▶", width=14,
                command=lambda: self.controller.show_page("recap"),
            ).pack(side="right", padx=4)

        # Panneau droit – schéma
        right = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", width=210)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        right.pack_propagate(False)

        tk.Label(right, text="Schéma Tilt / Azimut",
                  font=F_SUB, bg=BG_PANEL, fg=NAVY, pady=8).pack()
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=10)
        self._build_angle_diagram(right)
        tk.Label(right, text="Toit plat", font=F_SMALL,
                  bg=BG_PANEL, fg=GRAY, pady=8).pack()

    def _angle_ctrl(self, parent, label, var, from_, to):
        tk.Label(parent, text=label, font=F_SMALL,
                  bg=BG_PANEL, fg=TEXT_DARK, anchor="w").pack(fill="x", pady=(10, 0))
        row = tk.Frame(parent, bg=BG_PANEL)
        row.pack(fill="x")
        tk.Scale(row, variable=var, from_=from_, to=to, orient="horizontal",
                  bg=BG_PANEL, fg=NAVY, troughcolor=ORANGE_LT,
                  activebackground=ORANGE, sliderrelief="flat",
                  highlightthickness=0, showvalue=False,
                  command=lambda v: self._redraw()).pack(side="left", fill="x", expand=True)
        tk.Label(row, textvariable=var, font=F_SMALL,
                  bg=BG_PANEL, fg=NAVY, width=5).pack(side="left")

    def _build_angle_diagram(self, parent):
        c = tk.Canvas(parent, width=185, height=130, bg=BG_THUMB,
                       highlightthickness=1, highlightbackground=BORDER)
        c.pack(padx=10, pady=8)
        cx, cy = 92, 95
        c.create_line(10, cy, 174, cy, fill=GRAY, width=2)
        c.create_line(cx, cy, cx, 15, fill=GRAY_LT, width=1, dash=(4, 4))
        ang = math.radians(50)
        ex = cx + 65 * math.cos(ang)
        ey = cy - 65 * math.sin(ang)
        c.create_line(cx, cy, ex, ey, fill=ORANGE, width=3,
                       arrow="last", arrowshape=(9, 11, 4))
        c.create_arc(cx-40, cy-40, cx+40, cy+40, start=0, extent=50,
                      style="arc", outline=NAVY, width=1)
        c.create_text(cx+28, cy-15, text="Tilt", font=F_SMALL, fill=NAVY)
        c.create_text(92, 115, text="← N  S →", font=F_SMALL, fill=GRAY)

    def _redraw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()  or 480
        h = self.canvas.winfo_height() or 260
        cx, cy = w // 2 - 20, h // 2 + 20
        s = min(w, h) / 380
        tilt     = self.v_tilt.get()
        compress = 1.0 - (tilt / 90.0) * 0.55
        # Bâtiment
        self.canvas.create_polygon(
            [cx-110*s, cy+22*s, cx+110*s, cy+22*s, cx+110*s, cy+95*s, cx-110*s, cy+95*s],
            fill="#D5C8A0", outline="#A09060")
        self.canvas.create_polygon(
            [cx+110*s, cy+22*s, cx+155*s, cy-6*s, cx+155*s, cy+67*s, cx+110*s, cy+95*s],
            fill="#BFB080", outline="#A09060")
        self.canvas.create_polygon(
            [cx-110*s, cy+22*s, cx+110*s, cy+22*s, cx+155*s, cy-6*s, cx-65*s, cy-6*s],
            fill="#E8DDB5", outline="#A09060")
        # Panneaux inclinés
        for x0, x1 in [(-95, -38), (-30, 27)]:
            for base_y in [22, 10, -2]:
                h_panel = 13 * compress
                pts = [cx+x0*s, cy+base_y*s, cx+x1*s, cy+base_y*s,
                        cx+(x1+16)*s, cy+(base_y-h_panel)*s,
                        cx+(x0+16)*s, cy+(base_y-h_panel)*s]
                self.canvas.create_polygon(pts, fill=BLUE_PANEL, outline=BLUE_LT)
                self.canvas.create_line(
                    (pts[0]+pts[2])/2, (pts[1]+pts[3])/2,
                    (pts[4]+pts[6])/2, (pts[5]+pts[7])/2,
                    fill=BLUE_LT, width=1)

    def _calculate(self):
        self.controller.backend.calculate_orientation(
            azimuth=self.v_azimuth.get(),
            tilt=self.v_tilt.get(),
            angle_extra=self.v_anneau.get(),
        )

    def _optimize(self):
        self.controller.backend.optimize_orientation()

    def on_show(self, **kwargs):
        self.after(60, self._redraw)