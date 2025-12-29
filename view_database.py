#!/usr/bin/env python3
"""
Simple database viewer for the exam scheduling system
"""
import sys
from src.database import Database
import pandas as pd

def main():
    db = Database()
    
    print("\n" + "="*60)
    print("DATABASE OVERVIEW - Exam Scheduling System")
    print("="*60 + "\n")
    
    # Get counts
    tables = {
        'Étudiants': 'SELECT COUNT(*) as count FROM etudiants',
        'Professeurs': 'SELECT COUNT(*) as count FROM professeurs',
        'Modules': 'SELECT COUNT(*) as count FROM modules',
        'Formations': 'SELECT COUNT(*) as count FROM formations',
        'Départements': 'SELECT COUNT(*) as count FROM departements',
        'Salles': 'SELECT COUNT(*) as count FROM lieu_examen',
        'Examens': 'SELECT COUNT(*) as count FROM examens',
        'Inscriptions': 'SELECT COUNT(*) as count FROM inscriptions',
        'Surveillances': 'SELECT COUNT(*) as count FROM surveillances',
        'Périodes': 'SELECT COUNT(*) as count FROM periodes_examen'
    }
    
    print("TABLE COUNTS:")
    print("-" * 40)
    for table, query in tables.items():
        result = db.execute_query(query)
        count = result[0]['count'] if result else 0
        print(f"{table:.<30} {count:>8,}")
    
    print("\n" + "="*60)
    print("SAMPLE DATA")
    print("="*60 + "\n")
    
    # Show sample students
    print("\nSample Students (first 5):")
    students = db.execute_query("""
        SELECT e.nom, e.prenom, f.nom as formation, d.nom as departement
        FROM etudiants e
        JOIN formations f ON e.formation_id = f.id
        JOIN departements d ON f.dept_id = d.id
        LIMIT 5
    """)
    df = pd.DataFrame(students)
    print(df.to_string(index=False))
    
    # Show sample professors
    print("\n\nSample Professors (first 5):")
    profs = db.execute_query("""
        SELECT p.nom, p.prenom, p.grade, d.nom as departement
        FROM professeurs p
        JOIN departements d ON p.dept_id = d.id
        LIMIT 5
    """)
    df = pd.DataFrame(profs)
    print(df.to_string(index=False))
    
    # Show departments
    print("\n\nDepartments:")
    depts = db.execute_query("""
        SELECT nom, code, 
               (SELECT COUNT(*) FROM formations WHERE dept_id = d.id) as formations,
               (SELECT COUNT(*) FROM professeurs WHERE dept_id = d.id) as professeurs
        FROM departements d
        ORDER BY nom
    """)
    df = pd.DataFrame(depts)
    print(df.to_string(index=False))
    
    # Show exam periods
    print("\n\nExam Periods:")
    periods = db.execute_query("""
        SELECT nom, date_debut, date_fin, annee_universitaire, actif
        FROM periodes_examen
        ORDER BY date_debut DESC
    """)
    df = pd.DataFrame(periods)
    print(df.to_string(index=False))
    
    # Show recent exams
    print("\n\nRecent Exams (first 10):")
    exams = db.execute_query("""
        SELECT 
            m.nom as module,
            ex.date_heure,
            l.nom as salle,
            ex.nb_inscrits as etudiants,
            ex.statut
        FROM examens ex
        JOIN modules m ON ex.module_id = m.id
        JOIN lieu_examen l ON ex.salle_id = l.id
        ORDER BY ex.date_heure
        LIMIT 10
    """)
    df = pd.DataFrame(exams)
    print(df.to_string(index=False))
    
    print("\n" + "="*60)
    print("\nTo explore more, use:")
    print("  - pgAdmin: brew install --cask pgadmin4")
    print("  - DBeaver: brew install --cask dbeaver-community")
    print("  - psql: psql -h localhost -U postgres -d exam_scheduling")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
