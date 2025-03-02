import streamlit as st
import pyodbc
import os

@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + os.getenv("AZURE_SQL_SERVER")
        + ";DATABASE="
        + os.getenv("AZURE_SQL_DATABASE")
        + ";UID="
        + os.getenv("AZURE_SQL_USER")
        + ";PWD="
        + os.getenv("AZURE_SQL_PASSWORD")
    )

conn = init_connection()


@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


st.title("Whats for dinner")

st.subheader('Menu')

with st.form("my_form"):
   st.write("dinner options")
   my_name = st.text_input("Your full name")
   my_starter = st.selectbox("Pick a starter", ["calamari","grilled cabbage"])
   my_main = st.selectbox('Pick a main', ['fish','beef', 'pork','calamari'])
   my_dessert = st.selectbox('Pick a dessert', ["tiramisu","ice cream"])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(my_name)
st.write(my_starter)                           
st.write(my_main)
st.write(my_dessert)


rows = run_query("SELECT * FROM [dbo].[Menu];")

st.write(rows)
# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
                             
