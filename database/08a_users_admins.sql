-- Utilisateurs Admins et Chefs (no foreign key to etudiants)
-- Import this AFTER professeurs but BEFORE or WITHOUT etudiants

-- vice.doyen@univ.dz / admin123
INSERT INTO utilisateurs (username, password_hash, role) VALUES ('vice.doyen@univ.dz', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'vice_doyen');

-- admin.examens@univ.dz / admin123
INSERT INTO utilisateurs (username, password_hash, role) VALUES ('admin.examens@univ.dz', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin_examens');

-- Chefs de Departement (chef123)
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.info@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 1, 1);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.math@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 2, 2);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.phys@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 3, 3);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.chim@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 4, 4);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.bio@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 5, 5);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.eco@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 6, 6);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.lett@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 7, 7);

-- Professeurs (prof123)
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof1@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 1);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof2@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 2);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof3@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 3);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof4@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 4);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof5@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 5);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof6@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 6);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof7@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 7);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof8@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 8);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof9@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 9);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof10@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 10);
