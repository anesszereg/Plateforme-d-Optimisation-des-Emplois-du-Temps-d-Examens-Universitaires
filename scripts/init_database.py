import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

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
        schema_sql = f.read()
        cursor.execute(schema_sql)
    
    print("Création des vues et fonctions...")
    with open('database/queries.sql', 'r', encoding='utf-8') as f:
        queries_sql = f.read()
        cursor.execute(queries_sql)
    
    print("Création des index d'optimisation...")
    with open('database/indexes.sql', 'r', encoding='utf-8') as f:
        indexes_sql = f.read()
        cursor.execute(indexes_sql)
    
    cursor.close()
    conn.close()
    
    print("✅ Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_database()
