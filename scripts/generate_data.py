import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import random
from datetime import datetime, timedelta
from src.database import Database

fake = Faker('fr_FR')
db = Database()

def generate_departements():
    print("Génération des départements...")
    departements = [
        ('Informatique', 'INFO', 'Bâtiment A'),
        ('Mathématiques', 'MATH', 'Bâtiment B'),
        ('Physique', 'PHYS', 'Bâtiment C'),
        ('Chimie', 'CHIM', 'Bâtiment D'),
        ('Biologie', 'BIO', 'Bâtiment E'),
        ('Économie', 'ECO', 'Bâtiment F'),
        ('Lettres', 'LETT', 'Bâtiment G')
    ]
    
    query = "INSERT INTO departements (nom, code, batiment) VALUES (%s, %s, %s) RETURNING id"
    dept_ids = []
    for nom, code, batiment in departements:
        result = db.execute_query(query, (nom, code, batiment))
        dept_ids.append(result[0]['id'])
    
    print(f"✅ {len(dept_ids)} départements créés")
    return dept_ids

def generate_salles():
    print("Génération des salles et amphithéâtres...")
    salles = []
    
    batiments = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    for batiment in batiments:
        for i in range(1, 16):
            capacite = random.choice([30, 40, 50, 60])
            salles.append((
                f"Salle {batiment}{i:02d}",
                capacite,
                20,
                'salle',
                f"Bâtiment {batiment}",
                ['tableau', 'projecteur']
            ))
        
        for i in range(1, 4):
            capacite = random.choice([100, 150, 200, 250, 300])
            salles.append((
                f"Amphi {batiment}{i}",
                capacite,
                20,
                'amphitheatre',
                f"Bâtiment {batiment}",
                ['tableau', 'projecteur', 'micro', 'video']
            ))
    
    query = """
        INSERT INTO lieu_examen (nom, capacite, capacite_examen, type, batiment, equipements)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    db.execute_many(query, salles)
    
    print(f"✅ {len(salles)} salles créées")
    return len(salles)

def generate_formations(dept_ids):
    print("Génération des formations...")
    formations = []
    
    specialites = {
        'Informatique': ['Génie Logiciel', 'Réseaux et Sécurité', 'Intelligence Artificielle', 'Systèmes Embarqués'],
        'Mathématiques': ['Mathématiques Appliquées', 'Mathématiques Fondamentales', 'Statistiques'],
        'Physique': ['Physique Théorique', 'Physique Appliquée', 'Astrophysique'],
        'Chimie': ['Chimie Organique', 'Chimie Analytique', 'Chimie Industrielle'],
        'Biologie': ['Biologie Moléculaire', 'Écologie', 'Biotechnologie'],
        'Économie': ['Économie et Gestion', 'Finance', 'Management'],
        'Lettres': ['Littérature Française', 'Langues Étrangères', 'Sciences Humaines']
    }
    
    niveaux = ['L1', 'L2', 'L3', 'M1', 'M2']
    
    formation_ids = []
    counter = 1
    for dept_id in dept_ids:
        dept_info = db.execute_query("SELECT nom FROM departements WHERE id = %s", (dept_id,))[0]
        dept_nom = dept_info['nom']
        
        for spec in specialites.get(dept_nom, ['Général']):
            for niveau in niveaux:
                code = f"{dept_nom[:4].upper()}-{spec[:3].upper()}-{niveau}-{counter:03d}"
                nom = f"{niveau} {spec}"
                nb_modules = random.randint(8, 12)
                
                query = """
                    INSERT INTO formations (nom, code, dept_id, niveau, nb_modules)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """
                result = db.execute_query(query, (nom, code, dept_id, niveau, nb_modules))
                formation_ids.append(result[0]['id'])
                counter += 1
    
    print(f"✅ {len(formation_ids)} formations créées")
    return formation_ids

def generate_professeurs(dept_ids):
    print("Génération des professeurs...")
    professeurs = []
    grades = ['Professeur', 'Maitre de conférences', 'Assistant', 'Vacataire']
    
    for dept_id in dept_ids:
        nb_profs = random.randint(15, 25)
        for _ in range(nb_profs):
            nom = fake.last_name()
            prenom = fake.first_name()
            email = f"{prenom.lower()}.{nom.lower()}@university.edu"
            grade = random.choice(grades)
            specialite = fake.job()
            
            professeurs.append((nom, prenom, email, dept_id, specialite, grade))
    
    query = """
        INSERT INTO professeurs (nom, prenom, email, dept_id, specialite, grade)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    db.execute_many(query, professeurs)
    
    print(f"✅ {len(professeurs)} professeurs créés")
    return len(professeurs)

def generate_etudiants(formation_ids):
    print("Génération des étudiants (13,000+)...")
    etudiants = []
    promos = [2023, 2024, 2025]
    
    students_per_formation = 13000 // len(formation_ids)
    
    for formation_id in formation_ids:
        nb_etudiants = random.randint(students_per_formation - 20, students_per_formation + 20)
        for _ in range(nb_etudiants):
            nom = fake.last_name()
            prenom = fake.first_name()
            email = f"{prenom.lower()}.{nom.lower()}{random.randint(1, 999)}@student.university.edu"
            promo = random.choice(promos)
            
            etudiants.append((nom, prenom, email, formation_id, promo))
    
    query = """
        INSERT INTO etudiants (nom, prenom, email, formation_id, promo)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    batch_size = 1000
    for i in range(0, len(etudiants), batch_size):
        batch = etudiants[i:i + batch_size]
        db.execute_many(query, batch)
        print(f"  Batch {i//batch_size + 1}: {len(batch)} étudiants insérés")
    
    print(f"✅ {len(etudiants)} étudiants créés")
    return len(etudiants)

def generate_modules(formation_ids):
    print("Génération des modules...")
    modules = []
    
    module_names = [
        'Algorithmique', 'Structures de données', 'Bases de données', 'Réseaux',
        'Systèmes d\'exploitation', 'Programmation orientée objet', 'Web développement',
        'Intelligence artificielle', 'Machine Learning', 'Sécurité informatique',
        'Analyse mathématique', 'Algèbre linéaire', 'Probabilités', 'Statistiques',
        'Physique quantique', 'Thermodynamique', 'Électromagnétisme', 'Mécanique',
        'Chimie organique', 'Chimie analytique', 'Biochimie', 'Génétique',
        'Microéconomie', 'Macroéconomie', 'Finance', 'Marketing', 'Management'
    ]
    
    module_ids = []
    for formation_id in formation_ids:
        nb_modules = random.randint(8, 12)
        for i in range(nb_modules):
            nom = random.choice(module_names) + f" {i+1}"
            code = f"MOD-{formation_id}-{i+1:03d}"
            credits = random.choice([3, 4, 5, 6])
            semestre = random.choice([1, 2])
            duree_examen = random.choice([90, 120, 150, 180])
            
            query = """
                INSERT INTO modules (nom, code, credits, formation_id, semestre, duree_examen)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
            result = db.execute_query(query, (nom, code, credits, formation_id, semestre, duree_examen))
            module_ids.append(result[0]['id'])
    
    print(f"✅ {len(module_ids)} modules créés")
    return module_ids

def generate_inscriptions(module_ids):
    print("Génération des inscriptions (130,000+)...")
    
    etudiants = db.execute_query("SELECT id, formation_id FROM etudiants")
    
    inscriptions = []
    annee = "2024-2025"
    
    for etudiant in etudiants:
        formation_modules = db.execute_query(
            "SELECT id FROM modules WHERE formation_id = %s",
            (etudiant['formation_id'],)
        )
        
        nb_modules = random.randint(6, len(formation_modules))
        selected_modules = random.sample(formation_modules, min(nb_modules, len(formation_modules)))
        
        for module in selected_modules:
            inscriptions.append((etudiant['id'], module['id'], annee, 'inscrit'))
    
    query = """
        INSERT INTO inscriptions (etudiant_id, module_id, annee_universitaire, statut)
        VALUES (%s, %s, %s, %s)
    """
    
    batch_size = 5000
    for i in range(0, len(inscriptions), batch_size):
        batch = inscriptions[i:i + batch_size]
        db.execute_many(query, batch)
        print(f"  Batch {i//batch_size + 1}: {len(batch)} inscriptions insérées")
    
    print(f"✅ {len(inscriptions)} inscriptions créées")
    return len(inscriptions)

def generate_periode_examen():
    print("Génération de la période d'examen...")
    
    date_debut = datetime(2025, 1, 20).date()
    date_fin = datetime(2025, 2, 15).date()
    
    query = """
        INSERT INTO periodes_examen (nom, date_debut, date_fin, session, annee_universitaire, actif)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    """
    result = db.execute_query(query, (
        'Session Normale Janvier 2025',
        date_debut,
        date_fin,
        'normale',
        '2024-2025',
        True
    ))
    
    periode_id = result[0]['id']
    print(f"✅ Période d'examen créée (ID: {periode_id})")
    return periode_id

def main():
    print("=" * 60)
    print("GÉNÉRATION DES DONNÉES DE TEST")
    print("=" * 60)
    
    try:
        dept_ids = generate_departements()
        generate_salles()
        formation_ids = generate_formations(dept_ids)
        generate_professeurs(dept_ids)
        generate_etudiants(formation_ids)
        module_ids = generate_modules(formation_ids)
        generate_inscriptions(module_ids)
        generate_periode_examen()
        
        print("\n" + "=" * 60)
        print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        
        kpis = db.get_kpi_global()
        print("\n📊 Statistiques finales:")
        print(f"  - Départements: {kpis['total_departements']}")
        print(f"  - Formations: {kpis['total_formations']}")
        print(f"  - Étudiants: {kpis['total_etudiants']}")
        print(f"  - Professeurs: {kpis['total_professeurs']}")
        print(f"  - Modules: {kpis['total_modules']}")
        print(f"  - Inscriptions: {kpis['total_inscriptions']}")
        print(f"  - Salles: {kpis['total_salles']}")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
