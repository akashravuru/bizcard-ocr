# BizCardX — Business Card Data Extractor

A Streamlit web application that extracts information from business card images using OCR, stores it in a SQLite database, and allows users to view, update, and delete saved cards.

🔗 **Live App:** https://bizcard-ocr-zkfk5rn4he8ipgsbnuy9b9.streamlit.app/

---

## Features

- **Upload & Extract** — Upload a business card image and automatically extract name, email, phone, company, designation, address, and website
- **Editable Fields** — Review and correct extracted data before saving
- **View All Cards** — Browse all saved business cards in a clean table
- **Update & Delete** — Edit any saved card or remove it from the database

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| OCR Engine | easyOCR |
| Image Processing | Pillow, NumPy |
| Database | SQLite |
| Field Parsing | Regex (re) |

---

## How It Works

1. User uploads a business card image (JPG, JPEG, PNG)
2. easyOCR reads all text from the image
3. A custom parser identifies fields using pattern matching:
   - Email → contains `@`
   - Phone → contains more than 6 digits
   - Website → contains `www` or `.com`
   - Designation → contains job title keywords
   - Address → contains digits or street keywords
   - Company → remaining unmatched text
4. Extracted fields are displayed in editable text boxes
5. User reviews, edits if needed, and saves to SQLite
6. Full CRUD operations available on saved cards

---

## Project Structure

```
bizcard-ocr/
├── app.py                  # Streamlit application
├── bizcard_functions.py    # OCR + extraction + database functions
├── bizcard.db              # SQLite database (auto-created)
├── requirements.txt        # Dependencies
├── .gitignore
└── README.md
```

---

## How to Run Locally

1. Clone the repo:
```
git clone https://github.com/akashravuru/bizcard-ocr
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the app:
```
streamlit run app.py
```

---

## Database Schema

**business_cards** — id (AUTO), name, email (UNIQUE), phone, company, designation, address, website

---

Built by [Akash Ravuru](https://linkedin.com/in/akashravuru)