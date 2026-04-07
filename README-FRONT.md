# Solar System Designer – Frontend Tkinter

## Structure du projet

```
Solar/
├── main.py                          # Point d'entrée
├── requirements.txt
├── backend/
│   ├── __init__.py
│   └── solar_roof_designer.py       # Backend principal (stubs + implémentations évidentes)
├── frontend/
│   ├── __init__.py
│   ├── app.py                       # Contrôleur principal + layout fenêtre
│   ├── styles.py                    # Couleurs, polices, constantes
│   ├── components/
│   │   ├── __init__.py
│   │   └── sidebar.py               # Barre latérale gauche
│   └── pages/
│       ├── __init__.py
│       ├── base_page.py             # Classe de base (navbar, helpers)
│       ├── dashboard.py             # Page d'accueil
│       ├── nouveau_projet.py        # Formulaire nouveau projet
│       ├── plan.py                  # Onglets Modules / Frames / Paramètres + vue 3D
│       ├── orientation.py           # Azimut / Tilt / Anneau + vue 3D interactive
│       ├── recap.py                 # Checklist récapitulatif + lancement simulation
│       ├── simulation_params.py     # Résultats simulation + graphiques
│       ├── save_project.py          # Dialogue sauvegarde
│       └── site_file.py             # Tableau des sites météo
└── examples/
    ├── grande_maison.json
    ├── maison_moyenne.json
    └── petite_maison.json
```

## Lancement

```bash
python main.py
```

Aucune installation de dépendances requise (Tkinter est inclus dans Python ≥ 3.8).

## Navigation entre les pages

```
Dashboard
  └─▶ Nouveau Projet  (bouton "Démarrer" ou nav checkbox)
        └─▶ Plan  (onglets Modules / Frames / Paramètres)
              └─▶ Orientation  (azimut, tilt, vue 3D)
                    └─▶ Récap  (checklist simulation)
                          └─▶ Simulation Params  (résultats + graphiques)

Accès libre depuis toute page :
  • Save Project   (bouton "Enregistrer" dans navbar)
  • Site File      (lien dans Nouveau Projet)
  • Dashboard      (icône maison dans navbar)
```

## Convention des stubs backend

Dans `solar_roof_designer.py`, toute méthode dont le calcul métier
n'est pas encore implémenté contient uniquement :

```python
pass  # nom_de_la_fonction
```

Les méthodes implémentées (gestion fichiers JSON, données mock, 
paramètres) fonctionnent pleinement.