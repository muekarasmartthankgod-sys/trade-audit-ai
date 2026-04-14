import streamlit as st
import openai
import fitz  # PyMuPDF
from pydantic import BaseModel
from typing import List

# --- CONFIGURATION & SECRETS ---
st.set_page_config(page_title="Global Trade Auditor Pro", layout="wide")

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("API Key not found. Please configure Streamlit Secrets.")

# --- DATA STRUCTURE ---
class AuditResult(BaseModel):
    hs_code_verified: str
    risk_level: str
    findings: List[str]
    recommendation: str

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def run_audit(text):
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a Customs Audit Expert. Analyze the text for HS Code accuracy, sanctions, and valuation risks."},
            {"role": "user", "content": text}
        ],
        response_format=AuditResult,
    )
    return response.choices[0].message.parsed

# --- UI INTERFACE ---
st.title("🚢 Global Trade Compliance Auditor (Batch Mode)")
st.caption("Advanced AI Analysis for Professional Customs Verification")

with st.sidebar:
    st.header("Authentication")
    access_key = st.text_input("Enter your E-book Access Key:", type="password")
    st.divider()
    st.info("This tool is part of the 2026 Global Compliance Expert Guide.")

if access_key == "EXPERT-2026":
    # ENABLE MULTIPLE FILES HERE
    uploaded_files = st.file_uploader(
        "Upload shipping documents (PDFs)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Run Global Audit on All Files"):
            for uploaded_file in uploaded_files:
                with st.expander(f"Analysis for: {uploaded_file.name}", expanded=True):
                    with st.spinner(f"Auditing {uploaded_file.name}..."):
                        try:
                            # 1. Extract
                            raw_text = extract_text_from_pdf(uploaded_file)
                            # 2. Analyze
                            result = run_audit(raw_text)
                            # 3. Display
                            col1, col2 = st.columns(2)
                            col1.metric("HS Code Status", result.hs_code_verified)
                            col2.metric("Risk Level", result.risk_level)
                            
                            st.write("**Detailed Findings:**")
                            for finding in result.findings:
                                st.write(f"- {finding}")
                            
                            st.success(f"**Recommendation:** {result.recommendation}")
                        except Exception as e:
                            st.error(f"Could not process {uploaded_file.name}: {e}")
else:
    st.warning("Please enter your Access Key in the sidebar to begin.")

st.divider()
st.caption("Legal Disclaimer: This AI tool is for educational and research purposes only. Always verify findings with official Customs regulations.")
