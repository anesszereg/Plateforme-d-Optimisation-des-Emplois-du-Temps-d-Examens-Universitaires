# Guide d'Installation

## Prérequis

- Python 3.10 ou supérieur
- PostgreSQL 13 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation Étape par Étape

### 1. Installer PostgreSQL

**macOS (avec Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Téléchargez et installez depuis [postgresql.org](https://www.postgresql.org/download/windows/)

### 2. Créer la Base de Données

```bash
# Se connecter à PostgreSQL
psql postgres

# Créer la base de données
CREATE DATABASE exam_scheduling;

# Créer un utilisateur (optionnel)
CREATE USER exam_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE exam_scheduling TO exam_user;

# Quitter
\q
```

### 3. Cloner/Télécharger le Projet

```bash
cd ~/Desktop
# Le projet est déjà dans "DB PROJECT"
cd "DB PROJECT"
```

### 4. Installer les Dépendances Python

```bash
# Créer un environnement virtuel (recommandé)
python3 -m venv venv

# Activer l'environnement virtuel
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 5. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec vos paramètres
nano .env
```

Contenu du fichier `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=exam_scheduling
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

### 6. Initialiser la Base de Données

```bash
# Créer les tables et les vues
python scripts/init_database.py
```

Vous devriez voir:
```
Connexion à la base de données...
Exécution du schéma de base de données...
Création des vues et fonctions...
Création des index d'optimisation...
✅ Base de données initialisée avec succès!
```

### 7. Générer les Données de Test

```bash
# Générer 13,000+ étudiants et 130,000+ inscriptions
python scripts/generate_data.py
```

Cette étape peut prendre 2-5 minutes. Vous verrez:
```
Génération des départements...
✅ 7 départements créés
Génération des salles et amphithéâtres...
✅ 126 salles créées
...
✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!
```

### 8. Lancer l'Application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse:
```
http://localhost:8501
```

## Vérification de l'Installation

### Test 1: Vérifier la Base de Données

```bash
psql exam_scheduling

# Vérifier les tables
\dt

# Vérifier le nombre d'étudiants
SELECT COUNT(*) FROM etudiants;

# Devrait retourner ~13,000
```

### Test 2: Exécuter les Benchmarks

```bash
python scripts/benchmark.py
```

Cela testera:
- Les performances des requêtes SQL
- L'algorithme de génération d'EDT (objectif: <45s)
- Les analyses et KPIs

### Test 3: Générer un EDT

1. Ouvrir l'application: `http://localhost:8501`
2. Aller dans **Administration** (menu latéral)
3. Cliquer sur **🚀 Générer l'EDT**
4. Attendre la génération (devrait prendre <45 secondes)
5. Vérifier qu'il n'y a pas de conflits

## Résolution de Problèmes

### Erreur: "Connection refused"

**Problème:** PostgreSQL n'est pas démarré

**Solution:**
```bash
# macOS
brew services start postgresql@15

# Linux
sudo systemctl start postgresql

# Windows
# Démarrer le service PostgreSQL depuis les Services Windows
```

### Erreur: "FATAL: password authentication failed"

**Problème:** Mauvais mot de passe dans `.env`

**Solution:**
1. Vérifier le mot de passe PostgreSQL
2. Mettre à jour le fichier `.env`
3. Redémarrer l'application

### Erreur: "ModuleNotFoundError"

**Problème:** Dépendances non installées

**Solution:**
```bash
pip install -r requirements.txt
```

### L'application est lente

**Solutions:**
1. Vérifier que les index sont créés:
```bash
psql exam_scheduling -c "\di"
```

2. Analyser les tables:
```bash
python -c "from src.database import Database; db = Database(); db.execute_query('ANALYZE', fetch=False)"
```

3. Augmenter les ressources PostgreSQL dans `postgresql.conf`:
```
shared_buffers = 256MB
work_mem = 16MB
maintenance_work_mem = 128MB
```

## Utilisation en Production

### Sécurité

1. **Changer les mots de passe par défaut**
2. **Utiliser HTTPS** pour l'accès web
3. **Configurer un firewall** pour PostgreSQL
4. **Sauvegardes régulières:**

```bash
# Backup
pg_dump exam_scheduling > backup_$(date +%Y%m%d).sql

# Restore
psql exam_scheduling < backup_20250120.sql
```

### Performance

1. **Monitoring:**
```bash
# Installer pg_stat_statements
psql exam_scheduling -c "CREATE EXTENSION pg_stat_statements;"
```

2. **Optimisation:**
- Ajuster les paramètres PostgreSQL selon la charge
- Utiliser un pool de connexions (pgBouncer)
- Mettre en cache les résultats fréquents

## Support

Pour toute question ou problème:
1. Vérifier les logs: `tail -f /var/log/postgresql/postgresql-*.log`
2. Consulter la documentation PostgreSQL
3. Exécuter les benchmarks pour identifier les goulots d'étranglement

## Désinstallation

```bash
# Supprimer la base de données
psql postgres -c "DROP DATABASE exam_scheduling;"

# Supprimer l'environnement virtuel
rm -rf venv/

# Supprimer les fichiers Python compilés
find . -type d -name __pycache__ -exec rm -rf {} +
```
