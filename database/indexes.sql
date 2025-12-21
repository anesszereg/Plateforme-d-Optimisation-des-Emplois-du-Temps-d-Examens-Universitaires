-- Optimisations et Index Avancés
-- Pour améliorer les performances des requêtes complexes

-- Index partiels pour les examens actifs
CREATE INDEX idx_examens_planifies ON examens(date_heure, salle_id) 
WHERE statut = 'planifié';

-- Index pour les inscriptions actives
CREATE INDEX idx_inscriptions_actives ON inscriptions(etudiant_id, module_id) 
WHERE statut = 'inscrit';

-- Index GIN pour recherche dans les équipements
CREATE INDEX idx_lieu_equipements ON lieu_examen USING GIN(equipements);

-- Index pour améliorer les jointures fréquentes
CREATE INDEX idx_modules_formation_semestre ON modules(formation_id, semestre);
CREATE INDEX idx_examens_periode_date ON examens(periode_id, date_heure);

-- Statistiques pour l'optimiseur
ANALYZE departements;
ANALYZE formations;
ANALYZE etudiants;
ANALYZE professeurs;
ANALYZE modules;
ANALYZE inscriptions;
ANALYZE examens;
ANALYZE surveillances;
ANALYZE lieu_examen;
