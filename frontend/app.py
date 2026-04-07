import tkinter as tk
import sys
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))   # .../frontend/
_ROOT = os.path.dirname(_HERE)                        # .../Solar/

for p in (_HERE, _ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Imports absolus ───────────────────────────────────────────────────────────
from styles import *
from components.sidebar        import Sidebar
from pages.dashboard           import DashboardPage
from pages.nouveau_projet      import NouveauProjetPage
from pages.plan                import PlanPage
from pages.plan_3d             import Plan3DPage          # ← nouvelle page
from pages.orientation         import OrientationPage     # ← conservé, hors flow
from pages.recap               import RecapPage
from pages.simulation_params   import SimulationParamsPage
from pages.save_project        import SaveProjectPage
from pages.site_file           import SiteFilePage

from backend.other_functions import SolarRoofDesigner


class SolarApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Solar System Designer")
        self.root.geometry("1280x780")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG_MAIN)

        self.backend         = SolarRoofDesigner()
        self.current_project: dict = {}

        self._build_layout()
        self._setup_pages()
        self.show_page("dashboard")

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_layout(self):
        self.sidebar_frame = tk.Frame(self.root, bg=SIDEBAR_BG, width=SIDEBAR_W)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        tk.Frame(self.root, bg=BORDER, width=1).pack(side="left", fill="y")

        right = tk.Frame(self.root, bg=BG_MAIN)
        right.pack(side="left", fill="both", expand=True)

        self.nav_frame = tk.Frame(
            right, bg=NAV_BG, height=NAV_H,
            highlightthickness=1, highlightbackground=BORDER,
        )
        self.nav_frame.pack(side="top", fill="x")
        self.nav_frame.pack_propagate(False)

        self.content = tk.Frame(right, bg=BG_MAIN)
        self.content.pack(side="top", fill="both", expand=True)

        Sidebar(self.sidebar_frame, self)

    # ── Pages ─────────────────────────────────────────────────────────────────

    def _setup_pages(self):
        page_map = {
            # ── Flow principal ────────────────────────────────────────────
            "dashboard":         DashboardPage,
            "nouveau_projet":    NouveauProjetPage,
            "plan":              PlanPage,          # onglets Modules/Frames/Params
            "plan_3d":           Plan3DPage,        # pose panneaux + angles
            "recap":             RecapPage,
            "simulation_params": SimulationParamsPage,

            # ── Accès libre ───────────────────────────────────────────────
            "save_project":      SaveProjectPage,
            "site_file":         SiteFilePage,

            # ── Conservé hors flow (usage futur) ─────────────────────────
            "orientation":       OrientationPage,
        }
        self.pages: dict = {}
        for name, Cls in page_map.items():
            page = Cls(self.content, self)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages[name] = page

    # ── Navigation ────────────────────────────────────────────────────────────

    def show_page(self, name: str, **kwargs):
        if name not in self.pages:
            return
        for page in self.pages.values():
            page.place_forget()
        page = self.pages[name]
        page.place(relx=0, rely=0, relwidth=1, relheight=1)
        page.refresh_navbar(self.nav_frame)
        page.on_show(**kwargs)

    # ── Démarrage ─────────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()