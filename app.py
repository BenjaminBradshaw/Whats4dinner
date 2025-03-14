import streamlit as st
import pyodbc
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import basehash
import json
import base64

hash_fn = basehash.base36() 

ROLES = [None, "Waiter", "Admin"]

if "role" not in st.session_state:
    st.session_state.role = None

#if st.query_params:
#    hash=st.query_params["id"]
#    unhashed = hash_fn.unhash(hash) 
#    st.write(unhashed)

def init_connection():
    try:
        # Building the connection string for SQLAlchemy
        connection_string = (
            f"mssql+pyodbc://{os.getenv('AZURE_SQL_USER')}:{os.getenv('AZURE_SQL_PASSWORD')}"
            f"@{os.getenv('AZURE_SQL_SERVER')}/{os.getenv('AZURE_SQL_DATABASE')}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )

        # Creating the SQLAlchemy engine
        engine = create_engine(connection_string)

        # Establishing the connection
        conn = engine.connect()
        print("Connection established successfully.")
        return conn, engine
    except SQLAlchemyError as e:
        print("Error while connecting to the database:", e)
        return None, None



#pages
def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)
    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

def pick():
    st.subheader('Menu')


    if "data" in st.query_params:
        # Get and decode the data
        encoded_data = st.query_params["data"]
        decoded_list = decode_int_list(encoded_data)
        
        st.write("Received data:", decoded_list)
    else:
        st.write("No data received in URL parameters")
   
    whole_menu= pd.read_sql("SELECT * FROM [dbo].[Menu];", conn)

    #selected_menu= whole_menu[decoded_list]
    
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



    
    
   # rows = run_query("SELECT * FROM [dbo].[Menu];")
    
# Establish connection
conn, engine = init_connection()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
admin = st.Page(
    "admin/admin.py",
    title="Admin page",
    icon=":material/person_add:",
    default=(role == "Admin"))

waiter_page = st.Page(
    "waiter/waiter.py",
    title="Waiter",
    default =(role== "Waiter"))
     
pick_page = st.Page(pick, title="Whats for dinner")
menu_page =st.Page("menu_builder.py", title = "Menu builder", icon=":material/menu_open:")


admin_pages = [admin, settings]
waiter_pages =[waiter_page, menu_page]
account_pages = [logout_page]

page_dict = {}
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if st.session_state.role in ["Admin", "Waiter"]:
    page_dict["Waiter"] = waiter_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([ st.Page(pick), st.Page(login) ])

pg.run()



                             
