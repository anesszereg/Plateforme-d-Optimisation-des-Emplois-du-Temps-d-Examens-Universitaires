-- Utilisateurs
INSERT INTO utilisateurs (username, password_hash, role) VALUES ('vice.doyen@univ.dz', 'ViceDoyen2024!', 'vice_doyen');
INSERT INTO utilisateurs (username, password_hash, role) VALUES ('admin.examens@univ.dz', 'AdminExam2024!', 'admin_examens');
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.info@univ.dz', 'ChefInfo2024!', 'chef_departement', 1, 1);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.math@univ.dz', 'ChefMath2024!', 'chef_departement', 2, 2);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.phys@univ.dz', 'ChefPhys2024!', 'chef_departement', 3, 3);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.chim@univ.dz', 'ChefChim2024!', 'chef_departement', 4, 4);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.bio@univ.dz', 'ChefBio2024!', 'chef_departement', 5, 5);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.eco@univ.dz', 'ChefEco2024!', 'chef_departement', 6, 6);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.lett@univ.dz', 'ChefLett2024!', 'chef_departement', 7, 7);

-- Professeurs
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof1@university.edu', 'Prof1Pass2024!', 'professeur', 1);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof2@university.edu', 'Prof2Pass2024!', 'professeur', 2);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof3@university.edu', 'Prof3Pass2024!', 'professeur', 3);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof4@university.edu', 'Prof4Pass2024!', 'professeur', 4);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof5@university.edu', 'Prof5Pass2024!', 'professeur', 5);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof6@university.edu', 'Prof6Pass2024!', 'professeur', 6);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof7@university.edu', 'Prof7Pass2024!', 'professeur', 7);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof8@university.edu', 'Prof8Pass2024!', 'professeur', 8);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof9@university.edu', 'Prof9Pass2024!', 'professeur', 9);
INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof10@university.edu', 'Prof10Pass2024!', 'professeur', 10);

-- Etudiants
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant1@student.university.edu', 'Etudiant1Pass2024!', 'etudiant', 1);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant2@student.university.edu', 'Etudiant2Pass2024!', 'etudiant', 2);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant3@student.university.edu', 'Etudiant3Pass2024!', 'etudiant', 3);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant4@student.university.edu', 'Etudiant4Pass2024!', 'etudiant', 4);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant5@student.university.edu', 'Etudiant5Pass2024!', 'etudiant', 5);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant6@student.university.edu', 'Etudiant6Pass2024!', 'etudiant', 6);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant7@student.university.edu', 'Etudiant7Pass2024!', 'etudiant', 7);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant8@student.university.edu', 'Etudiant8Pass2024!', 'etudiant', 8);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant9@student.university.edu', 'Etudiant9Pass2024!', 'etudiant', 9);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant10@student.university.edu', 'Etudiant10Pass2024!', 'etudiant', 10);
