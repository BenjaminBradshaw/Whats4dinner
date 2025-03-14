import streamlit as st
import pyodbc
import os
import pandas as pd
import basehash

hash_fn = basehash.base36() 

ROLES = [None, "Waiter", "Admin"]

if "role" not in st.session_state:
    st.session_state.role = None

if st.query_params:
    hash=st.query_params["id"]
    unhashed = hash_fn.unhash(hash) 
    st.write(unhashed)

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
    



role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
admin = st.Page(
    "admin/admin.py",
    title="Admin page",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
waiter_page = st.Page(
    "waiter/waiter.py",
    title="waiter",
    default =(role== "Waiter"),
)
     
pick_page = st.Page(pick, title="Whats for dinner")
menu_page =st.Page("menu_builder.py", title = "Menu builder", icon=":material/menu_open:")


admin_pages = [admin,menu_page]
waiter_pages =[waiter_page, menu_page]
account_pages = [logout_page, settings]

page_dict = {}
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if st.session_state.role == "Waiter":
    page_dict["Waiter"] = waiter_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([ st.Page(pick), st.Page(login) ])

pg.run()



                             
