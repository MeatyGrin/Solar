"""
Application de Conception de Toits avec Panneaux Solaires
========================================================
Interface graphique pour modéliser des toits et optimiser le placement de panneaux solaires.
"""

import pyvista as pv
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from typing import List, Tuple, Dict
from dataclasses import dataclass, asdict


# ==============================================================================
# CLASSES DE DONNÉES
# ==============================================================================

@dataclass
class DimensionsToit:
    """Dimensions du toit en forme de L"""
    longueur_bras_x: float = 10.0  # Longueur du bras horizontal
    largeur_bras_x: float = 4.0    # Largeur du bras horizontal
    longueur_bras_y: float = 10.0  # Longueur du bras vertical
    largeur_bras_y: float = 4.0    # Largeur du bras vertical
    hauteur_mur: float = 4.0       # Hauteur des murs
    hauteur_toit: float = 2.0      # Hauteur supplémentaire du toit
    retrait_faitage: float = 2.0   # Retrait des faîtages


@dataclass
class Panneau:
    """Représentation d'un panneau solaire"""
    x: float
    y: float
    width: float
    height: float
    zone: str  # 'sud', 'noue', 'ouest', etc.
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict) -> 'Panneau':
        return Panneau(**data)


# ==============================================================================
# CLASSE PRINCIPALE - MODÈLE DE TOIT
# ==============================================================================

class ModeleToitL:
    """Gère la géométrie et les calculs d'un toit en L"""
    
    def __init__(self, dimensions: DimensionsToit):
        self.dim = dimensions
        self.panneaux: List[Panneau] = []
        self._update_geometry()
    
    def _update_geometry(self):
        """Calcule les points et faces du toit"""
        d = self.dim
        
        # Points au sol (Z=0)
        self.points = np.array([
            [0, 0, 0],                      # 0
            [d.longueur_bras_x, 0, 0],      # 1
            [d.longueur_bras_x, d.largeur_bras_x, 0],  # 2
            [d.largeur_bras_y, d.largeur_bras_x, 0],   # 3
            [d.largeur_bras_y, d.longueur_bras_y, 0],  # 4
            [0, d.longueur_bras_y, 0],      # 5
            
            # Points haut des murs (Z=hauteur_mur)
            [0, 0, d.hauteur_mur],                      # 6
            [d.longueur_bras_x, 0, d.hauteur_mur],      # 7
            [d.longueur_bras_x, d.largeur_bras_x, d.hauteur_mur],  # 8
            [d.largeur_bras_y, d.largeur_bras_x, d.hauteur_mur],   # 9
            [d.largeur_bras_y, d.longueur_bras_y, d.hauteur_mur],  # 10
            [0, d.longueur_bras_y, d.hauteur_mur],      # 11
            
            # Points haut du toit (faîtages)
            [d.retrait_faitage, d.retrait_faitage, d.hauteur_mur + d.hauteur_toit],  # 12
            [d.longueur_bras_x - d.retrait_faitage, d.retrait_faitage, d.hauteur_mur + d.hauteur_toit],  # 13
            [d.retrait_faitage, d.longueur_bras_y - d.retrait_faitage, d.hauteur_mur + d.hauteur_toit],  # 14
        ], dtype=float)
        
        # Faces des murs
        self.faces_murs = np.hstack([
            [4, 0, 1, 7, 6],
            [4, 1, 2, 8, 7],
            [4, 2, 3, 9, 8],
            [4, 3, 4, 10, 9],
            [4, 4, 5, 11, 10],
            [4, 5, 0, 6, 11],
        ])
        
        # Faces du toit
        self.faces_toit = np.hstack([
            [3, 7, 8, 13],           # Croupe Est
            [3, 10, 11, 14],         # Croupe Nord
            [4, 8, 9, 12, 13],       # Noue Est
            [4, 9, 10, 14, 12],      # Noue Nord
            [4, 6, 7, 13, 12],       # Versant Sud
            [4, 11, 6, 12, 14],      # Versant Ouest
        ])
    
    def update_dimensions(self, nouvelles_dims: DimensionsToit):
        """Met à jour les dimensions et recalcule la géométrie"""
        self.dim = nouvelles_dims
        self._update_geometry()
    
    def ajouter_panneau(self, panneau: Panneau):
        """Ajoute un panneau solaire"""
        self.panneaux.append(panneau)
    
    def supprimer_panneau(self, index: int):
        """Supprime un panneau par son index"""
        if 0 <= index < len(self.panneaux):
            self.panneaux.pop(index)
    
    def clear_panneaux(self):
        """Supprime tous les panneaux"""
        self.panneaux.clear()
    
    def calculer_z_panneau(self, x: float, y: float, zone: str) -> float:
        """Calcule la hauteur Z d'un point sur le toit selon la zone"""
        d = self.dim
        offset = 0.05  # Pour éviter le z-fighting
        
        if zone == "sud":
            # Pente: Z croît avec Y
            return y + d.hauteur_mur + offset
        elif zone == "noue_est":
            # Pente: Z décroît avec X
            return (d.longueur_bras_x + d.hauteur_mur - x) + offset
        elif zone == "noue_nord":
            # Pente: Z décroît avec Y
            return (d.longueur_bras_y + d.hauteur_mur - y) + offset
        elif zone == "ouest":
            # Pente: Z croît avec X
            return x + d.hauteur_mur + offset
        else:
            return d.hauteur_mur + offset
    
    def creer_points_panneau(self, panneau: Panneau) -> np.ndarray:
        """Crée les 4 points d'un panneau en suivant la pente du toit"""
        x0, y0 = panneau.x, panneau.y
        x1, y1 = x0 + panneau.width, y0 + panneau.height
        
        if panneau.zone == "sud":
            z0 = self.calculer_z_panneau(x0, y0, "sud")
            z1 = self.calculer_z_panneau(x1, y1, "sud")
            pts = [[x0, y0, z0], [x1, y0, z0], [x1, y1, z1], [x0, y1, z1]]
        
        elif panneau.zone == "noue_est":
            z_x0 = self.calculer_z_panneau(x0, y0, "noue_est")
            z_x1 = self.calculer_z_panneau(x1, y0, "noue_est")
            pts = [[x0, y0, z_x0], [x1, y0, z_x1], [x1, y1, z_x1], [x0, y1, z_x0]]
        
        else:  # ouest ou autres
            z0 = self.calculer_z_panneau(x0, y0, panneau.zone)
            z1 = self.calculer_z_panneau(x1, y1, panneau.zone)
            pts = [[x0, y0, z0], [x1, y0, z1], [x1, y1, z1], [x0, y1, z0]]
        
        return np.array(pts)
    
    def get_mesh_murs(self) -> pv.PolyData:
        """Retourne le maillage des murs"""
        return pv.PolyData(self.points, self.faces_murs)
    
    def get_mesh_toit(self) -> pv.PolyData:
        """Retourne le maillage du toit"""
        return pv.PolyData(self.points, self.faces_toit)
    
    def get_mesh_panneaux(self) -> pv.PolyData:
        """Retourne le maillage de tous les panneaux"""
        if not self.panneaux:
            return None
        
        all_points = []
        faces = []
        point_offset = 0
        
        for panneau in self.panneaux:
            pts = self.creer_points_panneau(panneau)
            all_points.extend(pts)
            faces.append([4, point_offset, point_offset+1, point_offset+2, point_offset+3])
            point_offset += 4
        
        all_points_array = np.array(all_points)
        faces_array = np.hstack(faces)
        
        return pv.PolyData(all_points_array, faces_array)
    
    def calculer_statistiques(self) -> Dict[str, float]:
        """Calcule les statistiques du toit et des panneaux"""
        mesh_toit = self.get_mesh_toit()
        aire_toit = mesh_toit.area
        
        mesh_panneaux = self.get_mesh_panneaux()
        aire_panneaux = mesh_panneaux.area if mesh_panneaux else 0.0
        
        taux_couverture = (aire_panneaux / aire_toit * 100) if aire_toit > 0 else 0
        
        return {
            'aire_toit': aire_toit,
            'aire_panneaux': aire_panneaux,
            'taux_couverture': taux_couverture,
            'nb_panneaux': len(self.panneaux)
        }
    
    def sauvegarder(self, filepath: str):
        """Sauvegarde la configuration dans un fichier JSON"""
        data = {
            'dimensions': asdict(self.dim),
            'panneaux': [p.to_dict() for p in self.panneaux]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def charger(self, filepath: str):
        """Charge une configuration depuis un fichier JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.dim = DimensionsToit(**data['dimensions'])
        self.panneaux = [Panneau.from_dict(p) for p in data['panneaux']]
        self._update_geometry()


# ==============================================================================
# INTERFACE GRAPHIQUE
# ==============================================================================

class InterfaceGraphique:
    """Interface graphique principale de l'application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Concepteur de Toits Solaires")
        self.root.geometry("800x700")
        
        # Modèle de données
        self.modele = ModeleToitL(DimensionsToit())
        
        # Configuration de l'interface
        self._creer_interface()
        self._mise_a_jour_stats()
    
    def _creer_interface(self):
        """Crée tous les widgets de l'interface"""
        
        # === FRAME PRINCIPAL ===
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === SECTION DIMENSIONS ===
        dim_frame = ttk.LabelFrame(main_frame, text="Dimensions du Toit (m)", padding="10")
        dim_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Variables pour les dimensions
        self.vars_dim = {}
        labels = [
            ("Longueur bras X:", "longueur_bras_x"),
            ("Largeur bras X:", "largeur_bras_x"),
            ("Longueur bras Y:", "longueur_bras_y"),
            ("Largeur bras Y:", "largeur_bras_y"),
            ("Hauteur murs:", "hauteur_mur"),
            ("Hauteur toit:", "hauteur_toit"),
            ("Retrait faîtage:", "retrait_faitage")
        ]
        
        for i, (label, attr) in enumerate(labels):
            ttk.Label(dim_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            var = tk.DoubleVar(value=getattr(self.modele.dim, attr))
            self.vars_dim[attr] = var
            ttk.Entry(dim_frame, textvariable=var, width=10).grid(row=i, column=1, padx=5, pady=2)
        
        ttk.Button(dim_frame, text="Appliquer Dimensions", 
                  command=self._appliquer_dimensions).grid(row=len(labels), column=0, columnspan=2, pady=10)
        
        # === SECTION PANNEAUX ===
        panel_frame = ttk.LabelFrame(main_frame, text="Ajouter un Panneau", padding="10")
        panel_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Variables pour les panneaux
        ttk.Label(panel_frame, text="Position X:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.panel_x = tk.DoubleVar(value=4.5)
        ttk.Entry(panel_frame, textvariable=self.panel_x, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(panel_frame, text="Position Y:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.panel_y = tk.DoubleVar(value=0.5)
        ttk.Entry(panel_frame, textvariable=self.panel_y, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(panel_frame, text="Largeur:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.panel_w = tk.DoubleVar(value=1.5)
        ttk.Entry(panel_frame, textvariable=self.panel_w, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(panel_frame, text="Hauteur:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.panel_h = tk.DoubleVar(value=1.0)
        ttk.Entry(panel_frame, textvariable=self.panel_h, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(panel_frame, text="Zone:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.panel_zone = tk.StringVar(value="sud")
        zone_combo = ttk.Combobox(panel_frame, textvariable=self.panel_zone, 
                                  values=["sud", "noue_est", "noue_nord", "ouest"], 
                                  state="readonly", width=10)
        zone_combo.grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Button(panel_frame, text="➕ Ajouter Panneau", 
                  command=self._ajouter_panneau).grid(row=5, column=0, columnspan=2, pady=10)
        
        # === LISTE DES PANNEAUX ===
        list_frame = ttk.LabelFrame(main_frame, text="Panneaux Installés", padding="10")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Scrollbar et Listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.liste_panneaux = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
        self.liste_panneaux.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.liste_panneaux.yview)
        
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="🗑️ Supprimer", 
                  command=self._supprimer_panneau).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🧹 Tout effacer", 
                  command=self._effacer_panneaux).pack(side=tk.LEFT, padx=2)
        
        # === STATISTIQUES ===
        stats_frame = ttk.LabelFrame(main_frame, text="Statistiques", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.label_stats = ttk.Label(stats_frame, text="", font=('Arial', 10))
        self.label_stats.pack()
        
        # === BOUTONS D'ACTION ===
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(action_frame, text="📊 Visualiser 3D", 
                  command=self._visualiser_3d, style='Accent.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(action_frame, text="💾 Sauvegarder", 
                  command=self._sauvegarder).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(action_frame, text="📂 Charger", 
                  command=self._charger).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def _appliquer_dimensions(self):
        """Applique les nouvelles dimensions au modèle"""
        try:
            nouvelles_dims = DimensionsToit(
                longueur_bras_x=self.vars_dim["longueur_bras_x"].get(),
                largeur_bras_x=self.vars_dim["largeur_bras_x"].get(),
                longueur_bras_y=self.vars_dim["longueur_bras_y"].get(),
                largeur_bras_y=self.vars_dim["largeur_bras_y"].get(),
                hauteur_mur=self.vars_dim["hauteur_mur"].get(),
                hauteur_toit=self.vars_dim["hauteur_toit"].get(),
                retrait_faitage=self.vars_dim["retrait_faitage"].get()
            )
            self.modele.update_dimensions(nouvelles_dims)
            self._mise_a_jour_stats()
            messagebox.showinfo("Succès", "Dimensions mises à jour !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {e}")
    
    def _ajouter_panneau(self):
        """Ajoute un nouveau panneau"""
        try:
            panneau = Panneau(
                x=self.panel_x.get(),
                y=self.panel_y.get(),
                width=self.panel_w.get(),
                height=self.panel_h.get(),
                zone=self.panel_zone.get()
            )
            self.modele.ajouter_panneau(panneau)
            self._mise_a_jour_liste()
            self._mise_a_jour_stats()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")
    
    def _supprimer_panneau(self):
        """Supprime le panneau sélectionné"""
        selection = self.liste_panneaux.curselection()
        if selection:
            index = selection[0]
            self.modele.supprimer_panneau(index)
            self._mise_a_jour_liste()
            self._mise_a_jour_stats()
    
    def _effacer_panneaux(self):
        """Efface tous les panneaux"""
        if messagebox.askyesno("Confirmation", "Supprimer tous les panneaux ?"):
            self.modele.clear_panneaux()
            self._mise_a_jour_liste()
            self._mise_a_jour_stats()
    
    def _mise_a_jour_liste(self):
        """Met à jour la liste des panneaux"""
        self.liste_panneaux.delete(0, tk.END)
        for i, p in enumerate(self.modele.panneaux):
            self.liste_panneaux.insert(tk.END, 
                f"#{i+1} - {p.zone} | ({p.x:.1f}, {p.y:.1f}) | {p.width}x{p.height}m")
    
    def _mise_a_jour_stats(self):
        """Met à jour les statistiques affichées"""
        stats = self.modele.calculer_statistiques()
        texte = (
            f"🏠 Superficie Toit: {stats['aire_toit']:.2f} m²\n"
            f"☀️ Superficie Panneaux: {stats['aire_panneaux']:.2f} m²\n"
            f"📊 Taux de Couverture: {stats['taux_couverture']:.1f}%\n"
            f"🔢 Nombre de Panneaux: {stats['nb_panneaux']}"
        )
        self.label_stats.config(text=texte)
    
    def _visualiser_3d(self):
        """Lance la visualisation 3D avec PyVista"""
        try:
            plotter = pv.Plotter()
            
            # Ajout des maillages
            mesh_murs = self.modele.get_mesh_murs()
            mesh_toit = self.modele.get_mesh_toit()
            
            plotter.add_mesh(mesh_murs, color='white', show_edges=True, line_width=2)
            plotter.add_mesh(mesh_toit, color='#C2B280', show_edges=True, line_width=1, 
                           pbr=True, metallic=0.1, roughness=0.7)
            
            # Ajout des panneaux si présents
            mesh_panneaux = self.modele.get_mesh_panneaux()
            if mesh_panneaux:
                plotter.add_mesh(mesh_panneaux, color='#2c3e50', show_edges=True, 
                               edge_color='red', line_width=2)
            
            # Ajout des statistiques
            stats = self.modele.calculer_statistiques()
            texte_info = (
                f"Superficie Toit: {stats['aire_toit']:.2f} m²\n"
                f"Superficie Panneaux: {stats['aire_panneaux']:.2f} m²\n"
                f"Taux couverture: {stats['taux_couverture']:.1f}%\n"
                f"Panneaux: {stats['nb_panneaux']}"
            )
            plotter.add_text(texte_info, position='upper_left', color='black', font_size=12)
            
            # Configuration de la caméra
            plotter.camera_position = [(-15, -15, 12), (5, 5, 3), (0, 0, 1)]
            plotter.enable_parallel_projection()
            plotter.set_background('#FFFBE6')
            
            plotter.show()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la visualisation: {e}")
    
    def _sauvegarder(self):
        """Sauvegarde la configuration"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            try:
                self.modele.sauvegarder(filepath)
                messagebox.showinfo("Succès", "Configuration sauvegardée !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def _charger(self):
        """Charge une configuration"""
        filepath = filedialog.askopenfilename(
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            try:
                self.modele.charger(filepath)
                
                # Mise à jour de l'interface
                for attr, var in self.vars_dim.items():
                    var.set(getattr(self.modele.dim, attr))
                
                self._mise_a_jour_liste()
                self._mise_a_jour_stats()
                messagebox.showinfo("Succès", "Configuration chargée !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()


# ==============================================================================
# POINT D'ENTRÉE
# ==============================================================================

if __name__ == "__main__":
    app = InterfaceGraphique()
    app.run()
