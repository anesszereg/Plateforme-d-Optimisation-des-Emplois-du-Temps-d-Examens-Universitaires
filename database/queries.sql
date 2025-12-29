-- Requêtes SQL Analytiques pour le Dashboard
-- Plateforme d'Optimisation des Emplois du Temps d'Examens

-- ============================================
-- 1. DÉTECTION DE CONFLITS
-- ============================================

-- Conflits étudiants (plus d'1 examen par jour)
CREATE OR REPLACE VIEW conflits_etudiants AS
SELECT 
    e.id as etudiant_id,
    e.nom,
    e.prenom,
    DATE(ex1.date_heure) as date_conflit,
    COUNT(DISTINCT ex1.id) as nb_examens,
    STRING_AGG(m.nom, ', ') as modules_en_conflit
FROM etudiants e
JOIN inscriptions i ON e.id = i.etudiant_id
JOIN examens ex1 ON i.module_id = ex1.module_id
JOIN modules m ON ex1.module_id = m.id
WHERE i.statut = 'inscrit'
GROUP BY e.id, e.nom, e.prenom, DATE(ex1.date_heure)
HAVING COUNT(DISTINCT ex1.id) > 1;

-- Conflits professeurs (plus de 3 examens par jour)
CREATE OR REPLACE VIEW conflits_professeurs AS
SELECT 
    p.id as prof_id,
    p.nom,
    p.prenom,
    DATE(ex.date_heure) as date_conflit,
    COUNT(DISTINCT ex.id) as nb_examens,
    STRING_AGG(m.nom, ', ') as modules_en_conflit
FROM professeurs p
JOIN surveillances s ON p.id = s.prof_id
JOIN examens ex ON s.examen_id = ex.id
JOIN modules m ON ex.module_id = m.id
GROUP BY p.id, p.nom, p.prenom, DATE(ex.date_heure)
HAVING COUNT(DISTINCT ex.id) > 3;

-- Conflits de capacité des salles
CREATE OR REPLACE VIEW conflits_capacite AS
SELECT 
    ex.id as examen_id,
    m.nom as module,
    l.nom as salle,
    l.capacite_examen as capacite_max,
    ex.nb_inscrits,
    ex.nb_inscrits - l.capacite_examen as depassement,
    ex.date_heure
FROM examens ex
JOIN modules m ON ex.module_id = m.id
JOIN lieu_examen l ON ex.salle_id = l.id
WHERE ex.nb_inscrits > l.capacite_examen;

-- Conflits de chevauchement de salles
CREATE OR REPLACE VIEW conflits_salles AS
SELECT 
    ex1.id as examen1_id,
    ex2.id as examen2_id,
    l.nom as salle,
    m1.nom as module1,
    m2.nom as module2,
    ex1.date_heure as debut1,
    ex1.date_heure + (ex1.duree_minutes || ' minutes')::INTERVAL as fin1,
    ex2.date_heure as debut2,
    ex2.date_heure + (ex2.duree_minutes || ' minutes')::INTERVAL as fin2
FROM examens ex1
JOIN examens ex2 ON ex1.salle_id = ex2.salle_id AND ex1.id < ex2.id
JOIN lieu_examen l ON ex1.salle_id = l.id
JOIN modules m1 ON ex1.module_id = m1.id
JOIN modules m2 ON ex2.module_id = m2.id
WHERE ex1.date_heure < ex2.date_heure + (ex2.duree_minutes || ' minutes')::INTERVAL
  AND ex2.date_heure < ex1.date_heure + (ex1.duree_minutes || ' minutes')::INTERVAL;

-- ============================================
-- 2. KPIs GLOBAUX
-- ============================================

-- Vue d'ensemble des statistiques
CREATE OR REPLACE VIEW kpi_global AS
SELECT 
    (SELECT COUNT(*) FROM etudiants) as total_etudiants,
    (SELECT COUNT(*) FROM professeurs) as total_professeurs,
    (SELECT COUNT(*) FROM departements) as total_departements,
    (SELECT COUNT(*) FROM formations) as total_formations,
    (SELECT COUNT(*) FROM modules) as total_modules,
    (SELECT COUNT(*) FROM examens WHERE statut = 'planifié') as examens_planifies,
    (SELECT COUNT(*) FROM inscriptions WHERE statut = 'inscrit') as total_inscriptions,
    (SELECT COUNT(*) FROM lieu_examen) as total_salles,
    (SELECT SUM(capacite_examen) FROM lieu_examen) as capacite_totale;

-- Taux d'occupation des salles par jour
CREATE OR REPLACE VIEW occupation_salles_par_jour AS
SELECT 
    DATE(ex.date_heure) as date_examen,
    COUNT(DISTINCT ex.salle_id) as salles_utilisees,
    (SELECT COUNT(*) FROM lieu_examen WHERE disponible = TRUE) as salles_disponibles,
    ROUND(100.0 * COUNT(DISTINCT ex.salle_id) / 
          (SELECT COUNT(*) FROM lieu_examen WHERE disponible = TRUE), 2) as taux_occupation_pct,
    SUM(ex.nb_inscrits) as total_etudiants_examens,
    COUNT(ex.id) as nb_examens
FROM examens ex
WHERE ex.statut = 'planifié'
GROUP BY DATE(ex.date_heure)
ORDER BY date_examen;

-- Charge de travail des professeurs (surveillance)
CREATE OR REPLACE VIEW charge_professeurs AS
SELECT 
    p.id,
    p.nom,
    p.prenom,
    d.nom as departement,
    COUNT(s.id) as nb_surveillances,
    COUNT(DISTINCT DATE(ex.date_heure)) as nb_jours_surveillance,
    ROUND(AVG(ex.duree_minutes) / 60.0, 2) as duree_moyenne_heures
FROM professeurs p
LEFT JOIN surveillances s ON p.id = s.prof_id
LEFT JOIN examens ex ON s.examen_id = ex.id
LEFT JOIN departements d ON p.dept_id = d.id
GROUP BY p.id, p.nom, p.prenom, d.nom
ORDER BY nb_surveillances DESC;

-- ============================================
-- 3. STATISTIQUES PAR DÉPARTEMENT
-- ============================================

CREATE OR REPLACE VIEW stats_departement AS
SELECT 
    d.id as dept_id,
    d.nom as departement,
    COUNT(DISTINCT f.id) as nb_formations,
    COUNT(DISTINCT e.id) as nb_etudiants,
    COUNT(DISTINCT p.id) as nb_professeurs,
    COUNT(DISTINCT m.id) as nb_modules,
    COUNT(DISTINCT ex.id) as nb_examens_planifies,
    COALESCE(SUM(ex.nb_inscrits), 0) as total_places_examens
FROM departements d
LEFT JOIN formations f ON d.id = f.dept_id
LEFT JOIN etudiants e ON f.id = e.formation_id
LEFT JOIN professeurs p ON d.id = p.dept_id
LEFT JOIN modules m ON f.id = m.formation_id
LEFT JOIN examens ex ON m.id = ex.module_id AND ex.statut = 'planifié'
GROUP BY d.id, d.nom
ORDER BY nb_etudiants DESC;

-- ============================================
-- 4. PLANNING PERSONNALISÉ
-- ============================================

-- Planning d'un étudiant
CREATE OR REPLACE FUNCTION get_planning_etudiant(p_etudiant_id INTEGER, p_periode_id INTEGER)
RETURNS TABLE (
    date_heure TIMESTAMP,
    module TEXT,
    code_module TEXT,
    salle TEXT,
    batiment TEXT,
    duree_minutes INTEGER,
    professeur TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ex.date_heure,
        m.nom::TEXT as module,
        m.code::TEXT as code_module,
        l.nom::TEXT as salle,
        l.batiment::TEXT,
        ex.duree_minutes,
        (p.nom || ' ' || p.prenom)::TEXT as professeur
    FROM inscriptions i
    JOIN examens ex ON i.module_id = ex.module_id
    JOIN modules m ON ex.module_id = m.id
    JOIN lieu_examen l ON ex.salle_id = l.id
    JOIN professeurs p ON ex.prof_responsable_id = p.id
    WHERE i.etudiant_id = p_etudiant_id
      AND ex.periode_id = p_periode_id
      AND i.statut = 'inscrit'
    ORDER BY ex.date_heure;
END;
$$ LANGUAGE plpgsql;

-- Planning d'un professeur (surveillance)
CREATE OR REPLACE FUNCTION get_planning_professeur(p_prof_id INTEGER, p_periode_id INTEGER)
RETURNS TABLE (
    date_heure TIMESTAMP,
    module_nom TEXT,
    salle_nom TEXT,
    batiment TEXT,
    duree_minutes INTEGER,
    nb_inscrits INTEGER,
    role TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ex.date_heure,
        m.nom::TEXT as module_nom,
        l.nom::TEXT as salle_nom,
        l.batiment::TEXT,
        ex.duree_minutes,
        ex.nb_inscrits,
        s.role::TEXT
    FROM surveillances s
    JOIN examens ex ON s.examen_id = ex.id
    JOIN modules m ON ex.module_id = m.id
    JOIN lieu_examen l ON ex.salle_id = l.id
    WHERE s.prof_id = p_prof_id
      AND ex.periode_id = p_periode_id
    ORDER BY ex.date_heure;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 5. OPTIMISATION ET ANALYSE
-- ============================================

-- Salles sous-utilisées
CREATE OR REPLACE VIEW salles_sous_utilisees AS
SELECT 
    l.id,
    l.nom as salle,
    l.batiment,
    l.capacite_examen,
    COALESCE(AVG(ex.nb_inscrits), 0) as moyenne_occupation,
    ROUND(100.0 * COALESCE(AVG(ex.nb_inscrits), 0) / l.capacite_examen, 2) as taux_utilisation_pct,
    COUNT(ex.id) as nb_utilisations
FROM lieu_examen l
LEFT JOIN examens ex ON l.id = ex.salle_id AND ex.statut = 'planifié'
GROUP BY l.id, l.nom, l.batiment, l.capacite_examen
HAVING COALESCE(AVG(ex.nb_inscrits), 0) < l.capacite_examen * 0.5
ORDER BY taux_utilisation_pct;

-- Distribution des examens par jour de la semaine
CREATE OR REPLACE VIEW distribution_examens_semaine AS
SELECT 
    TO_CHAR(ex.date_heure, 'Day') as jour_semaine,
    EXTRACT(DOW FROM ex.date_heure) as jour_numero,
    COUNT(ex.id) as nb_examens,
    SUM(ex.nb_inscrits) as total_etudiants,
    COUNT(DISTINCT ex.salle_id) as salles_utilisees
FROM examens ex
WHERE ex.statut = 'planifié'
GROUP BY TO_CHAR(ex.date_heure, 'Day'), EXTRACT(DOW FROM ex.date_heure)
ORDER BY jour_numero;

-- Équité de la charge de surveillance
CREATE OR REPLACE VIEW equite_surveillance AS
SELECT 
    d.nom as departement,
    COUNT(DISTINCT p.id) as nb_professeurs,
    COUNT(s.id) as total_surveillances,
    ROUND(COUNT(s.id)::NUMERIC / NULLIF(COUNT(DISTINCT p.id), 0), 2) as moyenne_par_prof,
    MAX(prof_count.nb_surv) as max_surveillances,
    MIN(prof_count.nb_surv) as min_surveillances,
    MAX(prof_count.nb_surv) - MIN(prof_count.nb_surv) as ecart
FROM departements d
JOIN professeurs p ON d.id = p.dept_id
LEFT JOIN surveillances s ON p.id = s.prof_id
LEFT JOIN (
    SELECT prof_id, COUNT(*) as nb_surv
    FROM surveillances
    GROUP BY prof_id
) prof_count ON p.id = prof_count.prof_id
GROUP BY d.id, d.nom
ORDER BY ecart DESC;
