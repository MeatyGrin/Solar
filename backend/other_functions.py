"""
solar_roof_designer.py
======================
Backend principal de Solar System Designer.

Convention de nommage des stubs
--------------------------------
Les méthodes dont le calcul de domaine (physique / métier) n'est pas
encore implémenté contiennent uniquement `pass  # <nom_fonction>`.
Les méthodes dont la logique est évidente (gestion de projet, mock data,
sauvegarde JSON) sont intégralement implémentées.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


class SolarRoofDesigner:
    """Gestionnaire principal du projet solaire et de la simulation."""

    def __init__(self) -> None:
        self.current_project: Dict[str, Any] = {}

    # ─── Gestion de projet ────────────────────────────────────────────────

    def create_new_project(
        self,
        name: str,
        associated_folder: str,
        meteo_file: str,
    ) -> Dict[str, Any]:
        """Crée un nouveau projet et le définit comme projet courant."""
        project: Dict[str, Any] = {
            "name":               name,
            "associated_folder":  associated_folder,
            "meteo_file":         meteo_file,
            "modules":            [],
            "frames":             [],
            "parameters":         {},
            "orientation":        {"azimuth": 180.0, "tilt": 30.0, "angle_extra": 0.0},
            "grid":               {},
            "simulation_results": {},
        }
        self.current_project = project
        return project

    def load_project(self, file_path: str) -> Dict[str, Any]:
        """Charge un projet depuis un fichier JSON."""
        with open(file_path, "r", encoding="utf-8") as f:
            project = json.load(f)
        self.current_project = project
        return project

    def save_project(
        self,
        description: str,
        filename: str,
        directory: str,
    ) -> str:
        """Sauvegarde le projet courant au format JSON. Retourne le chemin."""
        if not filename.endswith(".json"):
            filename += ".json"
        self.current_project["description"] = description
        directory = directory or "."
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.current_project, f, indent=2, ensure_ascii=False)
        return path

    def get_recent_projects(self) -> List[Dict[str, Any]]:
        """Retourne les projets récents (données de démonstration)."""
        return [
            {"name": "Projet Thomson",     "area": "48 m²", "power": "8.2 kWc"},
            {"name": "Projet Lino Olivie", "area": "32 m²", "power": "5.4 kWc"},
        ]

    def delete_project(self, project_id: str) -> bool:
        pass  # delete_project

    # ─── Sites météorologiques ────────────────────────────────────────────

    def get_site_data(self) -> List[Dict[str, str]]:
        """Retourne la liste des sites météo disponibles (données mockées)."""
        return [
            {"filename": "Paris_2022.epw",      "city": "Paris",        "country": "France", "source": "EnergyPlus"},
            {"filename": "Lyon_2022.epw",        "city": "Lyon",         "country": "France", "source": "EnergyPlus"},
            {"filename": "Marseille_2022.epw",   "city": "Marseille",    "country": "France", "source": "Meteonorm"},
            {"filename": "Bordeaux_2022.epw",    "city": "Bordeaux",     "country": "France", "source": "EnergyPlus"},
            {"filename": "Toulouse_2022.epw",    "city": "Toulouse",     "country": "France", "source": "Meteonorm"},
            {"filename": "Nice_2022.epw",        "city": "Nice",         "country": "France", "source": "PVGIS"},
            {"filename": "Strasbourg_2022.epw",  "city": "Strasbourg",   "country": "France", "source": "EnergyPlus"},
            {"filename": "Nantes_2022.epw",      "city": "Nantes",       "country": "France", "source": "Meteonorm"},
            {"filename": "Montpellier_2022.epw", "city": "Montpellier",  "country": "France", "source": "PVGIS"},
            {"filename": "Rennes_2022.epw",      "city": "Rennes",       "country": "France", "source": "EnergyPlus"},
            {"filename": "Lille_2022.epw",       "city": "Lille",        "country": "France", "source": "Meteonorm"},
            {"filename": "Grenoble_2022.epw",    "city": "Grenoble",     "country": "France", "source": "PVGIS"},
            {"filename": "Dijon_2022.epw",       "city": "Dijon",        "country": "France", "source": "EnergyPlus"},
            {"filename": "Angers_2022.epw",      "city": "Angers",       "country": "France", "source": "Meteonorm"},
            {"filename": "Le_Mans_2022.epw",     "city": "Le Mans",      "country": "France", "source": "PVGIS"},
            {"filename": "Toulon_2022.epw",      "city": "Toulon",       "country": "France", "source": "Meteonorm"},
            {"filename": "Brest_2022.epw",       "city": "Brest",        "country": "France", "source": "EnergyPlus"},
            {"filename": "Reims_2022.epw",       "city": "Reims",        "country": "France", "source": "PVGIS"},
            {"filename": "Clermont_2022.epw",    "city": "Clermont-Fd",  "country": "France", "source": "Meteonorm"},
            {"filename": "Tours_2022.epw",       "city": "Tours",        "country": "France", "source": "EnergyPlus"},
        ]

    def add_site(self, site_data: Dict[str, Any]) -> bool:
        pass  # add_site

    def export_sites(self, file_path: str) -> bool:
        pass  # export_sites

    def delete_site(self, site_id: str) -> bool:
        pass  # delete_site

    # ─── Modules ─────────────────────────────────────────────────────────

    def get_available_modules(self) -> List[Dict[str, Any]]:
        pass  # get_available_modules

    def configure_modules(
        self,
        module_type: str,
        count: int,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass  # configure_modules

    def add_module(self, module_data: Dict[str, Any]) -> bool:
        self.current_project.setdefault("modules", []).append(module_data)
        return True

    def remove_module(self, module_id: str) -> bool:
        pass  # remove_module

    # ─── Frames ──────────────────────────────────────────────────────────

    def get_available_frames(self) -> List[Dict[str, Any]]:
        pass  # get_available_frames

    def configure_frames(
        self, frame_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass  # configure_frames

    # ─── Paramètres généraux ─────────────────────────────────────────────

    def configure_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Enregistre les paramètres système dans le projet courant."""
        if self.current_project:
            self.current_project["parameters"] = params
        return params

    # ─── Orientation ─────────────────────────────────────────────────────

    def calculate_orientation(
        self,
        azimuth: float,
        tilt: float,
        angle_extra: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Calcule l'irradiance et le productible pour l'orientation donnée.
        Enregistre les valeurs dans le projet courant.
        """
        if self.current_project:
            self.current_project["orientation"] = {
                "azimuth":     azimuth,
                "tilt":        tilt,
                "angle_extra": angle_extra,
            }
        pass  # calculate_orientation

    def optimize_orientation(self) -> Dict[str, Any]:
        pass  # optimize_orientation

    def calculate_tilt(self, latitude: float, month: int = 0) -> float:
        pass  # calculate_tilt

    # ─── Système / Onduleur ──────────────────────────────────────────────

    def configure_grid_system(
        self, grid_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass  # configure_grid_system

    def calculate_inverter_sizing(
        self, pv_power: float, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass  # calculate_inverter_sizing

    # ─── Simulation ──────────────────────────────────────────────────────

    def run_simulation(
        self, simulation_params: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Lance la simulation photovoltaïque.
        simulation_params : dict {nom_étape: bool} issu de la page Récap.
        Retourne un dictionnaire de résultats.
        """
        pass  # run_simulation

    def run_advanced_simulation(self) -> Dict[str, Any]:
        pass  # run_advanced_simulation

    def get_simulation_summary(self) -> Dict[str, Any]:
        pass  # get_simulation_summary

    def calculate_losses(self) -> Dict[str, Any]:
        pass  # calculate_losses

    # ─── Export / Rapports ───────────────────────────────────────────────

    def generate_report(
        self, report_type: str, output_path: str
    ) -> bool:
        """
        Génère un rapport (rapport, tableaux, évaluation).
        report_type : "rapport" | "tableaux" | "evaluation"
        """
        pass  # generate_report

    def export_to_csv(self, data_type: str, output_path: str) -> bool:
        pass  # export_to_csv

    def export_to_pdf(self, output_path: str) -> bool:
        pass  # export_to_pdf