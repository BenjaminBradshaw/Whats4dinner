import streamlit as st
import pandas as pd
import pyodbc
import os


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



st.header("Settings")


st.write(f"You are logged in as {st.session_state.role}.")



df = pd.read_sql("SELECT * FROM [dbo].[Menu];", conn)

st.write(df)

edited_df = st.data_editor(df)



