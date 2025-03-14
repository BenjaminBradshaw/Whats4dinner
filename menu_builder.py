import streamlit as st
import pandas as pd
import pyodbc
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import basehash
import json
import base64
import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode

base_url = os.getenv("BASE_URL")
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

today = datetime.date.today()
two_months_later = today + relativedelta(months=2)




# Establish connection
conn, engine = init_connection()


st.header("Menu picker")


st.write(f"You are logged in as {st.session_state.role}.")

st.write("select a date for the dinner")

selected_date = st.date_input(
    "Select a date",
    value=today,
    min_value=today,
    max_value=two_months_later,
    format="YYYY-MM-DD"
)


St.write("select menu items")
df = pd.read_sql("SELECT * FROM [dbo].[Menu] WHERE IsActive = 1;", conn)


event = st.dataframe(
    df,
    key="data",
    on_select="rerun",
    selection_mode=["multi-row"],
    hide_index=True
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
    current_params={"date:selected_date,data:encoded)
    query_string = urlencode(current_params)
    full_url = f"{base_url}?{query_string}" if query_string else base_url

    # Display the URL in a text box
    st.text_input("URL with query parameters:", value=full_url, disabled=True)

    




# Don't forget to close the connection when done

if st.button("close"):
    if conn :
        conn.close()
        st.write("Connection closed.")
