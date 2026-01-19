"""
Script to generate user accounts from existing data
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.auth import Auth

def generate_all_users():
    db = Database()
    auth = Auth(db)
    
    print("=" * 60)
    print("GÉNÉRATION DES COMPTES UTILISATEURS")
    print("=" * 60)
    
    credentials = []
    
    # 1. Vice-Doyen
    print("\n📌 Création du compte Vice-Doyen...")
    pwd = Auth.generate_password(12)
    if auth.create_user("vice.doyen@univ.dz", pwd, "vice_doyen"):
        credentials.append(("Vice-Doyen", "vice.doyen@univ.dz", pwd))
        print("   ✅ Compte créé")
    
    # 2. Admin Examens
    print("\n📌 Création du compte Admin Examens...")
    pwd = Auth.generate_password(12)
    if auth.create_user("admin.examens@univ.dz", pwd, "admin_examens"):
        credentials.append(("Admin Examens", "admin.examens@univ.dz", pwd))
        print("   ✅ Compte créé")
    
    # 3. Chefs de Département
    print("\n📌 Création des comptes Chefs de Département...")
    departements = db.get_departements()
    
    for dept in departements:
        profs = db.get_professeurs(dept['id'])
        if profs:
            chef = profs[0]
            pwd = Auth.generate_professor_password(chef['nom'], chef['prenom'])
            username = f"chef.{dept['code'].lower()}@univ.dz"
            
            if auth.create_user(username, pwd, "chef_departement", 
                              professeur_id=chef['id'], departement_id=dept['id']):
                credentials.append((f"Chef {dept['nom']}", username, pwd))
                print(f"   ✅ Chef {dept['nom']}: {chef['prenom']} {chef['nom']}")
    
    # 4. Professeurs
    print("\n📌 Création des comptes Professeurs...")
    all_profs = db.execute_query("SELECT * FROM professeurs ORDER BY id")
    prof_count = 0
    sample_profs = []
    
    for prof in all_profs:
        email = prof['email'] or f"{prof['prenom'].lower()}.{prof['nom'].lower()}@univ.dz"
        pwd = Auth.generate_professor_password(prof['nom'], prof['prenom'])
        
        if auth.create_user(email, pwd, "professeur", professeur_id=prof['id']):
            prof_count += 1
            if len(sample_profs) < 3:
                sample_profs.append((f"{prof['prenom']} {prof['nom']}", email, pwd))
    
    print(f"   ✅ {prof_count} comptes professeurs créés")
    
    # 5. Étudiants
    print("\n📌 Création des comptes Étudiants...")
    all_students = db.execute_query("SELECT * FROM etudiants ORDER BY id LIMIT 1000")
    student_count = 0
    sample_students = []
    
    for etu in all_students:
        email = etu['email'] or f"{etu['prenom'].lower()}.{etu['nom'].lower()}@etu.univ.dz"
        pwd = Auth.generate_student_password(etu['nom'], etu['prenom'], etu['promo'])
        
        if auth.create_user(email, pwd, "etudiant", etudiant_id=etu['id']):
            student_count += 1
            if len(sample_students) < 3:
                sample_students.append((f"{etu['prenom']} {etu['nom']}", email, pwd))
    
    print(f"   ✅ {student_count} comptes étudiants créés")
    
    # Summary
    print("\n" + "=" * 60)
    print("IDENTIFIANTS DE CONNEXION")
    print("=" * 60)
    
    print("\n🔐 ADMINISTRATEURS:")
    for role, user, pwd in credentials:
        print(f"   {role}: {user} / {pwd}")
    
    print("\n👨‍🏫 PROFESSEURS (exemples):")
    for name, user, pwd in sample_profs:
        print(f"   {name}: {user} / {pwd}")
    
    print("\n👨‍🎓 ÉTUDIANTS (exemples):")
    print("   Format: Nom + Prénom + Promo (ex: DupontJean2024)")
    for name, user, pwd in sample_students:
        print(f"   {name}: {user} / {pwd}")
    
    # Save to file
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CREDENTIALS.txt'), 'w') as f:
        f.write("IDENTIFIANTS DE CONNEXION\n")
        f.write("=" * 50 + "\n\n")
        f.write("ADMINISTRATEURS:\n")
        for role, user, pwd in credentials:
            f.write(f"  {role}: {user} / {pwd}\n")
        f.write("\nPROFESSEURS (exemples):\n")
        for name, user, pwd in sample_profs:
            f.write(f"  {name}: {user} / {pwd}\n")
        f.write("\nÉTUDIANTS (exemples):\n")
        for name, user, pwd in sample_students:
            f.write(f"  {name}: {user} / {pwd}\n")
    
    print("\n📁 Identifiants sauvegardés dans CREDENTIALS.txt")

if __name__ == "__main__":
    generate_all_users()
