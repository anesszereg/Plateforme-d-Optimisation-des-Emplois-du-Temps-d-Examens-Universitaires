-- Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
-- Schéma de base de données PostgreSQL

-- Suppression des tables existantes (ordre inverse des dépendances)
DROP TABLE IF EXISTS examens CASCADE;
DROP TABLE IF EXISTS surveillances CASCADE;
DROP TABLE IF EXISTS inscriptions CASCADE;
DROP TABLE IF EXISTS modules CASCADE;
DROP TABLE IF EXISTS professeurs CASCADE;
DROP TABLE IF EXISTS etudiants CASCADE;
DROP TABLE IF EXISTS formations CASCADE;
DROP TABLE IF EXISTS lieu_examen CASCADE;
DROP TABLE IF EXISTS departements CASCADE;
DROP TABLE IF EXISTS periodes_examen CASCADE;

-- Table des départements
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    batiment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des lieux d'examen (salles et amphithéâtres)
CREATE TABLE lieu_examen (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    capacite INTEGER NOT NULL CHECK (capacite > 0),
    capacite_examen INTEGER NOT NULL CHECK (capacite_examen > 0 AND capacite_examen <= capacite),
    type VARCHAR(20) NOT NULL CHECK (type IN ('salle', 'amphitheatre')),
    batiment VARCHAR(50) NOT NULL,
    equipements TEXT[],
    disponible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_lieu UNIQUE (nom, batiment)
);

-- Table des formations
CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    dept_id INTEGER NOT NULL REFERENCES departements(id) ON DELETE CASCADE,
    niveau VARCHAR(20) NOT NULL CHECK (niveau IN ('L1', 'L2', 'L3', 'M1', 'M2')),
    nb_modules INTEGER NOT NULL CHECK (nb_modules > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des étudiants
CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    formation_id INTEGER NOT NULL REFERENCES formations(id) ON DELETE CASCADE,
    promo INTEGER NOT NULL CHECK (promo >= 2020 AND promo <= 2030),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des professeurs
CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    dept_id INTEGER NOT NULL REFERENCES departements(id) ON DELETE CASCADE,
    specialite VARCHAR(100),
    grade VARCHAR(50) CHECK (grade IN ('Professeur', 'Maitre de conférences', 'Assistant', 'Vacataire')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des modules
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    credits INTEGER NOT NULL CHECK (credits > 0),
    formation_id INTEGER NOT NULL REFERENCES formations(id) ON DELETE CASCADE,
    semestre INTEGER NOT NULL CHECK (semestre IN (1, 2)),
    pre_req_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
    duree_examen INTEGER NOT NULL DEFAULT 120 CHECK (duree_examen > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des inscriptions (étudiants inscrits aux modules)
CREATE TABLE inscriptions (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    annee_universitaire VARCHAR(9) NOT NULL,
    note DECIMAL(4,2) CHECK (note >= 0 AND note <= 20),
    statut VARCHAR(20) DEFAULT 'inscrit' CHECK (statut IN ('inscrit', 'validé', 'échoué', 'absent')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_inscription UNIQUE (etudiant_id, module_id, annee_universitaire)
);

-- Table des périodes d'examen
CREATE TABLE periodes_examen (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    session VARCHAR(20) NOT NULL CHECK (session IN ('normale', 'rattrapage')),
    annee_universitaire VARCHAR(9) NOT NULL,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_dates CHECK (date_fin > date_debut)
);

-- Table des examens
CREATE TABLE examens (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    prof_responsable_id INTEGER NOT NULL REFERENCES professeurs(id) ON DELETE RESTRICT,
    salle_id INTEGER NOT NULL REFERENCES lieu_examen(id) ON DELETE RESTRICT,
    periode_id INTEGER NOT NULL REFERENCES periodes_examen(id) ON DELETE CASCADE,
    date_heure TIMESTAMP NOT NULL,
    duree_minutes INTEGER NOT NULL CHECK (duree_minutes > 0),
    nb_inscrits INTEGER NOT NULL DEFAULT 0 CHECK (nb_inscrits >= 0),
    statut VARCHAR(20) DEFAULT 'planifié' CHECK (statut IN ('planifié', 'en_cours', 'terminé', 'annulé')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_examen UNIQUE (module_id, periode_id)
);

-- Table des surveillances (affectation des professeurs à la surveillance)
CREATE TABLE surveillances (
    id SERIAL PRIMARY KEY,
    examen_id INTEGER NOT NULL REFERENCES examens(id) ON DELETE CASCADE,
    prof_id INTEGER NOT NULL REFERENCES professeurs(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'surveillant' CHECK (role IN ('responsable', 'surveillant')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_surveillance UNIQUE (examen_id, prof_id)
);

-- Index pour optimisation des performances
CREATE INDEX idx_etudiants_formation ON etudiants(formation_id);
CREATE INDEX idx_etudiants_promo ON etudiants(promo);
CREATE INDEX idx_formations_dept ON formations(dept_id);
CREATE INDEX idx_modules_formation ON modules(formation_id);
CREATE INDEX idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_inscriptions_module ON inscriptions(module_id);
CREATE INDEX idx_inscriptions_annee ON inscriptions(annee_universitaire);
CREATE INDEX idx_examens_date ON examens(date_heure);
CREATE INDEX idx_examens_salle ON examens(salle_id);
CREATE INDEX idx_examens_module ON examens(module_id);
CREATE INDEX idx_examens_periode ON examens(periode_id);
CREATE INDEX idx_surveillances_prof ON surveillances(prof_id);
CREATE INDEX idx_surveillances_examen ON surveillances(examen_id);
CREATE INDEX idx_professeurs_dept ON professeurs(dept_id);

-- Index composites pour requêtes complexes
CREATE INDEX idx_examens_date_salle ON examens(date_heure, salle_id);
CREATE INDEX idx_inscriptions_etudiant_annee ON inscriptions(etudiant_id, annee_universitaire);

-- Commentaires sur les tables
COMMENT ON TABLE departements IS 'Départements de l''université';
COMMENT ON TABLE lieu_examen IS 'Salles et amphithéâtres pour les examens (capacité limitée à 20 en période d''examen)';
COMMENT ON TABLE formations IS 'Programmes de formation (Licence, Master)';
COMMENT ON TABLE etudiants IS 'Étudiants inscrits à l''université';
COMMENT ON TABLE professeurs IS 'Corps enseignant';
COMMENT ON TABLE modules IS 'Modules d''enseignement';
COMMENT ON TABLE inscriptions IS 'Inscriptions des étudiants aux modules';
COMMENT ON TABLE examens IS 'Planification des examens';
COMMENT ON TABLE surveillances IS 'Affectation des surveillants aux examens';
COMMENT ON TABLE periodes_examen IS 'Périodes d''examen (session normale, rattrapage)';
