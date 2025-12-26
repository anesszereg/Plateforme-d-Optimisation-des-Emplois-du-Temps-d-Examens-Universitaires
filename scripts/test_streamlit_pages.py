import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.scheduler import ExamScheduler
from src.analytics import Analytics
from src.constraints import ConstraintChecker

def test_page_dependencies():
    print("\n" + "="*60)
    print("STREAMLIT PAGES DEPENDENCY TEST")
    print("="*60)
    
    all_passed = True
    
    # Test 1: Main app dependencies
    print("\n📄 Testing app.py dependencies...")
    try:
        db = Database()
        analytics = Analytics(db)
        scheduler = ExamScheduler(db)
        print("✅ app.py: All dependencies loaded")
    except Exception as e:
        print(f"❌ app.py: {e}")
        all_passed = False
    
    # Test 2: Administration page
    print("\n📄 Testing 1_👨‍💼_Administration.py dependencies...")
    try:
        from src.fast_scheduler import FastScheduler
        fast_scheduler = FastScheduler(db)
        print("✅ Administration page: All dependencies loaded")
    except Exception as e:
        print(f"❌ Administration page: {e}")
        all_passed = False
    
    # Test 3: Statistics page
    print("\n📄 Testing 2_📊_Statistiques.py dependencies...")
    try:
        kpis = analytics.get_dashboard_kpis()
        dept_stats = analytics.get_department_stats()
        print("✅ Statistics page: All dependencies loaded")
    except Exception as e:
        print(f"❌ Statistics page: {e}")
        all_passed = False
    
    # Test 4: Departments page
    print("\n📄 Testing 3_🏛️_Départements.py dependencies...")
    try:
        departements = db.get_departements()
        formations = db.get_formations()
        print("✅ Departments page: All dependencies loaded")
    except Exception as e:
        print(f"❌ Departments page: {e}")
        all_passed = False
    
    # Test 5: Consultation page
    print("\n📄 Testing 4_👤_Consultation.py dependencies...")
    try:
        etudiants = db.get_etudiants()
        professeurs = db.get_professeurs()
        periodes = db.get_periodes_examen()
        print("✅ Consultation page: All dependencies loaded")
    except Exception as e:
        print(f"❌ Consultation page: {e}")
        all_passed = False
    
    return all_passed

def test_page_functionality():
    print("\n" + "="*60)
    print("STREAMLIT PAGES FUNCTIONALITY TEST")
    print("="*60)
    
    db = Database()
    analytics = Analytics(db)
    
    all_passed = True
    
    # Test dashboard KPIs
    print("\n📊 Testing dashboard KPIs...")
    try:
        kpis = analytics.get_dashboard_kpis()
        required_keys = ['total_etudiants', 'total_professeurs', 'total_modules', 
                        'total_inscriptions', 'total_departements', 'total_formations',
                        'total_salles', 'capacite_totale']
        
        for key in required_keys:
            if key not in kpis:
                print(f"⚠️  Missing KPI: {key}")
                all_passed = False
        
        if all_passed:
            print("✅ All KPIs available")
            print(f"   - Étudiants: {kpis['total_etudiants']:,}")
            print(f"   - Professeurs: {kpis['total_professeurs']:,}")
            print(f"   - Modules: {kpis['total_modules']:,}")
    except Exception as e:
        print(f"❌ Dashboard KPIs failed: {e}")
        all_passed = False
    
    # Test department statistics
    print("\n🏛️ Testing department statistics...")
    try:
        dept_stats = analytics.get_department_stats()
        if len(dept_stats) > 0:
            print(f"✅ Department stats: {len(dept_stats)} departments")
        else:
            print("⚠️  No department statistics available")
    except Exception as e:
        print(f"❌ Department stats failed: {e}")
        all_passed = False
    
    # Test conflict detection
    print("\n⚠️  Testing conflict detection...")
    try:
        conflict_summary = analytics.get_conflict_summary()
        total_conflicts = sum(conflict_summary.values())
        print(f"✅ Conflict detection: {total_conflicts} conflicts")
        print(f"   - Étudiants: {conflict_summary.get('etudiants', 0)}")
        print(f"   - Professeurs: {conflict_summary.get('professeurs', 0)}")
        print(f"   - Capacité: {conflict_summary.get('capacite', 0)}")
        print(f"   - Salles: {conflict_summary.get('salles', 0)}")
    except Exception as e:
        print(f"❌ Conflict detection failed: {e}")
        all_passed = False
    
    # Test exam period availability
    print("\n📅 Testing exam periods...")
    try:
        periodes = db.get_periodes_examen(actif=True)
        if periodes:
            print(f"✅ Active exam periods: {len(periodes)}")
            for p in periodes:
                print(f"   - {p['nom']} ({p['date_debut']} to {p['date_fin']})")
        else:
            print("⚠️  No active exam periods")
    except Exception as e:
        print(f"❌ Exam periods failed: {e}")
        all_passed = False
    
    return all_passed

def main():
    print("\n" + "="*60)
    print("STREAMLIT APPLICATION TESTING")
    print("="*60)
    
    results = {}
    
    results['Page Dependencies'] = test_page_dependencies()
    results['Page Functionality'] = test_page_functionality()
    
    print("\n" + "="*60)
    print("STREAMLIT TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30s}: {status}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed_tests}/{total_tests} test groups passed")
    
    if passed_tests == total_tests:
        print("✅ ALL STREAMLIT PAGES READY!")
    else:
        print(f"⚠️  {total_tests - passed_tests} test group(s) failed")
    
    print("="*60)

if __name__ == "__main__":
    main()
