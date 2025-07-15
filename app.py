import streamlit as st
import fitz  # PyMuPDF
import requests
import os
import base64
from dotenv import load_dotenv

# Page settings
st.set_page_config(page_title="📄 AI Research Paper Summarizer", layout="centered")

# Load environment variables
load_dotenv()
API_KEY = os.getenv("HF_API_KEY")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Load custom CSS
def load_local_css(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Convert image to base64 for background
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

# Load background and CSS
bg_image = get_base64_image("6869469.jpg")
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{bg_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
    </style>
""", unsafe_allow_html=True)

# Load external CSS
load_local_css("style.css")

# Header section
st.markdown("""
    <div style='text-align: center; padding-top: 10px;'>
        <img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" width="80"/>
        <h1 style='margin-bottom: 5px; color: black;'>AI Research Paper Summarizer</h1>
        <h3 style='color: black;'>Summarize research PDFs using GPT + Hugging Face</h3>
    </div>
""", unsafe_allow_html=True)

# Proper file uploader (NO extra empty box)
uploaded_file = st.file_uploader("📄 **Upload your Research Paper (PDF)**", type=["pdf"])

# Summarize Function
def summarize_text(text):
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 300,
            "min_length": 50,
            "do_sample": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, dict) and 'error' in result:
        return f"❌ Error: {result['error']}"
    return result[0]['summary_text']

# If file is uploaded
if uploaded_file is not None:
    with st.spinner("🔍 Reading PDF..."):
        pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_reader:
            text += page.get_text()

    st.success("✅ PDF Loaded Successfully!")

    # Button to generate summary
    if st.button("📝 Summarize"):
        with st.spinner("✍ Generating summary..."):
            summary = summarize_text(text[:3000])

        # Show summary inside a nice box
        st.markdown("### 🧠 Summary Result")
        st.markdown(f"""
            <div class="summary-box">
                {summary}
            </div>
        """, unsafe_allow_html=True)

        # Download summary button
        st.download_button("📥 Download Summary", summary, file_name="summary.txt")

# Footer
st.markdown("""
    <hr style="border:1px solid #444;">
    <p style='text-align:center; color:red;'>Made with ❤️ by Jyoti & Akankcha | Powered by Hugging Face + GPT</p>
""", unsafe_allow_html=True)
