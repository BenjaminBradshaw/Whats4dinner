import streamlit as st

st.title("Whats for dinner")

st.subheader('Menu')

with st.form("my_form"):
   st.write("Inside the form")
   my_name = st.text_input("Your name")
   my_main = st.selectbox('Pick a main', ['fish','beef', 'pork','calamari'])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(my_main)
st.write(my_name)
