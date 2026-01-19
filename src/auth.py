"""
Authentication module for the Exam Scheduling Platform
Handles user authentication, password hashing, and session management
"""

import hashlib
import secrets
import string
from datetime import datetime
from typing import Optional, Dict, Any

class Auth:
    """Authentication handler for the platform"""
    
    def __init__(self, db):
        self.db = db
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_password(length: int = 10) -> str:
        """Generate a random password for admin roles"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_student_password(nom: str, prenom: str, promo: int) -> str:
        """Generate password for students: nom + prenom + promo"""
        nom_clean = nom.strip().title().replace(" ", "").replace("-", "")
        prenom_clean = prenom.strip().title().replace(" ", "").replace("-", "")
        return f"{nom_clean}{prenom_clean}{promo}"
    
    @staticmethod
    def generate_professor_password(nom: str, prenom: str) -> str:
        """Generate password for professors: 3 letters nom + 3 letters prenom + 4 digits"""
        nom_clean = nom.strip().title().replace(" ", "")[:3]
        prenom_clean = prenom.strip().title().replace(" ", "")[:3]
        random_digits = ''.join(secrets.choice(string.digits) for _ in range(4))
        return f"{nom_clean}{prenom_clean}{random_digits}"
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username and password"""
        password_hash = self.hash_password(password)
        
        query = """
            SELECT u.id, u.username, u.role, u.etudiant_id, u.professeur_id, 
                   u.departement_id, u.actif
            FROM utilisateurs u
            WHERE u.username = %s AND u.password_hash = %s AND u.actif = TRUE
        """
        
        result = self.db.execute_query(query, (username.lower(), password_hash))
        
        if result and len(result) > 0:
            user = result[0]
            
            # Update last login
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE utilisateurs SET derniere_connexion = %s WHERE id = %s",
                    (datetime.now(), user['id'])
                )
                conn.commit()
                cursor.close()
            except:
                pass
            
            # Build user info
            user_info = {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'etudiant_id': user['etudiant_id'],
                'professeur_id': user['professeur_id'],
                'departement_id': user['departement_id']
            }
            
            # Get name based on role
            if user['role'] == 'etudiant' and user['etudiant_id']:
                etudiant = self.db.execute_query(
                    "SELECT nom, prenom, formation_id FROM etudiants WHERE id = %s",
                    (user['etudiant_id'],)
                )
                if etudiant:
                    user_info['nom'] = etudiant[0]['nom']
                    user_info['prenom'] = etudiant[0]['prenom']
                    user_info['formation_id'] = etudiant[0]['formation_id']
            
            elif user['professeur_id']:
                prof = self.db.execute_query(
                    "SELECT nom, prenom, dept_id, grade FROM professeurs WHERE id = %s",
                    (user['professeur_id'],)
                )
                if prof:
                    user_info['nom'] = prof[0]['nom']
                    user_info['prenom'] = prof[0]['prenom']
                    user_info['dept_id'] = prof[0]['dept_id']
                    user_info['grade'] = prof[0]['grade']
            
            return user_info
        
        return None
    
    def create_user(self, username: str, password: str, role: str, 
                    etudiant_id: int = None, professeur_id: int = None, 
                    departement_id: int = None) -> bool:
        """Create a new user account"""
        password_hash = self.hash_password(password)
        
        query = """
            INSERT INTO utilisateurs (username, password_hash, role, etudiant_id, professeur_id, departement_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
            RETURNING id
        """
        
        try:
            result = self.db.execute_query(
                query, 
                (username.lower(), password_hash, role, etudiant_id, professeur_id, departement_id)
            )
            return result is not None and len(result) > 0
        except Exception as e:
            print(f"Error creating user: {e}")
            return False


def get_role_display_name(role: str) -> str:
    """Get display name for a role"""
    role_names = {
        'vice_doyen': 'Vice-Doyen / Doyen',
        'admin_examens': 'Administrateur des Examens',
        'chef_departement': 'Chef de Département',
        'professeur': 'Professeur',
        'etudiant': 'Étudiant'
    }
    return role_names.get(role, role)


def get_role_icon(role: str) -> str:
    """Get icon for a role"""
    role_icons = {
        'vice_doyen': '',
        'admin_examens': '',
        'chef_departement': '',
        'professeur': '',
        'etudiant': ''
    }
    return role_icons.get(role, '👤')
