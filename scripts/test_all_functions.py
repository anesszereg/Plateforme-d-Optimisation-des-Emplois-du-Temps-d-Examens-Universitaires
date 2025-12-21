import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.scheduler import ExamScheduler
from src.constraints import ConstraintChecker
from src.analytics import Analytics

def test_database_connection():
    print("\n" + "="*60)
    print("TEST 1: DATABASE CONNECTION")
    print("="*60)
    
    try:
        db = Database()
        result = db.execute_query("SELECT version()")
        print(f"✅ Database connected: {result[0]['version'][:50]}...")
        return True, db
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False, None

def test_database_tables(db):
    print("\n" + "="*60)
    print("TEST 2: DATABASE TABLES")
    print("="*60)
    
    tables = [
        'departements', 'formations', 'etudiants', 'professeurs',
        'modules', 'inscriptions', 'lieu_examen', 'periodes_examen',
        'examens', 'surveillances'
    ]
    
    all_passed = True
    for table in tables:
        try:
            result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            count = result[0]['count']
            print(f"✅ {table:20s}: {count:6d} rows")
        except Exception as e:
            print(f"❌ {table:20s}: Error - {e}")
            all_passed = False
    
    return all_passed

def test_database_views(db):
    print("\n" + "="*60)
    print("TEST 3: DATABASE VIEWS")
    print("="*60)
    
    views = [
        'kpi_global',
        'stats_departement',
        'conflits_etudiants',
        'conflits_professeurs',
        'conflits_capacite',
        'conflits_salles',
        'occupation_salles_par_jour',
        'charge_professeurs'
    ]
    
    all_passed = True
    for view in views:
        try:
            result = db.execute_query(f"SELECT * FROM {view} LIMIT 1")
            print(f"✅ {view:30s}: OK")
        except Exception as e:
            print(f"❌ {view:30s}: {str(e)[:50]}")
            all_passed = False
    
    return all_passed

def test_database_functions(db):
    print("\n" + "="*60)
    print("TEST 4: DATABASE FUNCTIONS")
    print("="*60)
    
    try:
        etudiants = db.execute_query("SELECT id FROM etudiants LIMIT 1")
        periodes = db.execute_query("SELECT id FROM periodes_examen LIMIT 1")
        
        if etudiants and periodes:
            etudiant_id = etudiants[0]['id']
            periode_id = periodes[0]['id']
            
            result = db.get_planning_etudiant(etudiant_id, periode_id)
            print(f"✅ get_planning_etudiant: OK ({len(result)} results)")
        else:
            print("⚠️  get_planning_etudiant: No test data")
        
        profs = db.execute_query("SELECT id FROM professeurs LIMIT 1")
        if profs and periodes:
            prof_id = profs[0]['id']
            periode_id = periodes[0]['id']
            
            result = db.get_planning_professeur(prof_id, periode_id)
            print(f"✅ get_planning_professeur: OK ({len(result)} results)")
        else:
            print("⚠️  get_planning_professeur: No test data")
        
        return True
    except Exception as e:
        print(f"❌ Database functions failed: {e}")
        return False

def test_database_methods(db):
    print("\n" + "="*60)
    print("TEST 5: DATABASE CLASS METHODS")
    print("="*60)
    
    methods = [
        ('get_departements', []),
        ('get_formations', []),
        ('get_etudiants', []),
        ('get_professeurs', []),
        ('get_modules', []),
        ('get_lieu_examen', []),
        ('get_kpi_global', []),
        ('get_stats_departement', []),
        ('get_charge_professeurs', []),
        ('get_periodes_examen', [True])
    ]
    
    all_passed = True
    for method_name, args in methods:
        try:
            method = getattr(db, method_name)
            result = method(*args)
            count = len(result) if isinstance(result, list) else 1
            print(f"✅ {method_name:30s}: {count} results")
        except Exception as e:
            print(f"❌ {method_name:30s}: {str(e)[:50]}")
            all_passed = False
    
    return all_passed

def test_constraint_checker(db):
    print("\n" + "="*60)
    print("TEST 6: CONSTRAINT CHECKER")
    print("="*60)
    
    try:
        checker = ConstraintChecker(db)
        
        conflicts, total = checker.get_all_conflicts()
        print(f"✅ get_all_conflicts: {total} conflicts found")
        print(f"   - Étudiants: {len(conflicts['etudiants'])}")
        print(f"   - Professeurs: {len(conflicts['professeurs'])}")
        print(f"   - Capacité: {len(conflicts['capacite'])}")
        print(f"   - Salles: {len(conflicts['salles'])}")
        
        return True
    except Exception as e:
        print(f"❌ Constraint checker failed: {e}")
        return False

def test_analytics(db):
    print("\n" + "="*60)
    print("TEST 7: ANALYTICS")
    print("="*60)
    
    try:
        analytics = Analytics(db)
        
        kpis = analytics.get_dashboard_kpis()
        print(f"✅ get_dashboard_kpis: {len(kpis)} KPIs")
        
        dept_stats = analytics.get_department_stats()
        print(f"✅ get_department_stats: {len(dept_stats)} departments")
        
        prof_workload = analytics.get_professor_workload()
        print(f"✅ get_professor_workload: {len(prof_workload)} professors")
        
        occupation = analytics.get_occupation_analysis()
        print(f"✅ get_occupation_analysis: {len(occupation)} records")
        
        conflict_summary = analytics.get_conflict_summary()
        print(f"✅ get_conflict_summary: {sum(conflict_summary.values())} total conflicts")
        
        return True
    except Exception as e:
        print(f"❌ Analytics failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scheduler(db):
    print("\n" + "="*60)
    print("TEST 8: SCHEDULER (Quick Test)")
    print("="*60)
    
    try:
        scheduler = ExamScheduler(db)
        print("✅ Scheduler initialized")
        
        periodes = db.get_periodes_examen(actif=True)
        if periodes:
            print(f"✅ Found {len(periodes)} active exam period(s)")
        else:
            print("⚠️  No active exam periods found")
        
        return True
    except Exception as e:
        print(f"❌ Scheduler test failed: {e}")
        return False

def test_data_integrity(db):
    print("\n" + "="*60)
    print("TEST 9: DATA INTEGRITY")
    print("="*60)
    
    tests = [
        ("Formations have departments", 
         "SELECT COUNT(*) as count FROM formations f LEFT JOIN departements d ON f.dept_id = d.id WHERE d.id IS NULL"),
        
        ("Étudiants have formations",
         "SELECT COUNT(*) as count FROM etudiants e LEFT JOIN formations f ON e.formation_id = f.id WHERE f.id IS NULL"),
        
        ("Modules have formations",
         "SELECT COUNT(*) as count FROM modules m LEFT JOIN formations f ON m.formation_id = f.id WHERE f.id IS NULL"),
        
        ("Inscriptions valid",
         "SELECT COUNT(*) as count FROM inscriptions i LEFT JOIN etudiants e ON i.etudiant_id = e.id LEFT JOIN modules m ON i.module_id = m.id WHERE e.id IS NULL OR m.id IS NULL"),
    ]
    
    all_passed = True
    for test_name, query in tests:
        try:
            result = db.execute_query(query)
            orphans = result[0]['count']
            if orphans == 0:
                print(f"✅ {test_name:30s}: OK")
            else:
                print(f"⚠️  {test_name:30s}: {orphans} orphaned records")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name:30s}: {str(e)[:50]}")
            all_passed = False
    
    return all_passed

def main():
    print("\n" + "="*60)
    print("COMPREHENSIVE FUNCTION TESTING")
    print("Plateforme d'Optimisation des Emplois du Temps")
    print("="*60)
    
    results = {}
    
    success, db = test_database_connection()
    results['Database Connection'] = success
    
    if not success:
        print("\n❌ Cannot proceed without database connection")
        return
    
    results['Database Tables'] = test_database_tables(db)
    results['Database Views'] = test_database_views(db)
    results['Database Functions'] = test_database_functions(db)
    results['Database Methods'] = test_database_methods(db)
    results['Constraint Checker'] = test_constraint_checker(db)
    results['Analytics'] = test_analytics(db)
    results['Scheduler'] = test_scheduler(db)
    results['Data Integrity'] = test_data_integrity(db)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30s}: {status}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("✅ ALL FUNCTIONS WORKING CORRECTLY!")
    else:
        print(f"⚠️  {total_tests - passed_tests} test(s) failed")
    
    print("="*60)

if __name__ == "__main__":
    main()
