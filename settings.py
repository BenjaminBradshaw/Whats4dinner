import streamlit as st
import pandas as pd
import pyodbc
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

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
        return conn
    except SQLAlchemyError as e:
        print("Error while connecting to the database:", e)
        return None

# Establish connection
conn = init_connection()


st.header("Settings")


st.write(f"You are logged in as {st.session_state.role}.")



df = pd.read_sql("SELECT * FROM [dbo].[Menu];", conn)



edited_df = st.data_editor(df)

if st.button("submit change"):
    out= edited_df.to_sql( "Menu", con = conn.get_bind(), schema = "dbo", if_exists="replace", index=False)
    st.write( f"{out} rows changed")

if st.button("pull"):
    st.write(pd.read_sql("SELECT * FROM [dbo].[Menu];", conn))


# Don't forget to close the connection when done

if st.button("close"):
    if conn :
        conn.close()
        st.write("Connection closed.")



