import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from styles import *


class SiteFilePage(BasePage):

    NAV_ITEMS = [{"text": "Accueil", "page": "dashboard"}]

    def build_ui(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        main = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid")
        main.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        header = tk.Frame(main, bg=BG_PANEL)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))
        tk.Label(header, text="Sites météorologiques",
                  font=F_TITLE, bg=BG_PANEL, fg=NAVY).pack(side="left")
        tk.Label(header, text="Sélectionnez un site puis cliquez sur Ok",
                  font=F_SMALL, bg=BG_PANEL, fg=GRAY).pack(side="left", padx=14)

        tk.Frame(main, bg=BORDER, height=1).grid(
            row=1, column=0, sticky="ew", padx=12, pady=6)

        # Tableau
        table_frame = tk.Frame(main, bg=BG_PANEL)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=4)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        cols = ("filename", "city", "country", "source")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                  show="headings", selectmode="browse")
        for col, text, width in [
            ("filename", "Nom du fichier", 210),
            ("city",     "Ville",          130),
            ("country",  "Pays",           110),
            ("source",   "Source",         150),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=60)

        style = ttk.Style()
        style.configure("Site.Treeview", background=WHITE, fieldbackground=WHITE,
                          font=F_SMALL, rowheight=24)
        style.configure("Site.Treeview.Heading", font=("Arial", 9, "bold"),
                          background=BG_PANEL, foreground=NAVY)
        style.map("Site.Treeview",
                   background=[("selected", ORANGE_LT)],
                   foreground=[("selected", NAVY)])
        self.tree.configure(style="Site.Treeview")

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        # Barre outils
        toolbar = tk.Frame(main, bg=BG_PANEL)
        toolbar.grid(row=3, column=0, sticky="ew", padx=12, pady=8)

        for label, cmd in [
            ("Ajouter Site Terrain", self._add_site),
            ("Exporter",             self._export),
            ("Nouveau",              self._new_site),
            ("Supprimer",            self._delete_site),
        ]:
            tk.Button(toolbar, text=label, font=F_SMALL, bg=BG_PANEL, fg=NAVY,
                       relief="solid", bd=1, padx=8, pady=4, cursor="hand2",
                       command=cmd).pack(side="left", padx=3)

        close_lbl = tk.Label(toolbar, text="✕", font=("Arial", 12),
                               bg=BG_PANEL, fg=GRAY, cursor="hand2", padx=6)
        close_lbl.pack(side="right")
        close_lbl.bind("<Button-1>",
                        lambda e: self.controller.show_page("nouveau_projet"))

        self._orange_btn(toolbar, "Ok", width=7,
                          command=self._select_site).pack(side="right", padx=4)
        self._outline_btn(toolbar, "Annuler", width=8,
                           command=lambda: self.controller.show_page(
                               "nouveau_projet")).pack(side="right", padx=4)

    def on_show(self, **kwargs):
        self._load_data()

    def _load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = self.controller.backend.get_site_data()
        for i, item in enumerate(data):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", tags=(tag,),
                              values=(item["filename"], item["city"],
                                      item["country"], item["source"]))
        self.tree.tag_configure("even", background=WHITE)
        self.tree.tag_configure("odd",  background=BG_CARD)

    def _select_site(self):
        sel = self.tree.selection()
        if sel:
            values = self.tree.item(sel[0])["values"]
            target = self.controller.pages.get("nouveau_projet")
            if target and hasattr(target, "v_meteo"):
                target.v_meteo.set(str(values[0]))
        self.controller.show_page("nouveau_projet")

    def _add_site(self):
        self.controller.backend.add_site({})

    def _export(self):
        self.controller.backend.export_sites("")

    def _new_site(self):
        pass

    def _delete_site(self):
        sel = self.tree.selection()
        if sel:
            self.tree.delete(sel[0])
            self.controller.backend.delete_site("")