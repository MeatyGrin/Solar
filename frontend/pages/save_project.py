import tkinter as tk
from tkinter import filedialog, messagebox
from pages.base_page import BasePage
from styles import *


class SaveProjectPage(BasePage):

    NAV_ITEMS = []

    def build_ui(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        overlay = tk.Frame(self, bg="#D0C8B0")
        overlay.grid(row=0, column=0, sticky="nsew")
        overlay.rowconfigure(0, weight=1)
        overlay.columnconfigure(0, weight=1)

        card = tk.Frame(overlay, bg=BG_PANEL, bd=2, relief="solid")
        card.grid(row=0, column=0, padx=180, pady=80, sticky="nsew")
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="Sauvegarder le projet",
                  font=F_TITLE, bg=BG_PANEL, fg=NAVY, pady=12).pack(anchor="w", padx=18)
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=12, pady=(0, 10))

        form = tk.Frame(card, bg=BG_PANEL)
        form.pack(fill="x", padx=18, pady=6)
        form.columnconfigure(1, weight=1)

        self.v_desc  = tk.StringVar()
        self.v_fname = tk.StringVar()

        self._field(form, "Description",    row=0, var=self.v_desc)
        self._field(form, "Nom du fichier", row=1, var=self.v_fname)

        tk.Label(form, text="Répertoire", font=F_BODY,
                  bg=BG_PANEL, fg=TEXT_DARK, anchor="w").grid(
            row=2, column=0, sticky="nw", pady=(8, 0), padx=(0, 8))

        dir_row = tk.Frame(form, bg=BG_PANEL)
        dir_row.grid(row=2, column=1, sticky="ew", pady=(8, 0))
        self.dir_text = tk.Text(dir_row, height=3, font=F_SMALL,
                                 bg=WHITE, relief="solid", bd=1, width=28)
        self.dir_text.pack(side="left", fill="x", expand=True)
        tk.Button(dir_row, text=" … ", font=F_BODY, bg=GRAY_LT, relief="solid", bd=1,
                   cursor="hand2", command=self._browse_dir).pack(side="left", padx=4)

        btn_frame = tk.Frame(card, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=18, pady=14)

        close_lbl = tk.Label(btn_frame, text="✕", font=("Arial", 14),
                               bg=BG_PANEL, fg=GRAY, cursor="hand2", padx=6)
        close_lbl.pack(side="right")
        close_lbl.bind("<Button-1>", lambda e: self.controller.show_page("dashboard"))

        self._orange_btn(btn_frame, "✓  Valider",
                          command=self._save, width=12).pack(side="right")
        self._outline_btn(btn_frame, "Annuler",
                           command=lambda: self.controller.show_page("dashboard"),
                           width=10).pack(side="right", padx=8)

    def refresh_navbar(self, nav_frame: tk.Frame):
        for w in nav_frame.winfo_children():
            w.destroy()
        home = tk.Label(nav_frame, text="⌂", font=("Arial", 17),
                         bg=NAV_BG, fg=NAVY, cursor="hand2", padx=10)
        home.pack(side="left", pady=6)
        home.bind("<Button-1>", lambda e: self.controller.show_page("dashboard"))
        tk.Label(nav_frame, text="Sauvegarder le projet",
                  font=F_NAV, bg=NAV_BG, fg=NAVY).pack(side="left", padx=6)

    def _browse_dir(self):
        directory = filedialog.askdirectory(title="Sélectionner un répertoire")
        if directory:
            self.dir_text.delete("1.0", "end")
            self.dir_text.insert("1.0", directory)

    def _save(self):
        filename  = self.v_fname.get().strip()
        directory = self.dir_text.get("1.0", "end").strip()
        if not filename:
            messagebox.showwarning("Champ requis", "Veuillez saisir un nom de fichier.")
            return
        try:
            path = self.controller.backend.save_project(
                self.v_desc.get().strip(), filename, directory)
            messagebox.showinfo("Sauvegarde", f"Projet sauvegardé :\n{path}")
        except Exception as exc:
            messagebox.showerror("Erreur", str(exc))
        finally:
            self.controller.show_page("dashboard")