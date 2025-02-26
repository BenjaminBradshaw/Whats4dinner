import streamlit as st

st.title("Whats for dinner")

st.subheader('Menu')

with st.form("my_form"):
   st.write("Inside the form")
   name = st.text_input("Your name")
   my_color = st.selectbox('Pick a color', ['red','orange','green','blue','violet'])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(my_number)
st.write(my_color)
