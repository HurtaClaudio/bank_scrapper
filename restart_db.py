import pandas as pd
from DBHandler import DBHandler

if __name__ == "__main__":
    handler = DBHandler()
    handler.drop_table()
    handler.create_table()

    df = pd.read_csv("results.csv")
    handler.save_to_db(df)
    handler.query_db()
    
    handler.close_connection()
