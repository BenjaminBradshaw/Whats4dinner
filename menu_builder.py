import streamlit as st
import pandas as pd
import pyodbc
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import basehash


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

# Establish connection
conn, engine = init_connection()


st.header("Menu picker")


st.write(f"You are logged in as {st.session_state.role}.")


df = pd.read_sql("SELECT * FROM [dbo].[Menu];", conn)

hash_fn = basehash.base36()  # you can initialize a 36, 52, 56, 58, 62 and 94 base fn


if st.button("generate link change"):
  hash_value = hash_fn.hash([1,2,3])
  st.write(hash_value)

    




# Don't forget to close the connection when done

if st.button("close"):
    if conn :
        conn.close()
        st.write("Connection closed.")
