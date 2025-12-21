import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'exam_scheduling'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(**self.config)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @contextmanager
    def get_cursor(self, dict_cursor=True):
        with self.get_connection() as conn:
            cursor_factory = RealDictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
            finally:
                cursor.close()
    
    def execute_query(self, query, params=None, fetch=True):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            return None
    
    def execute_many(self, query, params_list):
        with self.get_cursor(dict_cursor=False) as cursor:
            cursor.executemany(query, params_list)
    
    def get_departements(self):
        query = "SELECT * FROM departements ORDER BY nom"
        return self.execute_query(query)
    
    def get_formations(self, dept_id=None):
        if dept_id:
            query = "SELECT * FROM formations WHERE dept_id = %s ORDER BY nom"
            return self.execute_query(query, (dept_id,))
        query = "SELECT * FROM formations ORDER BY nom"
        return self.execute_query(query)
    
    def get_etudiants(self, formation_id=None):
        if formation_id:
            query = "SELECT * FROM etudiants WHERE formation_id = %s ORDER BY nom, prenom"
            return self.execute_query(query, (formation_id,))
        query = "SELECT * FROM etudiants ORDER BY nom, prenom"
        return self.execute_query(query)
    
    def get_professeurs(self, dept_id=None):
        if dept_id:
            query = "SELECT * FROM professeurs WHERE dept_id = %s ORDER BY nom, prenom"
            return self.execute_query(query, (dept_id,))
        query = "SELECT * FROM professeurs ORDER BY nom, prenom"
        return self.execute_query(query)
    
    def get_modules(self, formation_id=None):
        if formation_id:
            query = "SELECT * FROM modules WHERE formation_id = %s ORDER BY nom"
            return self.execute_query(query, (formation_id,))
        query = "SELECT * FROM modules ORDER BY nom"
        return self.execute_query(query)
    
    def get_lieu_examen(self, type_lieu=None):
        if type_lieu:
            query = "SELECT * FROM lieu_examen WHERE type = %s AND disponible = TRUE ORDER BY capacite_examen DESC"
            return self.execute_query(query, (type_lieu,))
        query = "SELECT * FROM lieu_examen WHERE disponible = TRUE ORDER BY capacite_examen DESC"
        return self.execute_query(query)
    
    def get_examens(self, periode_id=None):
        if periode_id:
            query = """
                SELECT e.*, m.nom as module_nom, l.nom as salle_nom, 
                       p.nom || ' ' || p.prenom as professeur
                FROM examens e
                JOIN modules m ON e.module_id = m.id
                JOIN lieu_examen l ON e.salle_id = l.id
                JOIN professeurs p ON e.prof_responsable_id = p.id
                WHERE e.periode_id = %s
                ORDER BY e.date_heure
            """
            return self.execute_query(query, (periode_id,))
        query = """
            SELECT e.*, m.nom as module_nom, l.nom as salle_nom,
                   p.nom || ' ' || p.prenom as professeur
            FROM examens e
            JOIN modules m ON e.module_id = m.id
            JOIN lieu_examen l ON e.salle_id = l.id
            JOIN professeurs p ON e.prof_responsable_id = p.id
            ORDER BY e.date_heure
        """
        return self.execute_query(query)
    
    def get_kpi_global(self):
        query = "SELECT * FROM kpi_global"
        result = self.execute_query(query)
        return result[0] if result else {}
    
    def get_conflits_etudiants(self):
        query = "SELECT * FROM conflits_etudiants ORDER BY date_conflit, nb_examens DESC"
        return self.execute_query(query)
    
    def get_conflits_professeurs(self):
        query = "SELECT * FROM conflits_professeurs ORDER BY date_conflit, nb_examens DESC"
        return self.execute_query(query)
    
    def get_conflits_capacite(self):
        query = "SELECT * FROM conflits_capacite ORDER BY depassement DESC"
        return self.execute_query(query)
    
    def get_conflits_salles(self):
        query = "SELECT * FROM conflits_salles ORDER BY debut1"
        return self.execute_query(query)
    
    def get_occupation_salles(self):
        query = "SELECT * FROM occupation_salles_par_jour ORDER BY date_examen"
        return self.execute_query(query)
    
    def get_charge_professeurs(self):
        query = "SELECT * FROM charge_professeurs ORDER BY nb_surveillances DESC"
        return self.execute_query(query)
    
    def get_stats_departement(self):
        query = "SELECT * FROM stats_departement ORDER BY nb_etudiants DESC"
        return self.execute_query(query)
    
    def get_planning_etudiant(self, etudiant_id, periode_id):
        query = "SELECT * FROM get_planning_etudiant(%s, %s)"
        return self.execute_query(query, (etudiant_id, periode_id))
    
    def get_planning_professeur(self, prof_id, periode_id):
        query = "SELECT * FROM get_planning_professeur(%s, %s)"
        return self.execute_query(query, (prof_id, periode_id))
    
    def get_periodes_examen(self, actif=True):
        if actif:
            query = "SELECT * FROM periodes_examen WHERE actif = TRUE ORDER BY date_debut DESC"
        else:
            query = "SELECT * FROM periodes_examen ORDER BY date_debut DESC"
        return self.execute_query(query)
    
    def create_examen(self, module_id, prof_id, salle_id, periode_id, date_heure, duree_minutes, nb_inscrits):
        query = """
            INSERT INTO examens (module_id, prof_responsable_id, salle_id, periode_id, 
                                date_heure, duree_minutes, nb_inscrits)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, 
            (module_id, prof_id, salle_id, periode_id, date_heure, duree_minutes, nb_inscrits))
        return result[0]['id'] if result else None
    
    def create_surveillance(self, examen_id, prof_id, role='surveillant'):
        query = """
            INSERT INTO surveillances (examen_id, prof_id, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (examen_id, prof_id) DO NOTHING
            RETURNING id
        """
        result = self.execute_query(query, (examen_id, prof_id, role))
        return result[0]['id'] if result else None
    
    def delete_all_examens(self, periode_id):
        query = "DELETE FROM examens WHERE periode_id = %s"
        self.execute_query(query, (periode_id,), fetch=False)
    
    def get_inscriptions_count_by_module(self, annee_universitaire):
        query = """
            SELECT module_id, COUNT(*) as nb_inscrits
            FROM inscriptions
            WHERE annee_universitaire = %s AND statut = 'inscrit'
            GROUP BY module_id
        """
        return self.execute_query(query, (annee_universitaire,))
    
    def get_modules_with_inscriptions(self):
        """Get all modules with their enrollment counts and exam duration"""
        query = """
            SELECT 
                m.id,
                m.nom,
                m.code,
                m.formation_id,
                m.duree_examen,
                f.dept_id,
                COUNT(i.id) as nb_inscrits
            FROM modules m
            LEFT JOIN inscriptions i ON m.id = i.module_id AND i.statut = 'inscrit'
            LEFT JOIN formations f ON m.formation_id = f.id
            GROUP BY m.id, m.nom, m.code, m.formation_id, m.duree_examen, f.dept_id
            HAVING COUNT(i.id) > 0
            ORDER BY COUNT(i.id) DESC
        """
        return self.execute_query(query)
