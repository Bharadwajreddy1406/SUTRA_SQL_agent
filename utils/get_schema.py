import psycopg2
import json
from typing import Dict, List, Any

def get_schema() -> Dict[str, List[Dict[str, Any]]]:
    """
    Connect to PostgreSQL database and retrieve schema information.
    Returns a dictionary of tables and their column details.
    """
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname='SkillSage_niceone',
            user='postgres',
            password='reddy1406',
            host='localhost',
            port='5432'
        )

        # Create a cursor object to interact with the database
        cur = conn.cursor()

        # Query to retrieve table names from the public schema
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        
        # Create a dictionary to store schema information
        schema_info = {}
        
        # Iterate over each table and retrieve column information
        for table in tables:
            table_name = table[0]
            schema_info[table_name] = []

            # Query to retrieve column details for the current table
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

        # Close the cursor and connection
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