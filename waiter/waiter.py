import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import io


st.header("Waiter")
st.write(f"You are logged in as {st.session_state.role}.")



def generate_name_tags_pdf(df):
    """Generates a PDF of name tags in memory."""
    buffer = io.BytesIO()  # Use in-memory buffer
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    tag_width = 8.3 * cm
    tag_height = 5.4 * cm
    margin_x = 0.1 * cm
    margin_y = 0.1 * cm
    tags_per_row = int((width - 2 * margin_x) // tag_width)
    tags_per_column = int((height - 2 * margin_y) // tag_height)

    x, y = margin_x, height - margin_y - tag_height

    for index, row in df.iterrows():
        name = row['Name']
        meal_order = row['Meal Order']

        c.rect(x, y, tag_width, tag_height)

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x + tag_width / 2, y + tag_height * 0.7, name)

        c.setFont("Helvetica", 12)
        c.drawCentredString(x + tag_width / 2, y + tag_height * 0.3, meal_order)

        x += tag_width + 0.1 * cm

        if (index + 1) % tags_per_row == 0:
            x = margin_x
            y -= tag_height + 0.1 * cm

        if (index + 1) % (tags_per_row * tags_per_column) == 0:
            c.showPage()
            x, y = margin_x, height - margin_y - tag_height

    c.save()
    buffer.seek(0) #reset the buffer to the beginning.
    return buffer


st.title("Name Tag Generator")

data = {'Name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown', 'David Lee', 'Eve Wilson', 'Frank Garcia', 'Grace Rodriguez', 'Henry Martinez', 'Ivy Anderson', 'Jack Thomas', 'Kelly Jackson', 'Liam White'],
            'Meal Order': ['Chicken', 'Beef', 'Vegetarian', 'Fish', 'Pasta', 'Pizza', 'Salad', 'Steak', 'Soup', 'Burger', 'Tacos', 'Sushi']}
df = pd.DataFrame(data)

st.write("Sample Data:")
st.dataframe(df)

if st.button("Generate Name Tags PDF"):
        pdf_buffer = generate_name_tags_pdf(df)
        st.download_button(
            label="Download Name Tags PDF",
            data=pdf_buffer,
            file_name="name_tags.pdf",
            mime="application/pdf"
        )
