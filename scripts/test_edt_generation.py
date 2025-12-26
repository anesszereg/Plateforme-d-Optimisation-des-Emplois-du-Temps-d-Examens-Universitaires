import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.fast_scheduler import FastScheduler
from datetime import datetime

def test_edt_generation():
    print("\n" + "="*60)
    print("TESTING EDT GENERATION")
    print("="*60)
    
    try:
        # Initialize database
        print("\n1. Initializing database connection...")
        db = Database()
        print("✅ Database connected")
        
        # Get active exam period
        print("\n2. Getting active exam period...")
        periodes = db.get_periodes_examen(actif=True)
        
        if not periodes:
            print("❌ No active exam period found!")
            return False
        
        periode = periodes[0]
        periode_id = periode['id']
        print(f"✅ Found period: {periode['nom']}")
        print(f"   Date range: {periode['date_debut']} to {periode['date_fin']}")
        
        # Check modules with inscriptions
        print("\n3. Checking modules with inscriptions...")
        modules = db.get_modules_with_inscriptions()
        print(f"✅ Found {len(modules)} modules with enrollments")
        if modules:
            print(f"   Sample: {modules[0]['nom']} ({modules[0]['nb_inscrits']} students)")
        
        # Check rooms
        print("\n4. Checking available rooms...")
        salles = db.get_lieu_examen()
        print(f"✅ Found {len(salles)} available rooms")
        
        # Check professors
        print("\n5. Checking professors...")
        professeurs = db.get_professeurs()
        print(f"✅ Found {len(professeurs)} professors")
        
        # Initialize scheduler
        print("\n6. Initializing FastScheduler...")
        scheduler = FastScheduler(db)
        print("✅ Scheduler initialized")
        
        # Generate schedule
        print("\n7. Generating schedule...")
        print("   This may take 10-45 seconds...")
        
        start_time = datetime.now()
        success, result = scheduler.generate_schedule(periode_id, "2024-2025")
        end_time = datetime.now()
        
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*60}")
        print("GENERATION RESULTS")
        print(f"{'='*60}")
        
        if success:
            print(f"✅ SUCCESS!")
            print(f"\n📊 Statistics:")
            print(f"   - Execution time: {execution_time:.2f} seconds")
            print(f"   - Exams scheduled: {result['scheduled']}")
            print(f"   - Failed modules: {result['failed']}")
            print(f"   - Total conflicts: {result['total_conflicts']}")
            
            if result['failed'] > 0:
                print(f"\n⚠️  Failed modules:")
                for fm in result['failed_modules'][:5]:
                    print(f"   - {fm['module']} ({fm['nb_inscrits']} students)")
            
            if result['total_conflicts'] > 0:
                print(f"\n⚠️  Conflicts detected:")
                print(f"   - Students: {len(result['conflicts']['etudiants'])}")
                print(f"   - Professors: {len(result['conflicts']['professeurs'])}")
                print(f"   - Capacity: {len(result['conflicts']['capacite'])}")
                print(f"   - Rooms: {len(result['conflicts']['salles'])}")
            
            return True
        else:
            print(f"❌ FAILED!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_edt_generation()
    
    print("\n" + "="*60)
    if success:
        print("✅ EDT GENERATION TEST PASSED")
    else:
        print("❌ EDT GENERATION TEST FAILED")
    print("="*60)
