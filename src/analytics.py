import pandas as pd
from typing import Dict, List

class Analytics:
    def __init__(self, db):
        self.db = db
    
    def get_dashboard_kpis(self) -> Dict:
        kpis = self.db.get_kpi_global()
        return kpis
    
    def get_occupation_analysis(self) -> pd.DataFrame:
        data = self.db.get_occupation_salles()
        if data:
            df = pd.DataFrame(data)
            return df
        return pd.DataFrame()
    
    def get_department_stats(self) -> pd.DataFrame:
        data = self.db.get_stats_departement()
        if data:
            df = pd.DataFrame(data)
            return df
        return pd.DataFrame()
    
    def get_professor_workload(self) -> pd.DataFrame:
        data = self.db.get_charge_professeurs()
        if data:
            df = pd.DataFrame(data)
            return df
        return pd.DataFrame()
    
    def calculate_efficiency_score(self, periode_id: int) -> Dict:
        examens = self.db.get_examens(periode_id)
        
        if not examens:
            return {
                'score': 0,
                'metrics': {}
            }
        
        total_capacity = sum(e.get('capacite_examen', 0) for e in examens)
        total_students = sum(e.get('nb_inscrits', 0) for e in examens)
        
        utilization_rate = (total_students / total_capacity * 100) if total_capacity > 0 else 0
        
        conflits_etu = self.db.get_conflits_etudiants() or []
        conflits_prof = self.db.get_conflits_professeurs() or []
        total_conflicts = len(conflits_etu) + len(conflits_prof)
        conflict_rate = total_conflicts / len(examens) * 100 if examens else 0
        
        unique_dates = len(set(e['date_heure'].date() for e in examens if e.get('date_heure')))
        avg_exams_per_day = len(examens) / unique_dates if unique_dates > 0 else 0
        
        score = max(0, 100 - conflict_rate - (100 - utilization_rate) * 0.5)
        
        return {
            'score': round(score, 2),
            'metrics': {
                'utilization_rate': round(utilization_rate, 2),
                'conflict_rate': round(conflict_rate, 2),
                'avg_exams_per_day': round(avg_exams_per_day, 2),
                'total_exams': len(examens),
                'unique_dates': unique_dates
            }
        }
    
    def get_conflict_summary(self) -> Dict:
        conflits_etu = self.db.get_conflits_etudiants() or []
        conflits_prof = self.db.get_conflits_professeurs() or []
        conflits_cap = self.db.get_conflits_capacite() or []
        conflits_sal = self.db.get_conflits_salles() or []
        return {
            'etudiants': len(conflits_etu),
            'professeurs': len(conflits_prof),
            'capacite': len(conflits_cap),
            'salles': len(conflits_sal)
        }
    
    def export_schedule_to_csv(self, periode_id: int, filepath: str):
        examens = self.db.get_examens(periode_id)
        if examens:
            df = pd.DataFrame(examens)
            df.to_csv(filepath, index=False, encoding='utf-8')
            return True
        return False
