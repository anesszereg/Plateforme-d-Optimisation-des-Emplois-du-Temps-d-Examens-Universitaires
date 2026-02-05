"""
Generate SQL INSERT files for direct Supabase import
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import random
from datetime import datetime

fake = Faker('fr_FR')

def escape_sql(s):
    """Escape single quotes for SQL"""
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def generate_sql_files():
    output_dir = os.path.dirname(__file__)
    
    # 1. Departements
    print("Generating departements...")
    departements = [
        ('Informatique', 'INFO', 'Bâtiment A'),
        ('Mathématiques', 'MATH', 'Bâtiment B'),
        ('Physique', 'PHYS', 'Bâtiment C'),
        ('Chimie', 'CHIM', 'Bâtiment D'),
        ('Biologie', 'BIO', 'Bâtiment E'),
        ('Économie', 'ECO', 'Bâtiment F'),
        ('Lettres', 'LETT', 'Bâtiment G')
    ]
    
    with open(os.path.join(output_dir, '01_departements.sql'), 'w') as f:
        f.write("-- Departements\n")
        for nom, code, batiment in departements:
            f.write(f"INSERT INTO departements (nom, code, batiment) VALUES ({escape_sql(nom)}, {escape_sql(code)}, {escape_sql(batiment)});\n")
    
    # 2. Salles
    print("Generating salles...")
    with open(os.path.join(output_dir, '02_salles.sql'), 'w') as f:
        f.write("-- Salles et Amphitheatres\n")
        batiments = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for batiment in batiments:
            for i in range(1, 16):
                capacite = random.choice([30, 40, 50, 60])
                f.write(f"INSERT INTO lieu_examen (nom, capacite, capacite_examen, type, batiment, equipements) VALUES ('Salle {batiment}{i:02d}', {capacite}, 20, 'salle', 'Bâtiment {batiment}', ARRAY['tableau', 'projecteur']);\n")
            for i in range(1, 4):
                capacite = random.choice([100, 150, 200, 250, 300])
                f.write(f"INSERT INTO lieu_examen (nom, capacite, capacite_examen, type, batiment, equipements) VALUES ('Amphi {batiment}{i}', {capacite}, 20, 'amphitheatre', 'Bâtiment {batiment}', ARRAY['tableau', 'projecteur', 'micro', 'video']);\n")
    
    # 3. Formations
    print("Generating formations...")
    specialites = {
        1: ['Génie Logiciel', 'Réseaux et Sécurité', 'Intelligence Artificielle', 'Systèmes Embarqués'],
        2: ['Mathématiques Appliquées', 'Mathématiques Fondamentales', 'Statistiques'],
        3: ['Physique Théorique', 'Physique Appliquée', 'Astrophysique'],
        4: ['Chimie Organique', 'Chimie Analytique', 'Chimie Industrielle'],
        5: ['Biologie Moléculaire', 'Écologie', 'Biotechnologie'],
        6: ['Économie et Gestion', 'Finance', 'Management'],
        7: ['Littérature Française', 'Langues Étrangères', 'Sciences Humaines']
    }
    niveaux = ['L1', 'L2', 'L3', 'M1', 'M2']
    
    formation_id = 0
    formations_list = []
    with open(os.path.join(output_dir, '03_formations.sql'), 'w') as f:
        f.write("-- Formations\n")
        for dept_id in range(1, 8):
            for spec in specialites[dept_id]:
                for niveau in niveaux:
                    formation_id += 1
                    code = f"FORM-{formation_id:03d}"
                    nom = f"{niveau} {spec}"
                    nb_modules = random.randint(8, 12)
                    formations_list.append((formation_id, dept_id))
                    f.write(f"INSERT INTO formations (nom, code, dept_id, niveau, nb_modules) VALUES ({escape_sql(nom)}, {escape_sql(code)}, {dept_id}, {escape_sql(niveau)}, {nb_modules});\n")
    
    # 4. Professeurs
    print("Generating professeurs...")
    grades = ['Professeur', 'Maitre de conférences', 'Assistant', 'Vacataire']
    prof_id = 0
    with open(os.path.join(output_dir, '04_professeurs.sql'), 'w') as f:
        f.write("-- Professeurs\n")
        for dept_id in range(1, 8):
            nb_profs = random.randint(15, 25)
            for _ in range(nb_profs):
                prof_id += 1
                nom = fake.last_name()
                prenom = fake.first_name()
                email = f"{prenom.lower()}.{nom.lower()}.{prof_id}@university.edu"
                grade = random.choice(grades)
                specialite = fake.job()[:100]
                f.write(f"INSERT INTO professeurs (nom, prenom, email, dept_id, specialite, grade) VALUES ({escape_sql(nom)}, {escape_sql(prenom)}, {escape_sql(email)}, {dept_id}, {escape_sql(specialite)}, {escape_sql(grade)});\n")
    
    # 5. Etudiants (13,000+ students)
    print("Generating etudiants (13,000+)...")
    promos = [2023, 2024, 2025]
    student_id = 0
    with open(os.path.join(output_dir, '05_etudiants.sql'), 'w') as f:
        f.write("-- Etudiants\n")
        for formation_id in range(1, formation_id + 1):
            nb_etudiants = 120  # 120 per formation = ~13,200 total
            for _ in range(nb_etudiants):
                student_id += 1
                nom = fake.last_name()
                prenom = fake.first_name()
                email = f"{prenom.lower()}.{nom.lower()}.{student_id}@student.university.edu"
                promo = random.choice(promos)
                f.write(f"INSERT INTO etudiants (nom, prenom, email, formation_id, promo) VALUES ({escape_sql(nom)}, {escape_sql(prenom)}, {escape_sql(email)}, {formation_id}, {promo});\n")
    
    # 6. Modules
    print("Generating modules...")
    module_names = [
        'Algorithmique', 'Structures de données', 'Bases de données', 'Réseaux',
        'Programmation', 'Intelligence artificielle', 'Machine Learning',
        'Analyse', 'Algèbre', 'Probabilités', 'Statistiques',
        'Physique', 'Thermodynamique', 'Mécanique', 'Chimie', 'Biologie'
    ]
    module_id = 0
    with open(os.path.join(output_dir, '06_modules.sql'), 'w') as f:
        f.write("-- Modules\n")
        for formation_id in range(1, len(formations_list) + 1):
            nb_modules = random.randint(8, 12)
            for i in range(nb_modules):
                module_id += 1
                nom = random.choice(module_names) + f" {i+1}"
                code = f"MOD-{module_id:04d}"
                credits = random.choice([3, 4, 5, 6])
                semestre = random.choice([1, 2])
                duree = random.choice([90, 120, 150, 180])
                f.write(f"INSERT INTO modules (nom, code, credits, formation_id, semestre, duree_examen) VALUES ({escape_sql(nom)}, {escape_sql(code)}, {credits}, {formation_id}, {semestre}, {duree});\n")
    
    # 7. Periode examen
    print("Generating periode examen...")
    with open(os.path.join(output_dir, '07_periode.sql'), 'w') as f:
        f.write("-- Periode Examen\n")
        f.write("INSERT INTO periodes_examen (nom, date_debut, date_fin, session, annee_universitaire, actif) VALUES ('Session Normale Janvier 2025', '2025-01-20', '2025-02-15', 'normale', '2024-2025', true);\n")
    
    # 8. Users with hashed passwords (SHA-256)
    import hashlib
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    print("Generating users with hashed passwords...")
    with open(os.path.join(output_dir, '08_users.sql'), 'w') as f:
        f.write("-- Utilisateurs (passwords are SHA-256 hashed)\n")
        f.write("-- Plain text passwords listed in comments for reference\n\n")
        
        # Vice-Doyen
        pwd = 'admin123'
        f.write(f"-- vice.doyen@univ.dz / {pwd}\n")
        f.write(f"INSERT INTO utilisateurs (username, password_hash, role) VALUES ('vice.doyen@univ.dz', '{hash_password(pwd)}', 'vice_doyen');\n\n")
        
        # Admin Examens
        pwd = 'admin123'
        f.write(f"-- admin.examens@univ.dz / {pwd}\n")
        f.write(f"INSERT INTO utilisateurs (username, password_hash, role) VALUES ('admin.examens@univ.dz', '{hash_password(pwd)}', 'admin_examens');\n\n")
        
        # Chefs departement
        codes = ['info', 'math', 'phys', 'chim', 'bio', 'eco', 'lett']
        f.write("-- Chefs de Departement\n")
        for i, code in enumerate(codes):
            pwd = 'chef123'
            f.write(f"-- chef.{code}@univ.dz / {pwd}\n")
            f.write(f"INSERT INTO utilisateurs (username, password_hash, role, professeur_id, departement_id) VALUES ('chef.{code}@univ.dz', '{hash_password(pwd)}', 'chef_departement', {i+1}, {i+1});\n")
        
        # Professeurs (first 10 as examples)
        f.write("\n-- Professeurs\n")
        for prof_id in range(1, 11):
            pwd = 'prof123'
            f.write(f"-- prof{prof_id}@university.edu / {pwd}\n")
            f.write(f"INSERT INTO utilisateurs (username, password_hash, role, professeur_id) VALUES ('prof{prof_id}@university.edu', '{hash_password(pwd)}', 'professeur', {prof_id});\n")
        
        # Etudiants (first 10 as examples)
        f.write("\n-- Etudiants\n")
        for etu_id in range(1, 11):
            pwd = 'etudiant123'
            f.write(f"-- etudiant{etu_id}@student.university.edu / {pwd}\n")
            f.write(f"INSERT INTO utilisateurs (username, password_hash, role, etudiant_id) VALUES ('etudiant{etu_id}@student.university.edu', '{hash_password(pwd)}', 'etudiant', {etu_id});\n")
    
    print("\n✅ SQL files generated in database/ folder:")
    print("  - 01_departements.sql")
    print("  - 02_salles.sql")
    print("  - 03_formations.sql")
    print("  - 04_professeurs.sql")
    print("  - 05_etudiants.sql")
    print("  - 06_modules.sql")
    print("  - 07_periode.sql")
    print("  - 08_users.sql")
    print("\nImport in Supabase SQL Editor in order (01 to 08)")

if __name__ == "__main__":
    generate_sql_files()
