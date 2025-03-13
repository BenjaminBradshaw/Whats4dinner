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
        return conn, engine
    except SQLAlchemyError as e:
        print("Error while connecting to the database:", e)
        return None, None

# Establish connection
conn, engine = init_connection()


st.header("Settings")


st.write(f"You are logged in as {st.session_state.role}.")

def valadate(dataframe):
    

df = pd.read_sql("SELECT * FROM [dbo].[Menu];", conn)



edited_df = st.data_editor(df, column_config={
        "Id": st.column_config.NumberColumn(
        default=max(df["Id"])+1),
        "Course": st.column_config.SelectboxColumn(
            width="medium",
            options=[
                "Starter",
                "Main",
                "Dessert",
            ],
            required=True,
        )
    }, num_rows="dynamic")

if st.button("submit change"):
    if edited_df["Id"].is_unique:
        st.write("index validated")
        st.write("updating....")
        out= edited_df.to_sql( "Menu", con = engine, method=None, schema = "dbo", if_exists="replace", index=False)
        st.write( f"{out} rows changed")
    else:
        st.write("index not unique!)"
    

if st.button("pull"):
    st.write(pd.read_sql("SELECT * FROM [dbo].[Menu];", conn))


# Don't forget to close the connection when done

if st.button("close"):
    if conn :
        conn.close()
        st.write("Connection closed.")



