import psycopg2
import os
import time
from dotenv import load_dotenv

load_dotenv()

def execute_sql_statements(cursor, sql_content, description):
    """Execute SQL statements one by one to avoid timeout"""
    statements = []
    current = []
    in_function = False
    
    for line in sql_content.split('\n'):
        stripped = line.strip()
        
        # Track if we're inside a function/procedure
        if 'CREATE OR REPLACE FUNCTION' in line.upper() or 'CREATE FUNCTION' in line.upper():
            in_function = True
        if in_function and stripped.startswith('$$') and len(current) > 0:
            if current[-1].strip().endswith('$$'):
                in_function = False
        
        current.append(line)
        
        # End of statement
        if stripped.endswith(';') and not in_function:
            stmt = '\n'.join(current).strip()
            if stmt and not stmt.startswith('--'):
                statements.append(stmt)
            current = []
    
    # Add any remaining
    if current:
        stmt = '\n'.join(current).strip()
        if stmt and not stmt.startswith('--'):
            statements.append(stmt)
    
    print(f"  Exécution de {len(statements)} instructions pour {description}...")
    for i, stmt in enumerate(statements):
        if stmt.strip():
            try:
                cursor.execute(stmt)
            except Exception as e:
                if 'already exists' not in str(e) and 'does not exist' not in str(e):
                    print(f"    Warning: {str(e)[:80]}")

def init_database():
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'exam_scheduling'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '')
    }
    
    print("Connexion à la base de données...")
    conn = psycopg2.connect(**config)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Exécution du schéma de base de données...")
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        execute_sql_statements(cursor, f.read(), "schema")
    
    print("Création des vues et fonctions...")
    with open('database/queries.sql', 'r', encoding='utf-8') as f:
        execute_sql_statements(cursor, f.read(), "queries")
    
    print("Création des index d'optimisation...")
    with open('database/indexes.sql', 'r', encoding='utf-8') as f:
        execute_sql_statements(cursor, f.read(), "indexes")
    
    cursor.close()
    conn.close()
    
    print("✅ Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_database()
