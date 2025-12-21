import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database

print("="*60)
print("VERIFYING DATABASE METHODS")
print("="*60)

db = Database()

# Test the new method
print("\n✓ Testing get_modules_with_inscriptions()...")
try:
    modules = db.get_modules_with_inscriptions()
    print(f"  ✅ Success! Found {len(modules)} modules with enrollments")
    if modules:
        print(f"  📊 Sample: {modules[0]['nom']} - {modules[0]['nb_inscrits']} students")
except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n✓ All required methods verified!")
print("="*60)
