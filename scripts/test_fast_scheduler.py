import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.fast_scheduler import FastScheduler
import time

def test_fast_scheduler():
    print("\n" + "="*60)
    print("FAST SCHEDULER PERFORMANCE TEST")
    print("Target: < 10 seconds")
    print("="*60)
    
    db = Database()
    scheduler = FastScheduler(db)
    
    # Get active period
    periodes = db.get_periodes_examen(actif=True)
    if not periodes:
        print("❌ No active exam period found")
        return
    
    periode = periodes[0]
    periode_id = periode['id']
    
    print(f"\n📅 Période: {periode['nom']}")
    print(f"📆 Dates: {periode['date_debut']} → {periode['date_fin']}")
    
    # Get data stats
    kpis = db.get_kpi_global()
    print(f"\n📊 Données:")
    print(f"  - Étudiants: {kpis['total_etudiants']:,}")
    print(f"  - Modules: {kpis['total_modules']:,}")
    print(f"  - Inscriptions: {kpis['total_inscriptions']:,}")
    print(f"  - Salles: {kpis['total_salles']}")
    
    print("\n🚀 Lancement de la génération ULTRA-RAPIDE...")
    print("⏱️  Objectif: < 10 secondes")
    print("-" * 60)
    
    start_time = time.time()
    success, result = scheduler.generate_schedule(periode_id, "2024-2025")
    end_time = time.time()
    
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print(f"⏱️  TEMPS D'EXÉCUTION: {duration:.2f} secondes")
    print("="*60)
    
    if duration < 10:
        print(f"✅ OBJECTIF ATTEINT! ({duration:.2f}s < 10s)")
        improvement = ((340 - duration) / 340) * 100
        print(f"🎯 Amélioration: {improvement:.1f}% plus rapide que la version précédente")
    elif duration < 45:
        print(f"✅ Sous la cible de 45s ({duration:.2f}s)")
        print(f"⚠️  Mais au-dessus de l'objectif de 10s")
    else:
        print(f"❌ Au-dessus de la cible de 45s ({duration:.2f}s)")
    
    if success:
        print(f"\n📊 Résultats:")
        print(f"  ✅ Examens planifiés: {result['scheduled']}")
        print(f"  ❌ Modules non planifiés: {result['failed']}")
        
        total_modules = result['scheduled'] + result['failed']
        success_rate = (result['scheduled'] / total_modules * 100) if total_modules > 0 else 0
        print(f"  📈 Taux de succès: {success_rate:.1f}%")
        
        print(f"\n🔍 Conflits détectés: {result['total_conflicts']}")
        
        if result['failed'] > 0 and result['failed'] <= 10:
            print(f"\n⚠️  Modules non planifiés:")
            for module in result['failed_modules']:
                print(f"    - {module['module']} ({module['nb_inscrits']} étudiants)")
        
        # Verify in database
        examens = db.get_examens(periode_id)
        print(f"\n📋 Vérification base de données:")
        print(f"  - Examens en DB: {len(examens)}")
        
        surveillances = db.execute_query("SELECT COUNT(*) as count FROM surveillances")[0]['count']
        print(f"  - Surveillances en DB: {surveillances}")
        
        print("\n" + "="*60)
        if duration < 10 and result['scheduled'] > 500:
            print("✅ TEST RÉUSSI - Performance excellente!")
        elif duration < 10:
            print("✅ Performance atteinte mais taux de planification à améliorer")
        else:
            print("⚠️  Performance à optimiser davantage")
        print("="*60)
    else:
        print(f"\n❌ Erreur: {result.get('error', 'Erreur inconnue')}")

if __name__ == "__main__":
    test_fast_scheduler()
