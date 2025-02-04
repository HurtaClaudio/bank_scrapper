import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import yaml

# Connect to the database
conn = sqlite3.connect("../data.db")

# Load data
def load_data():
    query = "SELECT * FROM transactions"
    return pd.read_sql(query, conn)

def load_categories():
    with open("../categories.yaml", "r") as file:
        return yaml.safe_load(file)


data = load_data()
categories = load_categories()

# Add a separate page for detailed analysis
st.sidebar.header("Navigation")
page = st.sidebar.segmented_control("Go to", ["Data Labeler", "Dashboard", "SQL Console"])

# Sidebar Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Date Range", [])
category = st.sidebar.multiselect("Catergoria", ["All"] + list(data['Categoria_0'].unique()), default=["All"])

# Apply filters
if date_range:
    data = data[(data['Fecha'] >= str(date_range[0])) & (data['Fecha'] <= str(date_range[1]))]
if category != ["All"]:
    data = data[data['Categoria_0'].isin(category)]


if page == "Data Labeler":
    st.subheader("Interactive Data Labeler")
    data_no_label = data[data['Categoria_0'].isnull() | data['Categoria_1'].isnull()]
    selected_index = st.segmented_control("Select a transaction to label", data_no_label.index, default=data_no_label.index[0])   
    selected_transaction = data.loc[selected_index]

    st.table(selected_transaction)

    category = st.pills("Categoria_0", list(categories.keys()))
    subcategories = categories.get(category, [])
    if subcategories:
        subcategorie = st.pills("Subcategoria", subcategories)
    else:
        subcategorie = None

    if st.button("Apply Label"):
        # Update the database
        query = "UPDATE transactions SET Categoria_0 = ?, Categoria_1 = ? WHERE id = ?"
        cursor = conn.execute(query, (category, subcategorie, int(selected_transaction['id'])))
        conn.commit()
        
        st.success(f"Transaction {selected_index} labeled as {category}, {subcategorie}")

elif page=="SQL Console":
    st.subheader("SQL Console")
    sql_query = st.text_area("Enter SQL Query", value="select * from transactions where id<4")
    if st.button("Run Query"):
        try:
            result = conn.execute(sql_query)
            if sql_query.strip().lower().startswith("select"):
                data = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
                st.dataframe(data)
            else:
                conn.commit()
                st.success("Query executed successfully")
        except Exception as e:
            st.error(f"An error occurred: {e}")


else:
    st.title("Credit Card Purchases Dashboard")
    data_display = data.sort_values(by='Fecha', ascending=False).head(10)
    data_display['Detalle'] = data_display['Detalle'].str[:30]
    data_display = data_display[['Fecha', 'Categoria', 'Detalle', 'Categoria_0', 'Monto']]
    st.dataframe(data_display)

    # Plot Expenses
    fig = px.pie(data, values='Monto', names='Categoria_0', title='Expenses Distribution')
    fig.update_traces(textinfo='percent+label', texttemplate='%{percent:.0%}')
    st.plotly_chart(fig)

    # Display Total Expenses
    total_expenses = data['Monto'].sum()
    st.markdown("<h3 style='text-align: center;'>Total Expenses for the Period</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>${total_expenses:,}</h1>", unsafe_allow_html=True)