# Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires

## Description
Système automatisé de génération d'emplois du temps d'examens pour une université de 13,000+ étudiants.

## Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

2. Configurer la base de données PostgreSQL:
```bash
# Créer la base de données
createdb exam_scheduling

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos identifiants
```

3. Initialiser la base de données:
```bash
python scripts/init_database.py
```

4. Générer les données de test:
```bash
python scripts/generate_data.py
```

5. Lancer l'application:
```bash
streamlit run app.py
```

## Structure du Projet

```
DB PROJECT/
├── app.py                          # Application Streamlit principale
├── requirements.txt                # Dépendances Python
├── .env                           # Configuration (à créer)
├── database/
│   ├── schema.sql                 # Schéma de la base de données
│   ├── queries.sql                # Requêtes SQL analytiques
│   └── indexes.sql                # Optimisations et index
├── scripts/
│   ├── init_database.py           # Initialisation de la DB
│   ├── generate_data.py           # Génération de données réalistes
│   └── benchmark.py               # Tests de performance
├── src/
│   ├── database.py                # Connexion et opérations DB
│   ├── scheduler.py               # Algorithme d'optimisation
│   ├── constraints.py             # Vérification des contraintes
│   └── analytics.py               # Calcul des KPIs
└── pages/
    ├── 1_👨‍💼_Administration.py      # Interface administrateur
    ├── 2_📊_Statistiques.py         # Vue stratégique
    ├── 3_🏛️_Départements.py         # Gestion départementale
    └── 4_👤_Consultation.py         # Vue étudiants/professeurs
```

## Fonctionnalités

- ✅ Génération automatique d'EDT en <45 secondes
- ✅ Détection et résolution de conflits
- ✅ Respect des contraintes (1 examen/jour/étudiant, 3 max/jour/prof)
- ✅ Optimisation de l'utilisation des salles
- ✅ Tableaux de bord multi-rôles
- ✅ KPIs et statistiques en temps réel

## Technologies

- **Base de données**: PostgreSQL
- **Backend**: Python 3.10+
- **Frontend**: Streamlit + Plotly
- **Optimisation**: Algorithmes de contraintes + PL/pgSQL
