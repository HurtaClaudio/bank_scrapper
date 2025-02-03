import pandas as pd
import sqlite3

class DBHandler:
    def __init__(self, db_name="data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        placeholders = ", ".join(["?" for _ in data])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, tuple(data))
        self.conn.commit()

    def fetch_data(self, table_name):
        fetch_query = f"SELECT * FROM {table_name}"
        self.cursor.execute(fetch_query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

    def test(self):
        return 2

    def delete_all_rows(self, table_name):
        delete_query = f"DELETE FROM {table_name}"
        self.cursor.execute(delete_query)
        self.conn.commit()

def save_to_db(df, db_handler, table_name="transactions"):
    # Insert data into the table, avoiding duplicates
    for _, row in df.iterrows():
        # Check if the row already exists
        check_query = f"SELECT 1 FROM {table_name} WHERE Fecha=? AND Categoria=? AND Detalle=? AND Monto=?"
        db_handler.cursor.execute(check_query, (row['Fecha'], row['Categoria'], row['Detalle'], row['Monto']))
        if not db_handler.cursor.fetchone():
            db_handler.insert_data(table_name, (row['Fecha'], row['Categoria'], row['Detalle'], row['Monto']))
            print(f"Inserted row: {row['Fecha']}, {row['Categoria']}, {row['Detalle']}, {row['Monto']}")

def query_db(db_handler, table_name="transactions"):
    # Fetch all results
    rows = db_handler.fetch_data(table_name)

    # Print the results
    for row in rows:
        print(row)

# Example usage
if __name__ == "__main__":
    # Load the DataFrame from the CSV file
    df = pd.read_csv("results.csv")
    db_handler = DBHandler()

    table_name = "transactions"
    db_handler.create_table(table_name, {
        "Fecha": "TEXT",
        "Categoria": "TEXT",
        "Detalle": "TEXT",
        "Monto": "INTEGER",
        "PRIMARY KEY (Fecha, Categoria, Detalle, Monto)": ""
    })

    save_to_db(df, db_handler)
    query_db(db_handler)
    db_handler.close_connection()
