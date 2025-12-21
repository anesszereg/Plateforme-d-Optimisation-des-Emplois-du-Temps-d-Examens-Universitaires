from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class ConstraintChecker:
    def __init__(self, db):
        self.db = db
    
    def check_student_conflicts(self, examen_data: Dict, existing_examens: List[Dict]) -> Tuple[bool, str]:
        exam_date = examen_data['date_heure'].date() if isinstance(examen_data['date_heure'], datetime) else examen_data['date_heure']
        
        for existing in existing_examens:
            existing_date = existing['date_heure'].date() if isinstance(existing['date_heure'], datetime) else existing['date_heure']
            if existing_date == exam_date and existing['module_id'] != examen_data['module_id']:
                return False, "Conflit potentiel étudiant"
        
        return True, "OK"
    
    def check_professor_conflicts(self, prof_id: int, date_heure: datetime, duree_minutes: int) -> Tuple[bool, str]:
        exam_date = date_heure.date() if isinstance(date_heure, datetime) else date_heure
        
        query = """
            SELECT COUNT(DISTINCT ex.id) as count
            FROM surveillances s
            JOIN examens ex ON s.examen_id = ex.id
            WHERE s.prof_id = %s AND DATE(ex.date_heure) = %s
        """
        result = self.db.execute_query(query, (prof_id, exam_date))
        
        if result and result[0]['count'] >= 3:
            return False, f"Conflit: Le professeur a déjà 3 examens ce jour"
        
        query_overlap = """
            SELECT ex.id, m.nom
            FROM surveillances s
            JOIN examens ex ON s.examen_id = ex.id
            JOIN modules m ON ex.module_id = m.id
            WHERE s.prof_id = %s
              AND ex.date_heure < %s
              AND ex.date_heure + (ex.duree_minutes || ' minutes')::INTERVAL > %s
        """
        end_time = date_heure + timedelta(minutes=duree_minutes)
        overlaps = self.db.execute_query(query_overlap, (prof_id, end_time, date_heure))
        
        if overlaps:
            return False, f"Conflit: Chevauchement horaire avec l'examen {overlaps[0]['nom']}"
        
        return True, "OK"
    
    def check_room_capacity(self, salle_id: int, nb_inscrits: int) -> Tuple[bool, str]:
        query = "SELECT capacite_examen, nom FROM lieu_examen WHERE id = %s"
        result = self.db.execute_query(query, (salle_id,))
        
        if not result:
            return False, "Salle introuvable"
        
        capacite = result[0]['capacite_examen']
        if nb_inscrits > capacite:
            return False, f"Capacité insuffisante: {nb_inscrits} étudiants pour {capacite} places"
        
        return True, "OK"
    
    def check_room_availability(self, salle_id: int, date_heure: datetime, duree_minutes: int) -> Tuple[bool, str]:
        end_time = date_heure + timedelta(minutes=duree_minutes)
        
        query = """
            SELECT ex.id, m.nom
            FROM examens ex
            JOIN modules m ON ex.module_id = m.id
            WHERE ex.salle_id = %s
              AND ex.date_heure < %s
              AND ex.date_heure + (ex.duree_minutes || ' minutes')::INTERVAL > %s
        """
        conflicts = self.db.execute_query(query, (salle_id, end_time, date_heure))
        
        if conflicts:
            return False, f"Salle occupée par l'examen {conflicts[0]['nom']}"
        
        return True, "OK"
    
    def validate_examen(self, examen_data: Dict, existing_examens: List[Dict] = None) -> Tuple[bool, List[str]]:
        errors = []
        
        valid, msg = self.check_room_capacity(examen_data['salle_id'], examen_data['nb_inscrits'])
        if not valid:
            errors.append(msg)
        
        valid, msg = self.check_room_availability(
            examen_data['salle_id'], 
            examen_data['date_heure'], 
            examen_data['duree_minutes']
        )
        if not valid:
            errors.append(msg)
        
        valid, msg = self.check_student_conflicts(examen_data, existing_examens or [])
        if not valid:
            errors.append(msg)
        
        valid, msg = self.check_professor_conflicts(
            examen_data['prof_responsable_id'],
            examen_data['date_heure'],
            examen_data['duree_minutes']
        )
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, errors
    
    def get_all_conflicts(self):
        conflicts = {
            'etudiants': self.db.get_conflits_etudiants(),
            'professeurs': self.db.get_conflits_professeurs(),
            'capacite': self.db.get_conflits_capacite(),
            'salles': self.db.get_conflits_salles()
        }
        
        total = sum(len(v) for v in conflicts.values())
        return conflicts, total
