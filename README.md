# Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires

## 📋 Description

Système automatisé de génération d'emplois du temps d'examens pour une université de 13,000+ étudiants. Génère des plannings optimisés en moins de 2 minutes tout en respectant toutes les contraintes réglementaires.

## 🚀 Démarrage Rapide

### Prérequis

- **Python**: 3.9 ou supérieur
- **PostgreSQL**: 14 ou supérieur
- **Système**: macOS, Linux, ou Windows
- **RAM**: 4GB minimum recommandé

### Installation Complète

#### 1. Cloner le Projet

```bash
cd ~/Desktop
git clone https://github.com/anesszereg/Plateforme-d-Optimisation-des-Emplois-du-Temps-d-Examens-Universitaires.git
cd "DB PROJECT"
```

#### 2. Créer un Environnement Virtuel (Recommandé)

```bash
# Créer l'environnement virtuel
python3 -m venv .venv

# Activer l'environnement
# Sur macOS/Linux:
source .venv/bin/activate
# Sur Windows:
.venv\Scripts\activate
```

#### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

**Dépendances principales:**
- `streamlit==1.29.0` - Framework web
- `psycopg2-binary==2.9.9` - Connecteur PostgreSQL
- `pandas==2.1.4` - Analyse de données
- `plotly==5.18.0` - Visualisations
- `openpyxl==3.1.5` - Export Excel

#### 4. Configurer PostgreSQL

```bash
# Créer la base de données
createdb exam_scheduling

# Créer le fichier de configuration
cat > .env << EOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=exam_scheduling
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
EOF
```

**Note**: Remplacez `votre_mot_de_passe` par votre mot de passe PostgreSQL réel.

#### 5. Initialiser la Base de Données

```bash
# Créer le schéma (tables, vues, fonctions)
python3 scripts/init_database.py
```

**Ce script crée:**
- 10 tables relationnelles
- 8 vues analytiques
- 2 fonctions PL/pgSQL
- Indexes d'optimisation

#### 6. Générer les Données de Test

```bash
# Générer ~13,000 étudiants, 110 formations, 1,118 modules
python3 scripts/generate_data.py
```

**Données générées:**
- 7 départements
- 110 formations (L1-M2)
- 13,051 étudiants
- 148 professeurs
- 1,118 modules
- 105,468 inscriptions
- 126 salles
- 1 période d'examen active

#### 7. Lancer l'Application

```bash
# Démarrer Streamlit
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

**Si le port 8501 est occupé:**
```bash
streamlit run app.py --server.port 8502
```

## 🎯 Utilisation

### Première Utilisation

1. **Accéder au Dashboard** - Visualisez les KPIs globaux
2. **Aller dans Administration** - Page de génération d'EDT
3. **Cliquer sur "🚀 Générer l'EDT"** - Lance la génération automatique
4. **Attendre ~78 secondes** - Le système planifie tous les examens
5. **Consulter les résultats** - Examens planifiés, conflits détectés

### Interfaces Disponibles

| Page | Rôle | Fonctionnalités |
|------|------|-----------------|
| 🏠 **Dashboard** | Tous | KPIs globaux, détection de conflits |
| 👨‍💼 **Administration** | Admin | Génération EDT, optimisation, gestion |
| 📊 **Statistiques** | Direction | Analyses stratégiques, graphiques |
| 🏛️ **Départements** | Chefs dept. | Vues départementales, formations |
| 👤 **Consultation** | Étudiants/Profs | Plannings personnalisés, export |

### Fonctionnalités Clés

#### Génération d'EDT
```
1. Sélectionner la période d'examen
2. Cliquer sur "Générer l'EDT"
3. Le système:
   - Trie les modules par taille
   - Alloue les salles optimales
   - Affecte les professeurs
   - Vérifie toutes les contraintes
   - Génère le rapport
```

#### Détection de Conflits
- ✅ Conflits étudiants (examens simultanés)
- ✅ Conflits professeurs (surveillances multiples)
- ✅ Dépassements de capacité des salles
- ✅ Conflits d'occupation des salles

#### Export de Données
- 📄 **CSV**: Tous les tableaux exportables
- 📊 **Excel**: Planning par formation
- 🖨️ **Impression**: Plannings personnalisés

## 🧪 Tests et Validation

### Tester Toutes les Fonctionnalités

```bash
# Test complet du système
python3 scripts/test_all_functions.py
```

**Tests effectués:**
- ✓ Connexion base de données
- ✓ Intégrité des tables (10/10)
- ✓ Vues analytiques (8/8)
- ✓ Fonctions PL/pgSQL (2/2)
- ✓ Méthodes Python (10/10)
- ✓ Algorithme de planification
- ✓ Détection de conflits

### Tests de Performance

```bash
# Benchmark des requêtes SQL
python3 scripts/benchmark.py
```

### Tester la Génération d'EDT

```bash
# Test spécifique de l'algorithme FastScheduler
python3 scripts/test_edt_generation.py
```

## 🐛 Dépannage

### Problème: Port 8501 déjà utilisé

```bash
# Trouver le processus
lsof -ti:8501

# Tuer le processus
kill -9 $(lsof -ti:8501)

# Ou utiliser un autre port
streamlit run app.py --server.port 8502
```

### Problème: Erreur de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL est actif
pg_isready

# Vérifier les credentials dans .env
cat .env

# Tester la connexion
psql -d exam_scheduling -U postgres
```

### Problème: Module Python manquant

```bash
# Réinstaller toutes les dépendances
pip install -r requirements.txt --force-reinstall

# Ou installer un module spécifique
pip install openpyxl
```

### Problème: Base de données vide

```bash
# Réinitialiser complètement
python3 scripts/init_database.py
python3 scripts/generate_data.py
```

### Problème: Cache Streamlit

```bash
# Vider le cache Streamlit
streamlit cache clear

# Redémarrer l'application
streamlit run app.py
```

## 📦 Déploiement

### Option 1: Streamlit Cloud (Gratuit)

1. Push vers GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter votre repo
4. Configurer les secrets (DB credentials)
5. Déployer

**Fichiers requis:**
- `.python-version` ✅ (Python 3.11)
- `packages.txt` ✅ (libpq-dev)
- `requirements.txt` ✅

### Option 2: Railway (Production)

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Login
railway login

# Déployer
railway up

# Ajouter PostgreSQL
railway add postgresql
```

### Option 3: Serveur Universitaire

```bash
# Sur le serveur
git clone [repo-url]
cd "DB PROJECT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configurer PostgreSQL local
createdb exam_scheduling
python3 scripts/init_database.py
python3 scripts/generate_data.py

# Lancer avec nohup
nohup streamlit run app.py --server.port 8501 &
```

**Voir:** `Docs/DEPLOYMENT_GUIDE.md` pour plus de détails

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
