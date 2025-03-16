import psycopg2
import json
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

def get_schema() -> Dict[str, List[Dict[str, Any]]]:
    """
    Connect to PostgreSQL database and retrieve schema information.
    Returns a dictionary of tables and their column details.
    """
    try:

        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        cur = conn.cursor()


        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        
      
        schema_info = {}
        
       
        for table in tables:
            table_name = table[0]
            schema_info[table_name] = []

           
            cur.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
            """)
            columns = cur.fetchall()

            for column in columns:
                column_name, data_type = column
                schema_info[table_name].append({
                    "column_name": column_name,
                    "data_type": data_type
                })

        cur.close()
        conn.close()
        
        return schema_info
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def main():
    schema_info = get_schema()
    if schema_info:
        print("Database Schema Information:")
        print(json.dumps(schema_info, indent=2))
    else:
        print("Failed to retrieve database schema.")

if __name__ == "__main__":
    main()