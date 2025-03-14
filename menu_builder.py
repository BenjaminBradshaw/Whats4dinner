import streamlit as st
import pandas as pd
import pyodbc
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import basehash
import json
import base64


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

def encode_int_list(int_list):
    # Convert the list to JSON string
    json_str = json.dumps(int_list)
    # Encode to base64 (URL-safe)
    encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
    return encoded



# Establish connection
conn, engine = init_connection()


st.header("Menu picker")


st.write(f"You are logged in as {st.session_state.role}.")


df = pd.read_sql("SELECT * FROM [dbo].[Menu] WHERE IsActive = 1;", conn)




event = st.dataframe(
    df,
    key="data",
    on_select="rerun",
    selection_mode=["multi-row"],
)

# Get the selected columns
selected_indices = event.selection.rows

#selected id
Selected_id= df.loc[selected_indices].Id.to_list()
st.write(Selected_id)


if st.button("generate link change"):
    selected_indices = event.selection.rows
    encoded = encode_int_list([1,2,3])
    st.write(encoded)

    




# Don't forget to close the connection when done

if st.button("close"):
    if conn :
        conn.close()
        st.write("Connection closed.")
