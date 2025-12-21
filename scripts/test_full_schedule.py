import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.scheduler import ExamScheduler
from src.constraints import ConstraintChecker
import time

def test_full_schedule_generation():
    print("\n" + "="*60)
    print("FULL SCHEDULE GENERATION TEST")
    print("="*60)
    
    db = Database()
    scheduler = ExamScheduler(db)
    checker = ConstraintChecker(db)
    
    periodes = db.get_periodes_examen(actif=True)
    if not periodes:
        print("❌ No active exam period found")
        return False
    
    periode = periodes[0]
    periode_id = periode['id']
    
    print(f"\n📅 Période: {periode['nom']}")
    print(f"📆 Dates: {periode['date_debut']} → {periode['date_fin']}")
    
    kpis = db.get_kpi_global()
    print(f"\n📊 Données disponibles:")
    print(f"  - Étudiants: {kpis['total_etudiants']:,}")
    print(f"  - Modules: {kpis['total_modules']:,}")
    print(f"  - Inscriptions: {kpis['total_inscriptions']:,}")
    print(f"  - Salles: {kpis['total_salles']}")
    print(f"  - Professeurs: {kpis['total_professeurs']}")
    
    print("\n🚀 Lancement de la génération complète...")
    print("⏱️  Objectif: < 45 secondes")
    print("-" * 60)
    
    start_time = time.time()
    success, result = scheduler.generate_schedule(periode_id, "2024-2025")
    end_time = time.time()
    
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print(f"⏱️  TEMPS D'EXÉCUTION: {duration:.2f} secondes")
    print("="*60)
    
    if duration < 45:
        print(f"✅ OBJECTIF ATTEINT! ({duration:.2f}s < 45s)")
    else:
        print(f"❌ OBJECTIF NON ATTEINT ({duration:.2f}s > 45s)")
    
    if success:
        print(f"\n📊 Résultats de la génération:")
        print(f"  ✅ Examens planifiés: {result['scheduled']}")
        print(f"  ❌ Modules non planifiés: {result['failed']}")
        
        total_modules = result['scheduled'] + result['failed']
        success_rate = (result['scheduled'] / total_modules * 100) if total_modules > 0 else 0
        print(f"  📈 Taux de succès: {success_rate:.1f}%")
        
        print(f"\n🔍 Conflits détectés:")
        conflicts = result['conflicts']
        print(f"  - Étudiants: {len(conflicts['etudiants'])}")
        print(f"  - Professeurs: {len(conflicts['professeurs'])}")
        print(f"  - Capacité: {len(conflicts['capacite'])}")
        print(f"  - Salles: {len(conflicts['salles'])}")
        print(f"  - TOTAL: {result['total_conflicts']}")
        
        if result['failed'] > 0 and result['failed'] <= 10:
            print(f"\n⚠️  Modules non planifiés:")
            for module in result['failed_modules']:
                print(f"    - {module['module']} ({module['nb_inscrits']} étudiants)")
        
        examens = db.get_examens(periode_id)
        print(f"\n📋 Vérification base de données:")
        print(f"  - Examens en DB: {len(examens)}")
        
        surveillances = db.execute_query("SELECT COUNT(*) as count FROM surveillances")[0]['count']
        print(f"  - Surveillances en DB: {surveillances}")
        
        if result['scheduled'] > 0:
            print("\n✅ TEST RÉUSSI - Planning généré avec succès!")
            return True
        else:
            print("\n⚠️  Aucun examen planifié - Vérifier les contraintes")
            return False
    else:
        print(f"\n❌ Erreur: {result.get('error', 'Erreur inconnue')}")
        return False

if __name__ == "__main__":
    test_full_schedule_generation()
