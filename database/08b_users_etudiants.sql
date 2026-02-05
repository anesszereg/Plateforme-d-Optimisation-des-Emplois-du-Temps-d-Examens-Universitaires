-- Utilisateurs Etudiants (requires etudiants table to be populated first)
-- Import this AFTER all 05_etudiants_part_*.sql files

-- Etudiants (password: etude123)
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('valentine.dupont.1@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 1);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('aurélie.carlier.2@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 2);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('margaud.bourgeois.3@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 3);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('benjamin.samson.4@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 4);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('patrick.boyer.5@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 5);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('marcel.gaudin.6@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 6);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('christelle.duhamel.7@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 7);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('claudine.weber.8@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 8);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('noël.ledoux.9@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 9);
INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('laetitia.lopes.10@student.university.edu', '5bf50c2a7c349e9ca4b33dc1abedcbd1922f14f95525f34787fc474e560a7b59', 'etudiant', 10);
