# 🏠☀️ Solar Roof Designer - Concepteur de Toits Solaires

Application Python avec interface graphique pour concevoir des toits et optimiser le placement de panneaux solaires photovoltaïques.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Fonctionnalités

### ✨ Fonctionnalités Principales

- **Interface graphique intuitive** avec Tkinter
- **Modélisation 3D** interactive avec PyVista
- **Personnalisation complète** des dimensions du toit
- **Placement manuel ou automatique** des panneaux solaires
- **Calculs en temps réel** :
  - Superficie du toit
  - Surface couverte par les panneaux
  - Taux de couverture
  - Production électrique estimée
  - Économies annuelles
  - CO₂ évité

### 🚀 Fonctionnalités Avancées

- **Placement automatique optimisé** par zone
- **Templates prédéfinis** (petite maison, maison moyenne, grande maison, bâtiment commercial)
- **Export de rapports** (TXT, CSV)
- **Sauvegarde/Chargement** de projets (JSON)
- **Détection d'obstacles** (à venir)
- **Calcul d'ombrage** (à venir)

## 🔧 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner ou télécharger le projet
cd solar_roof_designer

# Installer les dépendances
pip install -r requirements.txt
```

## 🎮 Utilisation

### Lancer l'application principale

```bash
python solar_roof_designer.py
```

### Interface Graphique

L'application se compose de plusieurs sections :

#### 1️⃣ **Dimensions du Toit**
- Définissez les dimensions de votre toit en forme de L
- Cliquez sur "Appliquer Dimensions" pour mettre à jour le modèle

#### 2️⃣ **Ajouter un Panneau**
- Position X, Y : Coordonnées du coin inférieur gauche du panneau
- Largeur, Hauteur : Dimensions du panneau en mètres
- Zone : Choisir la face du toit (sud, noue_est, noue_nord, ouest)
- Cliquez sur "➕ Ajouter Panneau"

#### 3️⃣ **Panneaux Installés**
- Liste de tous les panneaux placés
- Sélectionnez un panneau et cliquez sur "🗑️ Supprimer" pour le retirer
- "🧹 Tout effacer" pour recommencer à zéro

#### 4️⃣ **Statistiques**
- Affichage en temps réel :
  - 🏠 Superficie du toit
  - ☀️ Superficie des panneaux
  - 📊 Taux de couverture
  - 🔢 Nombre de panneaux

#### 5️⃣ **Actions**
- **📊 Visualiser 3D** : Lance la visualisation 3D interactive
- **💾 Sauvegarder** : Enregistre votre projet (JSON)
- **📂 Charger** : Charge un projet existant

### Utilisation des fonctionnalités avancées

```python
from solar_roof_designer import ModeleToitL, DimensionsToit, Panneau
from advanced_features import OptimiseurPanneaux, ExporteurRapport

# Créer un modèle de toit
modele = ModeleToitL(DimensionsToit(
    longueur_bras_x=10.0,
    largeur_bras_x=4.0,
    longueur_bras_y=10.0,
    largeur_bras_y=4.0
))

# Placement automatique
optimiseur = OptimiseurPanneaux(modele)
panneaux = optimiseur.placement_automatique_zone('sud', orientation='paysage')

# Ajouter les panneaux au modèle
for p in panneaux:
    modele.ajouter_panneau(p)

# Calculer la production
production = optimiseur.calculer_production_estimee()
print(f"Production: {production['production_kwh_an']:.0f} kWh/an")

# Générer un rapport
exporteur = ExporteurRapport(modele)
exporteur.generer_rapport_texte('rapport_installation.txt')
exporteur.generer_rapport_csv('panneaux_liste.csv')
```

## 📁 Structure du Projet

```
solar_roof_designer/
│
├── solar_roof_designer.py    # Application principale avec GUI
├── advanced_features.py       # Fonctionnalités avancées
├── requirements.txt           # Dépendances Python
├── README.md                  # Cette documentation
│
├── examples/                  # Exemples de configurations
│   ├── petite_maison.json
│   ├── maison_moyenne.json
│   └── grande_maison.json
│
└── exports/                   # Dossier pour les rapports générés
    ├── rapport_installation.txt
    └── panneaux_liste.csv
```

## 🎯 Guide d'utilisation rapide

### Exemple 1 : Créer un toit simple

1. Lancez l'application
2. Laissez les dimensions par défaut ou modifiez-les
3. Ajoutez des panneaux manuellement :
   - X: 4.5, Y: 0.5, Largeur: 1.65, Hauteur: 1.0, Zone: sud
   - X: 6.5, Y: 0.5, Largeur: 1.65, Hauteur: 1.0, Zone: sud
4. Cliquez sur "📊 Visualiser 3D"

### Exemple 2 : Placement automatique

```python
from solar_roof_designer import *
from advanced_features import *

# Créer le modèle
app = InterfaceGraphique()
opt = OptimiseurPanneaux(app.modele)

# Placement auto sur toutes les faces
panneaux = opt.placement_automatique_complet(
    zones_prioritaires=['sud', 'ouest'],
    orientation='paysage'
)

# Ajouter au modèle
for p in panneaux:
    app.modele.ajouter_panneau(p)

# Lancer l'interface
app.run()
```

### Exemple 3 : Utiliser un template

```python
from advanced_features import GestionnaireTemplates

templates = GestionnaireTemplates.get_templates()
dim_maison_moyenne = templates['Maison moyenne']

modele = ModeleToitL(dim_maison_moyenne)
```

## 📊 Calculs et Estimations

### Production Électrique

La production est calculée selon la formule :
```
Production (kWh/an) = Surface panneaux (m²) × Ensoleillement (kWh/m²/an) × Rendement (0.75)
```

**Valeurs par défaut :**
- Ensoleillement : 1400 kWh/m²/an (moyenne France)
- Rendement global : 75% (pertes système, onduleur, câbles)
- Puissance panneau standard : 400 Wc

### Économies

```
Économies (€/an) = Production (kWh/an) × Prix électricité (0.18 €/kWh)
```

### CO₂ Évité

```
CO₂ évité (kg/an) = Production (kWh/an) × 0.05 kg/kWh
```

## 🎨 Personnalisation

### Modifier les couleurs

Dans `solar_roof_designer.py`, ligne ~350 :

```python
# Couleur du toit
couleur_toit = '#C2B280'  # Beige
# Couleur des panneaux
couleur_panneaux = '#2c3e50'  # Bleu foncé
# Couleur des murs
couleur_murs = 'white'
```

### Dimensions des panneaux standard

Dans `advanced_features.py`, ligne ~15 :

```python
@dataclass
class PanneauStandard:
    width: float = 1.65   # Largeur en mètres
    height: float = 1.00  # Hauteur en mètres
    puissance: float = 400  # Puissance en Watts
```

## 🐛 Résolution de problèmes

### Problème : La fenêtre 3D ne s'affiche pas

**Solution :** Vérifiez que PyVista est correctement installé :
```bash
pip install --upgrade pyvista
```

### Problème : Erreur "Module not found"

**Solution :** Installez toutes les dépendances :
```bash
pip install -r requirements.txt
```

### Problème : Les panneaux ne s'affichent pas sur le toit

**Solution :** Vérifiez que :
- Les coordonnées X, Y sont dans les limites du toit
- La zone sélectionnée correspond bien à la position
- L'offset Z (0.05m) est suffisant

## 🔮 Fonctionnalités à venir

- [ ] Import de plans cadastraux
- [ ] Détection automatique des obstacles (cheminées, fenêtres de toit)
- [ ] Calcul d'ombrage en temps réel selon la position du soleil
- [ ] Simulation 3D de l'ensoleillement annuel
- [ ] Export 3D (STL, OBJ) pour impression 3D
- [ ] Intégration avec Google Maps pour récupérer les coordonnées GPS
- [ ] Calcul du retour sur investissement détaillé
- [ ] Support de toits plus complexes (multi-pans, arrondis)

## 📝 Formats de fichiers

### Fichier de sauvegarde (.json)

```json
{
  "dimensions": {
    "longueur_bras_x": 10.0,
    "largeur_bras_x": 4.0,
    "longueur_bras_y": 10.0,
    "largeur_bras_y": 4.0,
    "hauteur_mur": 4.0,
    "hauteur_toit": 2.0,
    "retrait_faitage": 2.0
  },
  "panneaux": [
    {
      "x": 4.5,
      "y": 0.5,
      "width": 1.65,
      "height": 1.0,
      "zone": "sud"
    }
  ]
}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

Développé avec ❤️ pour faciliter la conception d'installations photovoltaïques.

## 🙏 Remerciements

- **PyVista** pour la visualisation 3D
- **Tkinter** pour l'interface graphique
- **NumPy** pour les calculs mathématiques

## 📞 Support

Pour toute question ou support :
- Ouvrir une issue sur GitHub
- Consulter la documentation
- Vérifier les exemples fournis

---

**Note :** Les estimations de production et d'économies sont approximatives et dépendent de nombreux facteurs (orientation, inclinaison, ombrage, localisation géographique, etc.). Consultez un professionnel pour une étude détaillée.
