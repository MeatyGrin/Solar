"""
Module Avancé - Placement Automatique et Optimisation
====================================================
Fonctionnalités supplémentaires pour l'optimisation du placement de panneaux solaires.
"""

import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
import itertools


@dataclass
class PanneauStandard:
    """Dimensions standard des panneaux solaires"""
    width: float = 1.65  # Largeur standard en mètres
    height: float = 1.00  # Hauteur standard en mètres
    puissance: float = 400  # Puissance en Watts


class OptimiseurPanneaux:
    """Optimise le placement automatique des panneaux solaires"""
    
    def __init__(self, modele_toit):
        self.modele = modele_toit
        self.panneau_std = PanneauStandard()
        
    def calculer_zones_disponibles(self) -> dict:
        """Identifie les zones disponibles sur chaque versant du toit"""
        d = self.modele.dim
        
        zones = {
            'sud': {
                'x_min': 0.5,
                'x_max': d.longueur_bras_x - 0.5,
                'y_min': 0.5,
                'y_max': d.largeur_bras_x - 0.5,
                'pente': 'sud'
            },
            'noue_est': {
                'x_min': d.largeur_bras_y + 0.5,
                'x_max': d.longueur_bras_x - 0.5,
                'y_min': d.largeur_bras_x + 0.5,
                'y_max': min(d.longueur_bras_y - 0.5, d.largeur_bras_x + 3),
                'pente': 'noue_est'
            },
            'noue_nord': {
                'x_min': 0.5,
                'x_max': d.largeur_bras_y - 0.5,
                'y_min': d.largeur_bras_x + 0.5,
                'y_max': d.longueur_bras_y - 0.5,
                'pente': 'noue_nord'
            },
            'ouest': {
                'x_min': 0.5,
                'x_max': d.largeur_bras_y - 0.5,
                'y_min': 0.5,
                'y_max': d.longueur_bras_y - 0.5,
                'pente': 'ouest'
            }
        }
        
        return zones
    
    def placement_automatique_zone(self, zone_nom: str, orientation: str = 'paysage',
                                  espacement: float = 0.1) -> List:
        """
        Place automatiquement des panneaux dans une zone
        
        Args:
            zone_nom: Nom de la zone ('sud', 'noue_est', etc.)
            orientation: 'paysage' ou 'portrait'
            espacement: Espace entre panneaux en mètres
        """
        zones = self.calculer_zones_disponibles()
        
        if zone_nom not in zones:
            return []
        
        zone = zones[zone_nom]
        panneaux_generes = []
        
        # Dimensions du panneau selon l'orientation
        if orientation == 'paysage':
            p_width = self.panneau_std.width
            p_height = self.panneau_std.height
        else:  # portrait
            p_width = self.panneau_std.height
            p_height = self.panneau_std.width
        
        # Placement en grille
        x = zone['x_min']
        while x + p_width <= zone['x_max']:
            y = zone['y_min']
            while y + p_height <= zone['y_max']:
                from solar_roof_designer import Panneau
                panneau = Panneau(
                    x=x,
                    y=y,
                    width=p_width,
                    height=p_height,
                    zone=zone['pente']
                )
                panneaux_generes.append(panneau)
                y += p_height + espacement
            x += p_width + espacement
        
        return panneaux_generes
    
    def placement_automatique_complet(self, zones_prioritaires: List[str] = None,
                                     orientation: str = 'paysage') -> List:
        """
        Place automatiquement des panneaux sur tout le toit
        
        Args:
            zones_prioritaires: Liste des zones à couvrir (toutes par défaut)
            orientation: 'paysage' ou 'portrait'
        """
        if zones_prioritaires is None:
            zones_prioritaires = ['sud', 'noue_est', 'ouest', 'noue_nord']
        
        tous_panneaux = []
        
        for zone in zones_prioritaires:
            panneaux_zone = self.placement_automatique_zone(zone, orientation)
            tous_panneaux.extend(panneaux_zone)
        
        return tous_panneaux
    
    def calculer_production_estimee(self, ensoleillement_annuel: float = 1400) -> dict:
        """
        Estime la production électrique annuelle
        
        Args:
            ensoleillement_annuel: kWh/m²/an (1400 pour la France métropolitaine moyenne)
        """
        stats = self.modele.calculer_statistiques()
        
        # Calcul de la puissance installée
        puissance_totale_kw = (stats['nb_panneaux'] * self.panneau_std.puissance) / 1000
        
        # Production estimée (avec facteur de performance ~0.75)
        production_kwh = stats['aire_panneaux'] * ensoleillement_annuel * 0.75
        
        # Économies estimées (prix moyen électricité ~0.18€/kWh)
        economies_annuelles = production_kwh * 0.18
        
        return {
            'puissance_kw': puissance_totale_kw,
            'production_kwh_an': production_kwh,
            'economies_euros_an': economies_annuelles,
            'co2_evite_kg_an': production_kwh * 0.05  # ~50g CO2/kWh évités
        }


class GestionnaireTemplates:
    """Gère les templates prédéfinis de toits"""
    
    @staticmethod
    def get_templates() -> dict:
        """Retourne les templates disponibles"""
        from solar_roof_designer import DimensionsToit
        
        return {
            'Petite maison': DimensionsToit(
                longueur_bras_x=8.0,
                largeur_bras_x=3.0,
                longueur_bras_y=8.0,
                largeur_bras_y=3.0,
                hauteur_mur=3.0,
                hauteur_toit=1.5,
                retrait_faitage=1.5
            ),
            'Maison moyenne': DimensionsToit(
                longueur_bras_x=10.0,
                largeur_bras_x=4.0,
                longueur_bras_y=10.0,
                largeur_bras_y=4.0,
                hauteur_mur=4.0,
                hauteur_toit=2.0,
                retrait_faitage=2.0
            ),
            'Grande maison': DimensionsToit(
                longueur_bras_x=15.0,
                largeur_bras_x=5.0,
                longueur_bras_y=15.0,
                largeur_bras_y=5.0,
                hauteur_mur=5.0,
                hauteur_toit=2.5,
                retrait_faitage=2.5
            ),
            'Bâtiment commercial': DimensionsToit(
                longueur_bras_x=20.0,
                largeur_bras_x=8.0,
                longueur_bras_y=20.0,
                largeur_bras_y=8.0,
                hauteur_mur=6.0,
                hauteur_toit=3.0,
                retrait_faitage=3.0
            )
        }
    
    @staticmethod
    def get_configurations_panneaux() -> dict:
        """Retourne des configurations pré-optimisées de panneaux"""
        return {
            'Minimal (4 panneaux)': [
                {'x': 4.5, 'y': 0.5, 'width': 1.65, 'height': 1.0, 'zone': 'sud'},
                {'x': 6.5, 'y': 0.5, 'width': 1.65, 'height': 1.0, 'zone': 'sud'},
                {'x': 0.5, 'y': 5.0, 'width': 1.0, 'height': 1.65, 'zone': 'ouest'},
                {'x': 2.0, 'y': 5.0, 'width': 1.0, 'height': 1.65, 'zone': 'ouest'}
            ],
            'Standard (8 panneaux)': [
                # Face sud
                {'x': 3.0, 'y': 0.5, 'width': 1.65, 'height': 1.0, 'zone': 'sud'},
                {'x': 5.0, 'y': 0.5, 'width': 1.65, 'height': 1.0, 'zone': 'sud'},
                {'x': 7.0, 'y': 0.5, 'width': 1.65, 'height': 1.0, 'zone': 'sud'},
                {'x': 3.0, 'y': 1.8, 'width': 1.65, 'height': 1.0, 'zone': 'sud'},
                # Face ouest
                {'x': 0.5, 'y': 5.0, 'width': 1.0, 'height': 1.65, 'zone': 'ouest'},
                {'x': 2.0, 'y': 5.0, 'width': 1.0, 'height': 1.65, 'zone': 'ouest'},
                {'x': 0.5, 'y': 7.0, 'width': 1.0, 'height': 1.65, 'zone': 'ouest'},
                {'x': 2.0, 'y': 7.0, 'width': 1.0, 'height': 1.65, 'zone': 'ouest'}
            ]
        }


class ExporteurRapport:
    """Génère des rapports détaillés sur l'installation"""
    
    def __init__(self, modele_toit):
        self.modele = modele_toit
        self.optimiseur = OptimiseurPanneaux(modele_toit)
    
    def generer_rapport_texte(self, filepath: str = None) -> str:
        """Génère un rapport texte complet"""
        stats = self.modele.calculer_statistiques()
        prod = self.optimiseur.calculer_production_estimee()
        
        rapport = f"""
╔══════════════════════════════════════════════════════════════╗
║        RAPPORT D'INSTALLATION PANNEAUX SOLAIRES              ║
╚══════════════════════════════════════════════════════════════╝

📐 DIMENSIONS DU TOIT
{'─' * 60}
  Bras X : {self.modele.dim.longueur_bras_x} × {self.modele.dim.largeur_bras_x} m
  Bras Y : {self.modele.dim.longueur_bras_y} × {self.modele.dim.largeur_bras_y} m
  Hauteur murs : {self.modele.dim.hauteur_mur} m
  Hauteur toit : {self.modele.dim.hauteur_toit} m
  
🏠 SUPERFICIE
{'─' * 60}  
  Surface totale du toit : {stats['aire_toit']:.2f} m²
  Surface couverte : {stats['aire_panneaux']:.2f} m²
  Taux de couverture : {stats['taux_couverture']:.1f}%
  
☀️ INSTALLATION PHOTOVOLTAÏQUE
{'─' * 60}
  Nombre de panneaux : {stats['nb_panneaux']}
  Puissance installée : {prod['puissance_kw']:.2f} kWc
  
📊 PRODUCTION ESTIMÉE (Annuelle)
{'─' * 60}
  Production électrique : {prod['production_kwh_an']:.0f} kWh/an
  Économies : {prod['economies_euros_an']:.2f} €/an
  CO₂ évité : {prod['co2_evite_kg_an']:.0f} kg/an
  
💰 RETOUR SUR INVESTISSEMENT (Estimation)
{'─' * 60}
  Coût installation (est.) : {stats['nb_panneaux'] * 500:.0f} € (500€/panneau)
  Retour sur investissement : ~{(stats['nb_panneaux'] * 500) / prod['economies_euros_an']:.1f} ans
  
📍 LISTE DES PANNEAUX
{'─' * 60}
"""
        
        for i, p in enumerate(self.modele.panneaux, 1):
            rapport += f"  #{i:02d} | Zone: {p.zone:10s} | Position: ({p.x:5.2f}, {p.y:5.2f}) | Taille: {p.width:.2f}×{p.height:.2f}m\n"
        
        rapport += "\n" + "═" * 60 + "\n"
        rapport += "  Rapport généré par Solar Roof Designer v1.0\n"
        rapport += "═" * 60 + "\n"
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(rapport)
        
        return rapport
    
    def generer_rapport_csv(self, filepath: str):
        """Génère un fichier CSV avec les données des panneaux"""
        import csv
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Numéro', 'Zone', 'Position X', 'Position Y', 
                           'Largeur', 'Hauteur', 'Surface (m²)'])
            
            for i, p in enumerate(self.modele.panneaux, 1):
                writer.writerow([i, p.zone, p.x, p.y, p.width, p.height, 
                               p.width * p.height])
            
            # Ligne de total
            stats = self.modele.calculer_statistiques()
            writer.writerow([])
            writer.writerow(['TOTAL', '', '', '', '', '', stats['aire_panneaux']])


# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def detecter_obstacles(modele_toit, obstacles: List[Tuple[float, float, float, float]]) -> List:
    """
    Filtre les panneaux qui entrent en collision avec des obstacles
    
    Args:
        obstacles: Liste de (x, y, width, height) représentant les obstacles
    """
    panneaux_valides = []
    
    for panneau in modele_toit.panneaux:
        collision = False
        
        for obs_x, obs_y, obs_w, obs_h in obstacles:
            # Test de collision AABB (Axis-Aligned Bounding Box)
            if not (panneau.x + panneau.width < obs_x or
                   panneau.x > obs_x + obs_w or
                   panneau.y + panneau.height < obs_y or
                   panneau.y > obs_y + obs_h):
                collision = True
                break
        
        if not collision:
            panneaux_valides.append(panneau)
    
    return panneaux_valides


def calculer_ombrage(heure: int, latitude: float = 48.8566) -> float:
    """
    Calcule un coefficient d'ombrage approximatif selon l'heure
    
    Args:
        heure: Heure de la journée (0-23)
        latitude: Latitude du lieu (par défaut Paris)
    
    Returns:
        Coefficient entre 0 (plein soleil) et 1 (ombre complète)
    """
    # Modèle simplifié
    if heure < 6 or heure > 20:
        return 1.0  # Nuit
    elif 10 <= heure <= 16:
        return 0.0  # Plein soleil
    else:
        # Transition matin/soir
        return 0.5


if __name__ == "__main__":
    # Exemple d'utilisation
    from solar_roof_designer import ModeleToitL, DimensionsToit
    
    print("🔧 Test des fonctionnalités avancées\n")
    
    # Créer un modèle
    modele = ModeleToitL(DimensionsToit())
    
    # Optimiseur
    opt = OptimiseurPanneaux(modele)
    
    # Placement automatique
    print("📍 Placement automatique sur la face sud...")
    panneaux_auto = opt.placement_automatique_zone('sud', orientation='paysage')
    print(f"   → {len(panneaux_auto)} panneaux générés\n")
    
    # Ajouter au modèle
    for p in panneaux_auto[:6]:  # Limiter à 6 pour l'exemple
        modele.ajouter_panneau(p)
    
    # Calculer la production
    production = opt.calculer_production_estimee()
    print("⚡ Production estimée:")
    print(f"   → Puissance: {production['puissance_kw']:.2f} kWc")
    print(f"   → Production: {production['production_kwh_an']:.0f} kWh/an")
    print(f"   → Économies: {production['economies_euros_an']:.2f} €/an\n")
    
    # Générer un rapport
    print("📄 Génération du rapport...")
    exporteur = ExporteurRapport(modele)
    rapport = exporteur.generer_rapport_texte()
    print(rapport)
