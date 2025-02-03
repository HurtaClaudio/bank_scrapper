import pandas as pd
import sqlite3

class DBHandler:
    def __init__(self, db_name="data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.table_name = 'transactions'
        self.table_columns = {
            "Fecha": "TEXT",
            "Categoria": "TEXT",
            "Detalle": "TEXT",
            "Monto": "INTEGER",
            "Categoria_0": "TEXT",
            "Categoria_1": "TEXT",
            "PRIMARY KEY (Fecha, Categoria, Detalle, Monto)": ""
        }

    def create_table(self):
        columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in self.table_columns.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_with_types})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, data):
        placeholders = ", ".join(["?" for _ in data]) + ", ?, ?"
        insert_query = f"INSERT INTO {self.table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, tuple(data) + (None, None,))
        self.conn.commit()

    def fetch_data(self):
        fetch_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(fetch_query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

    def test(self):
        return 3

    def delete_all_rows(self):
        delete_query = f"DELETE FROM {self.table_name}"
        self.cursor.execute(delete_query)
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.conn.commit()

    def save_to_db(self, df):
        # Insert data into the table, avoiding duplicates
        for _, row in df.iterrows():
            # Check if the row already exists
            check_query = f"SELECT 1 FROM {self.table_name} WHERE Fecha=? AND Categoria=? AND Detalle=? AND Monto=?"
            self.cursor.execute(check_query, (row['Fecha'], row['Categoria'], row['Detalle'], row['Monto']))
            if not self.cursor.fetchone():
                self.insert_data((row['Fecha'], row['Categoria'], row['Detalle'], row['Monto']))
                print(f"Inserted row: {row['Fecha']}, {row['Categoria']}, {row['Detalle']}, {row['Monto']}")

    def query_db(self):
        # Fetch all results
        rows = self.fetch_data()

        # Print the results
        for row in rows:
            print(row)

    def update_data(self, df):
        update_query = f"""
        UPDATE {self.table_name}
        SET Categoria_0 = ?, Categoria_1 = ?
        WHERE Fecha = ? AND Categoria = ? AND Detalle = ? AND Monto = ?
        """
        for _, row in df.iterrows():
            self.cursor.execute(update_query, (
                row['Categoria_0'], row['Categoria_1'],
                row['Fecha'], row['Categoria'], row['Detalle'], row['Monto']
            ))
        self.conn.commit()

# Example usage
if __name__ == "__main__":
    # Load the DataFrame from the CSV file
    df = pd.read_csv("results.csv")
    db_handler = DBHandler()
    db_handler.create_table()
    db_handler.save_to_db(df)
    db_handler.query_db()
    db_handler.close_connection()
