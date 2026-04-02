#Imports 
import streamlit as st
import easyocr as ocr
import re
from PIL import Image
import sqlite3

reader = ocr.Reader(['en'])

#Extracting fields
def extract_fields(text_list):
    designations = ["ceo", "manager", "director", "engineer", "developer", 
                "founder", "president", "officer", "analyst", "consultant","executive"]
    email = ""
    phone = []
    website = ""
    name = ""
    pincode = ""
    address = []
    company_name = []
    designation = ""
    
    name = text_list[0] if text_list else ""
    for item in text_list:
        if "@" in item:
            email = item
        elif sum(c.isdigit() for c in item) > 6:
            phone.append(item)
        elif "www" in item.lower() or ".com" in item.lower():
            website = item
        elif any(title in item.lower() for title in designations):
            designation = item     
        
        else:
            match = re.search(r'\b\d{6}\b', item)
            if match:
                address.append(item)
            else:
                if item != name and any(c.isdigit() for c in item) or any(c in item for c in [',', '.', 'St', 'Rd', 'Ave', 'Nagar']):
                    address.append(item)
                elif item != name:
                    company_name.append(item)
                    
                

    
    return {
        "name": name,
        "email": email,
        "phone": ", ".join(phone),
        "website": website,
        "designation": designation,
        "address": ", ".join(address),
        "company": " ".join(company_name)
        
        
    }
#SQLITE connection 

conn = sqlite3.connect("bizcard.db", check_same_thread=False)
cursor = conn.cursor()


#CREATING TABLE 


cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_cards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        email VARCHAR(50) UNIQUE,
        phone TEXT,
        company VARCHAR(50),
        designation VARCHAR(50),
        address VARCHAR(255),
        website VARCHAR(50)
    )
""")
conn.commit()

#INSERTING CARD DETAILS INTO TABLE 
def insert_card(fields):
    cursor.execute("""
                   INSERT OR IGNORE INTO business_cards(name, email, phone, company, designation, address, website) VALUES (?,?,?,?,?,?,?)
                   """,(
                       fields['name'],
                       fields['email'],
                       fields['phone'],
                       fields['company'],
                       fields['designation'],
                       fields['address'],
                       fields['website']
        ))
    conn.commit()
