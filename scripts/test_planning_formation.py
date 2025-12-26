import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
import pandas as pd

def test_planning_by_formation():
    print("\n" + "="*60)
    print("TESTING PLANNING BY FORMATION")
    print("="*60)
    
    try:
        db = Database()
        
        # Get active exam period
        print("\n1. Getting active exam period...")
        periodes = db.get_periodes_examen(actif=True)
        
        if not periodes:
            print("❌ No active exam period found!")
            return False
        
        periode = periodes[0]
        periode_id = periode['id']
        print(f"✅ Period: {periode['nom']}")
        
        # Test get_all_planning_by_formations
        print("\n2. Testing get_all_planning_by_formations()...")
        formations_summary = db.get_all_planning_by_formations(periode_id)
        
        if formations_summary:
            print(f"✅ Found {len(formations_summary)} formations with exams")
            
            # Display summary
            df_summary = pd.DataFrame(formations_summary)
            print("\n📊 Formations Summary:")
            print(df_summary[['formation_niveau', 'formation_nom', 'departement_nom', 'nb_examens']].head(10).to_string(index=False))
            
            total_exams = sum(f['nb_examens'] for f in formations_summary)
            avg_exams = total_exams / len(formations_summary)
            print(f"\n   Total exams: {total_exams}")
            print(f"   Average per formation: {avg_exams:.1f}")
        else:
            print("⚠️  No formations with exams found")
            return False
        
        # Test get_planning_by_formation for first formation
        print("\n3. Testing get_planning_by_formation()...")
        first_formation = formations_summary[0]
        formation_id = first_formation['formation_id']
        
        print(f"   Testing with: {first_formation['formation_niveau']} - {first_formation['formation_nom']}")
        
        planning = db.get_planning_by_formation(formation_id, periode_id)
        
        if planning:
            print(f"✅ Found {len(planning)} exams for this formation")
            
            # Display sample exams
            df_planning = pd.DataFrame(planning)
            print("\n📅 Sample Exams:")
            sample = df_planning[['date_heure', 'module_nom', 'salle_nom', 'professeur_responsable', 'nb_inscrits']].head(5)
            print(sample.to_string(index=False))
            
            # Statistics
            print("\n📊 Statistics:")
            print(f"   - Total exams: {len(planning)}")
            print(f"   - Total student-exams: {df_planning['nb_inscrits'].sum()}")
            print(f"   - Average duration: {df_planning['duree_minutes'].mean():.0f} minutes")
            print(f"   - Unique dates: {df_planning['date_heure'].nunique()}")
            
            return True
        else:
            print("❌ No planning found for this formation")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_planning_by_formation()
    
    print("\n" + "="*60)
    if success:
        print("✅ PLANNING BY FORMATION TEST PASSED")
    else:
        print("❌ PLANNING BY FORMATION TEST FAILED")
    print("="*60)
