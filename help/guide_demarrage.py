"""
🚀 GUIDE DE DÉMARRAGE RAPIDE
============================

Installation et premiers pas avec Solar Roof Designer
"""

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 1 : INSTALLATION
# ═══════════════════════════════════════════════════════════════

# 1. Assurez-vous d'avoir Python 3.8+ installé
# Vérifiez votre version :
# python --version

# 2. Installez les dépendances
# pip install -r requirements.txt

# Sur Linux, vous pourriez avoir besoin de :
# sudo apt-get install python3-tk


# ═══════════════════════════════════════════════════════════════
# ÉTAPE 2 : LANCER L'APPLICATION
# ═══════════════════════════════════════════════════════════════

# Méthode 1 : Lancer l'interface graphique
# python solar_roof_designer.py

# Méthode 2 : Utiliser en mode programmation
from backend.solar_roof_designer import ModeleToitL, DimensionsToit, Panneau, InterfaceGraphique
from backend.advanced_features import OptimiseurPanneaux, ExporteurRapport, GestionnaireTemplates


# ═══════════════════════════════════════════════════════════════
# EXEMPLES D'UTILISATION
# ═══════════════════════════════════════════════════════════════

def exemple_1_base():
    """Exemple 1 : Créer un toit et ajouter des panneaux manuellement"""
    print("🏠 Exemple 1 : Création manuelle\n")
    
    # Créer un modèle de toit avec dimensions personnalisées
    dimensions = DimensionsToit(
        longueur_bras_x=10.0,
        largeur_bras_x=4.0,
        longueur_bras_y=10.0,
        largeur_bras_y=4.0,
        hauteur_mur=4.0,
        hauteur_toit=2.0,
        retrait_faitage=2.0
    )
    
    modele = ModeleToitL(dimensions)
    
    # Ajouter des panneaux manuellement
    modele.ajouter_panneau(Panneau(x=4.5, y=0.5, width=1.65, height=1.0, zone="sud"))
    modele.ajouter_panneau(Panneau(x=6.5, y=0.5, width=1.65, height=1.0, zone="sud"))
    modele.ajouter_panneau(Panneau(x=0.5, y=5.0, width=1.0, height=1.65, zone="ouest"))
    
    # Afficher les statistiques
    stats = modele.calculer_statistiques()
    print(f"✅ Panneaux installés : {stats['nb_panneaux']}")
    print(f"📊 Taux de couverture : {stats['taux_couverture']:.1f}%\n")
    
    return modele


def exemple_2_automatique():
    """Exemple 2 : Placement automatique des panneaux"""
    print("🤖 Exemple 2 : Placement automatique\n")
    
    # Utiliser un template prédéfini
    templates = GestionnaireTemplates.get_templates()
    modele = ModeleToitL(templates['Maison moyenne'])
    
    # Créer l'optimiseur
    optimiseur = OptimiseurPanneaux(modele)
    
    # Placement automatique sur la face sud
    print("📍 Placement automatique sur face sud...")
    panneaux_sud = optimiseur.placement_automatique_zone('sud', orientation='paysage')
    
    for p in panneaux_sud:
        modele.ajouter_panneau(p)
    
    print(f"✅ {len(panneaux_sud)} panneaux placés automatiquement\n")
    
    # Calculer la production
    production = optimiseur.calculer_production_estimee()
    print("⚡ Production estimée :")
    print(f"   Puissance : {production['puissance_kw']:.2f} kWc")
    print(f"   Production : {production['production_kwh_an']:.0f} kWh/an")
    print(f"   Économies : {production['economies_euros_an']:.2f} €/an\n")
    
    return modele


def exemple_3_export():
    """Exemple 3 : Générer des rapports"""
    print("📄 Exemple 3 : Export et rapports\n")
    
    # Charger un exemple
    modele = ModeleToitL(DimensionsToit())
    optimiseur = OptimiseurPanneaux(modele)
    
    # Placement auto complet
    panneaux = optimiseur.placement_automatique_complet(
        zones_prioritaires=['sud', 'ouest']
    )
    
    for p in panneaux[:8]:  # Limiter à 8 panneaux
        modele.ajouter_panneau(p)
    
    # Générer les rapports
    exporteur = ExporteurRapport(modele)
    
    # Rapport texte
    rapport = exporteur.generer_rapport_texte()
    print(rapport)
    
    # Sauvegarder
    print("💾 Sauvegarde du rapport...")
    exporteur.generer_rapport_texte('/home/claude/rapport_exemple.txt')
    exporteur.generer_rapport_csv('/home/claude/panneaux_exemple.csv')
    modele.sauvegarder('/home/claude/config_exemple.json')
    print("✅ Fichiers sauvegardés !\n")


def exemple_4_charger():
    """Exemple 4 : Charger une configuration existante"""
    print("📂 Exemple 4 : Charger un exemple\n")
    
    modele = ModeleToitL(DimensionsToit())
    
    # Charger une configuration d'exemple
    modele.charger('/home/claude/examples/maison_moyenne.json')
    
    stats = modele.calculer_statistiques()
    print(f"✅ Configuration chargée")
    print(f"   Panneaux : {stats['nb_panneaux']}")
    print(f"   Surface : {stats['aire_panneaux']:.2f} m²\n")
    
    return modele


def exemple_5_gui():
    """Exemple 5 : Lancer l'interface graphique"""
    print("🎨 Exemple 5 : Interface graphique\n")
    print("Lancement de l'interface...")
    
    app = InterfaceGraphique()
    app.run()


# ═══════════════════════════════════════════════════════════════
# EXÉCUTION DES EXEMPLES
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   🏠☀️  SOLAR ROOF DESIGNER - GUIDE DE DÉMARRAGE       ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # Menu interactif
    while True:
        print("\n" + "─" * 60)
        print("Choisissez un exemple à exécuter :")
        print("─" * 60)
        print("1. Création manuelle d'un toit avec panneaux")
        print("2. Placement automatique des panneaux")
        print("3. Génération de rapports et exports")
        print("4. Charger une configuration existante")
        print("5. Lancer l'interface graphique")
        print("6. Exécuter tous les exemples (1-4)")
        print("0. Quitter")
        print("─" * 60)
        
        try:
            choix = input("\nVotre choix (0-6) : ").strip()
            print()
            
            if choix == "0":
                print("👋 Au revoir !")
                break
            elif choix == "1":
                exemple_1_base()
            elif choix == "2":
                exemple_2_automatique()
            elif choix == "3":
                exemple_3_export()
            elif choix == "4":
                exemple_4_charger()
            elif choix == "5":
                exemple_5_gui()
                break
            elif choix == "6":
                exemple_1_base()
                exemple_2_automatique()
                exemple_3_export()
                exemple_4_charger()
                print("\n✅ Tous les exemples ont été exécutés avec succès !")
            else:
                print("⚠️  Choix invalide. Veuillez choisir entre 0 et 6.")
                
            input("\n[Appuyez sur Entrée pour continuer...]")
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            input("\n[Appuyez sur Entrée pour continuer...]")


# ═══════════════════════════════════════════════════════════════
# ASTUCES ET CONSEILS
# ═══════════════════════════════════════════════════════════════

"""
💡 ASTUCES :

1. DIMENSIONS DU TOIT
   - Les dimensions sont en mètres
   - Le toit est en forme de L (deux bras perpendiculaires)
   - Pensez à laisser de l'espace pour les faîtages

2. PLACEMENT DES PANNEAUX
   - Panneaux standard : 1.65m × 1.0m (400 Wc)
   - Zones disponibles : sud, ouest, noue_est, noue_nord
   - Laissez 10-20cm d'espace entre les panneaux

3. OPTIMISATION
   - Face sud = meilleur rendement (orientation optimale)
   - Face ouest = bon rendement (après-midi)
   - Noues = rendement moyen mais exploitable
   - Évitez les zones ombragées

4. PRODUCTION
   - 1 m² de panneau ≈ 200 W de puissance installée
   - 1 kWc produit ≈ 1000-1400 kWh/an en France
   - Variation selon la région : 1000 kWh (nord) à 1500 kWh (sud)

5. ÉCONOMIES
   - Prix électricité moyen : ~0.18 €/kWh
   - Retour sur investissement : 8-12 ans en moyenne
   - Durée de vie panneau : 25-30 ans

6. FICHIERS
   - Sauvegardez vos configurations en .json
   - Exportez les rapports en .txt ou .csv
   - Partagez vos configurations avec d'autres utilisateurs
"""
