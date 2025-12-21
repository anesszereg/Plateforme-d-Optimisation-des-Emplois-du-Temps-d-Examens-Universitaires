import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime
from src.database import Database
from src.scheduler import ExamScheduler
from src.analytics import Analytics

def benchmark_queries(db):
    print("\n" + "="*60)
    print("BENCHMARK DES REQUÊTES SQL")
    print("="*60)
    
    queries = {
        "KPIs Globaux": "SELECT * FROM kpi_global",
        "Statistiques Départements": "SELECT * FROM stats_departement",
        "Conflits Étudiants": "SELECT * FROM conflits_etudiants",
        "Conflits Professeurs": "SELECT * FROM conflits_professeurs",
        "Conflits Capacité": "SELECT * FROM conflits_capacite",
        "Conflits Salles": "SELECT * FROM conflits_salles",
        "Occupation Salles": "SELECT * FROM occupation_salles_par_jour",
        "Charge Professeurs": "SELECT * FROM charge_professeurs",
        "Liste Étudiants": "SELECT * FROM etudiants LIMIT 1000",
        "Liste Modules": "SELECT * FROM modules",
        "Inscriptions (10K)": "SELECT * FROM inscriptions LIMIT 10000"
    }
    
    results = []
    
    for name, query in queries.items():
        start = time.time()
        try:
            data = db.execute_query(query)
            end = time.time()
            duration = (end - start) * 1000
            count = len(data) if data else 0
            
            results.append({
                'Requête': name,
                'Durée (ms)': f"{duration:.2f}",
                'Résultats': count,
                'Statut': '✅'
            })
            
            print(f"✅ {name:30s} | {duration:8.2f} ms | {count:6d} résultats")
        except Exception as e:
            results.append({
                'Requête': name,
                'Durée (ms)': 'N/A',
                'Résultats': 0,
                'Statut': '❌'
            })
            print(f"❌ {name:30s} | Erreur: {e}")
    
    return results

def benchmark_scheduler(db):
    print("\n" + "="*60)
    print("BENCHMARK DE L'ALGORITHME DE PLANIFICATION")
    print("="*60)
    
    periodes = db.get_periodes_examen(actif=True)
    
    if not periodes:
        print("❌ Aucune période d'examen active trouvée")
        return None
    
    periode = periodes[0]
    periode_id = periode['id']
    
    print(f"\nPériode: {periode['nom']}")
    print(f"Date: {periode['date_debut']} - {periode['date_fin']}")
    
    scheduler = ExamScheduler(db)
    
    print("\n🚀 Lancement de la génération d'EDT...")
    print("Objectif: < 45 secondes")
    
    start = time.time()
    success, result = scheduler.generate_schedule(periode_id, "2024-2025")
    end = time.time()
    
    duration = end - start
    
    print(f"\n{'='*60}")
    print(f"⏱️  TEMPS D'EXÉCUTION: {duration:.2f} secondes")
    print(f"{'='*60}")
    
    if duration < 45:
        print(f"✅ OBJECTIF ATTEINT! ({duration:.2f}s < 45s)")
    else:
        print(f"⚠️  Objectif non atteint ({duration:.2f}s > 45s)")
    
    if success:
        print(f"\n📊 Résultats:")
        print(f"  - Examens planifiés: {result['scheduled']}")
        print(f"  - Modules non planifiés: {result['failed']}")
        print(f"  - Conflits détectés: {result['total_conflicts']}")
        
        if result['failed'] > 0:
            print(f"\n⚠️  Modules non planifiés:")
            for module in result['failed_modules'][:5]:
                print(f"    - {module['module']} ({module['nb_inscrits']} étudiants)")
    
    return {
        'duration': duration,
        'success': success,
        'result': result
    }

def benchmark_analytics(db):
    print("\n" + "="*60)
    print("BENCHMARK DES ANALYSES")
    print("="*60)
    
    analytics = Analytics(db)
    
    tests = []
    
    print("\n📊 Test 1: Dashboard KPIs")
    start = time.time()
    kpis = analytics.get_dashboard_kpis()
    duration = (time.time() - start) * 1000
    print(f"  ✅ Complété en {duration:.2f} ms")
    tests.append(('Dashboard KPIs', duration))
    
    print("\n📊 Test 2: Statistiques Départements")
    start = time.time()
    dept_stats = analytics.get_department_stats()
    duration = (time.time() - start) * 1000
    print(f"  ✅ Complété en {duration:.2f} ms")
    tests.append(('Stats Départements', duration))
    
    print("\n📊 Test 3: Charge Professeurs")
    start = time.time()
    charge = analytics.get_professor_workload()
    duration = (time.time() - start) * 1000
    print(f"  ✅ Complété en {duration:.2f} ms")
    tests.append(('Charge Professeurs', duration))
    
    print("\n📊 Test 4: Occupation Salles")
    start = time.time()
    occupation = analytics.get_occupation_analysis()
    duration = (time.time() - start) * 1000
    print(f"  ✅ Complété en {duration:.2f} ms")
    tests.append(('Occupation Salles', duration))
    
    periodes = db.get_periodes_examen(actif=True)
    if periodes:
        print("\n📊 Test 5: Score d'Efficacité")
        start = time.time()
        efficiency = analytics.calculate_efficiency_score(periodes[0]['id'])
        duration = (time.time() - start) * 1000
        print(f"  ✅ Complété en {duration:.2f} ms")
        print(f"  Score: {efficiency['score']:.1f}/100")
        tests.append(('Score Efficacité', duration))
    
    return tests

def generate_report(query_results, scheduler_result, analytics_results):
    print("\n" + "="*60)
    print("RAPPORT DE PERFORMANCE")
    print("="*60)
    
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📊 RÉSUMÉ DES REQUÊTES SQL:")
    total_queries = len(query_results)
    successful_queries = sum(1 for r in query_results if r['Statut'] == '✅')
    print(f"  - Total: {total_queries}")
    print(f"  - Réussies: {successful_queries}")
    print(f"  - Échouées: {total_queries - successful_queries}")
    
    if scheduler_result:
        print("\n🚀 PERFORMANCE DE PLANIFICATION:")
        print(f"  - Temps d'exécution: {scheduler_result['duration']:.2f}s")
        print(f"  - Objectif (<45s): {'✅ ATTEINT' if scheduler_result['duration'] < 45 else '❌ NON ATTEINT'}")
        if scheduler_result['success']:
            result = scheduler_result['result']
            print(f"  - Examens planifiés: {result['scheduled']}")
            print(f"  - Taux de succès: {(result['scheduled'] / (result['scheduled'] + result['failed']) * 100):.1f}%")
    
    print("\n📈 PERFORMANCE DES ANALYSES:")
    for name, duration in analytics_results:
        print(f"  - {name:25s}: {duration:8.2f} ms")
    
    avg_analytics = sum(d for _, d in analytics_results) / len(analytics_results)
    print(f"  - Moyenne: {avg_analytics:.2f} ms")
    
    print("\n" + "="*60)
    print("✅ BENCHMARK TERMINÉ")
    print("="*60)

def main():
    print("="*60)
    print("BENCHMARK DE PERFORMANCE")
    print("Plateforme d'Optimisation des Emplois du Temps")
    print("="*60)
    
    db = Database()
    
    try:
        query_results = benchmark_queries(db)
        
        scheduler_result = benchmark_scheduler(db)
        
        analytics_results = benchmark_analytics(db)
        
        generate_report(query_results, scheduler_result, analytics_results)
        
        print("\n💡 Recommandations:")
        if scheduler_result and scheduler_result['duration'] > 45:
            print("  - Optimiser l'algorithme de planification")
            print("  - Ajouter plus d'index sur les tables critiques")
            print("  - Considérer le partitionnement des grandes tables")
        else:
            print("  - ✅ Performances excellentes!")
            print("  - Continuer le monitoring régulier")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du benchmark: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
