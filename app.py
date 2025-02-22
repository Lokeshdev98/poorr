import streamlit as st
import sqlite3
import os

# Database connection
def connect_db():
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            payment_file TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

# Set upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit app UI
st.set_page_config(page_title="Helping for Poor", layout="centered")

# HTML and CSS styling using Streamlit components
st.markdown(
    """
    <style>
        .main {
            background-image: url('o.jpg');
            background-size: cover;
            padding: 50px;
            border-radius: 20px;
            color: white;
            text-align: center;
        }
        h1 {
            color: #23bd51;
        }
        .stButton>button {
            background: linear-gradient(135deg, #74ebd5, #acb6e5);
            color: white;
            font-weight: bold;
            padding: 10px 24px;
            border-radius: 10px;
        }
        .stButton>button:hover {
            transform: scale(1.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Form UI
st.markdown("<h1>Please Help Poor</h1>", unsafe_allow_html=True)
st.markdown("<h3>Submit Payment Details</h3>", unsafe_allow_html=True)

with st.form("donation_form"):
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    payment_file = st.file_uploader("Upload Payment File (PDF, DOC, DOCX)", type=['pdf', 'doc', 'docx'])
    submit = st.form_submit_button("Submit")

# Form Submission Logic
if submit:
    if name and email and payment_file:
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, payment_file.name)
        with open(file_path, "wb") as f:
            f.write(payment_file.getbuffer())

        # Insert data into SQLite
        try:
            conn, cursor = connect_db()
            query = "INSERT INTO donations (name, email, payment_file) VALUES (?, ?, ?)"
            values = (name, email, payment_file.name)
            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ Submission Successful! Thank you for your contribution.")
        except Exception as e:
            st.error(f"❌ Error while submitting: {e}")
    else:
        st.warning("⚠️ Please fill in all fields and upload a file.")

# Contact Info
st.markdown("""
    <h4>If any Queries?<br>Contact us: 6281770026<br>lokeshdevarakonda143@gmail.com</h4>
""", unsafe_allow_html=True)

