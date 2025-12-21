from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random

class FastScheduler:
    """Ultra-fast scheduling algorithm optimized for <10 second execution"""
    
    def __init__(self, db):
        self.db = db
    
    def generate_schedule(self, periode_id: int, annee_universitaire: str) -> Tuple[bool, Dict]:
        start_time = datetime.now()
        
        # Get period info
        periode = self.db.execute_query(
            "SELECT * FROM periodes_examen WHERE id = %s", 
            (periode_id,)
        )[0]
        
        date_debut = periode['date_debut']
        date_fin = periode['date_fin']
        
        # Load all data in one go
        modules = self.db.get_modules_with_inscriptions()
        modules = sorted(modules, key=lambda x: x['nb_inscrits'], reverse=True)
        
        salles = self.db.get_lieu_examen()
        salles_by_capacity = sorted(salles, key=lambda x: x['capacite_examen'], reverse=True)
        
        professeurs = self.db.get_professeurs()
        prof_by_dept = {}
        for p in professeurs:
            if p['dept_id'] not in prof_by_dept:
                prof_by_dept[p['dept_id']] = []
            prof_by_dept[p['dept_id']].append(p)
        
        # Delete existing exams
        self.db.delete_all_examens(periode_id)
        
        # Time slots
        time_slots = [(8, 30), (11, 0), (14, 30), (17, 0)]
        available_dates = [(date_debut + timedelta(days=i)) for i in range((date_fin - date_debut).days + 1)]
        
        # In-memory tracking for fast constraint checking
        room_schedule = {}  # {salle_id: [(start_datetime, end_datetime)]}
        prof_daily_count = {}  # {(prof_id, date): count}
        student_exams = {}  # {(student_id, date): count}
        
        print("Loading enrollments...")
        enrollments = self.db.execute_query(
            "SELECT module_id, etudiant_id FROM inscriptions WHERE statut = 'inscrit'"
        )
        module_students = {}
        student_modules = {}
        for enroll in enrollments:
            mid = enroll['module_id']
            sid = enroll['etudiant_id']
            
            if mid not in module_students:
                module_students[mid] = set()
            module_students[mid].add(sid)
            
            if sid not in student_modules:
                student_modules[sid] = set()
            student_modules[sid].add(mid)
        
        student_daily_exams = {}  # {(student_id, date): count}
        
        # Batch insert lists
        exams_to_insert = []
        surveillances_to_insert = []
        
        scheduled_count = 0
        failed_modules = []
        
        # Greedy scheduling
        current_slot_index = 0
        total_slots = len(available_dates) * len(time_slots)
        
        for module in modules:
            module_id = module['id']
            nb_inscrits = module['nb_inscrits']
            students = module_students.get(module_id, set())
            
            scheduled = False
            
            # Get all suitable rooms
            suitable_rooms = [s for s in salles_by_capacity if s['capacite_examen'] >= nb_inscrits]
            
            if not suitable_rooms:
                failed_modules.append({'module': module['nom'], 'nb_inscrits': nb_inscrits})
                continue
            
            # Try to schedule in next available slot
            attempts = 0
            max_attempts = min(100, total_slots * 2)
            
            while not scheduled and attempts < max_attempts:
                slot_idx = (current_slot_index + attempts) % total_slots
                date_idx = slot_idx // len(time_slots)
                time_idx = slot_idx % len(time_slots)
                
                if date_idx >= len(available_dates):
                    break
                
                exam_date = available_dates[date_idx]
                slot_hour, slot_minute = time_slots[time_idx]
                exam_datetime = datetime.combine(
                    exam_date,
                    datetime.min.time().replace(hour=slot_hour, minute=slot_minute)
                )
                
                # Try each suitable room for this time slot
                suitable_room = None
                exam_end_datetime = exam_datetime + timedelta(minutes=module['duree_examen'])
                
                for room in suitable_rooms:
                    room_id = room['id']
                    # Check for time overlap with existing exams in this room
                    room_available = True
                    if room_id in room_schedule:
                        for existing_start, existing_end in room_schedule[room_id]:
                            # Check if times overlap
                            if not (exam_end_datetime <= existing_start or exam_datetime >= existing_end):
                                room_available = False
                                break
                    
                    if room_available:
                        suitable_room = room
                        break
                
                if not suitable_room:
                    attempts += 1
                    continue
                
                # Get professor
                dept_profs = prof_by_dept.get(module['dept_id'], professeurs[:5])
                prof = None
                
                for p in dept_profs:
                    prof_key = (p['id'], exam_date)
                    if prof_daily_count.get(prof_key, 0) < 3:
                        prof = p
                        break
                
                if not prof:
                    attempts += 1
                    continue
                
                # Check student conflicts (fast) - max 1 exam per day
                student_conflict = False
                for student_id in students:
                    student_key = (student_id, exam_date)
                    if student_daily_exams.get(student_key, 0) >= 1:
                        student_conflict = True
                        break
                
                if student_conflict:
                    attempts += 1
                    continue
                
                # All checks passed - schedule exam
                exams_to_insert.append({
                    'module_id': module_id,
                    'prof_id': prof['id'],
                    'salle_id': suitable_room['id'],
                    'periode_id': periode_id,
                    'date_heure': exam_datetime,
                    'duree_minutes': module['duree_examen'],
                    'nb_inscrits': nb_inscrits
                })
                
                # Update tracking
                room_id = suitable_room['id']
                if room_id not in room_schedule:
                    room_schedule[room_id] = []
                room_schedule[room_id].append((exam_datetime, exam_end_datetime))
                
                prof_key = (prof['id'], exam_date)
                prof_daily_count[prof_key] = prof_daily_count.get(prof_key, 0) + 1
                
                for student_id in students:
                    student_key = (student_id, exam_date)
                    student_daily_exams[student_key] = student_daily_exams.get(student_key, 0) + 1
                
                scheduled = True
                scheduled_count += 1
                current_slot_index = (slot_idx + 1) % total_slots
                
                attempts += 1
            
            if not scheduled:
                failed_modules.append({'module': module['nom'], 'nb_inscrits': nb_inscrits})
        
        # Batch insert all exams
        print(f"Inserting {len(exams_to_insert)} exams...")
        exam_ids = []
        for exam_data in exams_to_insert:
            try:
                exam_id = self.db.create_examen(
                    exam_data['module_id'],
                    exam_data['prof_id'],
                    exam_data['salle_id'],
                    exam_data['periode_id'],
                    exam_data['date_heure'],
                    exam_data['duree_minutes'],
                    exam_data['nb_inscrits']
                )
                if exam_id:
                    exam_ids.append((exam_id, exam_data['prof_id'], exam_data['module_id']))
            except Exception as e:
                print(f"Error inserting exam: {e}")
        
        # Create surveillances (simplified)
        print(f"Creating surveillances...")
        for exam_id, prof_id, module_id in exam_ids:
            try:
                self.db.create_surveillance(exam_id, prof_id, 'responsable')
            except Exception as e:
                print(f"Error creating surveillance: {e}")
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Get conflicts
        conflicts, total_conflicts = self.get_conflicts()
        
        result = {
            'scheduled': scheduled_count,
            'failed': len(failed_modules),
            'failed_modules': failed_modules[:10],
            'execution_time': execution_time,
            'conflicts': conflicts,
            'total_conflicts': total_conflicts
        }
        
        return True, result
    
    def get_conflicts(self):
        """Fast conflict detection"""
        try:
            conflicts = {
                'etudiants': self.db.execute_query("SELECT * FROM conflits_etudiants LIMIT 100") or [],
                'professeurs': self.db.execute_query("SELECT * FROM conflits_professeurs LIMIT 100") or [],
                'capacite': self.db.execute_query("SELECT * FROM conflits_capacite LIMIT 100") or [],
                'salles': self.db.execute_query("SELECT * FROM conflits_salles LIMIT 100") or []
            }
            total = sum(len(v) for v in conflicts.values())
            return conflicts, total
        except:
            return {'etudiants': [], 'professeurs': [], 'capacite': [], 'salles': []}, 0
