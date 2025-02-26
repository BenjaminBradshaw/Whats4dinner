import streamlit as st

st.title("Whats for dinner")

st.subheader('Menu')

with st.form("my_form"):
   st.write("dinner options")
   my_name = st.text_input("Your name")
   my_starter = st.selectbox("Pick a starter", ["calamari","grilled cabbage"])
   my_main = st.selectbox('Pick a main', ['fish','beef', 'pork','calamari'])
   my_dessert = st.selectbox('Pick a dessert', ["tiramisu","ice cream"])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(my_name)
st.write(my_starter)                           
st.write(my_main)
st.write(my_dessert)
                             
