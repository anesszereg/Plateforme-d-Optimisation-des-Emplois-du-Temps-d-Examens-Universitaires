from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random
from src.constraints import ConstraintChecker

class ExamScheduler:
    def __init__(self, db):
        self.db = db
        self.constraint_checker = ConstraintChecker(db)
    
    def generate_schedule(self, periode_id: int, annee_universitaire: str) -> Tuple[bool, Dict]:
        start_time = datetime.now()
        
        periode = self.db.execute_query(
            "SELECT * FROM periodes_examen WHERE id = %s", 
            (periode_id,)
        )[0]
        
        date_debut = periode['date_debut']
        date_fin = periode['date_fin']
        
        modules = self.db.get_modules_with_inscriptions()
        modules = sorted(modules, key=lambda x: x['nb_inscrits'], reverse=True)
        
        salles = self.db.get_lieu_examen()
        professeurs = self.db.get_professeurs()
        
        self.db.delete_all_examens(periode_id)
        
        scheduled_exams = []
        failed_modules = []
        
        time_slots = [(8, 30), (11, 0), (14, 30), (17, 0)]
        available_dates = [(date_debut + timedelta(days=i)) for i in range((date_fin - date_debut).days + 1)]
        
        # In-memory tracking for fast constraint checking
        room_schedule = {}  # {(salle_id, datetime): True}
        prof_schedule = {}  # {(prof_id, date): count}
        student_exams = {}  # {(student_id, date): count}
        
        # Pre-load student enrollments
        enrollments = self.db.execute_query(
            "SELECT module_id, etudiant_id FROM inscriptions WHERE statut = 'inscrit'"
        )
        module_students = {}
        for enroll in enrollments:
            if enroll['module_id'] not in module_students:
                module_students[enroll['module_id']] = []
            module_students[enroll['module_id']].append(enroll['etudiant_id'])
        
        for module in modules:
            scheduled = False
            module_id = module['id']
            students = module_students.get(module_id, [])
            
            for attempt_date in available_dates:
                if scheduled:
                    break
                    
                for slot_hour, slot_minute in time_slots:
                    if scheduled:
                        break
                    
                    exam_datetime = datetime.combine(
                        attempt_date,
                        datetime.min.time().replace(hour=slot_hour, minute=slot_minute)
                    )
                    
                    suitable_salles = [
                        s for s in salles 
                        if s['capacite_examen'] >= module['nb_inscrits']
                        and (s['id'], exam_datetime) not in room_schedule
                    ]
                    
                    if not suitable_salles:
                        continue
                    
                    dept_profs = [p for p in professeurs if p['dept_id'] == module['dept_id']]
                    if not dept_profs:
                        dept_profs = professeurs[:5]
                    
                    for salle in suitable_salles[:3]:
                        if scheduled:
                            break
                        
                        for prof in dept_profs[:3]:
                            # Fast in-memory constraint checks
                            prof_key = (prof['id'], attempt_date)
                            prof_count = prof_schedule.get(prof_key, 0)
                            if prof_count >= 3:
                                continue
                            
                            # Check student conflicts
                            student_conflict = False
                            for student_id in students:
                                student_key = (student_id, attempt_date)
                                if student_exams.get(student_key, 0) >= 2:
                                    student_conflict = True
                                    break
                            
                            if student_conflict:
                                continue
                            
                            # All constraints passed - schedule exam
                            try:
                                examen_id = self.db.create_examen(
                                    module_id,
                                    prof['id'],
                                    salle['id'],
                                    periode_id,
                                    exam_datetime,
                                    module['duree_examen'],
                                    module['nb_inscrits']
                                )
                                
                                if examen_id:
                                    # Update in-memory tracking
                                    room_schedule[(salle['id'], exam_datetime)] = True
                                    prof_schedule[prof_key] = prof_count + 1
                                    for student_id in students:
                                        student_key = (student_id, attempt_date)
                                        student_exams[student_key] = student_exams.get(student_key, 0) + 1
                                    
                                    # Create surveillances
                                    self.db.create_surveillance(examen_id, prof['id'], 'responsable')
                                    
                                    nb_surveillants = min(2, len(dept_profs) - 1)
                                    for i, surveillant in enumerate(dept_profs):
                                        if i >= nb_surveillants or surveillant['id'] == prof['id']:
                                            break
                                        self.db.create_surveillance(examen_id, surveillant['id'], 'surveillant')
                                    
                                    scheduled_exams.append({
                                        'module_id': module_id,
                                        'prof_responsable_id': prof['id'],
                                        'salle_id': salle['id'],
                                        'periode_id': periode_id,
                                        'date_heure': exam_datetime,
                                        'duree_minutes': module['duree_examen'],
                                        'nb_inscrits': module['nb_inscrits']
                                    })
                                    scheduled = True
                                    break
                            except Exception as e:
                                continue
            
            if not scheduled:
                failed_modules.append({
                    'module': module['nom'],
                    'nb_inscrits': module['nb_inscrits']
                })
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        conflicts, total_conflicts = self.constraint_checker.get_all_conflicts()
        
        result = {
            'success': len(failed_modules) == 0,
            'scheduled': len(scheduled_exams),
            'failed': len(failed_modules),
            'failed_modules': failed_modules,
            'execution_time': execution_time,
            'conflicts': conflicts,
            'total_conflicts': total_conflicts
        }
        
        return True, result
    
    def optimize_schedule(self, periode_id: int):
        query = """
            SELECT ex.id, ex.salle_id, ex.nb_inscrits, l.capacite_examen,
                   l.capacite_examen - ex.nb_inscrits as espace_libre
            FROM examens ex
            JOIN lieu_examen l ON ex.salle_id = l.id
            WHERE ex.periode_id = %s
              AND l.capacite_examen - ex.nb_inscrits > 10
            ORDER BY espace_libre DESC
        """
        
        underutilized = self.db.execute_query(query, (periode_id,))
        
        optimizations = 0
        for exam in underutilized:
            smaller_rooms = self.db.execute_query("""
                SELECT id, nom, capacite_examen
                FROM lieu_examen
                WHERE capacite_examen >= %s
                  AND capacite_examen < %s
                ORDER BY capacite_examen ASC
                LIMIT 1
            """, (exam['nb_inscrits'], exam['capacite_examen']))
            
            if smaller_rooms:
                new_room = smaller_rooms[0]
                exam_data = self.db.execute_query(
                    "SELECT date_heure, duree_minutes FROM examens WHERE id = %s",
                    (exam['id'],)
                )[0]
                
                valid, _ = self.constraint_checker.check_room_availability(
                    new_room['id'],
                    exam_data['date_heure'],
                    exam_data['duree_minutes']
                )
                
                if valid:
                    self.db.execute_query(
                        "UPDATE examens SET salle_id = %s WHERE id = %s",
                        (new_room['id'], exam['id']),
                        fetch=False
                    )
                    optimizations += 1
        
        return optimizations
