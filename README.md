# Portfolio de Projets Informatiques

Ce repository contient deux projets informatiques développés dans le cadre de formations académiques, démontrant des compétences en développement logiciel, gestion de bases de données et interfaces utilisateur.

##  Table des Matières

- [CleanCampus Manager](#cleancampus-manager)
- [Système de Gestion d'Inventaire](#système-de-gestion-dinventaire)
- [Installation et Utilisation](#installation-et-utilisation)
- [Technologies Utilisées](#technologies-utilisées)
- [Équipe de Développement](#équipe-de-développement)

---

##  CleanCampus Manager

### Description
**CleanCampus Manager** est une application desktop moderne développée en Python avec Tkinter, conçue pour automatiser et moderniser la gestion du nettoyage dans les résidences universitaires. Cette solution complète offre une gestion intelligente des tâches, un suivi des performances et une communication optimisée entre étudiants, gestionnaires de bâtiments et administrateurs.

###  Fonctionnalités Principales

####  Authentification et Rôles
- **Administrateur** : Contrôle total sur la gestion des bâtiments, utilisateurs et paramètres globaux
- **Gestionnaire de Bâtiment** : Gestion complète de leur bâtiment assigné, création de groupes, suivi des tâches et validation
- **Étudiant/Invité** : Accès en lecture seule aux horaires, classements et notifications

####  Gestion Intelligente
- **Planification Automatique** : Génération d'horaires de nettoyage hebdomadaires avec rotation intelligente des tâches
- **Groupes Automatisés** : Création automatique de groupes de nettoyage basée sur les blocs et étudiants disponibles
- **Suivi en Temps Réel** : Tableau de bord interactif pour surveiller la progression, le statut et la qualité du travail

####  Gamification et Motivation
- **Système de Badges** : Attribution de badges pour encourager la constance, la ponctualité et la qualité du travail
- **Classements de Performance** : Affichage des tableaux de classement des meilleurs groupes et étudiants
- **Système de Notifications** : Notifications pour informer les utilisateurs des tâches assignées, validations et récompenses

####  Rapports et Exports
- **Exports CSV** : Export facile des horaires, listes d'étudiants et rapports de performance
- **Sauvegarde et Restauration** : Outils intégrés pour sauvegarder et restaurer les données de l'application

###  Stack Technologique
- **Langage** : Python 3
- **Interface Graphique** : Tkinter (via `ttk`)
- **Gestion des Données** : `json`, `csv`
- **Dépendances** : Aucune dépendance externe requise

---

##  Système de Gestion d'Inventaire

### Description
**Système de Gestion d'Inventaire** est une application console développée en C, conçue pour la gestion complète d'un inventaire de produits. Cette solution offre une interface intuitive pour gérer les stocks, suivre les mouvements de marchandises et générer des rapports détaillés.

###  Fonctionnalités Principales

####  Gestion des Produits
- **Ajout de Produits** : Interface intuitive pour ajouter de nouveaux produits avec génération automatique d'ID unique
- **Modification de Produits** : Mise à jour des informations produit (nom, catégorie, quantité, prix, stock minimum)
- **Suppression de Produits** : Gestion sécurisée de la suppression avec confirmation

####  Suivi et Analyse
- **Affichage Complet** : Visualisation de tous les produits avec code couleur (vert = stock normal, jaune = stock faible, rouge = rupture)
- **Produits en Rupture** : Filtrage automatique des produits nécessitant un réapprovisionnement
- **Statistiques d'Inventaire** : Calculs automatiques (nombre total, valeur totale, prix moyen, pourcentage de produits en rupture)

####  Recherche et Navigation
- **Recherche Intelligente** : Recherche par nom de produit ou ID
- **Historique des Modifications** : Suivi complet des changements avec horodatage
- **Interface Colorée** : Utilisation de couleurs pour une meilleure lisibilité et expérience utilisateur

####  Persistance des Données
- **Sauvegarde Automatique** : Sauvegarde des données dans des fichiers texte
- **Gestion des Fichiers** : Lecture/écriture sécurisée avec gestion d'erreurs
- **Log des Modifications** : Enregistrement de toutes les modifications pour audit

###  Stack Technologique
- **Langage** : C
- **Système d'Exploitation** : Windows (utilisation de `windows.h`)
- **Gestion des Fichiers** : I/O standard C
- **Interface** : Console avec couleurs et formatage

---

##  Installation et Utilisation

### CleanCampus Manager

1. **Prérequis** : Assurez-vous d'avoir Python 3.8 ou supérieur installé
2. **Cloner le repository** (si applicable) ou télécharger les fichiers
3. **Lancer l'application** :
   ```bash
   cd CleanCampusManager
   python main.py
   ```

### Système de Gestion d'Inventaire

1. **Prérequis** : Compilateur C compatible Windows (GCC, MinGW, ou Visual Studio)
2. **Compilation** :
   ```bash
   cd Project/Project
   gcc -o inventory *.c
   ```
3. **Exécution** :
   ```bash
   ./inventory
   ```

---

## 🛠️ Technologies Utilisées

### CleanCampus Manager
- **Python 3** : Langage principal
- **Tkinter** : Interface graphique
- **JSON** : Stockage des données
- **CSV** : Export des rapports

### Système de Gestion d'Inventaire
- **C** : Langage principal
- **Windows API** : Gestion des couleurs console
- **Fichiers texte** : Persistance des données
- **Structures de données** : Gestion efficace de l'inventaire

---

##  Équipe de Développement

### CleanCampus Manager
Ce projet a été réalisé par une équipe passionnée :

| Nom de Famille | Prénom(s) |
|----------------|-----------|
| **KOALAGA** | Héliane Elichebat |
| **NIKIEMA** | Mariata |
| **ZONGO** | Abdel Sadek Nerebewendé |
| **YANOGO** | Fabiana |
| **ZOUNGRANA** | Pengdwendé Sébastien |

### Système de Gestion d'Inventaire
Développé individuellement dans le cadre d'un projet académique.

---

##  Licence

Ces projets sont développés à des fins éducatives et académiques.

---
