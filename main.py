import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='SkillSage',
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

# Iterate over each table and retrieve column information
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")

    # Query to retrieve column details for the current table
    cur.execute(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
    """)
    columns = cur.fetchall()

    for column in columns:
        column_name, data_type = column
        print(f"    Column: {column_name}, Data Type: {data_type}")

# Close the cursor and connection
cur.close()
conn.close()
