-- Utilisateurs (passwords are SHA-256 hashed)
-- Plain text passwords listed in comments for reference

-- vice.doyen@univ.dz / admin123
INSERT INTO utilisateurs (username, password_hash, role) VALUES ('vice.doyen@univ.dz', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'vice_doyen');

-- admin.examens@univ.dz / admin123
INSERT INTO utilisateurs (username, password_hash, role) VALUES ('admin.examens@univ.dz', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin_examens');

-- Chefs de Departement
-- chef.info@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.info@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 1, 1);
-- chef.math@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.math@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 2, 2);
-- chef.phys@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.phys@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 3, 3);
-- chef.chim@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.chim@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 4, 4);
-- chef.bio@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.bio@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 5, 5);
-- chef.eco@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.eco@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 6, 6);
-- chef.lett@univ.dz / chef123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.lett@univ.dz', 'fa0990ab6f2ecfd562611cedad67152e8c1117f91c22d15094d1e242314243af', 'chef_departement', 7, 7);

-- Professeurs
-- prof1@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof1@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 1);
-- prof2@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof2@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 2);
-- prof3@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof3@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 3);
-- prof4@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof4@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 4);
-- prof5@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof5@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 5);
-- prof6@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof6@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 6);
-- prof7@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof7@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 7);
-- prof8@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof8@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 8);
-- prof9@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof9@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 9);
-- prof10@university.edu / prof123
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof10@university.edu', '00624b02e1f9b996a3278f559d5d55313552ad2c0bafc82adfd975c12df61eaf', 'professeur', 10);

-- Etudiants
-- etudiant1@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant1@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 1);
-- etudiant2@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant2@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 2);
-- etudiant3@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant3@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 3);
-- etudiant4@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant4@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 4);
-- etudiant5@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant5@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 5);
-- etudiant6@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant6@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 6);
-- etudiant7@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant7@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 7);
-- etudiant8@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant8@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 8);
-- etudiant9@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant9@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 9);
-- etudiant10@student.university.edu / etudiant123
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant10@student.university.edu', '36432aa0a54a06c13ca2ff16cef78ca66e1cd5fa869f36791a79bc4f4c5d8120', 'etudiant', 10);
