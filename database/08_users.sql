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
