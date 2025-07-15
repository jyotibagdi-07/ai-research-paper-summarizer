import streamlit as st
import fitz  # PyMuPDF
import requests
import os
import base64
from dotenv import load_dotenv

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="📄 AI Research Paper Summarizer",
    page_icon="📄",
    layout="centered"
)

# -------------------- LOAD ENV --------------------
load_dotenv()
API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_KEY}"}

# -------------------- LOAD CSS --------------------
def load_local_css(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_local_css("style.css")

# -------------------- BACKGROUND IMAGE --------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

bg_image = get_base64_image("clean-business-simple-splice-creative-green-powerpoint-background_4a032eb92a__960_540.avif")
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

# -------------------- HEADER --------------------
st.markdown("""
    <div style='text-align:center; margin-top:20px;'>
        <img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" width="80"/>
        <h1>AI Research Paper Summarizer</h1>
        <h3>📄 Summarize your research PDFs instantly</h3>
        <hr style="margin-top: -10px; margin-bottom: 30px;">
    </div>
""", unsafe_allow_html=True)

# -------------------- FILE UPLOADER --------------------
uploaded_file = st.file_uploader("📄 **Upload your Research Paper (PDF)**", type=["pdf"])

# -------------------- HUGGING FACE SUMMARIZATION --------------------
def summarize_text(text):
    payload = {
        "inputs": text,
        "parameters": {"max_length": 300, "min_length": 50, "do_sample": False}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        result = response.json()
        if isinstance(result, dict) and 'error' in result:
            return f"❌ Error: {result['error']}"
        return result[0]['summary_text']
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# -------------------- PROCESS PDF --------------------
if uploaded_file is not None:
    with st.spinner("🔍 Extracting text from PDF..."):
        pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in pdf_reader])

    st.success("✅ PDF Loaded Successfully!")

    if st.button("📝 Generate Summary"):
        with st.spinner("✨ Summarizing..."):
            summary = summarize_text(text[:3000])  # Limit input for performance
        st.markdown("### 🧠 Summary")
        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
        st.download_button("📥 Download Summary", summary, file_name="summary.txt")

# -------------------- FOOTER --------------------
st.markdown("""
<hr>
<footer>Made with ❤️ by <b>Jyoti & Akankcha</b> | Powered by Hugging Face + GPT</footer>
""", unsafe_allow_html=True)
       
