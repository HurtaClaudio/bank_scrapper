import sqlite3

def query_db(db_path="data.db", table_name="transactions"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all results
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# Example usage
if __name__ == "__main__":
    query_db()
