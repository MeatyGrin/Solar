import tkinter as tk
from pages.base_page import BasePage
from styles import *


class PlanPage(BasePage):

    NAV_ITEMS = [
        {"text": "Accueil",    "page": "dashboard"},
        {"text": "Modules",    "checkbox": True, "checked": True},
        {"text": "Frames",     "checkbox": True, "checked": True},
        {"text": "Paramètres", "checkbox": True, "checked": True},
    ]

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # ── Panneau principal ────────────────────────────────────────────────
        main = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        main.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        # Barre d'onglets
        tab_bar = tk.Frame(main, bg=BG_PANEL)
        tab_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))

        self.tab_frames: dict = {}
        self.tab_btns: dict = {}
        tabs = [
            ("Modules",    "modules"),
            ("Frames",     "frames"),
            ("Paramètres", "params"),
        ]
        for label, key in tabs:
            btn = tk.Button(
                tab_bar, text=label, font=F_NAV,
                bg=ORANGE if key == "modules" else BG_CARD,
                fg=WHITE if key == "modules" else NAVY,
                relief="flat", padx=16, pady=6, cursor="hand2",
                command=lambda k=key: self._switch_tab(k),
            )
            btn.pack(side="left", padx=2)
            self.tab_btns[key] = btn

        tk.Frame(main, bg=BORDER, height=1).grid(
            row=0, column=0, sticky="ew", padx=10, pady=(42, 0))

        # Zone de contenu des onglets
        self.tab_area = tk.Frame(main, bg=BG_PANEL)
        self.tab_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=4)
        self.tab_area.columnconfigure(0, weight=1)
        self.tab_area.rowconfigure(0, weight=1)

        self._build_modules_tab()
        self._build_frames_tab()
        self._build_params_tab()
        self._switch_tab("modules")

        # Navigation bottom
        nav_bar = tk.Frame(main, bg=BG_PANEL)
        nav_bar.grid(row=2, column=0, sticky="ew", pady=6, padx=12)

        if "nouveau_projet":
            self._outline_btn(
                nav_bar, "◀  Précédent", width=14,
                command=lambda: self.controller.show_page("nouveau_projet"),
            ).pack(side="left", padx=4)

        if "orientation":
            self._orange_btn(
                nav_bar, "Suivant  ▶", width=14,
                command=lambda: self.controller.show_page("orientation"),
            ).pack(side="right", padx=4)

        # ── Panneau droit – miniatures ───────────────────────────────────────
        right = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", width=210)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        right.pack_propagate(False)

        for title in ("Projet Thomson", "Projet Lino Olivie"):
            tk.Label(right, text=title, font=("Arial", 9, "bold"),
                      bg=BG_PANEL, fg=NAVY, pady=6, padx=10, anchor="w").pack(fill="x")
            self._right_canvas(right)

    def _right_canvas(self, parent):
        c = tk.Canvas(parent, width=185, height=85, bg="#E8EEFF",
                       highlightthickness=1, highlightbackground=BORDER)
        c.pack(padx=10, pady=(0, 8))
        cx, cy, s = 92, 42, 0.44
        c.create_polygon(
            [cx-70*s, cy+18*s, cx+70*s, cy+18*s, cx+70*s, cy+55*s, cx-70*s, cy+55*s],
            fill="#D5C8A0", outline="#B0A070")
        c.create_polygon(
            [cx+70*s, cy+18*s, cx+100*s, cy+3*s, cx+100*s, cy+40*s, cx+70*s, cy+55*s],
            fill="#C0B085", outline="#B0A070")
        c.create_polygon(
            [cx-70*s, cy+18*s, cx+70*s, cy+18*s, cx+100*s, cy+3*s, cx-40*s, cy+3*s],
            fill="#E8DDB0", outline="#B0A070")
        for col in range(2):
            for row in range(2):
                px = cx + (-55 + col*50)*s
                py = cy + (14 - row*12)*s
                panel = [px, py, px+44*s, py, px+54*s, py-10*s, px+10*s, py-10*s]
                c.create_polygon(panel, fill=BLUE_PANEL, outline=BLUE_LT)

    # ── Onglets ──────────────────────────────────────────────────────────────

    def _switch_tab(self, key: str):
        for k, f in self.tab_frames.items():
            f.grid_remove()
        self.tab_frames[key].grid(row=0, column=0, sticky="nsew")
        for k, btn in self.tab_btns.items():
            btn.configure(bg=ORANGE if k == key else BG_CARD,
                           fg=WHITE  if k == key else NAVY)

    def _build_modules_tab(self):
        frame = tk.Frame(self.tab_area, bg=BG_PANEL)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self.tab_frames["modules"] = frame

        self.canvas_modules = tk.Canvas(
            frame, bg="#DDE8FF", bd=1, relief="solid", highlightthickness=0)
        self.canvas_modules.grid(row=0, column=0, sticky="nsew", pady=4)
        self.canvas_modules.bind(
            "<Configure>", lambda e: self._redraw(self.canvas_modules))

        info = tk.Frame(frame, bg=BG_PANEL)
        info.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        tk.Label(info, text="Cliquez sur le plan pour placer les modules solaires",
                  font=F_SMALL, bg=BG_PANEL, fg=TEXT_MED).pack(side="left", padx=4)
        self._orange_btn(
            info, "Configurer modules",
            command=self._configure_modules, width=18,
        ).pack(side="right", padx=4)

    def _build_frames_tab(self):
        frame = tk.Frame(self.tab_area, bg=BG_PANEL)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self.tab_frames["frames"] = frame

        self.canvas_frames = tk.Canvas(
            frame, bg="#DDE8FF", bd=1, relief="solid", highlightthickness=0)
        self.canvas_frames.grid(row=0, column=0, sticky="nsew", pady=4)
        self.canvas_frames.bind(
            "<Configure>", lambda e: self._redraw(self.canvas_frames))

        info = tk.Frame(frame, bg=BG_PANEL)
        info.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        tk.Label(info, text="Sélectionnez le type de structure (frame) pour les modules",
                  font=F_SMALL, bg=BG_PANEL, fg=TEXT_MED).pack(side="left", padx=4)
        self._orange_btn(
            info, "Configurer frames",
            command=self._configure_frames, width=18,
        ).pack(side="right", padx=4)

    def _build_params_tab(self):
        frame = tk.Frame(self.tab_area, bg=BG_PANEL)
        frame.columnconfigure(1, weight=1)
        self.tab_frames["params"] = frame

        tk.Label(frame, text="Paramètres du système",
                  font=F_SUB, bg=BG_PANEL, fg=NAVY, pady=6).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=4)

        self.v_piles = tk.StringVar(value="4")
        self.v_n_axe = tk.StringVar(value="2")
        self.v_t_axe = tk.StringVar(value="Horizontal")
        self.v_angle = tk.StringVar(value="30")

        self._field(frame, "Nombre de piles",     row=1, var=self.v_piles)
        self._field(frame, "Nombre d'axes",       row=2, var=self.v_n_axe)
        self._field(frame, "Type d'axe",          row=3, var=self.v_t_axe)
        self._field(frame, "Angle Extra Solaire", row=4, var=self.v_angle)

        preview = tk.Canvas(frame, width=160, height=120, bg="#E8EEFF",
                             highlightthickness=1, highlightbackground=BORDER)
        preview.grid(row=1, column=2, rowspan=4, padx=16, pady=4, sticky="ns")
        preview.create_text(80, 60, text="Aperçu\npanneau",
                             font=F_SMALL, fill=GRAY, justify="center")

        self._orange_btn(
            frame, "Appliquer",
            command=self._apply_params, width=14,
        ).grid(row=5, column=1, sticky="e", pady=12, padx=(0, 4))

    # ── Dessin 3D ────────────────────────────────────────────────────────────

    def _redraw(self, canvas: tk.Canvas):
        canvas.delete("all")
        w = canvas.winfo_width()  or 500
        h = canvas.winfo_height() or 300
        self._draw_building(canvas, w // 2 - 20, h // 2 + 30, min(w, h) / 370)

    def _draw_building(self, canvas: tk.Canvas, cx, cy, s=1.0):
        canvas.create_polygon(
            [cx-110*s, cy+22*s, cx+110*s, cy+22*s,
             cx+110*s, cy+100*s, cx-110*s, cy+100*s],
            fill="#D5C8A0", outline="#A09060", width=1)
        canvas.create_polygon(
            [cx+110*s, cy+22*s, cx+155*s, cy-6*s,
             cx+155*s, cy+72*s, cx+110*s, cy+100*s],
            fill="#BFB080", outline="#A09060", width=1)
        canvas.create_polygon(
            [cx-110*s, cy+22*s, cx+110*s, cy+22*s,
             cx+155*s, cy-6*s, cx-65*s, cy-6*s],
            fill="#E8DDB5", outline="#A09060", width=1)
        panel_cols = [(-95, -38), (-30, 27)]
        panel_rows = [22, 10, -2]
        for pc_x0, pc_x1 in panel_cols:
            for pr_y in panel_rows:
                pts = [
                    cx + pc_x0*s, cy + pr_y*s,
                    cx + pc_x1*s, cy + pr_y*s,
                    cx + (pc_x1+16)*s, cy + (pr_y-13)*s,
                    cx + (pc_x0+16)*s, cy + (pr_y-13)*s,
                ]
                canvas.create_polygon(pts, fill=BLUE_PANEL, outline=BLUE_LT, width=1)
                mx1 = (pts[0] + pts[2]) / 2
                my1 = (pts[1] + pts[3]) / 2
                mx2 = (pts[4] + pts[6]) / 2
                my2 = (pts[5] + pts[7]) / 2
                canvas.create_line(mx1, my1, mx2, my2, fill=BLUE_LT, width=1)

    # ── Actions ──────────────────────────────────────────────────────────────

    def _configure_modules(self):
        self.controller.backend.configure_modules("standard", 12, {})

    def _configure_frames(self):
        self.controller.backend.configure_frames("aluminium", {})

    def _apply_params(self):
        self.controller.backend.configure_parameters({
            "nombre_piles": self.v_piles.get(),
            "nombre_axe":   self.v_n_axe.get(),
            "type_axe":     self.v_t_axe.get(),
            "angle_extra":  self.v_angle.get(),
        })

    def on_show(self, **kwargs):
        self.after(60, lambda: self._redraw(self.canvas_modules))
        self.after(60, lambda: self._redraw(self.canvas_frames))