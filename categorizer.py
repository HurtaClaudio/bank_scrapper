import sqlite3
import pandas as pd
import yaml

with open("categories.yaml", "r") as file:
    categories = yaml.safe_load(file)

def categorize_purchases(df):
    categories_0 = list(categories.keys())
    n = len(df)
    
    # Loop through the records that need categorization
    for index, row in df.iterrows():        
        # Display available categories
        print("Select a category:")
        for i, category in enumerate(categories_0, 1):
            print(f"{i}. {category}")

        # Get user input
        print(f"\n{(index+1)}/{n}")
        print(f"Purchase: {row['Detalle']} - Amount: {row['Monto']}")
        selected_category_int = int(input("Enter category number: "))

        # Assign the selected category to the row
        selected_category = categories_0[selected_category_int - 1]
        print(f"Selected category: {selected_category}")

        sub_categories = categories[selected_category]
        for i, sub_category in enumerate(sub_categories, 1):
            print(f"{i}. {sub_category}")

        selected_subcategory_int = int(input("Enter subcategory number: "))
        selected_subcategory = sub_categories[selected_subcategory_int - 1]
        print(f"Selected subcategory: {selected_subcategory}")

        df.at[index, 'Categoria_0'] = selected_category
        df.at[index, 'Categoria_1'] = selected_subcategory
        
    return df


if __name__ == '__main__':

    from DBHandler import DBHandler

    db_handler = DBHandler()
    db_handler.query_db()
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query("SELECT * FROM transactions WHERE Categoria_0 IS NULL", conn)
    df = categorize_purchases(df)

    db_handler.update_data(df)
    db_handler.query_db()
