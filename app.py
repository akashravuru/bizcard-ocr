from bizcard_functions import *
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

page = st.sidebar.radio("Navigation", ["Upload & Extract", "View All Cards", "Update/Delete"])

if page == "Upload & Extract":
    st.title("BizCard Extractor")
    st.subheader("Upload a Business Card")
    uploaded_image = st.file_uploader('', type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Card", width=400)

        image = Image.open(uploaded_image)
        image_array = np.array(image)
        result = reader.readtext(image_array)
        text = [item[1] for item in result]
        fields = extract_fields(text)
        name = st.text_input("Name", value=fields['name'])
        email = st.text_input("Email", value=fields['email'])
        phone = st.text_input("Phone", value=fields['phone'])
        company = st.text_input("Company", value=fields['company'])
        designation = st.text_input("Designation", value=fields['designation'])
        address = st.text_input("Address", value=fields['address'])
        website = st.text_input("Website", value=fields['website'])

        if st.button("Save Card"):
            insert_card({
                'name': name,
                'email': email,
                'phone': phone,
                'company': company,
                'designation': designation,
                'address': address,
                'website': website
            })
            st.success("Card saved successfully!")

elif page == "View All Cards":
    cursor.execute("SELECT * FROM business_cards")
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=["ID", "Name", "Email", "Phone", "Company", "Designation", "Address", "Website"])
    st.dataframe(df.drop(columns=["ID"]))

elif page == "Update/Delete":
    
    cursor.execute("SELECT name FROM business_cards")
    names = [row[0] for row in cursor.fetchall()]
    
    selected_title = st.selectbox("Select a card", ["Select a card"] + names)

    if selected_title != "Select a card":
        cursor.execute("SELECT * FROM business_cards WHERE name = ?", (selected_title,))
        card = cursor.fetchone()
        st.subheader(card[1])
        st.caption(card[2]) 
        st.caption(card[3])
        st.caption(card[4]) 
        st.caption(card[5])
        st.caption(card[6])
        st.caption(card[7]) 

        name = st.text_input("Name", value=card[1])
        email = st.text_input("Email", value=card[2])
        phone = st.text_input("Phone", value=card[3])
        company = st.text_input("Company", value=card[4])
        designation = st.text_input("Designation", value=card[5])
        address = st.text_input("Address", value=card[6])
        website = st.text_input("Website", value=card[7])
        
    if st.button("Update Card"):
        cursor.execute("""
            UPDATE business_cards 
            SET name=?, email=?, phone=?, company=?, designation=?, address=?, website=?
            WHERE name=?
        """, (name, email, phone, company, designation, address, website, selected_title))
        conn.commit()
        st.success("Card updated successfully!")

    elif st.button("Delete Card"):
        cursor.execute("DELETE FROM business_cards WHERE name = ?", (selected_title,))
        conn.commit()
        st.success("Card deleted successfully!")


        